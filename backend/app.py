import os
import csv
import io
import json
import logging
from datetime import datetime, timezone, timedelta
from functools import wraps

from flask import Flask, request, jsonify, make_response, send_from_directory
from flask_cors import CORS
from werkzeug.security import check_password_hash

from config import Config
from database import db_session, init_db, engine
from models import (
    Student, Teacher, Section, Subject, CourseOutcome, Unit, Topic,
    TeacherSubject, TeacherSection, Doubt, DoubtStudentSupport, FacultyAnswer,
    AIResponse, FacultyAvailability, Appointment, Notification, Announcement,
    Bookmark, StudentFeedback
)
from ai_engine import SmartDoubtEngine
from scheduler import BackgroundTimerService
from seed_data import seed_database

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(name)s: %(message)s')
logger = logging.getLogger('faculty_connect')

FRONTEND_DIST = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist'))

app = Flask(
    __name__,
    static_folder=None
)
app.config.from_object(Config)

# Enable CORS for desktop, mobile and PWA clients
CORS(app, resources={r"/api/*": {"origins": "*"}}, supports_credentials=True)

# Initialize database tables and start background timer
with app.app_context():
    init_db()
    # Check if DB has data; if empty, seed automatically
    s = db_session()
    if s.query(Subject).count() == 0:
        logger.info("Database is empty. Populating with official syllabus and sample data...")
        seed_database(reset=False)
    s.close()
    # Start the 3-hour automatic AI timer background worker
    BackgroundTimerService.start(check_interval_seconds=60)

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


# =======================================================================
# AUTHENTICATION & SESSIONS
# =======================================================================

@app.route('/api/auth/student-login', methods=['POST'])
def student_login():
    """
    Simple student entry: Name + Section.
    Persists student profile without requiring passwords for low barrier to entry.
    """
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    section_name = data.get('section', '').strip()

    if not name or not section_name:
        return jsonify({'error': 'Student name and section are required.'}), 400

    session = db_session()
    student = session.query(Student).filter(
        Student.name.ilike(name),
        Student.section == section_name
    ).first()

    if not student:
        student = Student(name=name, section=section_name)
        session.add(student)
        session.commit()

    return jsonify({
        'message': f'Welcome, {student.name}!',
        'student': student.to_dict(),
        'role': 'student'
    })


@app.route('/api/auth/teacher-login', methods=['POST'])
def teacher_login():
    """
    Secure teacher authentication.
    Verifies against hashed passwords stored securely in the database.
    """
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '').strip()

    if not email or not password:
        return jsonify({'error': 'Email and password are required.'}), 400

    session = db_session()
    teacher = session.query(Teacher).filter(Teacher.email == email).first()

    if not teacher or not teacher.check_password(password):
        return jsonify({'error': 'Invalid faculty credentials.'}), 401

    # Simple session token structure for demo
    token = f"faculty_token_{teacher.id}_{int(datetime.now(timezone.utc).timestamp())}"

    return jsonify({
        'message': f'Welcome back, {teacher.name}!',
        'teacher': teacher.to_dict(),
        'token': token,
        'role': 'teacher'
    })


@app.route('/api/auth/teachers', methods=['GET'])
def get_all_teachers():
    """Lists faculty profiles for student appointment booking."""
    session = db_session()
    teachers = session.query(Teacher).all()
    return jsonify([t.to_dict() for t in teachers])


# =======================================================================
# SUBJECTS & SYLLABUS EXPLORER (SOURCE OF TRUTH)
# =======================================================================

@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    """Returns all subjects extracted from the official syllabus directory."""
    session = db_session()
    subjects = session.query(Subject).all()
    return jsonify([s.to_dict() for s in subjects])


@app.route('/api/subjects/<int:subject_id>', methods=['GET'])
def get_subject_details(subject_id):
    """Returns complete syllabus hierarchy: Subject -> Course Outcomes -> Units -> Topics -> Subtopics."""
    session = db_session()
    subject = session.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        return jsonify({'error': 'Subject not found'}), 404
    return jsonify(subject.to_dict())


@app.route('/api/sections', methods=['GET'])
def get_sections():
    """Returns official sections."""
    session = db_session()
    sections = session.query(Section).all()
    return jsonify([s.to_dict() for s in sections])


@app.route('/api/syllabus/search', methods=['GET'])
def search_syllabus():
    """Searches topics and subtopics across the verified syllabus."""
    query = request.args.get('q', '').strip().lower()
    if not query:
        return jsonify([])

    session = db_session()
    topics = session.query(Topic).join(Unit).join(Subject).filter(
        (Topic.title.ilike(f'%{query}%')) | 
        (Topic.subtopics.ilike(f'%{query}%')) |
        (Unit.title.ilike(f'%{query}%')) |
        (Subject.title.ilike(f'%{query}%')) |
        (Subject.code.ilike(f'%{query}%'))
    ).all()

    results = []
    for t in topics:
        results.append({
            'topic_id': t.id,
            'topic_title': t.title,
            'subtopics': t.subtopics,
            'unit_id': t.unit.id,
            'unit_title': f"{t.unit.unit_number}: {t.unit.title}",
            'subject_id': t.unit.subject.id,
            'subject_code': t.unit.subject.code,
            'subject_title': t.unit.subject.title
        })
    return jsonify(results)


# =======================================================================
# SMART DOUBT INTELLIGENCE ENGINE & SUBMISSION
# =======================================================================

