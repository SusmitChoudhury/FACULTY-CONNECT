from datetime import datetime, timezone
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, 
    Boolean, Float, UniqueConstraint
)
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from database import Base

class Student(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    section = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'section': self.section,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Teacher(Base):
    __tablename__ = 'teachers'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    department = Column(String(100), default='School of Computer Science & Engineering')
    cabin_location = Column(String(100), default='Block 34, Cabin 601')
    phone = Column(String(20), default='+91 98765 43210')
    bio = Column(Text, default='')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    subjects = relationship('TeacherSubject', back_populates='teacher', cascade="all, delete-orphan")
    sections = relationship('TeacherSection', back_populates='teacher', cascade="all, delete-orphan")
    availabilities = relationship('FacultyAvailability', back_populates='teacher', cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'department': self.department,
            'cabin_location': self.cabin_location,
            'phone': self.phone,
            'bio': self.bio,
            'assigned_subjects': [ts.subject.to_summary_dict() for ts in self.subjects if ts.subject],
            'assigned_sections': [sec.section_name for sec in self.sections]
        }

class Section(Base):
    __tablename__ = 'sections'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    department = Column(String(100), default='Computer Science & Engineering')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'department': self.department
        }

class Subject(Base):
    __tablename__ = 'subjects'
    
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    title = Column(String(150), nullable=False)
    credits = Column(Integer, default=3)
    lecture_hours = Column(String(50), default='L:3 T:0 P:0')
    textbooks = Column(Text, default='')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    units = relationship('Unit', back_populates='subject', order_by='Unit.id', cascade="all, delete-orphan")
    course_outcomes = relationship('CourseOutcome', back_populates='subject', cascade="all, delete-orphan")
    doubts = relationship('Doubt', back_populates='subject')
    
    def to_summary_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'title': self.title,
            'credits': self.credits,
            'lecture_hours': self.lecture_hours
        }

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'title': self.title,
            'credits': self.credits,
            'lecture_hours': self.lecture_hours,
            'textbooks': self.textbooks,
            'course_outcomes': [co.to_dict() for co in self.course_outcomes],
            'units': [u.to_dict() for u in self.units]
        }

class CourseOutcome(Base):
    __tablename__ = 'course_outcomes'
    
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    co_code = Column(String(20), nullable=False)
    description = Column(Text, nullable=False)
    
    subject = relationship('Subject', back_populates='course_outcomes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'co_code': self.co_code,
            'description': self.description
        }

class Unit(Base):
    __tablename__ = 'units'
    
    id = Column(Integer, primary_key=True)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    unit_number = Column(String(20), nullable=False)
    title = Column(String(200), nullable=False)
    
    subject = relationship('Subject', back_populates='units')
    topics = relationship('Topic', back_populates='unit', order_by='Topic.id', cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'subject_id': self.subject_id,
            'unit_number': self.unit_number,
            'title': self.title,
            'topics': [t.to_dict() for t in self.topics]
        }

class Topic(Base):
    __tablename__ = 'topics'
    
    id = Column(Integer, primary_key=True)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    title = Column(String(250), nullable=False)
    subtopics = Column(Text, default='')
    
    unit = relationship('Unit', back_populates='topics')
    
    def to_dict(self):
        return {
            'id': self.id,
            'unit_id': self.unit_id,
            'title': self.title,
            'subtopics': self.subtopics
        }

class TeacherSubject(Base):
    __tablename__ = 'teacher_subjects'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    
    teacher = relationship('Teacher', back_populates='subjects')
    subject = relationship('Subject')

class TeacherSection(Base):
    __tablename__ = 'teacher_sections'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    section_name = Column(String(50), nullable=False)
    
    teacher = relationship('Teacher', back_populates='sections')

