import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  HelpCircle, BookOpen, Calendar, MessageSquare, 
  Clock, CheckCircle, Sparkles, Megaphone, ArrowRight,
  TrendingUp, Users, ChevronRight, Bookmark, BookCheck
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api';
import { Doubt, Appointment, Announcement } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export const StudentDashboard: React.FC = () => {
  const { student } = useAuth();
  const navigate = useNavigate();

  const [doubts, setDoubts] = useState<Doubt[]>([]);
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!student) return;

    const loadData = async () => {
      try {
        setLoading(true);
        const [doubtsRes, appRes, annRes] = await Promise.all([
          api.getDoubts({ student_name: student.name }),
          api.getAppointments({ student_name: student.name }),
          api.getAnnouncements({ section: student.section })
        ]);

        setDoubts(doubtsRes);
        setAppointments(appRes);
        setAnnouncements(annRes);
      } catch (e) {
        console.warn('Failed loading student dashboard:', e);
      } finally {
        setLoading(false);
      }
    };

    loadData();
  }, [student]);

  const totalSubmitted = doubts.length;
  const pendingCount = doubts.filter(d => d.status === 'Pending' || d.status === 'Under Review').length;
  const resolvedCount = doubts.filter(d => ['Resolved', 'Faculty Answered', 'Faculty Verified', 'AI Answered'].includes(d.status)).length;
  const upcomingAppointments = appointments.filter(a => ['Pending', 'Accepted'].includes(a.status));

  return (
    <div className="space-y-6 animate-fade-in pb-12">
      
      {/* Welcome Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-[#15370D] text-[#FCF9EA] shadow-md border border-[#F2842F]/30 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FCF9EA]/10 border border-[#F2842F]/40 text-xs font-semibold text-[#F2842F] mb-2">
            <span>Section {student?.section}</span>
            <span>•</span>
            <span>School of Computer Science & Engineering</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-[#FCF9EA]">
            Welcome back, {student?.name}!
          </h1>
          <p className="text-xs sm:text-sm text-[#FCF9EA]/80 mt-1 max-w-xl">
            Track your academic questions, discover duplicate queries from your classmates, and schedule cabin consultations with your course professors.
          </p>
        </div>

        <button
          onClick={() => navigate('/student/ask')}
          className="px-5 py-3 rounded-2xl bg-[#F2842F] hover:bg-[#F2842F]/90 text-[#000000] font-extrabold text-sm shadow-lg flex items-center gap-2 shrink-0 transition"
        >
          <HelpCircle className="w-5 h-5" />
          <span>Ask a Doubt</span>
        </button>
      </div>

      {/* Prominent Quick Actions Grid (Section 5 Requirement) */}
      <div className="grid grid-cols-2 lg:grid-cols-5 gap-3 sm:gap-4">
        <button
          onClick={() => navigate('/student/ask')}
          className="p-4 sm:p-5 rounded-2xl bg-white border border-[#E5DFC8] hover:border-[#15370D] hover:shadow-md transition text-left group"
        >
          <div className="w-10 h-10 rounded-xl bg-[#F2842F]/15 text-[#F2842F] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
            <HelpCircle className="w-6 h-6 text-[#F2842F]" />
          </div>
          <h3 className="font-bold text-sm sm:text-base text-gray-900 group-hover:text-[#15370D]">
            ASK A DOUBT
          </h3>
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">Smart duplicate detection</p>
        </button>

        <button
          onClick={() => navigate('/student/questions')}
          className="p-4 sm:p-5 rounded-2xl bg-white border border-[#E5DFC8] hover:border-[#15370D] hover:shadow-md transition text-left group"
        >
          <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-800 flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
            <MessageSquare className="w-6 h-6 text-emerald-800" />
          </div>
          <h3 className="font-bold text-sm sm:text-base text-gray-900 group-hover:text-[#15370D]">
            MY QUESTIONS
          </h3>
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">Track answers &amp; statuses</p>
        </button>

        <button
          onClick={() => navigate('/student/answered')}
          className="p-4 sm:p-5 rounded-2xl bg-white border border-[#E5DFC8] hover:border-[#15370D] hover:shadow-md transition text-left group"
        >
          <div className="w-10 h-10 rounded-xl bg-amber-50 text-[#F2842F] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
            <BookCheck className="w-6 h-6 text-[#F2842F]" />
          </div>
          <h3 className="font-bold text-sm sm:text-base text-gray-900 group-hover:text-[#15370D]">
            ANSWERED DOUBTS
          </h3>
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">Verified Knowledge Base</p>
        </button>

        <button
          onClick={() => navigate('/student/subjects')}
          className="p-4 sm:p-5 rounded-2xl bg-white border border-[#E5DFC8] hover:border-[#15370D] hover:shadow-md transition text-left group"
        >
          <div className="w-10 h-10 rounded-xl bg-[#15370D]/10 text-[#15370D] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
            <BookOpen className="w-6 h-6 text-[#15370D]" />
          </div>
          <h3 className="font-bold text-sm sm:text-base text-gray-900 group-hover:text-[#15370D]">
            EXPLORE SUBJECTS
          </h3>
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">Official course syllabus</p>
        </button>

        <button
          onClick={() => navigate('/student/availability')}
          className="p-4 sm:p-5 rounded-2xl bg-white border border-[#E5DFC8] hover:border-[#15370D] hover:shadow-md transition text-left group"
        >
          <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-800 flex items-center justify-center mb-3 group-hover:scale-105 transition-transform">
            <Calendar className="w-6 h-6 text-blue-800" />
          </div>
          <h3 className="font-bold text-sm sm:text-base text-gray-900 group-hover:text-[#15370D]">
            CHECK AVAILABILITY
          </h3>
          <p className="text-xs text-gray-500 mt-0.5 line-clamp-1">Book cabin appointments</p>
        </button>
      </div>

      {/* Metrics Summary Strip */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4">
        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-xs font-semibold text-gray-500">Total Doubts</p>
          <p className="text-2xl font-black text-gray-900 mt-1">{totalSubmitted}</p>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-xs font-semibold text-[#F2842F]">Pending Doubts</p>
          <p className="text-2xl font-black text-[#000000] mt-1">{pendingCount}</p>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-xs font-semibold text-emerald-700">Resolved / Answered</p>
          <p className="text-2xl font-black text-[#15370D] mt-1">{resolvedCount}</p>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-xs font-semibold text-blue-700">Upcoming Appointments</p>
          <p className="text-2xl font-black text-gray-900 mt-1">{upcomingAppointments.length}</p>
        </div>
      </div>

      {/* Two Column Content: Recent Questions & Faculty Announcements */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left 2 Cols: Recent Doubts Activity */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base sm:text-lg font-bold text-gray-900 flex items-center gap-2">
              <MessageSquare className="w-5 h-5 text-[#15370D]" />
              <span>Recent Academic Doubts</span>
            </h2>
            <Link
              to="/student/questions"
              className="text-xs font-bold text-[#15370D] hover:text-[#F2842F] flex items-center gap-1 transition"
            >
              <span>View All</span>
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="space-y-3">
            {doubts.slice(0, 4).map((doubt) => (
              <div
                key={doubt.id}
                onClick={() => navigate('/student/questions')}
                className="p-4 rounded-2xl bg-white border border-[#E5DFC8] hover:border-[#15370D] shadow-xs hover:shadow-md cursor-pointer transition"
              >
                <div className="flex items-center justify-between gap-2 mb-2">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[11px] font-black bg-[#15370D] text-[#FCF9EA]">
                      {doubt.subject_code}
                    </span>
                    <span className="text-xs font-semibold text-gray-600 truncate max-w-[200px]">
                      {doubt.topic_title}
                    </span>
                  </div>
                  <StatusBadge status={doubt.status} size="sm" />
                </div>

                <p className="text-xs sm:text-sm font-semibold text-gray-900 line-clamp-2">
                  {doubt.question_text}
                </p>

                <div className="mt-3 pt-2.5 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-500">
                  <div className="flex items-center gap-3">
                    <span>{doubt.teaching_date ? `Lecture: ${doubt.teaching_date}` : `Submitted recently`}</span>
                    {doubt.duplicate_count > 1 && (
                      <span className="font-bold text-[#F2842F] flex items-center gap-1">
                        +{doubt.duplicate_count - 1} classmates shared this
                      </span>
                    )}
                  </div>
                  {doubt.faculty_answers && doubt.faculty_answers.length > 0 && (
                    <span className="text-[#15370D] font-bold">Answered by {doubt.faculty_answers[0].teacher_name}</span>
                  )}
                  {(!doubt.faculty_answers || doubt.faculty_answers.length === 0) && doubt.ai_responses && doubt.ai_responses.length > 0 && (
                    <span className="text-[#F2842F] font-bold">AI Answer Available</span>
                  )}
                </div>
              </div>
            ))}

            {doubts.length === 0 && !loading && (
              <div className="p-8 text-center bg-white rounded-2xl border border-dashed border-[#D8D2BA]">
                <HelpCircle className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
                <p className="font-bold text-gray-800 text-sm">No doubts submitted yet</p>
                <p className="text-xs text-gray-500 mt-1 max-w-sm mx-auto">
                  Have a question from today's lecture? Click below to submit your query and check if your classmates asked the same thing.
                </p>
                <button
                  onClick={() => navigate('/student/ask')}
                  className="mt-4 px-4 py-2 bg-[#15370D] text-[#FCF9EA] font-bold rounded-xl text-xs"
                >
                  Ask a Doubt Now
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Right Col: Announcements & Upcoming Consultation */}
        <div className="space-y-6">
          
          {/* Upcoming Appointment Widget */}
          <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3">
            <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
              <Calendar className="w-4 h-4 text-blue-700" />
              <span>Upcoming Cabin Consultations</span>
            </h3>

            {upcomingAppointments.length > 0 ? (
              <div className="p-3.5 rounded-2xl bg-blue-50/70 border border-blue-200 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-blue-900">
                    {upcomingAppointments[0].teacher_name}
                  </span>
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${
                    upcomingAppointments[0].status === 'Accepted' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {upcomingAppointments[0].status}
                  </span>
                </div>
                <p className="text-xs text-gray-700 font-medium">
                  {upcomingAppointments[0].time_slot} • {upcomingAppointments[0].appointment_date}
                </p>
                <p className="text-[11px] text-gray-600">
                  Location: <span className="font-semibold">{upcomingAppointments[0].location}</span>
                </p>
              </div>
            ) : (
              <p className="text-xs text-gray-500 py-2">
                No active consultation appointments. Need help? Book an open slot with your faculty.
              </p>
            )}

            <button
              onClick={() => navigate('/student/availability')}
              className="w-full py-2 bg-[#FAF6E4] hover:bg-[#FAF6E4]/80 text-[#15370D] border border-[#D8D2BA] rounded-xl text-xs font-bold transition"
            >
              Browse Faculty Schedules
            </button>
          </div>

          {/* Announcements Widget */}
          <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3">
            <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
              <Megaphone className="w-4 h-4 text-[#15370D]" />
              <span>Course Announcements</span>
            </h3>

            <div className="space-y-2.5">
              {announcements.slice(0, 3).map((ann) => (
                <div key={ann.id} className="p-3 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8]">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#15370D] text-[#FCF9EA]">
                      {ann.subject_code || 'Notice'}
                    </span>
                    <span className="text-[10px] text-gray-500">
                      {new Date(ann.created_at).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                    </span>
                  </div>
                  <h4 className="text-xs font-bold text-gray-900">{ann.title}</h4>
                  <p className="text-[11px] text-gray-600 mt-1 line-clamp-2 leading-relaxed">
                    {ann.content}
                  </p>
                  <p className="text-[10px] font-semibold text-[#F2842F] mt-1.5">
                    — {ann.teacher_name}
                  </p>
                </div>
              ))}

              {announcements.length === 0 && (
                <p className="text-xs text-gray-500 py-2">No announcements posted for your section yet.</p>
              )}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};