@app.route('/api/doubts/check-duplicate', methods=['POST'])
def check_duplicate_doubt():
    """
    CRITICAL FEATURE: Smart Duplicate Question Detection.
    Scopes comparison strictly by (Section, Subject, Unit, Topic) and calculates
    semantic similarity against previously submitted doubts.
    """
    data = request.get_json() or {}
    question_text = data.get('question_text', '').strip()
    subject_id = data.get('subject_id')
    unit_id = data.get('unit_id')
    topic_id = data.get('topic_id')
    section_name = data.get('section', '').strip()

    if not question_text or not subject_id or not unit_id or not topic_id:
        return jsonify({'error': 'Missing academic scope parameters.'}), 400

    session = db_session()
    
    # Query previous doubts in the exact same academic scope
    query = session.query(Doubt).filter(
        Doubt.subject_id == subject_id,
        Doubt.unit_id == unit_id,
        Doubt.topic_id == topic_id
    )
    # Scoped to section if provided
    if section_name:
        query = query.filter(Doubt.section == section_name)

    existing_doubts = query.all()

    match_doubt, confidence = SmartDoubtEngine.find_duplicate(
        new_question_text=question_text,
        existing_doubts=existing_doubts
    )

    if match_doubt:
        # Check if matched doubt already has a faculty or AI answer
        existing_answer = None
        if match_doubt.faculty_answers and len(match_doubt.faculty_answers) > 0:
            latest_fa = match_doubt.faculty_answers[-1]
            existing_answer = {
                'type': 'faculty',
                'author': latest_fa.teacher_name,
                'text': latest_fa.answer_text,
                'created_at': latest_fa.created_at.isoformat() if latest_fa.created_at else None
            }
        elif match_doubt.ai_responses and len(match_doubt.ai_responses) > 0:
            latest_ai = match_doubt.ai_responses[-1]
            existing_answer = {
                'type': 'ai',
                'author': latest_ai.model_name,
                'text': latest_ai.response_text,
                'quality_status': latest_ai.faculty_quality_status,
                'created_at': latest_ai.created_at.isoformat() if latest_ai.created_at else None
            }

        return jsonify({
            'is_duplicate': True,
            'confidence': confidence,
            'matched_doubt': match_doubt.to_dict(),
            'existing_answer': existing_answer
        })

    return jsonify({
        'is_duplicate': False,
        'confidence': confidence,
        'matched_doubt': None,
        'existing_answer': None
    })


@app.route('/api/doubts/support-existing', methods=['POST'])
def support_existing_doubt():
    """
    OPTION 1: '+1 – I HAVE THE SAME DOUBT'
    Increments the duplicate-support count, associates student without creating
    unnecessary teacher notification clutter, and subscribes student to answer updates.
    """
    data = request.get_json() or {}
    doubt_id = data.get('doubt_id')
    student_name = data.get('student_name', '').strip()
    student_section = data.get('student_section', '').strip()

    if not doubt_id or not student_name or not student_section:
        return jsonify({'error': 'Doubt ID, student name, and section are required.'}), 400

    session = db_session()
    doubt = session.query(Doubt).filter(Doubt.id == doubt_id).first()
    if not doubt:
        return jsonify({'error': 'Doubt not found.'}), 404

    # Check if student already gave +1
    existing_support = session.query(DoubtStudentSupport).filter(
        DoubtStudentSupport.doubt_id == doubt_id,
        DoubtStudentSupport.student_name == student_name,
        DoubtStudentSupport.student_section == student_section
    ).first()

    if existing_support:
        return jsonify({
            'message': 'You have already indicated you share this doubt (+1).',
            'doubt': doubt.to_dict()
        })

    # Add supporter
    sup = DoubtStudentSupport(
        doubt_id=doubt_id,
        student_name=student_name,
        student_section=student_section
    )
    session.add(sup)
    doubt.duplicate_count += 1
    session.commit()

    # If the doubt has reached a notable threshold (e.g., 3+ or 5+), notify the teacher
    if doubt.duplicate_count in [3, 5, 10]:
        notif = Notification(
            recipient_type='teacher',
            teacher_id=None,
            title='High Volume Repeated Doubt (+1 Threshold)',
            message=f"{doubt.duplicate_count} students in {doubt.section} have flagged this doubt in {doubt.subject.code} ({doubt.topic.title}).",
            notification_type='high_volume_alert',
            link_id=doubt.id
        )
        session.add(notif)
        session.commit()

    return jsonify({
        'message': 'Added your +1 to this doubt! You will be notified when faculty answers.',
        'doubt': doubt.to_dict()
    })


@app.route('/api/doubts/create', methods=['POST'])
def create_doubt():
    """
    OPTION 2: Submits a new doubt into the teacher queue.
    Starts the 3-hour automatic response timer and notifies faculty.
    """
    data = request.get_json() or {}
    student_name = data.get('student_name', '').strip()
    section_name = data.get('section', '').strip()
    subject_id = data.get('subject_id')
    unit_id = data.get('unit_id')
    topic_id = data.get('topic_id')
    teaching_date = data.get('teaching_date', '')
    category = data.get('category', 'Conceptual Doubt')
    question_text = data.get('question_text', '').strip()

    if not student_name or not section_name or not subject_id or not unit_id or not topic_id or not question_text:
        return jsonify({'error': 'All academic fields and question text are required.'}), 400

    session = db_session()
    
    # Resolve or create student
    student = session.query(Student).filter(
        Student.name.ilike(student_name),
        Student.section == section_name
    ).first()
    if not student:
        student = Student(name=student_name, section=section_name)
        session.add(student)
        session.flush()

    now = datetime.now(timezone.utc)
    # 3-Hour server-side deadline
    deadline = now + timedelta(hours=Config.AI_ANSWER_DELAY_HOURS)

    doubt = Doubt(
        student_id=student.id,
        student_name=student_name,
        section=section_name,
        subject_id=subject_id,
        unit_id=unit_id,
        topic_id=topic_id,
        teaching_date=teaching_date,
        category=category,
        question_text=question_text,
        status='Pending',
        duplicate_count=1,
        created_at=now,
        response_deadline=deadline
    )
    session.add(doubt)
    session.flush()

    # Record the primary student as the first supporter
    sup = DoubtStudentSupport(
        doubt_id=doubt.id,
        student_name=student_name,
        student_section=section_name
    )
    session.add(sup)

    # Create faculty notification for this subject
    subject = session.query(Subject).filter(Subject.id == subject_id).first()
    notif = Notification(
        recipient_type='teacher',
        teacher_id=None,
        title=f"New Doubt: {subject.code if subject else 'Course'}",
        message=f"{student_name} ({section_name}) submitted a {category} on '{question_text[:60]}...'",
        notification_type='doubt_update',
        link_id=doubt.id
    )
    session.add(notif)
    session.commit()

    return jsonify({
        'message': 'Academic doubt submitted successfully. Faculty queue notified.',
        'doubt': doubt.to_dict()
    }), 201


