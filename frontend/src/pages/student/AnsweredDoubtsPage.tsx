import React, { useState, useEffect } from 'react';
import { 
  BookCheck, Search, Filter, Bookmark, CheckCircle2, 
  Sparkles, ThumbsUp, Calendar, ArrowRight, User, ShieldCheck, ChevronDown 
} from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Doubt, Subject } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export const AnsweredDoubtsPage: React.FC = () => {
  const { student } = useAuth();
  const [doubts, setDoubts] = useState<Doubt[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('All');
  const [selectedUnitId, setSelectedUnitId] = useState<string>('All');
  const [sourceFilter, setSourceFilter] = useState<'All' | 'Faculty' | 'AI'>('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [bookmarkedIds, setBookmarkedIds] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [allDoubts, allSubjects] = await Promise.all([
        api.getDoubts(),
        api.getSubjects()
      ]);

      // Only show answered doubts (Faculty Answered, Faculty Verified, AI Answered, Resolved)
      const answered = allDoubts.filter(d => 
        (d.faculty_answers && d.faculty_answers.length > 0) ||
        (d.ai_responses && d.ai_responses.length > 0) ||
        ['Faculty Answered', 'Faculty Verified', 'AI Answered', 'Resolved'].includes(d.status)
      );

      setDoubts(answered);
      setSubjects(allSubjects);

      if (student) {
        const bms = await api.getBookmarks(student.name);
        setBookmarkedIds(bms.map(b => b.doubt_id));
      }
    } catch (e) {
      console.warn('Failed loading answered doubts:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [student]);

  const handleToggleBookmark = async (doubtId: number) => {
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

  // Filtered list
  const currentSubject = subjects.find(s => s.id.toString() === selectedSubjectId);
  const availableUnits = currentSubject?.units || [];

  const filteredDoubts = doubts.filter(d => {
    if (selectedSubjectId !== 'All' && d.subject_id.toString() !== selectedSubjectId) return false;
    if (selectedUnitId !== 'All' && d.unit_id.toString() !== selectedUnitId) return false;

    if (sourceFilter === 'Faculty') {
      if (!d.faculty_answers || d.faculty_answers.length === 0) return false;
    } else if (sourceFilter === 'AI') {
      if (!d.ai_responses || d.ai_responses.length === 0) return false;
    }

    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      return (
        d.question_text.toLowerCase().includes(q) ||
        d.subject_code?.toLowerCase().includes(q) ||
        d.topic_title?.toLowerCase().includes(q) ||
        (d.faculty_answers && d.faculty_answers.some(fa => fa.answer_text.toLowerCase().includes(q))) ||
        (d.ai_responses && d.ai_responses.some(ai => ai.response_text.toLowerCase().includes(q)))
      );
    }
    return true;
  });

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
            <BookCheck className="w-7 h-7 text-[#15370D]" />
            <span>Previously Answered Doubts &amp; Knowledge Bank</span>
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Browse and search faculty-verified explanations and AI preliminary answers from past lectures across all sections.
          </p>
        </div>

        {/* Search */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search verified answers..."
            className="w-full pl-10 pr-4 py-2 bg-white border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs font-medium outline-hidden shadow-xs transition"
          />
        </div>
      </div>

      {/* Filter Row */}
      <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] flex flex-wrap items-center gap-3 text-xs">
        <span className="font-bold text-gray-500 uppercase tracking-wider text-[10px] flex items-center gap-1">
          <Filter className="w-3.5 h-3.5" /> Filter by:
        </span>

        {/* Subject Filter */}
        <select
          value={selectedSubjectId}
          onChange={(e) => {
            setSelectedSubjectId(e.target.value);
            setSelectedUnitId('All');
          }}
          className="px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-lg font-semibold outline-hidden"
        >
          <option value="All">All Subjects</option>
          {subjects.map(s => (
            <option key={s.id} value={s.id.toString()}>{s.code}: {s.title}</option>
          ))}
        </select>

        {/* Unit Filter */}
        {selectedSubjectId !== 'All' && (
          <select
            value={selectedUnitId}
            onChange={(e) => setSelectedUnitId(e.target.value)}
            className="px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-lg font-semibold outline-hidden"
          >
            <option value="All">All Units</option>
            {availableUnits.map(u => (
              <option key={u.id} value={u.id.toString()}>{u.unit_number}: {u.title}</option>
            ))}
          </select>
        )}

        {/* Answer Source Filter */}
        <div className="flex bg-[#FAF6E4] p-1 rounded-xl border border-[#D8D2BA] ml-auto">
          {(['All', 'Faculty', 'AI'] as const).map((src) => (
            <button
              key={src}
              onClick={() => setSourceFilter(src)}
              className={`px-3 py-1 rounded-lg text-xs font-bold transition ${
                sourceFilter === src
                  ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
                  : 'text-gray-700 hover:text-black'
              }`}
            >
              {src === 'Faculty' ? 'Faculty Verified' : src === 'AI' ? '3h AI Answer' : 'All Answers'}
            </button>
          ))}
        </div>
      </div>

      {/* Cards List */}
      <div className="space-y-4">
        {filteredDoubts.map((doubt) => {
          const isBookmarked = bookmarkedIds.includes(doubt.id);
          const hasFaculty = doubt.faculty_answers && doubt.faculty_answers.length > 0;
          const hasAI = doubt.ai_responses && doubt.ai_responses.length > 0;

          return (
            <div
              key={doubt.id}
              className="p-6 rounded-3xl bg-white border border-[#E5DFC8] hover:border-[#15370D] shadow-xs hover:shadow-md transition space-y-4"
            >
              {/* Question Header */}
              <div className="flex items-start justify-between gap-3">
                <div className="space-y-1">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="px-2 py-0.5 rounded text-[11px] font-black bg-[#15370D] text-[#FCF9EA]">
                      {doubt.subject_code}
                    </span>
                    <span className="text-xs font-bold text-gray-800">{doubt.unit_title}</span>
                    <span className="text-gray-400">•</span>
                    <span className="text-xs text-gray-600">{doubt.topic_title}</span>
                    <StatusBadge status={doubt.status} size="sm" />
                  </div>

                  <h3 className="text-sm sm:text-base font-extrabold text-gray-900 leading-snug pt-1">
                    "{doubt.question_text}"
                  </h3>
                </div>

                <button
                  onClick={() => handleToggleBookmark(doubt.id)}
                  className={`p-2 rounded-xl border transition ${
                    isBookmarked 
                      ? 'border-[#F2842F] bg-[#F2842F]/10 text-[#F2842F]' 
                      : 'border-gray-200 text-gray-400 hover:text-gray-700 hover:bg-gray-50'
                  }`}
                  title={isBookmarked ? 'Remove bookmark' : 'Bookmark solution'}
                >
                  <Bookmark className="w-4 h-4 fill-current" />
                </button>
              </div>

              {/* Verified Faculty Answer */}
              {hasFaculty && (
                <div className="p-4 rounded-2xl bg-emerald-50/70 border border-emerald-200 text-xs sm:text-sm text-gray-900 space-y-2">
                  <div className="flex items-center justify-between font-bold text-[#15370D]">
                    <span className="flex items-center gap-1.5">
                      <ShieldCheck className="w-4 h-4 text-[#F2842F]" />
                      Official Faculty Response: {doubt.faculty_answers![0].teacher_name}
                    </span>
                    <span className="text-[10px] text-gray-500 font-normal">
                      Verified on {new Date(doubt.faculty_answers![0].created_at).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })}
                    </span>
                  </div>
                  <p className="leading-relaxed whitespace-pre-line text-gray-800">
                    {doubt.faculty_answers![0].answer_text}
                  </p>
                </div>
              )}

              {/* AI Fallback Answer */}
              {!hasFaculty && hasAI && (
                <div className="p-4 rounded-2xl bg-[#FAF6E4] border border-[#F2842F]/40 text-xs sm:text-sm text-gray-900 space-y-2">
                  <div className="flex items-center justify-between font-bold text-[#15370D]">
                    <span className="flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4 text-[#F2842F]" />
                      3-Hour Automated AI Academic Explanation
                    </span>
                    <span className="text-[10px] text-gray-500 font-normal">
                      Generated on {new Date(doubt.ai_responses![0].created_at).toLocaleDateString([], { month: 'short', day: 'numeric' })}
                    </span>
                  </div>
                  <p className="leading-relaxed whitespace-pre-line text-gray-800">
                    {doubt.ai_responses![0].response_text}
                  </p>
                </div>
              )}

              {/* Bottom Meta */}
              <div className="pt-2 border-t border-gray-100 flex items-center justify-between text-xs text-gray-500 flex-wrap gap-2">
                <div className="flex items-center gap-4">
                  <span>Asked by {doubt.student_name} (Section {doubt.section})</span>
                  {doubt.teaching_date && <span>Lecture: {doubt.teaching_date}</span>}
                </div>

                <div className="flex items-center gap-2">
                  {doubt.duplicate_count > 1 && (
                    <span className="font-extrabold text-[#F2842F] text-[11px] px-2 py-0.5 rounded-full bg-[#F2842F]/10">
                      👥 {doubt.duplicate_count} students shared this query
                    </span>
                  )}
                  {doubt.positive_feedback && doubt.positive_feedback > 0 ? (
                    <span className="font-semibold text-emerald-800 text-[11px] flex items-center gap-1">
                      <ThumbsUp className="w-3 h-3" />
                      {doubt.positive_feedback} found helpful
                    </span>
                  ) : null}
                </div>
              </div>

            </div>
          );
        })}

        {filteredDoubts.length === 0 && !loading && (
          <div className="p-12 text-center bg-white rounded-3xl border border-dashed border-[#D8D2BA]">
            <BookCheck className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
            <p className="font-bold text-gray-800 text-sm">No answered doubts found</p>
            <p className="text-xs text-gray-500 mt-1">Try searching for other topics or reset the filters.</p>
          </div>
        )}
      </div>

    </div>
  );
};
