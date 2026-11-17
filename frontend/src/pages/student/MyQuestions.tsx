import React, { useState, useEffect } from 'react';
import { 
  MessageSquare, Search, Filter, Bookmark, 
  Sparkles, CheckCircle2, Clock, ThumbsUp, 
  ThumbsDown, ChevronRight, X, ExternalLink 
} from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Doubt } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export const MyQuestions: React.FC = () => {
  const { student } = useAuth();
  const [doubts, setDoubts] = useState<Doubt[]>([]);
  const [filteredDoubts, setFilteredDoubts] = useState<Doubt[]>([]);
  const [selectedDoubt, setSelectedDoubt] = useState<Doubt | null>(null);
  const [statusFilter, setStatusFilter] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [bookmarkedIds, setBookmarkedIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [feedbackSent, setFeedbackSent] = useState<Record<number, boolean>>({});

  useEffect(() => {
    if (!student) return;

    const loadData = async () => {
      try {
        setLoading(true);
        const [doubtsData, bookmarksData] = await Promise.all([
          api.getDoubts({ student_name: student.name }),
          api.getBookmarks(student.name)
        ]);
        setDoubts(doubtsData);
        setFilteredDoubts(doubtsData);
        setBookmarkedIds(bookmarksData.map(b => b.doubt_id));
      } catch (e) {
        console.warn('Failed to load student questions:', e);
      } finally {
        setLoading(false);
      }
    };
    loadData();
  }, [student]);

  // Handle Filtering
  useEffect(() => {
    let result = doubts;
    if (statusFilter !== 'All') {
      result = result.filter(d => d.status === statusFilter);
    }
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      result = result.filter(d => 
        d.question_text.toLowerCase().includes(q) ||
        d.subject_code?.toLowerCase().includes(q) ||
        d.topic_title?.toLowerCase().includes(q)
      );
    }
    setFilteredDoubts(result);
  }, [statusFilter, searchQuery, doubts]);

  const handleToggleBookmark = async (doubtId: number, e: React.MouseEvent) => {
    e.stopPropagation();
    if (!student) return;
    try {
      const res = await api.toggleBookmark(student.name, doubtId);
      if (res.bookmarked) {
        setBookmarkedIds(prev => [...prev, doubtId]);
      } else {
        setBookmarkedIds(prev => prev.filter(id => id !== doubtId));
      }
    } catch {
      // ignore
    }
  };

  const handleSendFeedback = async (doubtId: number, resolved: boolean) => {
    if (!student) return;
    try {
      await api.submitStudentFeedback(doubtId, {
        student_name: student.name,
        resolved: resolved,
        feedback_text: resolved ? 'Resolved doubt successfully' : 'Need further clarification'
      });
      setFeedbackSent(prev => ({ ...prev, [doubtId]: true }));
    } catch {
      // ignore
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
            <MessageSquare className="w-7 h-7 text-[#15370D]" />
            <span>My Academic Questions &amp; Answers</span>
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Track status, view faculty responses, review 3-hour automated AI explanations, and bookmark solutions.
          </p>
        </div>

        {/* Search Input */}
        <div className="relative w-full md:w-72">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search my doubts..."
            className="w-full pl-10 pr-4 py-2 bg-white border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs font-medium outline-hidden shadow-xs transition"
          />
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
        {['All', 'Pending', 'Faculty Answered', 'AI Answered', 'Faculty Verified', 'Resolved'].map((st) => (
          <button
            key={st}
            onClick={() => setStatusFilter(st)}
            className={`px-3.5 py-1.5 rounded-full text-xs font-bold whitespace-nowrap transition ${
              statusFilter === st
                ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
                : 'bg-white text-gray-700 hover:bg-[#EFEAD3] border border-[#E5DFC8]'
            }`}
          >
            {st}
          </button>
        ))}
      </div>

      {/* Questions List */}
      <div className="space-y-3">
        {filteredDoubts.map((doubt) => {
          const isBookmarked = bookmarkedIds.includes(doubt.id);
          const hasFacultyAnswer = doubt.faculty_answers && doubt.faculty_answers.length > 0;
          const hasAiAnswer = doubt.ai_responses && doubt.ai_responses.length > 0;

          return (
            <div
              key={doubt.id}
              onClick={() => setSelectedDoubt(doubt)}
              className="p-5 rounded-2xl bg-white border border-[#E5DFC8] hover:border-[#15370D] shadow-xs hover:shadow-md cursor-pointer transition"
            >
              <div className="flex items-start justify-between gap-3 mb-2">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="px-2 py-0.5 rounded text-[11px] font-black bg-[#15370D] text-[#FCF9EA]">
                    {doubt.subject_code}
                  </span>
                  <span className="text-xs font-bold text-gray-700">
                    {doubt.unit_title}
                  </span>
                  <span className="text-gray-400">•</span>
                  <span className="text-xs font-medium text-gray-600 truncate max-w-[220px]">
                    {doubt.topic_title}
                  </span>
                </div>

                <div className="flex items-center gap-2">
                  <StatusBadge status={doubt.status} size="sm" />
                  <button
                    onClick={(e) => handleToggleBookmark(doubt.id, e)}
                    className={`p-1 rounded-lg transition ${
                      isBookmarked ? 'text-[#F2842F] bg-[#F2842F]/10' : 'text-gray-400 hover:text-gray-600'
                    }`}
                    title={isBookmarked ? 'Remove bookmark' : 'Bookmark answer'}
                  >
                    <Bookmark className="w-4 h-4 fill-current" />
                  </button>
                </div>
              </div>

              <h3 className="text-sm font-bold text-gray-900 leading-snug">
                {doubt.question_text}
              </h3>

              {/* Answer Preview Snippet if available */}
              {hasFacultyAnswer && (
                <div className="mt-3 p-3 rounded-xl bg-emerald-50/70 border border-emerald-200 text-xs text-emerald-950 space-y-1">
                  <div className="flex items-center justify-between font-bold text-[#15370D]">
                    <span className="flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#F2842F]" />
                      Faculty Answer: {doubt.faculty_answers![0].teacher_name}
                    </span>
                    <span className="text-[10px] text-gray-500 font-normal">
                      {new Date(doubt.faculty_answers![0].created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="line-clamp-2 text-gray-800 leading-relaxed">
                    {doubt.faculty_answers![0].answer_text}
                  </p>
                </div>
              )}

              {!hasFacultyAnswer && hasAiAnswer && (
                <div className="mt-3 p-3 rounded-xl bg-[#FAF6E4] border border-[#F2842F]/40 text-xs text-gray-900 space-y-1">
                  <div className="flex items-center justify-between font-bold text-[#15370D]">
                    <span className="flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4 text-[#F2842F]" />
                      3-Hour Automated AI Answer
                    </span>
                    <span className="text-[10px] text-gray-500 font-normal">
                      {new Date(doubt.ai_responses![0].created_at).toLocaleDateString()}
                    </span>
                  </div>
                  <p className="line-clamp-2 text-gray-800 leading-relaxed">
                    {doubt.ai_responses![0].response_text}
                  </p>
                </div>
              )}

              {/* Footer Meta */}
              <div className="mt-3 pt-2.5 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-500">
                <div className="flex items-center gap-3">
                  <span>Submitted: {new Date(doubt.created_at).toLocaleDateString([], { month: 'short', day: 'numeric' })}</span>
                  {doubt.duplicate_count > 1 && (
                    <span className="font-bold text-[#F2842F]">
                      👥 {doubt.duplicate_count} students supported (+1)
                    </span>
                  )}
                </div>
                <span className="text-[#15370D] font-bold flex items-center gap-1 hover:underline">
                  View Full Thread <ChevronRight className="w-3.5 h-3.5" />
                </span>
              </div>
            </div>
          );
        })}

        {filteredDoubts.length === 0 && !loading && (
          <div className="p-12 text-center bg-white rounded-2xl border border-dashed border-[#D8D2BA]">
            <MessageSquare className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
            <p className="font-bold text-gray-800 text-sm">No matching questions found</p>
            <p className="text-xs text-gray-500 mt-1">Try resetting the filter or submit a new academic doubt.</p>
          </div>
        )}
      </div>

      {/* FULL QUESTION DETAIL MODAL */}
      {selectedDoubt && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
          <div className="w-full max-w-2xl bg-[#FCF9EA] border border-[#D8D2BA] rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh] animate-fade-in">
            
            {/* Modal Header */}
            <div className="px-6 py-4 bg-[#15370D] text-[#FCF9EA] flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold text-[#F2842F] uppercase tracking-wider">
                  {selectedDoubt.subject_code} • {selectedDoubt.unit_title}
                </span>
                <h2 className="text-sm sm:text-base font-bold text-white truncate max-w-md">
                  Topic: {selectedDoubt.topic_title}
                </h2>
              </div>
              <button
                onClick={() => setSelectedDoubt(null)}
                className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Scrollable Body */}
            <div className="p-6 overflow-y-auto space-y-5 flex-1">
              
              {/* Question Box */}
              <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-bold text-gray-500">
                    Question from {selectedDoubt.student_name} (Sec {selectedDoubt.section})
                  </span>
                  <StatusBadge status={selectedDoubt.status} size="sm" />
                </div>
                <p className="text-sm font-bold text-gray-900 leading-relaxed">
                  {selectedDoubt.question_text}
                </p>
                <div className="pt-2 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-500">
                  <span>Lecture Date: {selectedDoubt.teaching_date || 'N/A'}</span>
                  <span>Category: {selectedDoubt.category}</span>
                  <span className="text-[#F2842F] font-bold">
                    +{selectedDoubt.duplicate_count} Supporters
                  </span>
                </div>
              </div>

              {/* Faculty Answer Box */}
              {selectedDoubt.faculty_answers && selectedDoubt.faculty_answers.length > 0 && (
                <div className="p-5 rounded-2xl bg-white border-2 border-[#15370D] shadow-xs space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-black text-[#15370D] flex items-center gap-1.5">
                      <CheckCircle2 className="w-4 h-4 text-[#F2842F]" />
                      Official Faculty Response: {selectedDoubt.faculty_answers[0].teacher_name}
                    </span>
                    <span className="text-[10px] text-gray-500">
                      {new Date(selectedDoubt.faculty_answers[0].created_at).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] text-xs sm:text-sm text-gray-900 leading-relaxed whitespace-pre-line">
                    {selectedDoubt.faculty_answers[0].answer_text}
                  </div>

                  {/* Student Feedback (Section 21.G) */}
                  <div className="pt-3 border-t border-gray-100 flex items-center justify-between">
                    <span className="text-xs text-gray-600 font-medium">Did this answer resolve your doubt?</span>
                    {feedbackSent[selectedDoubt.id] ? (
                      <span className="text-xs font-bold text-[#15370D]">Thank you for your feedback!</span>
                    ) : (
                      <div className="flex gap-2">
                        <button
                          onClick={() => handleSendFeedback(selectedDoubt.id, true)}
                          className="px-3 py-1 rounded-lg bg-[#15370D] text-[#FCF9EA] text-xs font-bold hover:bg-[#15370D]/90 flex items-center gap-1 transition"
                        >
                          <ThumbsUp className="w-3.5 h-3.5 text-[#F2842F]" />
                          Yes, Resolved
                        </button>
                        <button
                          onClick={() => handleSendFeedback(selectedDoubt.id, false)}
                          className="px-3 py-1 rounded-lg bg-gray-100 hover:bg-gray-200 text-gray-700 text-xs font-bold flex items-center gap-1 transition"
                        >
                          <ThumbsDown className="w-3.5 h-3.5 text-gray-500" />
                          Need More Help
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* AI Answer Box */}
              {selectedDoubt.ai_responses && selectedDoubt.ai_responses.length > 0 && (
                <div className="p-5 rounded-2xl bg-white border border-[#F2842F] shadow-xs space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-black text-gray-900 flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4 text-[#F2842F]" />
                      3-Hour Automated AI Response ({selectedDoubt.ai_responses[0].model_name})
                    </span>
                    <span className="text-[10px] text-gray-500">
                      {new Date(selectedDoubt.ai_responses[0].created_at).toLocaleDateString()}
                    </span>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] text-xs sm:text-sm text-gray-900 leading-relaxed whitespace-pre-line">
                    {selectedDoubt.ai_responses[0].response_text}
                  </div>

                  <p className="text-[10px] text-gray-500 italic">
                    Grounded in the verified course curriculum. Faculty will review and provide official verification.
                  </p>
                </div>
              )}

              {/* No answer yet (Pending in 3-hour window) */}
              {(!selectedDoubt.faculty_answers || selectedDoubt.faculty_answers.length === 0) &&
               (!selectedDoubt.ai_responses || selectedDoubt.ai_responses.length === 0) && (
                <div className="p-6 text-center bg-white rounded-2xl border border-dashed border-[#D8D2BA] space-y-2">
                  <Clock className="w-8 h-8 mx-auto text-[#F2842F] animate-pulse" />
                  <p className="text-sm font-bold text-gray-900">In Faculty Queue</p>
                  <p className="text-xs text-gray-600 max-w-sm mx-auto leading-relaxed">
                    This doubt has been assigned to the course professor. If unanswered within 3 hours, our syllabus AI assistant will generate a preliminary explanation.
                  </p>
                </div>
              )}

            </div>

            {/* Modal Footer */}
            <div className="px-6 py-3 bg-[#F4EFCF] border-t border-[#D8D2BA] flex items-center justify-between">
              <button
                onClick={(e) => handleToggleBookmark(selectedDoubt.id, e)}
                className="text-xs font-bold text-gray-700 hover:text-black flex items-center gap-1.5"
              >
                <Bookmark className="w-4 h-4 text-[#F2842F]" />
                {bookmarkedIds.includes(selectedDoubt.id) ? 'Saved in Bookmarks' : 'Bookmark this Doubt'}
              </button>

              <button
                onClick={() => setSelectedDoubt(null)}
                className="px-5 py-1.5 bg-[#15370D] text-[#FCF9EA] hover:bg-[#15370D]/90 rounded-xl text-xs font-bold transition"
              >
                Close
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};
