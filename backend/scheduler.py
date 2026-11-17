import time
import threading
import logging
from datetime import datetime, timezone, timedelta
from database import db_session
from models import Doubt, AIResponse, Notification, Subject, Unit, Topic, Teacher
from ai_engine import SmartDoubtEngine
from config import Config

logger = logging.getLogger('scheduler')

class BackgroundTimerService:
    """
    Robust server-side background timer service.
    Runs periodically (every 60 seconds) to check for pending doubts that have exceeded
    the configurable response deadline (default 3 hours from creation).
    Generates intelligent syllabus-grounded AI answers and delivers notifications.
    """
    _running = False
    _thread = None

    @classmethod
    def start(cls, check_interval_seconds=60):
        if cls._running:
            return
        cls._running = True
        cls._thread = threading.Thread(
            target=cls._run_loop,
            args=(check_interval_seconds,),
            daemon=True
        )
        cls._thread.start()
        logger.info("BackgroundTimerService started (checks every %s seconds).", check_interval_seconds)

    @classmethod
    def stop(cls):
        cls._running = False

    @classmethod
    def _run_loop(cls, interval):
        while cls._running:
            try:
                cls.check_and_process_pending_doubts()
            except Exception as e:
                logger.error(f"Error in scheduler check loop: {e}", exc_info=True)
            time.sleep(interval)

    @classmethod
    def check_and_process_pending_doubts(cls):
        """
        Scans database for doubts that are still 'Pending' and whose response_deadline
        is in the past (i.e. > 3 hours since submission, or test threshold).
        """
        now = datetime.now(timezone.utc)
        session = db_session()
        try:
            # Query pending doubts with expired deadlines and no answers yet
            pending_doubts = session.query(Doubt).filter(
                Doubt.status.in_(['Pending', 'Under Review']),
                Doubt.response_deadline != None,
                Doubt.response_deadline <= now
            ).all()

            processed_count = 0
            for doubt in pending_doubts:
                # Double check that no faculty answer was posted
                if doubt.faculty_answers and len(doubt.faculty_answers) > 0:
                    doubt.status = 'Faculty Answered'
                    continue
                
                # Double check if AI has already answered
                if doubt.ai_responses and len(doubt.ai_responses) > 0:
                    doubt.status = 'AI Answered'
                    continue

                logger.info(f"Triggering 3-hour AI answer for Doubt #{doubt.id}: '{doubt.question_text[:40]}...'")
                
                subject = doubt.subject
                unit = doubt.unit
                topic = doubt.topic
                
                subject_title = subject.title if subject else "Academic Subject"
                unit_title = f"{unit.unit_number}: {unit.title}" if unit else "Unit"
                topic_title = topic.title if topic else "Topic"
                subtopics = topic.subtopics if topic else ""
                textbooks = subject.textbooks if subject else ""

                # Generate syllabus-grounded answer
                answer_text, confidence = SmartDoubtEngine.generate_academic_answer(
                    question_text=doubt.question_text,
                    subject_title=subject_title,
                    unit_title=unit_title,
                    topic_title=topic_title,
                    subtopics=subtopics,
                    textbooks=textbooks
                )

                # Create AI Response record
                ai_resp = AIResponse(
                    doubt_id=doubt.id,
                    model_name='FacultyConnect-Academic-AI (3-Hour Fallback)',
                    response_text=answer_text,
                    confidence_score=confidence,
                    faculty_quality_status='Pending'
                )
                session.add(ai_resp)

                # Update doubt status
                doubt.status = 'AI Answered'
                doubt.updated_at = now

                # Notify primary student
                notif_student = Notification(
                    recipient_type='student',
                    student_name=doubt.student_name,
                    title='Academic AI Assistant Responded',
                    message=f"An automated AI answer is now available for your doubt on {subject_title} ({topic_title}). Faculty will review it shortly.",
                    notification_type='ai_answer',
                    link_id=doubt.id
                )
                session.add(notif_student)

                # Also notify all +1 supporters who joined this doubt!
                for supporter in doubt.supporters:
                    if supporter.student_name != doubt.student_name:
                        notif_sup = Notification(
                            recipient_type='student',
                            student_name=supporter.student_name,
                            title='Update on Saved Doubt (+1)',
                            message=f"An AI answer has been posted for the {subject_title} doubt you supported (+1).",
                            notification_type='ai_answer',
                            link_id=doubt.id
                        )
                        session.add(notif_sup)

                # Notify faculty that AI responded after 3 hours and is awaiting faculty verification
                # Find teachers for this subject
                for ts in (subject.doubts if False else []): # placeholder
                    pass
                notif_teacher = Notification(
                    recipient_type='teacher',
                    teacher_id=None, # Global or subject-scoped
                    title='3-Hour AI Answer Triggered',
                    message=f"Doubt #{doubt.id} from {doubt.section} reached the 3-hour threshold and received an automated AI response. Please review and verify.",
                    notification_type='ai_answer',
                    link_id=doubt.id
                )
                session.add(notif_teacher)

                processed_count += 1

            if processed_count > 0:
                session.commit()
                logger.info(f"Processed {processed_count} doubts through the 3-hour AI engine.")
            return processed_count
        except Exception as e:
            session.rollback()
            logger.error(f"Error during pending doubts processing: {e}", exc_info=True)
            return 0
        finally:
            session.close()