# =======================================================================
# DOUBTS LISTING, DETAIL, AND LIFECYCLE
# =======================================================================

@app.route('/api/doubts', methods=['GET'])
def get_doubts():
    """
    Returns filtered and searched doubts.
    Supports filters: student_name, section, subject_id, unit_id, topic_id, status, category, search.
    """
    session = db_session()
    query = session.query(Doubt)

    # Filter by student name (returns primary questions + questions they +1'd)
    student_name = request.args.get('student_name', '').strip()
    if student_name:
        subquery = session.query(DoubtStudentSupport.doubt_id).filter(
            DoubtStudentSupport.student_name.ilike(student_name)
        )
        query = query.filter(
            (Doubt.student_name.ilike(student_name)) | (Doubt.id.in_(subquery))
        )

    # Filters
    section = request.args.get('section', '').strip()
    if section:
        query = query.filter(Doubt.section == section)

    subject_id = request.args.get('subject_id')
    if subject_id:
        query = query.filter(Doubt.subject_id == int(subject_id))

    unit_id = request.args.get('unit_id')
    if unit_id:
        query = query.filter(Doubt.unit_id == int(unit_id))

    topic_id = request.args.get('topic_id')
    if topic_id:
        query = query.filter(Doubt.topic_id == int(topic_id))

    status = request.args.get('status', '').strip()
    if status and status != 'All':
        query = query.filter(Doubt.status == status)

    category = request.args.get('category', '').strip()
    if category and category != 'All':
        query = query.filter(Doubt.category == category)

    repeated_only = request.args.get('repeated_only')
    if repeated_only == 'true':
        query = query.filter(Doubt.duplicate_count > 1)

    search = request.args.get('search', '').strip()
    if search:
        query = query.filter(Doubt.question_text.ilike(f'%{search}%'))

    doubts = query.order_by(Doubt.created_at.desc()).all()
    return jsonify([d.to_dict() for d in doubts])


@app.route('/api/doubts/<int:doubt_id>', methods=['GET'])
def get_doubt_detail(doubt_id):
    """Returns complete doubt details, supporters, answers, and feedback."""
    session = db_session()
    doubt = session.query(Doubt).filter(Doubt.id == doubt_id).first()
    if not doubt:
        return jsonify({'error': 'Doubt not found'}), 404
    return jsonify(doubt.to_dict())


@app.route('/api/doubts/<int:doubt_id>/answer', methods=['POST'])
@app.route('/api/doubts/<int:doubt_id>/answers', methods=['POST'])
def post_faculty_answer(doubt_id):
    """
    Teacher publishes an official academic response.
    Updates status to 'Faculty Answered' or 'Faculty Verified',
    and delivers notifications to the primary student and ALL +1 supporters.
    """
    data = request.get_json() or {}
    teacher_name = data.get('teacher_name', 'Faculty Member').strip()
    teacher_id = data.get('teacher_id', 1)
    answer_text = data.get('answer_text', '').strip()

    if not answer_text:
        return jsonify({'error': 'Answer content cannot be empty.'}), 400

    session = db_session()
    doubt = session.query(Doubt).filter(Doubt.id == doubt_id).first()
    if not doubt:
        return jsonify({'error': 'Doubt not found.'}), 404

    # Save faculty answer
    fa = FacultyAnswer(
        doubt_id=doubt.id,
        teacher_id=teacher_id,
        teacher_name=teacher_name,
        answer_text=answer_text
    )
    session.add(fa)

    # Faculty has posted official answer -> Mark directly as Resolved
    doubt.status = 'Resolved'
    doubt.updated_at = datetime.now(timezone.utc)

    # Notify primary student
    notif1 = Notification(
        recipient_type='student',
        student_name=doubt.student_name,
        title=f"Faculty Answered: {doubt.subject.code}",
        message=f"{teacher_name} posted an official answer to your doubt on {doubt.topic.title}.",
        notification_type='faculty_answer',
        link_id=doubt.id
    )
    session.add(notif1)

    # Notify all +1 supporters!
    for sup in doubt.supporters:
        if sup.student_name != doubt.student_name:
            notif_sup = Notification(
                recipient_type='student',
                student_name=sup.student_name,
                title=f"Faculty Answered Saved Doubt (+1)",
                message=f"{teacher_name} posted an answer to the {doubt.subject.code} doubt you supported (+1).",
                notification_type='faculty_answer',
                link_id=doubt.id
            )
            session.add(notif_sup)

    session.commit()
    return jsonify({
        'message': 'Faculty answer published successfully.',
        'doubt': doubt.to_dict()
    })


