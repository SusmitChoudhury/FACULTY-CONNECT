import {
  Student, Teacher, Subject, Section, Doubt,
  FacultyAvailability, Appointment, Notification,
  Announcement, AnalyticsData
} from './types';

const API_BASE = '/api';

async function request<T>(endpoint: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {})
    },
    ...options
  });

  if (!res.ok) {
    let errorMsg = 'An unexpected server error occurred.';
    try {
      const errData = await res.json();
      if (errData && errData.error) errorMsg = errData.error;
    } catch {
      // fallback
    }
    throw new Error(errorMsg);
  }

  return res.json();
}

// Authentication
export const api = {
  // Auth
  studentLogin: (name: string, section: string) =>
    request<{ student: Student; message: string; role: 'student' }>('/auth/student-login', {
      method: 'POST',
      body: JSON.stringify({ name, section })
    }),

  teacherLogin: (email: string, password: string) =>
    request<{ teacher: Teacher; token: string; message: string; role: 'teacher' }>('/auth/teacher-login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    }),

  getAllTeachers: () => request<Teacher[]>('/auth/teachers'),

  // Subjects & Syllabus
  getSubjects: () => request<Subject[]>('/subjects'),
  getSubjectDetails: (id: number) => request<Subject>(`/subjects/${id}`),
  getSections: () => request<Section[]>('/sections'),
  searchSyllabus: (query: string) => request<any[]>(`/syllabus/search?q=${encodeURIComponent(query)}`),

  // Smart Doubt Intelligence Engine
  checkDuplicateDoubt: (data: {
    question_text: string;
    subject_id: number;
    unit_id: number;
    topic_id: number;
    section: string;
  }) =>
    request<{
      is_duplicate: boolean;
      confidence: number;
      matched_doubt: Doubt | null;
      existing_answer: {
        type: 'faculty' | 'ai';
        author: string;
        text: string;
        quality_status?: string;
        created_at: string;
      } | null;
    }>('/doubts/check-duplicate', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  supportExistingDoubt: (doubt_id: number, student_name: string, student_section: string) =>
    request<{ message: string; doubt: Doubt }>('/doubts/support-existing', {
      method: 'POST',
      body: JSON.stringify({ doubt_id, student_name, student_section })
    }),

  createDoubt: (data: {
    student_name: string;
    section: string;
    subject_id: number;
    unit_id: number;
    topic_id: number;
    teaching_date?: string;
    category?: string;
    question_text: string;
  }) =>
    request<{ message: string; doubt: Doubt }>('/doubts/create', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  // Doubts Management
  getDoubts: (params?: {
    student_name?: string;
    section?: string;
    subject_id?: number;
    unit_id?: number;
    topic_id?: number;
    status?: string;
    category?: string;
    repeated_only?: boolean;
    search?: string;
  }) => {
    const query = new URLSearchParams();
    if (params?.student_name) query.append('student_name', params.student_name);
    if (params?.section) query.append('section', params.section);
    if (params?.subject_id) query.append('subject_id', params.subject_id.toString());
    if (params?.unit_id) query.append('unit_id', params.unit_id.toString());
    if (params?.topic_id) query.append('topic_id', params.topic_id.toString());
    if (params?.status) query.append('status', params.status);
    if (params?.category) query.append('category', params.category);
    if (params?.repeated_only) query.append('repeated_only', 'true');
    if (params?.search) query.append('search', params.search);

    const queryString = query.toString() ? `?${query.toString()}` : '';
    return request<Doubt[]>(`/doubts${queryString}`);
  },

  getDoubtDetail: (id: number) => request<Doubt>(`/doubts/${id}`),

  postFacultyAnswer: (doubt_id: number, data: { teacher_id: number; teacher_name: string; answer_text: string }) =>
    request<{ message: string; doubt: Doubt }>(`/doubts/${doubt_id}/answer`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  generateAiAnswer: (doubt_id: number, data: { publish_immediately?: boolean; teacher_id?: number; teacher_name?: string }) =>
    request<{ message: string; doubt?: Doubt; ai_response?: any; ai_text?: string }>(`/doubts/${doubt_id}/generate-ai-answer`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  updateDoubtStatus: (doubt_id: number, status: string) =>
    request<{ message: string; doubt: Doubt }>(`/doubts/${doubt_id}/update-status`, {
      method: 'POST',
      body: JSON.stringify({ status })
    }),

  submitAiQualityFeedback: (doubt_id: number, data: { quality_status: string; notes?: string }) =>
    request<{ message: string }> (`/doubts/${doubt_id}/ai-quality-feedback`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  submitStudentFeedback: (doubt_id: number, data: { student_name: string; resolved: boolean; feedback_text?: string }) =>
    request<{ message: string }> (`/doubts/${doubt_id}/feedback`, {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  // Bookmarks
  getBookmarks: (student_name: string) =>
    request<{ id: number; student_name: string; doubt_id: number; doubt: Doubt }[]>(`/bookmarks?student_name=${encodeURIComponent(student_name)}`),

  toggleBookmark: (student_name: string, doubt_id: number) =>
    request<{ bookmarked: boolean; message: string }>('/bookmarks/toggle', {
      method: 'POST',
      body: JSON.stringify({ student_name, doubt_id })
    }),

  // Availability & Appointments
  getFacultyAvailability: (teacher_id?: number) => {
    const q = teacher_id ? `?teacher_id=${teacher_id}` : '';
    return request<FacultyAvailability[]>(`/faculty/availability${q}`);
  },

  addAvailability: (data: Partial<FacultyAvailability>) =>
    request<{ message: string; slot: FacultyAvailability }>('/faculty/availability', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  deleteAvailability: (slot_id: number) =>
    request<{ message: string }>(`/faculty/availability/${slot_id}`, {
      method: 'DELETE'
    }),

  getAppointments: (params?: { teacher_id?: number; student_name?: string; status?: string }) => {
    const query = new URLSearchParams();
    if (params?.teacher_id) query.append('teacher_id', params.teacher_id.toString());
    if (params?.student_name) query.append('student_name', params.student_name);
    if (params?.status) query.append('status', params.status);
    const qStr = query.toString() ? `?${query.toString()}` : '';
    return request<Appointment[]>(`/appointments${qStr}`);
  },

  bookAppointment: (data: {
    teacher_id: number;
    student_name: string;
    student_section: string;
    subject_id?: number;
    availability_id?: number;
    appointment_date: string;
    time_slot: string;
    location: string;
    reason: string;
  }) =>
    request<{ message: string; appointment: Appointment }>('/appointments/book', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  updateAppointmentStatus: (appointment_id: number, status: string, teacher_notes?: string) =>
    request<{ message: string; appointment: Appointment }>(`/appointments/${appointment_id}/status`, {
      method: 'POST',
      body: JSON.stringify({ status, teacher_notes })
    }),

  // Notifications
  getNotifications: (recipient_type: 'student' | 'teacher', identifier?: string | number) => {
    let url = `/notifications?recipient_type=${recipient_type}`;
    if (recipient_type === 'student' && identifier) url += `&student_name=${encodeURIComponent(identifier.toString())}`;
    if (recipient_type === 'teacher' && identifier) url += `&teacher_id=${identifier}`;
    return request<{ notifications: Notification[]; unread_count: number }>(url);
  },

  markNotificationRead: (id: number) =>
    request<{ success: boolean }>(`/notifications/${id}/read`, { method: 'POST' }),

  markAllNotificationsRead: (recipient_type: 'student' | 'teacher', identifier?: string | number) =>
    request<{ success: boolean; message: string }>('/notifications/mark-all-read', {
      method: 'POST',
      body: JSON.stringify({
        recipient_type,
        student_name: recipient_type === 'student' ? identifier : undefined,
        teacher_id: recipient_type === 'teacher' ? identifier : undefined
      })
    }),

  // Announcements
  getAnnouncements: (params?: { section?: string; subject_id?: number }) => {
    const query = new URLSearchParams();
    if (params?.section) query.append('section', params.section);
    if (params?.subject_id) query.append('subject_id', params.subject_id.toString());
    const qStr = query.toString() ? `?${query.toString()}` : '';
    return request<Announcement[]>(`/announcements${qStr}`);
  },

  createAnnouncement: (data: {
    teacher_id: number;
    teacher_name: string;
    subject_id: number;
    target_section: string;
    title: string;
    content: string;
    priority: string;
  }) =>
    request<{ message: string; announcement: Announcement }>('/announcements', {
      method: 'POST',
      body: JSON.stringify(data)
    }),

  // Analytics
  getAnalyticsDashboard: (params?: { teacher_id?: number; subject_id?: number; section?: string }) => {
    const query = new URLSearchParams();
    if (params?.teacher_id) query.append('teacher_id', params.teacher_id.toString());
    if (params?.subject_id) query.append('subject_id', params.subject_id.toString());
    if (params?.section) query.append('section', params.section);
    const qStr = query.toString() ? `?${query.toString()}` : '';
    return request<AnalyticsData>(`/analytics/dashboard${qStr}`);
  },

  exportAnalyticsCsvUrl: () => `${API_BASE}/analytics/export-csv`,

  // Demo Control
  resetDemoData: () =>
    request<{ success: boolean; message: string }>('/demo/reset', { method: 'POST' }),

  triggerTimerCheck: () =>
    request<{ success: boolean; processed_count: number; message: string }>('/admin/trigger-timer-check', { method: 'POST' }),

  // AI Configuration
  getAiConfig: () =>
    request<{ provider: string; has_gemini_key: boolean; model_name: string }>('/config/ai'),

  saveAiConfig: (gemini_api_key: string) =>
    request<{ success: boolean; message: string; provider: string }>('/config/ai', {
      method: 'POST',
      body: JSON.stringify({ gemini_api_key })
    })
};
