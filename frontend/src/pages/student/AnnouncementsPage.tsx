import React, { useState, useEffect } from 'react';
import { Megaphone, Calendar, Tag, ShieldCheck, User } from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Announcement } from '../../types';

export const AnnouncementsPage: React.FC = () => {
  const { student } = useAuth();
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!student) return;
    const fetchAnnouncements = async () => {
      try {
        setLoading(true);
        const data = await api.getAnnouncements({ section: student.section });
        setAnnouncements(data);
      } catch (e) {
        console.warn('Failed loading announcements:', e);
      } finally {
        setLoading(false);
      }
    };
    fetchAnnouncements();
  }, [student]);

  const getPriorityBadge = (priority: string) => {
    switch (priority) {
      case 'Urgent':
        return <span className="px-2 py-0.5 rounded-full text-[10px] font-black bg-red-100 text-red-800 border border-red-300">Urgent</span>;
      case 'Important':
        return <span className="px-2 py-0.5 rounded-full text-[10px] font-black bg-[#F2842F]/20 text-[#000000] border border-[#F2842F]">Important</span>;
      default:
        return <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-gray-100 text-gray-700">Notice</span>;
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      <div>
        <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
          <Megaphone className="w-7 h-7 text-[#15370D]" />
          <span>Official Faculty Announcements</span>
        </h1>
        <p className="text-xs sm:text-sm text-gray-600 mt-1">
          Direct course notices, exam instructions, and consultation schedules for Section {student?.section}.
        </p>
      </div>

      <div className="space-y-4">
        {announcements.map((ann) => (
          <div
            key={ann.id}
            className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3"
          >
            <div className="flex items-start justify-between gap-3">
              <div className="flex items-center gap-2 flex-wrap">
                <span className="px-2 py-0.5 rounded text-[11px] font-black bg-[#15370D] text-[#FCF9EA]">
                  {ann.subject_code || 'General'}
                </span>
                <span className="text-xs font-semibold text-gray-600">
                  Target: {ann.target_section === 'All' ? 'All Sections' : `Section ${ann.target_section}`}
                </span>
                {getPriorityBadge(ann.priority)}
              </div>

              <span className="text-[11px] text-gray-500 font-medium">
                {new Date(ann.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })}
              </span>
            </div>

            <h2 className="text-base font-extrabold text-gray-900">{ann.title}</h2>

            <div className="p-4 rounded-2xl bg-[#FAF6E4] border border-[#E5DFC8] text-xs sm:text-sm text-gray-800 leading-relaxed whitespace-pre-line">
              {ann.content}
            </div>

            <div className="pt-2 flex items-center gap-2 text-xs text-gray-600 font-semibold">
              <ShieldCheck className="w-4 h-4 text-[#15370D]" />
              <span>Published by {ann.teacher_name}</span>
            </div>
          </div>
        ))}

        {announcements.length === 0 && !loading && (
          <div className="p-12 text-center bg-white rounded-3xl border border-dashed border-[#D8D2BA]">
            <Megaphone className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
            <p className="font-bold text-gray-800 text-sm">No announcements posted</p>
            <p className="text-xs text-gray-500 mt-1">Your professors have not published any announcements for this section yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};
