import React, { useState, useEffect } from 'react';
import { Users, Calendar, Clock, MapPin, Check, X, AlertCircle, MessageSquare } from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Appointment } from '../../types';

export const TeacherAppointments: React.FC = () => {
  const { teacher } = useAuth();
  const [appointments, setAppointments] = useState<Appointment[]>([]);
  const [statusFilter, setStatusFilter] = useState('All');
  const [loading, setLoading] = useState(true);
  const [selectedApp, setSelectedApp] = useState<Appointment | null>(null);
  const [teacherNote, setTeacherNote] = useState('');
  const [actionSuccess, setActionSuccess] = useState('');

  const loadAppointments = async () => {
    if (!teacher) return;
    try {
      setLoading(true);
      const data = await api.getAppointments({ teacher_id: teacher.id });
      setAppointments(data);
    } catch (e) {
      console.warn('Failed loading appointments:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAppointments();
  }, [teacher]);

  const handleUpdateStatus = async (appId: number, newStatus: string) => {
    try {
      await api.updateAppointmentStatus(appId, newStatus, teacherNote.trim());
      setActionSuccess(`Appointment successfully marked as ${newStatus}. Student notified.`);
      setSelectedApp(null);
      setTeacherNote('');
      await loadAppointments();
      setTimeout(() => setActionSuccess(''), 3000);
    } catch (e: any) {
      alert(e.message || 'Failed updating appointment.');
    }
  };

  const filteredApps = statusFilter === 'All'
    ? appointments
    : appointments.filter(a => a.status === statusFilter);

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
            <Users className="w-7 h-7 text-[#15370D]" />
            <span>Consultation &amp; Cabin Booking Requests</span>
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Review, accept, or reschedule student appointments for your cabin hours.
          </p>
        </div>

        {/* Filter Tabs */}
        <div className="flex bg-[#F4EFCF] p-1 rounded-2xl border border-[#D8D2BA] overflow-x-auto scrollbar-none">
          {['All', 'Pending', 'Accepted', 'Completed', 'Rejected'].map((st) => (
            <button
              key={st}
              onClick={() => setStatusFilter(st)}
              className={`px-3.5 py-1.5 rounded-xl text-xs font-bold transition whitespace-nowrap ${
                statusFilter === st
                  ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
                  : 'text-gray-700 hover:text-black'
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {actionSuccess && (
        <div className="p-3.5 rounded-2xl bg-emerald-50 border border-emerald-300 text-xs font-bold text-emerald-900 flex items-center gap-2">
          <Check className="w-4 h-4 text-emerald-600 shrink-0" />
          <span>{actionSuccess}</span>
        </div>
      )}

      {/* Appointment Cards */}
      <div className="space-y-3">
        {filteredApps.map((app) => (
          <div
            key={app.id}
            className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3"
          >
            <div className="flex items-start justify-between gap-3 flex-wrap">
              <div>
                <div className="flex items-center gap-2">
                  <h3 className="font-extrabold text-base text-gray-900">{app.student_name}</h3>
                  <span className="px-2 py-0.5 rounded text-[11px] font-bold bg-[#15370D] text-[#FCF9EA]">
                    Section {app.student_section}
                  </span>
                </div>
                <p className="text-xs text-gray-600 mt-0.5">
                  Requested on {new Date(app.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                </p>
              </div>

              <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                app.status === 'Accepted'
                  ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                  : app.status === 'Pending'
                  ? 'bg-amber-100 text-amber-800 border border-amber-300'
                  : app.status === 'Rejected'
                  ? 'bg-red-100 text-red-800 border border-red-300'
                  : 'bg-gray-100 text-gray-800'
              }`}>
                {app.status}
              </span>
            </div>

            <div className="p-3.5 rounded-2xl bg-[#FAF6E4] border border-[#E5DFC8] text-xs space-y-1.5">
              <div className="flex items-center gap-4 flex-wrap text-gray-800 font-semibold">
                <span className="flex items-center gap-1.5">
                  <Calendar className="w-3.5 h-3.5 text-[#15370D]" />
                  {app.appointment_date}
                </span>
                <span className="flex items-center gap-1.5">
                  <Clock className="w-3.5 h-3.5 text-[#F2842F]" />
                  {app.time_slot}
                </span>
                <span className="flex items-center gap-1.5">
                  <MapPin className="w-3.5 h-3.5 text-gray-500" />
                  {app.location}
                </span>
              </div>

              <p className="text-gray-900 font-medium pt-1">
                Reason for Consultation: <span className="font-bold">"{app.reason}"</span>
              </p>

              {app.teacher_notes && (
                <p className="text-[#15370D] text-[11px] font-semibold pt-1 border-t border-gray-200">
                  Note to student: {app.teacher_notes}
                </p>
              )}
            </div>

            {/* Actions */}
            {app.status === 'Pending' && (
              <div className="pt-2 flex flex-wrap items-center justify-between gap-3">
                <input
                  type="text"
                  placeholder="Optional note / cabin instruction for student..."
                  value={selectedApp?.id === app.id ? teacherNote : ''}
                  onChange={(e) => {
                    setSelectedApp(app);
                    setTeacherNote(e.target.value);
                  }}
                  className="flex-1 min-w-[220px] px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs outline-hidden"
                />

                <div className="flex gap-2">
                  <button
                    onClick={() => { setSelectedApp(app); handleUpdateStatus(app.id, 'Accepted'); }}
                    className="px-4 py-1.5 bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] text-xs font-bold rounded-xl shadow-xs transition"
                  >
                    Accept Slot
                  </button>
                  <button
                    onClick={() => { setSelectedApp(app); handleUpdateStatus(app.id, 'Rejected'); }}
                    className="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-red-700 text-xs font-bold rounded-xl transition"
                  >
                    Decline
                  </button>
                </div>
              </div>
            )}

            {app.status === 'Accepted' && (
              <div className="pt-2 flex justify-end gap-2">
                <button
                  onClick={() => handleUpdateStatus(app.id, 'Completed')}
                  className="px-4 py-1.5 bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold rounded-xl shadow-xs transition"
                >
                  Mark Completed
                </button>
              </div>
            )}

          </div>
        ))}

        {filteredApps.length === 0 && !loading && (
          <div className="p-12 text-center bg-white rounded-3xl border border-dashed border-[#D8D2BA]">
            <Users className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
            <p className="font-bold text-gray-800 text-sm">No appointment requests in this category</p>
            <p className="text-xs text-gray-500 mt-1">Students can book slots based on your published schedule.</p>
          </div>
        )}
      </div>

    </div>
  );
};