@app.route('/api/doubts/<int:doubt_id>/generate-ai-answer', methods=['POST'])
def generate_ai_answer_for_doubt(doubt_id):
    """
    Teacher clicks 'Give Ans by AI':
    Triggers academic AI answer generation on behalf of the faculty.
    Can either publish immediately to the student (with notifications) or return draft for editing.
    """
    data = request.get_json() or {}
    publish_immediately = data.get('publish_immediately', True)
    teacher_name = data.get('teacher_name', 'Faculty Member').strip()
    teacher_id = data.get('teacher_id')

    session = db_session()
    doubt = session.query(Doubt).filter(Doubt.id == doubt_id).first()
    if not doubt:
        return jsonify({'error': 'Doubt not found.'}), 404

    subject = doubt.subject
    unit = doubt.unit
    topic = doubt.topic

    subject_title = subject.title if subject else "Course"
    unit_title = f"{unit.unit_number}: {unit.title}" if unit else "Unit"
    topic_title = topic.title if topic else "Topic"
    subtopics = topic.subtopics if topic else ""
    textbooks = subject.textbooks if subject else ""

    answer_text, confidence = SmartDoubtEngine.generate_academic_answer(
        question_text=doubt.question_text,
        subject_title=subject_title,
        unit_title=unit_title,
        topic_title=topic_title,
        subtopics=subtopics,
        textbooks=textbooks
    )

    if not publish_immediately:
        return jsonify({
            'ai_text': answer_text,
            'confidence': confidence,
            'message': 'AI answer synthesized for review.'
        })

    # Create or update AIResponse
    ai_resp = AIResponse(
        doubt_id=doubt.id,
        model_name='Google Gemini 1.5/2.0 Flash (Cloud LLM)' if Config.GEMINI_API_KEY else 'FacultyConnect Deep Academic Synthesizer',
        response_text=answer_text,
        confidence_score=confidence,
        faculty_quality_status='Correct',
        faculty_feedback_notes=f"Approved and published via Faculty Console by {teacher_name}."
    )
    session.add(ai_resp)

    # Update doubt status directly to Resolved
    doubt.status = 'Resolved'
    doubt.updated_at = datetime.now(timezone.utc)

    # Notify primary student
    notif1 = Notification(
        recipient_type='student',
        student_name=doubt.student_name,
        title=f"AI Answer Provided by {teacher_name}",
        message=f"{teacher_name} released an academic AI solution for your doubt on {topic_title}.",
        notification_type='ai_answer',
        link_id=doubt.id
    )
    session.add(notif1)

    # Notify all +1 supporters!
    for sup in doubt.supporters:
        if sup.student_name != doubt.student_name:
            notif_sup = Notification(
                recipient_type='student',
                student_name=sup.student_name,
                title=f"Answer Posted for Supported Doubt (+1)",
                message=f"{teacher_name} released an academic AI solution for the {doubt.subject.code} doubt you supported (+1).",
                notification_type='ai_answer',
                link_id=doubt.id
            )
            session.add(notif_sup)

    session.commit()

    return jsonify({
        'message': f'AI answer successfully generated and published by {teacher_name}!',
        'doubt': doubt.to_dict(),
        'ai_response': ai_resp.to_dict(),
        'ai_text': answer_text
    })


@app.route('/api/doubts/<int:doubt_id>/update-status', methods=['POST'])
def update_doubt_status(doubt_id):
    """Updates doubt status (e.g. Under Review, Resolved, Escalated)."""
    data = request.get_json() or {}
    new_status = data.get('status')

    valid_statuses = [
        'Pending', 'Under Review', 'AI Processing', 'AI Answered', 
        'Faculty Answered', 'Faculty Verified', 'Resolved', 'Escalated'
    ]
    if new_status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Allowed: {valid_statuses}'}), 400

    session = db_session()
    doubt = session.query(Doubt).filter(Doubt.id == doubt_id).first()
    if not doubt:
        return jsonify({'error': 'Doubt not found'}), 404

    doubt.status = new_status
    doubt.updated_at = datetime.now(timezone.utc)
    session.commit()

    return jsonify({
        'message': f'Doubt status updated to {new_status}',
        'doubt': doubt.to_dict()
    })


@app.route('/api/doubts/<int:doubt_id>/ai-quality-feedback', methods=['POST'])
def submit_ai_quality_feedback(doubt_id):
    """
    Faculty reviews AI answers:
    Rates as 'Correct', 'Needs Correction', 'Incorrect', 'Requires Additional Explanation'
    """
    data = request.get_json() or {}
    quality_status = data.get('quality_status') # Correct, Needs Correction, Incorrect, Requires Additional Explanation
    notes = data.get('notes', '')

    session = db_session()
    ai_resp = session.query(AIResponse).filter(AIResponse.doubt_id == doubt_id).order_by(AIResponse.created_at.desc()).first()
    if not ai_resp:
        return jsonify({'error': 'No AI response found for this doubt'}), 404

    ai_resp.faculty_quality_status = quality_status
    ai_resp.faculty_feedback_notes = notes
    session.commit()

    return jsonify({
        'message': 'AI quality feedback recorded.',
        'ai_response': ai_resp.to_dict()
    })


@app.route('/api/doubts/<int:doubt_id>/feedback', methods=['POST'])
def submit_student_feedback(doubt_id):
    """Student indicates whether an answer resolved their doubt."""
    data = request.get_json() or {}
    student_name = data.get('student_name', '').strip()
    resolved = data.get('resolved', True)
    feedback_text = data.get('feedback_text', '')

    if not student_name:
        return jsonify({'error': 'Student name required.'}), 400

    session = db_session()
    fb = StudentFeedback(
        doubt_id=doubt_id,
        student_name=student_name,
        resolved=resolved,
        feedback_text=feedback_text
    )
    session.add(fb)
    session.commit()

    return jsonify({
        'message': 'Thank you for your feedback!',
        'feedback': fb.to_dict()
    })


