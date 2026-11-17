export interface Section {
  id: number;
  name: string;
  department?: string;
}

export interface Student {
  id: number;
  name: string;
  section: string;
  created_at: string;
}

export interface Teacher {
  id: number;
  name: string;
  email: string;
  department: string;
  cabin_location: string;
  phone: string;
  bio: string;
  assigned_subjects: {
    id: number;
    code: string;
    title: string;
    credits: number;
    lecture_hours: string;
  }[];
  assigned_sections: string[];
}

export interface CourseOutcome {
  id: number;
  co_code: string;
  description: string;
}

export interface Topic {
  id: number;
  unit_id: number;
  title: string;
  subtopics: string;
}

export interface Unit {
  id: number;
  subject_id: number;
  unit_number: string;
  title: string;
  topics: Topic[];
}

export interface Subject {
  id: number;
  code: string;
  title: string;
  credits: number;
  lecture_hours: string;
  textbooks: string;
  course_outcomes: CourseOutcome[];
  units: Unit[];
}

export interface FacultyAnswer {
  id: number;
  doubt_id: number;
  teacher_id: number;
  teacher_name: string;
  answer_text: string;
  created_at: string;
  updated_at?: string;
}

export interface AIResponse {
  id: number;
  doubt_id: number;
  model_name: string;
  response_text: string;
  confidence_score: number;
  faculty_quality_status: 'Pending' | 'Correct' | 'Needs Correction' | 'Incorrect' | 'Requires Additional Explanation';
  faculty_feedback_notes?: string;
  created_at: string;
}

export interface Supporter {
  id: number;
  doubt_id: number;
  student_name: string;
  student_section: string;
  created_at: string;
}

export interface Doubt {
  id: number;
  student_id: number;
  student_name: string;
  section: string;
  subject_id: number;
  subject_code: string;
  subject_title: string;
  unit_id: number;
  unit_title: string;
  topic_id: number;
  topic_title: string;
  teaching_date?: string;
  category: string;
  question_text: string;
  status: 'Pending' | 'Under Review' | 'AI Processing' | 'AI Answered' | 'Faculty Answered' | 'Faculty Verified' | 'Resolved' | 'Escalated';
  duplicate_count: number;
  is_duplicate_of?: number;
  response_deadline?: string;
  created_at: string;
  updated_at?: string;
  supporters?: Supporter[];
  faculty_answers?: FacultyAnswer[];
  ai_responses?: AIResponse[];
  feedback_count?: number;
  positive_feedback?: number;
}

export interface FacultyAvailability {
  id: number;
  teacher_id: number;
  teacher_name?: string;
  day_of_week: string;
  start_time: string;
  end_time: string;
  location: string;
  max_bookings: number;
  instructions: string;
  is_active: boolean;
}

export interface Appointment {
  id: number;
  teacher_id: number;
  teacher_name?: string;
  student_id: number;
  student_name: string;
  student_section: string;
  subject_id?: number;
  subject_code?: string;
  subject_title?: string;
  availability_id?: number;
  appointment_date: string;
  time_slot: string;
  location: string;
  reason: string;
  status: 'Pending' | 'Accepted' | 'Rejected' | 'Rescheduled' | 'Completed' | 'Cancelled';
  teacher_notes?: string;
  created_at: string;
}

export interface Notification {
  id: number;
  recipient_type: 'student' | 'teacher';
  student_name?: string;
  teacher_id?: number;
  title: string;
  message: string;
  notification_type: string;
  link_id?: number;
  is_read: boolean;
  created_at: string;
}

export interface Announcement {
  id: number;
  teacher_id: number;
  teacher_name: string;
  subject_id: number;
  subject_code?: string;
  subject_title?: string;
  target_section: string;
  title: string;
  content: string;
  priority: 'Normal' | 'Important' | 'Urgent';
  created_at: string;
}

export interface AnalyticsSummary {
  total_doubts: number;
  pending_doubts: number;
  resolved_doubts: number;
  repeated_doubts: number;
  ai_answered: number;
  faculty_answered: number;
  total_appointments: number;
  pending_appointments: number;
  avg_response_hours: number;
  answered_within_3h: number;
  answered_after_3h: number;
}

export interface AnalyticsData {
  summary: AnalyticsSummary;
  section_analytics: { section: string; doubts: number }[];
  subject_analytics: { subject: string; doubts: number }[];
  unit_analytics: { unit: string; doubts: number }[];
  topic_analytics: { topic: string; impact_score: number }[];
  top_repeated_doubts: {
    id: number;
    question: string;
    subject: string;
    topic: string;
    section: string;
    supporters_count: number;
    status: string;
  }[];
}