class Doubt(Base):
    __tablename__ = 'doubts'
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    student_name = Column(String(100), nullable=False)
    section = Column(String(50), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    unit_id = Column(Integer, ForeignKey('units.id'), nullable=False)
    topic_id = Column(Integer, ForeignKey('topics.id'), nullable=False)
    teaching_date = Column(String(20), nullable=True)
    category = Column(String(50), default='Conceptual Doubt')
    question_text = Column(Text, nullable=False)
    status = Column(String(50), default='Pending') # Pending, Under Review, AI Processing, AI Answered, Faculty Answered, Faculty Verified, Resolved, Escalated
    duplicate_count = Column(Integer, default=1)
    is_duplicate_of = Column(Integer, ForeignKey('doubts.id'), nullable=True)
    response_deadline = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    subject = relationship('Subject', back_populates='doubts')
    unit = relationship('Unit')
    topic = relationship('Topic')
    supporters = relationship('DoubtStudentSupport', back_populates='doubt', cascade="all, delete-orphan")
    faculty_answers = relationship('FacultyAnswer', back_populates='doubt', cascade="all, delete-orphan")
    ai_responses = relationship('AIResponse', back_populates='doubt', cascade="all, delete-orphan")
    feedbacks = relationship('StudentFeedback', back_populates='doubt', cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'student_name': self.student_name,
            'section': self.section,
            'subject_id': self.subject_id,
            'subject_code': self.subject.code if self.subject else None,
            'subject_title': self.subject.title if self.subject else None,
            'unit_id': self.unit_id,
            'unit_title': f"{self.unit.unit_number}: {self.unit.title}" if self.unit else None,
            'topic_id': self.topic_id,
            'topic_title': self.topic.title if self.topic else None,
            'teaching_date': self.teaching_date,
            'category': self.category,
            'question_text': self.question_text,
            'status': self.status,
            'duplicate_count': self.duplicate_count,
            'is_duplicate_of': self.is_duplicate_of,
            'response_deadline': self.response_deadline.isoformat() if self.response_deadline else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'supporters': [s.to_dict() for s in self.supporters],
            'faculty_answers': [fa.to_dict() for fa in self.faculty_answers],
            'ai_responses': [ar.to_dict() for ar in self.ai_responses],
            'feedback_count': len(self.feedbacks),
            'positive_feedback': sum(1 for fb in self.feedbacks if fb.resolved)
        }

class DoubtStudentSupport(Base):
    __tablename__ = 'doubt_student_supports'
    
    id = Column(Integer, primary_key=True)
    doubt_id = Column(Integer, ForeignKey('doubts.id'), nullable=False)
    student_name = Column(String(100), nullable=False)
    student_section = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        UniqueConstraint('doubt_id', 'student_name', 'student_section', name='_doubt_student_uc'),
    )
    
    doubt = relationship('Doubt', back_populates='supporters')
    
    def to_dict(self):
        return {
            'id': self.id,
            'doubt_id': self.doubt_id,
            'student_name': self.student_name,
            'student_section': self.student_section,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class FacultyAnswer(Base):
    __tablename__ = 'faculty_answers'
    
    id = Column(Integer, primary_key=True)
    doubt_id = Column(Integer, ForeignKey('doubts.id'), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher_name = Column(String(100), nullable=False)
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    doubt = relationship('Doubt', back_populates='faculty_answers')
    teacher = relationship('Teacher')
    
    def to_dict(self):
        return {
            'id': self.id,
            'doubt_id': self.doubt_id,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'answer_text': self.answer_text,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class AIResponse(Base):
    __tablename__ = 'ai_responses'
    
    id = Column(Integer, primary_key=True)
    doubt_id = Column(Integer, ForeignKey('doubts.id'), nullable=False)
    model_name = Column(String(100), default='FacultyConnect-Academic-Engine')
    response_text = Column(Text, nullable=False)
    confidence_score = Column(Float, default=0.92)
    faculty_quality_status = Column(String(50), default='Pending') # Correct, Needs Correction, Incorrect, Requires Additional Explanation
    faculty_feedback_notes = Column(Text, default='')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    doubt = relationship('Doubt', back_populates='ai_responses')
    
    def to_dict(self):
        return {
            'id': self.id,
            'doubt_id': self.doubt_id,
            'model_name': self.model_name,
            'response_text': self.response_text,
            'confidence_score': self.confidence_score,
            'faculty_quality_status': self.faculty_quality_status,
            'faculty_feedback_notes': self.faculty_feedback_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class FacultyAvailability(Base):
    __tablename__ = 'faculty_availabilities'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    day_of_week = Column(String(20), nullable=False) # Monday, Tuesday, etc.
    start_time = Column(String(20), nullable=False) # "10:00 AM"
    end_time = Column(String(20), nullable=False)   # "11:00 AM"
    location = Column(String(100), default='Cabin 34-601')
    max_bookings = Column(Integer, default=3)
    instructions = Column(Text, default='Bring your lecture notes and specific code/problem statements.')
    is_active = Column(Boolean, default=True)
    
    teacher = relationship('Teacher', back_populates='availabilities')
    appointments = relationship('Appointment', back_populates='availability')
    
    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.name if self.teacher else None,
            'day_of_week': self.day_of_week,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'location': self.location,
            'max_bookings': self.max_bookings,
            'instructions': self.instructions,
            'is_active': self.is_active
        }

class Appointment(Base):
    __tablename__ = 'appointments'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=True)
    student_name = Column(String(100), nullable=False)
    student_section = Column(String(50), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=True)
    availability_id = Column(Integer, ForeignKey('faculty_availabilities.id'), nullable=True)
    appointment_date = Column(String(20), nullable=False) # YYYY-MM-DD
    time_slot = Column(String(50), nullable=False) # e.g. "10:00 AM - 11:00 AM"
    location = Column(String(100), default='Cabin 34-601')
    reason = Column(Text, nullable=False)
    status = Column(String(50), default='Pending') # Pending, Accepted, Rejected, Rescheduled, Completed, Cancelled
    teacher_notes = Column(Text, default='')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    teacher = relationship('Teacher')
    student = relationship('Student')
    subject = relationship('Subject')
    availability = relationship('FacultyAvailability', back_populates='appointments')
    
    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher.name if self.teacher else None,
            'student_id': self.student_id,
            'student_name': self.student_name,
            'student_section': self.student_section,
            'subject_id': self.subject_id,
            'subject_code': self.subject.code if self.subject else None,
            'subject_title': self.subject.title if self.subject else None,
            'availability_id': self.availability_id,
            'appointment_date': self.appointment_date,
            'time_slot': self.time_slot,
            'location': self.location,
            'reason': self.reason,
            'status': self.status,
            'teacher_notes': self.teacher_notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Notification(Base):
    __tablename__ = 'notifications'
    
    id = Column(Integer, primary_key=True)
    recipient_type = Column(String(20), nullable=False) # 'student' or 'teacher'
    student_name = Column(String(100), nullable=True)
    teacher_id = Column(Integer, nullable=True)
    title = Column(String(150), nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String(50), default='general')
    link_id = Column(Integer, nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'recipient_type': self.recipient_type,
            'student_name': self.student_name,
            'teacher_id': self.teacher_id,
            'title': self.title,
            'message': self.message,
            'notification_type': self.notification_type,
            'link_id': self.link_id,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Announcement(Base):
    __tablename__ = 'announcements'
    
    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('teachers.id'), nullable=False)
    teacher_name = Column(String(100), nullable=False)
    subject_id = Column(Integer, ForeignKey('subjects.id'), nullable=False)
    target_section = Column(String(50), default='All')
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(String(20), default='Normal') # Normal, Important, Urgent
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    teacher = relationship('Teacher')
    subject = relationship('Subject')
    
    def to_dict(self):
        return {
            'id': self.id,
            'teacher_id': self.teacher_id,
            'teacher_name': self.teacher_name,
            'subject_id': self.subject_id,
            'subject_code': self.subject.code if self.subject else None,
            'subject_title': self.subject.title if self.subject else None,
            'target_section': self.target_section,
            'title': self.title,
            'content': self.content,
            'priority': self.priority,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Bookmark(Base):
    __tablename__ = 'bookmarks'
    
    id = Column(Integer, primary_key=True)
    student_name = Column(String(100), nullable=False)
    doubt_id = Column(Integer, ForeignKey('doubts.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    __table_args__ = (
        UniqueConstraint('student_name', 'doubt_id', name='_student_bookmark_uc'),
    )
    
    doubt = relationship('Doubt')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_name': self.student_name,
            'doubt_id': self.doubt_id,
            'doubt': self.doubt.to_dict() if self.doubt else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class StudentFeedback(Base):
    __tablename__ = 'student_feedbacks'
    
    id = Column(Integer, primary_key=True)
    doubt_id = Column(Integer, ForeignKey('doubts.id'), nullable=False)
    student_name = Column(String(100), nullable=False)
    resolved = Column(Boolean, default=True)
    feedback_text = Column(Text, default='')
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    doubt = relationship('Doubt', back_populates='feedbacks')
    
    def to_dict(self):
        return {
            'id': self.id,
            'doubt_id': self.doubt_id,
            'student_name': self.student_name,
            'resolved': self.resolved,
            'feedback_text': self.feedback_text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