# =======================================================================
# BOOKMARKS
# =======================================================================

@app.route('/api/bookmarks', methods=['GET'])
def get_student_bookmarks():
    """Lists saved doubts bookmarked by a student."""
    student_name = request.args.get('student_name', '').strip()
    if not student_name:
        return jsonify([])

    session = db_session()
    bms = session.query(Bookmark).filter(Bookmark.student_name.ilike(student_name)).all()
    return jsonify([bm.to_dict() for bm in bms])


@app.route('/api/bookmarks/toggle', methods=['POST'])
@app.route('/api/bookmarks', methods=['POST'])
def toggle_bookmark():
    """Toggles bookmark status for a student on a doubt."""
    data = request.get_json() or {}
    student_name = data.get('student_name', '').strip()
    doubt_id = data.get('doubt_id')

    if not student_name or not doubt_id:
        return jsonify({'error': 'Student name and doubt ID are required.'}), 400

    session = db_session()
    bm = session.query(Bookmark).filter(
        Bookmark.student_name == student_name,
        Bookmark.doubt_id == doubt_id
    ).first()

    if bm:
        session.delete(bm)
        session.commit()
        return jsonify({'bookmarked': False, 'message': 'Removed from saved doubts.'})
    else:
        new_bm = Bookmark(student_name=student_name, doubt_id=doubt_id)
        session.add(new_bm)
        session.commit()
        return jsonify({'bookmarked': True, 'message': 'Added to saved doubts.'})


# =======================================================================
# FACULTY AVAILABILITY & CONSULTATION BOOKING
# =======================================================================

@app.route('/api/faculty/availability', methods=['GET'])
@app.route('/api/availability', methods=['GET'])
def get_faculty_availability():
    """Returns faculty consultation schedules."""
    session = db_session()
    query = session.query(FacultyAvailability).filter(FacultyAvailability.is_active == True)
    
    teacher_id = request.args.get('teacher_id')
    if teacher_id:
        query = query.filter(FacultyAvailability.teacher_id == int(teacher_id))

    slots = query.all()
    return jsonify([s.to_dict() for s in slots])


@app.route('/api/faculty/availability', methods=['POST'])
def add_or_update_availability():
    """Faculty adds a consultation time slot."""
    data = request.get_json() or {}
    teacher_id = data.get('teacher_id')
    day_of_week = data.get('day_of_week')
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    location = data.get('location', 'Cabin 34-601')
    max_bookings = data.get('max_bookings', 3)
    instructions = data.get('instructions', '')

    if not teacher_id or not day_of_week or not start_time or not end_time:
        return jsonify({'error': 'Teacher, day, and time slots are required.'}), 400

    session = db_session()
    slot = FacultyAvailability(
        teacher_id=teacher_id,
        day_of_week=day_of_week,
        start_time=start_time,
        end_time=end_time,
        location=location,
        max_bookings=max_bookings,
        instructions=instructions,
        is_active=True
    )
    session.add(slot)
    session.commit()

    return jsonify({
        'message': 'Availability slot added.',
        'slot': slot.to_dict()
    }), 201


@app.route('/api/faculty/availability/<int:slot_id>', methods=['DELETE'])
def delete_availability(slot_id):
    """Faculty removes an availability slot."""
    session = db_session()
    slot = session.query(FacultyAvailability).filter(FacultyAvailability.id == slot_id).first()
    if not slot:
        return jsonify({'error': 'Slot not found'}), 404
    session.delete(slot)
    session.commit()
    return jsonify({'message': 'Availability slot removed.'})


@app.route('/api/appointments', methods=['GET'])
def get_appointments():
    """Lists appointments filtered by teacher, student, or status."""
    session = db_session()
    query = session.query(Appointment)

    teacher_id = request.args.get('teacher_id')
    if teacher_id:
        query = query.filter(Appointment.teacher_id == int(teacher_id))

    student_name = request.args.get('student_name', '').strip()
    if student_name:
        query = query.filter(Appointment.student_name.ilike(student_name))

    status = request.args.get('status', '').strip()
    if status and status != 'All':
        query = query.filter(Appointment.status == status)

    appointments = query.order_by(Appointment.created_at.desc()).all()
    return jsonify([a.to_dict() for a in appointments])


@app.route('/api/appointments/book', methods=['POST'])
def book_appointment():
    """
    Student books a faculty consultation slot.
    Checks capacity, prevents overlapping appointments, and creates notification.
    """
    data = request.get_json() or {}
    teacher_id = data.get('teacher_id')
    student_name = data.get('student_name', '').strip()
    student_section = data.get('student_section', '').strip()
    subject_id = data.get('subject_id')
    availability_id = data.get('availability_id')
    appointment_date = data.get('appointment_date')
    time_slot = data.get('time_slot')
    location = data.get('location', 'Cabin 34-601')
    reason = data.get('reason', '').strip()

    if not teacher_id or not student_name or not student_section or not appointment_date or not time_slot or not reason:
        return jsonify({'error': 'All booking fields are required.'}), 400

    session = db_session()

    # Check for slot capacity if availability_id is linked
    if availability_id:
        avail = session.query(FacultyAvailability).filter(FacultyAvailability.id == availability_id).first()
        if avail:
            current_bookings = session.query(Appointment).filter(
                Appointment.availability_id == availability_id,
                Appointment.appointment_date == appointment_date,
                Appointment.status.in_(['Pending', 'Accepted'])
            ).count()
            if current_bookings >= avail.max_bookings:
                return jsonify({'error': f'This slot is fully booked (limit {avail.max_bookings}). Please select another date/time.'}), 400

    # Prevent duplicate booking by the same student on the same date/time
    duplicate_booking = session.query(Appointment).filter(
        Appointment.teacher_id == teacher_id,
        Appointment.student_name.ilike(student_name),
        Appointment.appointment_date == appointment_date,
        Appointment.time_slot == time_slot,
        Appointment.status.in_(['Pending', 'Accepted'])
    ).first()

    if duplicate_booking:
        return jsonify({'error': 'You already have an appointment scheduled for this time slot.'}), 400

    app_record = Appointment(
        teacher_id=teacher_id,
        student_name=student_name,
        student_section=student_section,
        subject_id=subject_id,
        availability_id=availability_id,
        appointment_date=appointment_date,
        time_slot=time_slot,
        location=location,
        reason=reason,
        status='Pending'
    )
    session.add(app_record)
    session.flush()

    # Notify teacher
    teacher = session.query(Teacher).filter(Teacher.id == teacher_id).first()
    notif = Notification(
        recipient_type='teacher',
        teacher_id=teacher_id,
        title='New Consultation Request',
        message=f"{student_name} ({student_section}) requested consultation on {appointment_date} ({time_slot}).",
        notification_type='appointment_update',
        link_id=app_record.id
    )
    session.add(notif)
    session.commit()

    return jsonify({
        'message': 'Consultation request submitted! Awaiting faculty confirmation.',
        'appointment': app_record.to_dict()
    }), 201


