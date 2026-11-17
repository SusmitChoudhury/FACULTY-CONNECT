import React, { useState, useEffect } from 'react';
import { Bookmark, MessageSquare, Trash2, CheckCircle2, ChevronRight } from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Doubt } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export const BookmarksPage: React.FC = () => {
  const { student } = useAuth();
  const [bookmarks, setBookmarks] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadBookmarks = async () => {
    if (!student) return;
    try {
      setLoading(true);
      const data = await api.getBookmarks(student.name);
      setBookmarks(data);
    } catch (e) {
      console.warn('Failed loading bookmarks:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadBookmarks();
  }, [student]);

  const handleRemove = async (doubtId: number) => {
    if (!student) return;
    try {
      await api.toggleBookmark(student.name, doubtId);
      setBookmarks(prev => prev.filter(b => b.doubt_id !== doubtId));
    } catch {
      // ignore
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      <div>
        <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
          <Bookmark className="w-7 h-7 text-[#F2842F]" />
          <span>Saved Academic Answers &amp; Solutions</span>
        </h1>
        <p className="text-xs sm:text-sm text-gray-600 mt-1">
          Quick reference library of verified faculty explanations you bookmarked for exams and revision.
        </p>
      </div>

      <div className="space-y-4">
        {bookmarks.map((b) => {
          const d: Doubt = b.doubt;
          if (!d) return null;

          return (
            <div
              key={b.id}
              className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3"
            >
              <div className="flex items-start justify-between gap-3">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="px-2 py-0.5 rounded text-[11px] font-black bg-[#15370D] text-[#FCF9EA]">
                    {d.subject_code}
                  </span>
                  <span className="text-xs font-bold text-gray-700">{d.unit_title}</span>
                  <span className="text-gray-400">•</span>
                  <span className="text-xs text-gray-600">{d.topic_title}</span>
                </div>

                <button
                  onClick={() => handleRemove(d.id)}
                  className="p-1.5 text-gray-400 hover:text-red-600 rounded-lg transition"
                  title="Remove from saved answers"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              <h3 className="text-sm sm:text-base font-bold text-gray-900">
                {d.question_text}
              </h3>

              {/* Answers */}
              {d.faculty_answers && d.faculty_answers.length > 0 && (
                <div className="p-4 rounded-2xl bg-emerald-50/70 border border-emerald-200 text-xs text-gray-900 space-y-1.5">
                  <span className="font-bold text-[#15370D] flex items-center gap-1.5">
                    <CheckCircle2 className="w-4 h-4 text-[#F2842F]" />
                    Verified Answer from {d.faculty_answers[0].teacher_name}:
                  </span>
                  <p className="leading-relaxed whitespace-pre-line text-gray-800">
                    {d.faculty_answers[0].answer_text}
                  </p>
                </div>
              )}

              {(!d.faculty_answers || d.faculty_answers.length === 0) && d.ai_responses && d.ai_responses.length > 0 && (
                <div className="p-4 rounded-2xl bg-[#FAF6E4] border border-[#F2842F]/40 text-xs text-gray-900 space-y-1.5">
                  <span className="font-bold text-[#15370D]">Automated Syllabus AI Answer:</span>
                  <p className="leading-relaxed whitespace-pre-line text-gray-800">
                    {d.ai_responses[0].response_text}
                  </p>
                </div>
              )}
            </div>
          );
        })}

        {bookmarks.length === 0 && !loading && (
          <div className="p-12 text-center bg-white rounded-3xl border border-dashed border-[#D8D2BA]">
            <Bookmark className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
            <p className="font-bold text-gray-800 text-sm">No saved answers yet</p>
            <p className="text-xs text-gray-500 mt-1">
              Click the bookmark icon on any answered question in "My Questions" to save it here for fast exam revision.
            </p>
          </div>
        )}
      </div>
    </div>
  );
};
