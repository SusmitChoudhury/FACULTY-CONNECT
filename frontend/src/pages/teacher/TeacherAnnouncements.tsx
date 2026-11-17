import React, { useState, useEffect } from 'react';
import { Megaphone, Plus, Check, AlertCircle, ShieldCheck, Tag } from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Announcement, Subject } from '../../types';

export const TeacherAnnouncements: React.FC = () => {
  const { teacher } = useAuth();
  const [announcements, setAnnouncements] = useState<Announcement[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  
  // Form State
  const [subjectId, setSubjectId] = useState<number | ''>('');
  const [targetSection, setTargetSection] = useState('All');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [priority, setPriority] = useState('Normal');
  const [loading, setLoading] = useState(true);
  const [actionSuccess, setActionSuccess] = useState('');
  const [actionError, setActionError] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      const [annData, subData] = await Promise.all([
        api.getAnnouncements(),
        api.getSubjects()
      ]);
      setAnnouncements(annData);
      setSubjects(subData);
      if (subData.length > 0) setSubjectId(subData[0].id);
    } catch (e) {
      console.warn('Failed loading announcements:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleCreateAnnouncement = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teacher || !subjectId) return;
    if (!title.trim() || !content.trim()) {
      setActionError('Title and content are required.');
      return;
    }

    setActionError('');
    try {
      await api.createAnnouncement({
        teacher_id: teacher.id,
        teacher_name: teacher.name,
        subject_id: Number(subjectId),
        target_section: targetSection,
        title: title.trim(),
        content: content.trim(),
        priority: priority
      });

      setActionSuccess('Announcement published and delivered to student dashboards!');
      setTitle('');
      setContent('');
      await loadData();
      setTimeout(() => setActionSuccess(''), 3000);
    } catch (err: any) {
      setActionError(err.message || 'Failed creating announcement.');
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
          <Megaphone className="w-7 h-7 text-[#15370D]" />
          <span>Faculty Course Announcements</span>
        </h1>
        <p className="text-xs sm:text-sm text-gray-600 mt-1">
          Publish official notices, assignment reminders, and consultation timing updates.
        </p>
      </div>

      {actionSuccess && (
        <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-300 text-xs font-bold text-emerald-900 flex items-center gap-2">
          <Check className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{actionSuccess}</span>
        </div>
      )}

      {actionError && (
        <div className="p-3.5 rounded-2xl bg-red-50 border border-red-300 text-xs font-bold text-red-900 flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
          <span>{actionError}</span>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Left Col: Create Announcement */}
        <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-4">
          <div className="flex items-center gap-2 border-b border-gray-100 pb-3">
            <Plus className="w-5 h-5 text-[#F2842F]" />
            <h2 className="text-base font-bold text-gray-900">Post Announcement</h2>
          </div>

          <form onSubmit={handleCreateAnnouncement} className="space-y-3.5">
            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                Course Subject *
              </label>
              <select
                value={subjectId}
                onChange={(e) => setSubjectId(Number(e.target.value))}
                className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
                required
              >
                {subjects.map(s => (
                  <option key={s.id} value={s.id}>{s.code}: {s.title}</option>
                ))}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                  Target Section
                </label>
                <select
                  value={targetSection}
                  onChange={(e) => setTargetSection(e.target.value)}
                  className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
                >
                  <option value="All">All Sections</option>
                  <option value="K22DF">Section K22DF</option>
                  <option value="K22GF">Section K22GF</option>
                  <option value="K22SE">Section K22SE</option>
                  <option value="K23AA">Section K23AA</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                  Priority
                </label>
                <select
                  value={priority}
                  onChange={(e) => setPriority(e.target.value)}
                  className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
                >
                  <option value="Normal">Normal</option>
                  <option value="Important">Important</option>
                  <option value="Urgent">Urgent</option>
                </select>
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                Announcement Title *
              </label>
              <input
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="e.g. CA1 Syllabus Revision & Cabin Session"
                className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                Content / Message Body *
              </label>
              <textarea
                rows={4}
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Details of the announcement..."
                className="w-full p-3 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-medium outline-hidden"
                required
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] text-xs font-bold rounded-xl shadow-md flex items-center justify-center gap-1.5 transition"
            >
              <Megaphone className="w-4 h-4 text-[#F2842F]" />
              <span>Broadcast Notice</span>
            </button>
          </form>
        </div>

        {/* Right 2 Cols: Published Announcements */}
        <div className="lg:col-span-2 space-y-3">
          <h2 className="text-base font-bold text-gray-900">
            Published Announcements ({announcements.length})
          </h2>

          <div className="space-y-3">
            {announcements.map((ann) => (
              <div
                key={ann.id}
                className="p-5 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs space-y-2.5"
              >
                <div className="flex items-start justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded text-[10px] font-black bg-[#15370D] text-[#FCF9EA]">
                      {ann.subject_code || 'Notice'}
                    </span>
                    <span className="text-xs font-bold text-gray-700">
                      Target: {ann.target_section}
                    </span>
                    {ann.priority === 'Urgent' && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-red-100 text-red-800 border border-red-300">Urgent</span>
                    )}
                    {ann.priority === 'Important' && (
                      <span className="px-2 py-0.5 rounded-full text-[10px] font-bold bg-[#F2842F]/20 text-black border border-[#F2842F]">Important</span>
                    )}
                  </div>

                  <span className="text-[11px] text-gray-500">
                    {new Date(ann.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', year: 'numeric' })}
                  </span>
                </div>

                <h3 className="text-sm font-bold text-gray-900">{ann.title}</h3>
                <p className="text-xs text-gray-700 leading-relaxed whitespace-pre-line bg-[#FAF6E4] p-3 rounded-xl border border-[#E5DFC8]">
                  {ann.content}
                </p>

                <p className="text-[10px] font-semibold text-[#15370D]">
                  Published by {ann.teacher_name}
                </p>
              </div>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
};