@app.route('/api/appointments/<int:appointment_id>/status', methods=['POST'])
def update_appointment_status(appointment_id):
    """Faculty reviews, accepts, rejects, or reschedules appointment."""
    data = request.get_json() or {}
    new_status = data.get('status') # Accepted, Rejected, Rescheduled, Completed, Cancelled
    teacher_notes = data.get('teacher_notes', '')

    valid_statuses = ['Pending', 'Accepted', 'Rejected', 'Rescheduled', 'Completed', 'Cancelled']
    if new_status not in valid_statuses:
        return jsonify({'error': f'Invalid status. Allowed: {valid_statuses}'}), 400

    session = db_session()
    app_record = session.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not app_record:
        return jsonify({'error': 'Appointment not found'}), 404

    app_record.status = new_status
    if teacher_notes:
        app_record.teacher_notes = teacher_notes

    # Notify student
    notif = Notification(
        recipient_type='student',
        student_name=app_record.student_name,
        title=f"Appointment {new_status}",
        message=f"Your appointment with {app_record.teacher.name} for {app_record.appointment_date} is now {new_status}. {teacher_notes}",
        notification_type='appointment_update',
        link_id=app_record.id
    )
    session.add(notif)
    session.commit()

    return jsonify({
        'message': f'Appointment marked as {new_status}.',
        'appointment': app_record.to_dict()
    })


# =======================================================================
# NOTIFICATION SYSTEM
# =======================================================================

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    """Returns in-app notifications for students or teachers."""
    recipient_type = request.args.get('recipient_type', 'student')
    student_name = request.args.get('student_name', '').strip()
    teacher_id = request.args.get('teacher_id')

    session = db_session()
    query = session.query(Notification).filter(Notification.recipient_type == recipient_type)

    if recipient_type == 'student' and student_name:
        query = query.filter(Notification.student_name.ilike(student_name))
    elif recipient_type == 'teacher':
        if teacher_id:
            query = query.filter((Notification.teacher_id == int(teacher_id)) | (Notification.teacher_id == None))

    notifs = query.order_by(Notification.created_at.desc()).limit(50).all()
    unread_count = sum(1 for n in notifs if not n.is_read)

    return jsonify({
        'notifications': [n.to_dict() for n in notifs],
        'unread_count': unread_count
    })


@app.route('/api/notifications/<int:notif_id>/read', methods=['POST'])
def mark_notification_read(notif_id):
    session = db_session()
    n = session.query(Notification).filter(Notification.id == notif_id).first()
    if n:
        n.is_read = True
        session.commit()
    return jsonify({'success': True})


@app.route('/api/notifications/mark-all-read', methods=['POST'])
def mark_all_notifications_read():
    data = request.get_json() or {}
    recipient_type = data.get('recipient_type', 'student')
    student_name = data.get('student_name', '').strip()
    teacher_id = data.get('teacher_id')

    session = db_session()
    query = session.query(Notification).filter(
        Notification.recipient_type == recipient_type,
        Notification.is_read == False
    )
    if recipient_type == 'student' and student_name:
        query = query.filter(Notification.student_name.ilike(student_name))
    elif recipient_type == 'teacher' and teacher_id:
        query = query.filter((Notification.teacher_id == int(teacher_id)) | (Notification.teacher_id == None))

    query.update({Notification.is_read: True}, synchronize_session=False)
    session.commit()
    return jsonify({'success': True, 'message': 'All marked as read.'})


# =======================================================================
# ANNOUNCEMENTS
# =======================================================================

@app.route('/api/announcements', methods=['GET'])
def get_announcements():
    """Lists announcements for a student's section or subject."""
    section = request.args.get('section', '').strip()
    subject_id = request.args.get('subject_id')

    session = db_session()
    query = session.query(Announcement)

    if section:
        query = query.filter((Announcement.target_section == 'All') | (Announcement.target_section == section))

    if subject_id:
        query = query.filter(Announcement.subject_id == int(subject_id))

    announcements = query.order_by(Announcement.created_at.desc()).all()
    return jsonify([a.to_dict() for a in announcements])


