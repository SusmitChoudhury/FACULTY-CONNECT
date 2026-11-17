import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  MessageSquare, Clock, CheckCircle2, Sparkles, 
  Copy, Users, Calendar, BarChart3, AlertTriangle, 
  ArrowRight, ShieldCheck, ChevronRight, Layers, Flame, Loader2
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { api } from '../../api';
import { Doubt, Appointment, AnalyticsData } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export const TeacherDashboard: React.FC = () => {
  const { teacher } = useAuth();
  const navigate = useNavigate();

  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [pendingDoubts, setPendingDoubts] = useState<Doubt[]>([]);
  const [upcomingAppointments, setUpcomingAppointments] = useState<Appointment[]>([]);
  const [loading, setLoading] = useState(true);
  const [generatingAiForId, setGeneratingAiForId] = useState<number | null>(null);
  const [actionNotice, setActionNotice] = useState<string | null>(null);

  const handleGiveAnsByAi = async (doubtId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!teacher) return;
    try {
      setGeneratingAiForId(doubtId);
      const res = await api.generateAiAnswer(doubtId, {
        publish_immediately: true,
        teacher_id: teacher.id,
        teacher_name: teacher.name
      });
      // Remove answered question from pending queue and display confirmation
      setPendingDoubts(prev => prev.filter(d => d.id !== doubtId));
      setActionNotice(res.message || 'AI Answer generated and published to student!');
      setTimeout(() => setActionNotice(null), 6000);
    } catch (err: any) {
      alert(err?.response?.data?.error || err.message || 'Failed to generate AI answer');
    } finally {
      setGeneratingAiForId(null);
    }
  };

  useEffect(() => {
    if (!teacher) return;

    const loadDashboard = async () => {
      try {
        setLoading(true);
        const [dashRes, doubtsRes, appRes] = await Promise.all([
          api.getAnalyticsDashboard({ teacher_id: teacher.id }),
          api.getDoubts({ status: 'Pending' }),
          api.getAppointments({ teacher_id: teacher.id, status: 'Pending' })
        ]);

        setAnalytics(dashRes);
        setPendingDoubts(doubtsRes);
        setUpcomingAppointments(appRes);
      } catch (e) {
        console.warn('Failed loading teacher dashboard:', e);
      } finally {
        setLoading(false);
      }
    };

    loadDashboard();
  }, [teacher]);

  const summary = analytics?.summary;

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header Banner */}
      <div className="p-6 sm:p-8 rounded-3xl bg-[#15370D] text-[#FCF9EA] shadow-md border border-[#F2842F]/30 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FCF9EA]/10 border border-[#F2842F]/40 text-xs font-semibold text-[#F2842F] mb-2">
            <span>Faculty Console</span>
            <span>•</span>
            <span>Cabin: {teacher?.cabin_location}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black text-[#FCF9EA]">
            {teacher?.name}
          </h1>
          <p className="text-xs sm:text-sm text-[#FCF9EA]/80 mt-1 max-w-xl">
            {teacher?.department}. Assigned courses: {teacher?.assigned_subjects.map(s => s.code).join(', ')}.
          </p>
        </div>

        <button
          onClick={() => navigate('/teacher/doubts')}
          className="px-5 py-3 rounded-2xl bg-[#F2842F] hover:bg-[#F2842F]/90 text-[#000000] font-extrabold text-sm shadow-lg flex items-center gap-2 shrink-0 transition"
        >
          <MessageSquare className="w-5 h-5" />
          <span>Review Doubt Queue</span>
        </button>
      </div>

      {/* 6 Analytics Overview Cards (Section 13 Requirement) */}
      <div className="grid grid-cols-2 lg:grid-cols-6 gap-3 sm:gap-4">
        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-[11px] font-bold text-gray-500 uppercase tracking-wider">Total Doubts</p>
          <p className="text-2xl font-black text-gray-900 mt-1">{summary?.total_doubts ?? 0}</p>
        </div>

        <div className="p-4 rounded-2xl bg-white border-2 border-[#F2842F] shadow-xs">
          <p className="text-[11px] font-bold text-[#F2842F] uppercase tracking-wider">Pending Doubts</p>
          <p className="text-2xl font-black text-[#000000] mt-1">{summary?.pending_doubts ?? 0}</p>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-[11px] font-bold text-emerald-800 uppercase tracking-wider">Resolved</p>
          <p className="text-2xl font-black text-[#15370D] mt-1">{summary?.resolved_doubts ?? 0}</p>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-[11px] font-bold text-amber-600 uppercase tracking-wider flex items-center gap-1">
            <Flame className="w-3.5 h-3.5 text-[#F2842F]" />
            Repeated (+1)
          </p>
          <p className="text-2xl font-black text-gray-900 mt-1">{summary?.repeated_doubts ?? 0}</p>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-[11px] font-bold text-indigo-700 uppercase tracking-wider flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-[#F2842F]" />
            AI Answered
          </p>
          <p className="text-2xl font-black text-gray-900 mt-1">{summary?.ai_answered ?? 0}</p>
        </div>

        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs">
          <p className="text-[11px] font-bold text-[#15370D] uppercase tracking-wider flex items-center gap-1">
            <CheckCircle2 className="w-3.5 h-3.5 text-[#15370D]" />
            Faculty Answered
          </p>
          <p className="text-2xl font-black text-gray-900 mt-1">{summary?.faculty_answered ?? 0}</p>
        </div>
      </div>

      {/* Two Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left 2 Cols: Questions Awaiting Response (With 3-Hour Timer Warning) */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-base sm:text-lg font-bold text-gray-900 flex items-center gap-2">
              <Clock className="w-5 h-5 text-[#F2842F]" />
              <span>Questions Awaiting Faculty Response</span>
            </h2>
            <Link
              to="/teacher/doubts?tab=pending"
              className="text-xs font-bold text-[#15370D] hover:text-[#F2842F] flex items-center gap-1 transition"
            >
              <span>View All Pending</span>
              <ChevronRight className="w-4 h-4" />
            </Link>
          </div>

          {actionNotice && (
            <div className="p-4 rounded-2xl bg-emerald-50 border border-emerald-300 text-emerald-900 text-xs font-bold flex items-center gap-2 animate-fade-in">
              <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
              <span>{actionNotice}</span>
            </div>
          )}

          <div className="space-y-3">
            {pendingDoubts.slice(0, 4).map((doubt) => (
              <div
                key={doubt.id}
                onClick={() => navigate('/teacher/doubts')}
                className="p-5 rounded-2xl bg-white border border-[#E5DFC8] hover:border-[#15370D] shadow-xs hover:shadow-md cursor-pointer transition space-y-3"
              >
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-black bg-[#15370D] text-[#FCF9EA]">
                      {doubt.subject_code}
                    </span>
                    <span className="text-xs font-bold text-gray-800">Section {doubt.section}</span>
                    <span className="text-gray-400">•</span>
                    <span className="text-xs text-gray-600 truncate max-w-[200px]">{doubt.topic_title}</span>
                  </div>

                  <span className="px-2.5 py-1 rounded-full bg-amber-50 border border-amber-300 text-amber-900 text-xs font-bold flex items-center gap-1">
                    <Clock className="w-3.5 h-3.5 text-[#F2842F]" />
                    <span>3h Timer Active</span>
                  </span>
                </div>

                <p className="text-sm font-bold text-gray-900 leading-snug">
                  "{doubt.question_text}"
                </p>

                <div className="pt-2 border-t border-gray-100 flex flex-wrap items-center justify-between gap-3 text-[11px] text-gray-500">
                  <div className="flex items-center gap-3">
                    <span>From: <strong>{doubt.student_name}</strong></span>
                    <span>Lecture: {doubt.teaching_date || 'N/A'}</span>
                    {doubt.duplicate_count > 1 && (
                      <span className="font-extrabold text-[#F2842F]">
                        👥 {doubt.duplicate_count} students affected
                      </span>
                    )}
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <button
                      onClick={(e) => handleGiveAnsByAi(doubt.id, e)}
                      disabled={generatingAiForId === doubt.id}
                      title="Generate and immediately publish verified AI answer to student"
                      className="px-3 py-1.5 rounded-xl bg-[#FAF6E4] hover:bg-[#F2842F] text-[#15370D] hover:text-white border border-[#E5DFC8] hover:border-[#F2842F] text-xs font-bold flex items-center gap-1.5 transition shadow-2xs disabled:opacity-50"
                    >
                      {generatingAiForId === doubt.id ? (
                        <>
                          <Loader2 className="w-3.5 h-3.5 animate-spin text-[#F2842F]" />
                          <span>Generating...</span>
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-3.5 h-3.5 text-[#F2842F]" />
                          <span>Give Ans by AI</span>
                        </>
                      )}
                    </button>

                    <span className="text-[#15370D] font-bold flex items-center gap-1 hover:underline">
                      Answer Manual <ArrowRight className="w-3.5 h-3.5" />
                    </span>
                  </div>
                </div>
              </div>
            ))}

            {pendingDoubts.length === 0 && !loading && (
              <div className="p-8 text-center bg-white rounded-2xl border border-dashed border-[#D8D2BA]">
                <CheckCircle2 className="w-10 h-10 mx-auto text-emerald-600 mb-2 stroke-1" />
                <p className="font-bold text-gray-900 text-sm">Inbox Zero!</p>
                <p className="text-xs text-gray-500 mt-0.5">All incoming student questions have been answered.</p>
              </div>
            )}
          </div>

          {/* Section-Wise Activity Bar Preview */}
          <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-4">
            <h3 className="text-sm font-bold text-gray-900 flex items-center justify-between">
              <span>Section-Wise Doubt Volume (Real Database Records)</span>
              <Link to="/teacher/analytics" className="text-xs font-semibold text-[#15370D] hover:underline">
                Full Analytics
              </Link>
            </h3>

            <div className="space-y-3">
              {analytics?.section_analytics.map((sec) => (
                <div key={sec.section} className="space-y-1">
                  <div className="flex justify-between text-xs font-bold text-gray-700">
                    <span>Section {sec.section}</span>
                    <span>{sec.doubts} doubts</span>
                  </div>
                  <div className="w-full h-2.5 rounded-full bg-[#FAF6E4] overflow-hidden">
                    <div 
                      className="h-full bg-[#15370D] rounded-full transition-all duration-500"
                      style={{ width: `${Math.min(100, (sec.doubts / (summary?.total_doubts || 1)) * 100)}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Col: Consultation Requests & High Impact Repeated Topics */}
        <div className="space-y-6">
          
          {/* Pending Appointment Requests */}
          <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
                <Users className="w-4 h-4 text-blue-700" />
                <span>Pending Consultations</span>
              </h3>
              <Link to="/teacher/appointments" className="text-xs font-bold text-[#15370D] hover:underline">
                Manage
              </Link>
            </div>

            <div className="space-y-2.5">
              {upcomingAppointments.slice(0, 3).map((app) => (
                <div key={app.id} className="p-3.5 rounded-2xl bg-blue-50/60 border border-blue-200 text-xs space-y-1.5">
                  <div className="flex items-center justify-between font-bold text-blue-950">
                    <span>{app.student_name} ({app.student_section})</span>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-amber-100 text-amber-800">
                      Pending
                    </span>
                  </div>
                  <p className="text-gray-700 font-medium">
                    {app.appointment_date} • {app.time_slot}
                  </p>
                  <p className="text-[11px] text-gray-600 line-clamp-2">
                    Reason: "{app.reason}"
                  </p>
                </div>
              ))}

              {upcomingAppointments.length === 0 && (
                <p className="text-xs text-gray-500 py-3 text-center">
                  No pending consultation bookings.
                </p>
              )}
            </div>
          </div>

          {/* Top Repeated Topics (Confusion Heatmap Preview) */}
          <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3">
            <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
              <Flame className="w-4 h-4 text-[#F2842F]" />
              <span>Highest Confusion Topics</span>
            </h3>

            <div className="space-y-2">
              {analytics?.topic_analytics.slice(0, 4).map((top, idx) => (
                <div key={idx} className="p-3 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] flex items-center justify-between text-xs">
                  <span className="font-bold text-gray-900 truncate max-w-[190px]">
                    {top.topic}
                  </span>
                  <span className="px-2 py-0.5 rounded bg-[#F2842F]/20 text-[#000000] font-extrabold text-[11px]">
                    {top.impact_score} queries
                  </span>
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>

    </div>
  );
};