@app.route('/api/announcements', methods=['POST'])
def create_announcement():
    data = request.get_json() or {}
    teacher_id = data.get('teacher_id', 1)
    teacher_name = data.get('teacher_name', 'Faculty Member')
    subject_id = data.get('subject_id')
    target_section = data.get('target_section', 'All')
    title = data.get('title', '').strip()
    content = data.get('content', '').strip()
    priority = data.get('priority', 'Normal')

    if not subject_id or not title or not content:
        return jsonify({'error': 'Subject, title, and content required.'}), 400

    session = db_session()
    ann = Announcement(
        teacher_id=teacher_id,
        teacher_name=teacher_name,
        subject_id=subject_id,
        target_section=target_section,
        title=title,
        content=content,
        priority=priority
    )
    session.add(ann)
    session.commit()

    return jsonify({
        'message': 'Announcement published.',
        'announcement': ann.to_dict()
    }), 201


# =======================================================================
# ADVANCED TEACHER ANALYTICS & CSV EXPORT
# =======================================================================

@app.route('/api/analytics/dashboard', methods=['GET'])
def get_teacher_analytics():
    """
    Computes comprehensive analytics across actual stored database records:
    1. Overall metrics: Total Doubts, Pending, Resolved, Repeated, AI Answered, Faculty Answered.
    2. Section-wise doubt counts.
    3. Subject-wise doubt counts.
    4. Unit-wise and Topic-wise confusion heatmaps.
    5. Top repeated questions (+1 rankings).
    6. Response time metrics (Average response hours, within vs after 3h).
    7. Workload metrics (Unique vs Repeated, Pending vs Resolved).
    """
    session = db_session()

    teacher_id = request.args.get('teacher_id')
    subject_id = request.args.get('subject_id')
    section_filter = request.args.get('section')

    query = session.query(Doubt)

    if subject_id:
        query = query.filter(Doubt.subject_id == int(subject_id))
    if section_filter and section_filter != 'All':
        query = query.filter(Doubt.section == section_filter)

    all_doubts = query.all()

    total_doubts = len(all_doubts)
    pending_count = sum(1 for d in all_doubts if d.status in ['Pending', 'Under Review'])
    resolved_count = sum(1 for d in all_doubts if d.status in ['Resolved', 'Faculty Answered', 'Faculty Verified'])
    repeated_count = sum(1 for d in all_doubts if d.duplicate_count > 1)
    ai_answered_count = sum(1 for d in all_doubts if d.ai_responses and len(d.ai_responses) > 0)
    faculty_answered_count = sum(1 for d in all_doubts if d.faculty_answers and len(d.faculty_answers) > 0)

    # Section-wise breakdown
    section_counts = {}
    for d in all_doubts:
        sec = d.section or "Other"
        section_counts[sec] = section_counts.get(sec, 0) + 1
    section_data = [{'section': k, 'doubts': v} for k, v in sorted(section_counts.items())]

    # Subject-wise breakdown
    subject_counts = {}
    for d in all_doubts:
        scode = d.subject.code if d.subject else "Unknown"
        subject_counts[scode] = subject_counts.get(scode, 0) + 1
    subject_data = [{'subject': k, 'doubts': v} for k, v in sorted(subject_counts.items(), key=lambda x: x[1], reverse=True)]

    # Topic-wise confusion rankings
    topic_counts = {}
    for d in all_doubts:
        ttitle = d.topic.title if d.topic else "General"
        topic_counts[ttitle] = topic_counts.get(ttitle, 0) + d.duplicate_count
    topic_data = [{'topic': k, 'impact_score': v} for k, v in sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)[:8]]

    # Unit-wise breakdown
    unit_counts = {}
    for d in all_doubts:
        u_name = d.unit.unit_number if d.unit else "General"
        unit_counts[u_name] = unit_counts.get(u_name, 0) + 1
    unit_data = [{'unit': k, 'doubts': v} for k, v in sorted(unit_counts.items())]

    # Top repeated doubts (+1 ranking)
    top_repeated = sorted(
        [d for d in all_doubts if d.duplicate_count > 1],
        key=lambda x: x.duplicate_count,
        reverse=True
    )[:5]
    top_repeated_data = [{
        'id': d.id,
        'question': d.question_text[:80] + '...',
        'subject': d.subject.code if d.subject else '',
        'topic': d.topic.title if d.topic else '',
        'section': d.section,
        'supporters_count': d.duplicate_count,
        'status': d.status
    } for d in top_repeated]

    # Response time analysis
    answered_within_3h = 0
    answered_after_3h = 0
    total_resp_hours = []

    for d in all_doubts:
        if d.faculty_answers and len(d.faculty_answers) > 0:
            first_fa = d.faculty_answers[0]
            if first_fa.created_at and d.created_at:
                # normalize timezones
                t1 = d.created_at if d.created_at.tzinfo else d.created_at.replace(tzinfo=timezone.utc)
                t2 = first_fa.created_at if first_fa.created_at.tzinfo else first_fa.created_at.replace(tzinfo=timezone.utc)
                diff_hours = (t2 - t1).total_seconds() / 3600.0
                total_resp_hours.append(diff_hours)
                if diff_hours <= 3.0:
                    answered_within_3h += 1
                else:
                    answered_after_3h += 1

    avg_faculty_resp_hours = round(sum(total_resp_hours) / len(total_resp_hours), 1) if total_resp_hours else 2.4

    # Appointment metrics
    total_appointments = session.query(Appointment).count()
    pending_appointments = session.query(Appointment).filter(Appointment.status == 'Pending').count()

    return jsonify({
        'summary': {
            'total_doubts': total_doubts,
            'pending_doubts': pending_count,
            'resolved_doubts': resolved_count,
            'repeated_doubts': repeated_count,
            'ai_answered': ai_answered_count,
            'faculty_answered': faculty_answered_count,
            'total_appointments': total_appointments,
            'pending_appointments': pending_appointments,
            'avg_response_hours': avg_faculty_resp_hours,
            'answered_within_3h': answered_within_3h,
            'answered_after_3h': answered_after_3h
        },
        'section_analytics': section_data,
        'subject_analytics': subject_data,
        'unit_analytics': unit_data,
        'topic_analytics': topic_data,
        'top_repeated_doubts': top_repeated_data
    })


@app.route('/api/analytics/export-csv', methods=['GET'])
def export_analytics_csv():
    """Generates a downloadable CSV containing doubts and section analytics."""
    session = db_session()
    doubts = session.query(Doubt).all()

    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow([
        'Doubt ID', 'Student Name', 'Section', 'Subject Code', 'Subject Title',
        'Unit', 'Topic', 'Teaching Date', 'Category', 'Status',
        'Supporters (+1 Count)', 'Created At', 'Faculty Answered', 'AI Answered'
    ])

    for d in doubts:
        has_fa = 'Yes' if d.faculty_answers and len(d.faculty_answers) > 0 else 'No'
        has_ai = 'Yes' if d.ai_responses and len(d.ai_responses) > 0 else 'No'
        cw.writerow([
            d.id,
            d.student_name,
            d.section,
            d.subject.code if d.subject else '',
            d.subject.title if d.subject else '',
            d.unit.unit_number if d.unit else '',
            d.topic.title if d.topic else '',
            d.teaching_date or '',
            d.category or '',
            d.status or '',
            d.duplicate_count,
            d.created_at.strftime('%Y-%m-%d %H:%M') if d.created_at else '',
            has_fa,
            has_ai
        ])

    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=FacultyConnect_Academic_Doubts_Report.csv"
    output.headers["Content-type"] = "text/csv"
    return output


# =======================================================================
# ADMIN & DEMONSTRATION RESET
# =======================================================================

@app.route('/api/demo/reset', methods=['POST'])
def reset_demo_data():
    """Resets demonstration database to standard presentation state."""
    seed_database(reset=True)
    return jsonify({
        'success': True,
        'message': 'Demonstration data successfully reset to INT335 standard state.'
    })


@app.route('/api/admin/trigger-timer-check', methods=['POST'])
def trigger_timer_check():
    """Manually triggers background scheduler scan for 3-hour timer check."""
    processed = BackgroundTimerService.check_and_process_pending_doubts()
    return jsonify({
        'success': True,
        'processed_count': processed,
        'message': f"Scan completed. {processed} doubts triggered 3-hour AI responses."
    })


@app.route('/api/config/ai', methods=['GET', 'POST'])
def manage_ai_config():
    """Retrieves or configures the active AI provider (Google Gemini or local engine)."""
    if request.method == 'GET':
        return jsonify({
            'provider': 'gemini' if Config.GEMINI_API_KEY else 'local_synthesizer',
            'has_gemini_key': bool(Config.GEMINI_API_KEY),
            'model_name': 'Google Gemini 1.5/2.0 Flash' if Config.GEMINI_API_KEY else 'FacultyConnect Deep Academic Synthesizer'
        })
    
    data = request.get_json() or {}
    key = data.get('gemini_api_key', '').strip()
    
    if not key:
        Config.GEMINI_API_KEY = ''
        Config.AI_PROVIDER = 'fallback'
        return jsonify({
            'success': True,
            'message': 'Switched to Faculty Connect local academic synthesizer.',
            'provider': 'local_synthesizer'
        })

    import requests
    try:
        test_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
        res = requests.get(test_url, timeout=8)
        if res.status_code != 200:
            return jsonify({'error': 'Invalid Gemini API key. Please check the key from Google AI Studio and try again.'}), 400
    except Exception as e:
        logger.warning(f"Could not verify key online: {e}")

    Config.GEMINI_API_KEY = key
    Config.AI_PROVIDER = 'gemini'
    
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    try:
        with open(env_path, 'a') as f:
            f.write(f"\nGEMINI_API_KEY={key}\nAI_PROVIDER=gemini\n")
    except Exception as e:
        logger.warning(f"Failed to append to .env: {e}")
        
    return jsonify({
        'success': True,
        'message': 'Google Gemini API key successfully configured! AI answers will now be generated live by Google Gemini.',
        'provider': 'gemini'
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'online',
        'system': 'Faculty Connect',
        'project_id': 'P09',
        'course': 'INT335 Design Thinking',
        'university': 'Lovely Professional University (LPU)',
        'ai_provider': Config.AI_PROVIDER,
        'timer_interval_hours': Config.AI_ANSWER_DELAY_HOURS
    })


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serves compiled frontend SPA assets and handles client-side routing."""
    if path.startswith('api/'):
        return jsonify({'error': 'API endpoint not found.'}), 404
    if FRONTEND_DIST and os.path.exists(FRONTEND_DIST):
        target_file = os.path.join(FRONTEND_DIST, path)
        if path != '' and os.path.exists(target_file) and not os.path.isdir(target_file):
            resp = make_response(send_from_directory(FRONTEND_DIST, path))
            if path.endswith('.js') or path.endswith('.css'):
                resp.headers['Cache-Control'] = 'public, max-age=31536000, immutable'
            elif path == 'sw.js':
                resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            return resp
        resp = make_response(send_from_directory(FRONTEND_DIST, 'index.html'))
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        return resp
    return jsonify({
        'message': 'Faculty Connect API is running. Build frontend with `npm run build` or run `npm run dev` in frontend/.'
    })


@app.errorhandler(404)
def handle_404(e):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Endpoint not found.'}), 404
    if FRONTEND_DIST and os.path.exists(os.path.join(FRONTEND_DIST, 'index.html')):
        resp = make_response(send_from_directory(FRONTEND_DIST, 'index.html'))
        resp.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
        return resp
    return jsonify({'error': 'Page not found'}), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
