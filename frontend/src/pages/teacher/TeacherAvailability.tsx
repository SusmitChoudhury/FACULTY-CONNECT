import React, { useState, useEffect } from 'react';
import { Calendar, Clock, MapPin, Plus, Trash2, Check, AlertCircle } from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { FacultyAvailability } from '../../types';

export const TeacherAvailability: React.FC = () => {
  const { teacher } = useAuth();
  const [slots, setSlots] = useState<FacultyAvailability[]>([]);
  const [loading, setLoading] = useState(true);

  // Form State for new slot
  const [dayOfWeek, setDayOfWeek] = useState('Monday');
  const [startTime, setStartTime] = useState('10:00 AM');
  const [endTime, setEndTime] = useState('11:30 AM');
  const [location, setLocation] = useState(teacher?.cabin_location || 'Block 34, Cabin 601');
  const [maxBookings, setMaxBookings] = useState(3);
  const [instructions, setInstructions] = useState('Bring your course notes and specific problem statements.');
  const [actionSuccess, setActionSuccess] = useState('');
  const [actionError, setActionError] = useState('');

  const loadSlots = async () => {
    if (!teacher) return;
    try {
      setLoading(true);
      const data = await api.getFacultyAvailability(teacher.id);
      setSlots(data);
    } catch (e) {
      console.warn('Failed loading slots:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadSlots();
  }, [teacher]);

  const handleAddSlot = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teacher) return;
    setActionError('');
    try {
      await api.addAvailability({
        teacher_id: teacher.id,
        day_of_week: dayOfWeek,
        start_time: startTime,
        end_time: endTime,
        location: location.trim(),
        max_bookings: Number(maxBookings),
        instructions: instructions.trim(),
        is_active: true
      });

      setActionSuccess('Consultation time slot added successfully!');
      await loadSlots();
      setTimeout(() => setActionSuccess(''), 3000);
    } catch (err: any) {
      setActionError(err.message || 'Failed adding slot.');
    }
  };

  const handleDeleteSlot = async (slotId: number) => {
    if (!confirm('Are you sure you want to remove this availability slot?')) return;
    try {
      await api.deleteAvailability(slotId);
      setActionSuccess('Slot removed.');
      await loadSlots();
      setTimeout(() => setActionSuccess(''), 2500);
    } catch (e: any) {
      alert(e.message || 'Failed deleting slot.');
    }
  };

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
          <Calendar className="w-7 h-7 text-[#15370D]" />
          <span>My Faculty Consultation Availability</span>
        </h1>
        <p className="text-xs sm:text-sm text-gray-600 mt-1">
          Publish your weekly cabin and office hours so students can schedule academic consultations.
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
        
        {/* Left Col: Add New Consultation Slot Form */}
        <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-4">
          <div className="flex items-center gap-2 border-b border-gray-100 pb-3">
            <Plus className="w-5 h-5 text-[#F2842F]" />
            <h2 className="text-base font-bold text-gray-900">Add Available Time Slot</h2>
          </div>

          <form onSubmit={handleAddSlot} className="space-y-3.5">
            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                Day of Week *
              </label>
              <select
                value={dayOfWeek}
                onChange={(e) => setDayOfWeek(e.target.value)}
                className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
              >
                {days.map(d => <option key={d} value={d}>{d}</option>)}
              </select>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                  Start Time *
                </label>
                <input
                  type="text"
                  value={startTime}
                  onChange={(e) => setStartTime(e.target.value)}
                  placeholder="e.g. 10:00 AM"
                  className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                  End Time *
                </label>
                <input
                  type="text"
                  value={endTime}
                  onChange={(e) => setEndTime(e.target.value)}
                  placeholder="e.g. 11:30 AM"
                  className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                Consultation Location *
              </label>
              <input
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                placeholder="e.g. Block 34, Cabin 601"
                className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                Maximum Bookings Per Slot
              </label>
              <input
                type="number"
                min={1}
                max={10}
                value={maxBookings}
                onChange={(e) => setMaxBookings(Number(e.target.value))}
                className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-semibold outline-hidden"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1">
                Instructions for Students
              </label>
              <textarea
                rows={2}
                value={instructions}
                onChange={(e) => setInstructions(e.target.value)}
                placeholder="e.g. Bring your course notes, homework drafts, or code trace."
                className="w-full px-3 py-2 bg-[#FAF6E4] border border-[#D8D2BA] rounded-xl text-xs font-medium outline-hidden"
              />
            </div>

            <button
              type="submit"
              className="w-full py-2.5 bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] text-xs font-bold rounded-xl shadow-md flex items-center justify-center gap-1.5 transition"
            >
              <Plus className="w-4 h-4 text-[#F2842F]" />
              <span>Publish Slot to Students</span>
            </button>
          </form>
        </div>

        {/* Right 2 Cols: Published Schedule Cards */}
        <div className="lg:col-span-2 space-y-3">
          <h2 className="text-base font-bold text-gray-900">
            Currently Published Slots ({slots.length})
          </h2>

          <div className="space-y-3">
            {slots.map((slot) => (
              <div
                key={slot.id}
                className="p-5 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs flex items-center justify-between gap-4"
              >
                <div className="space-y-1">
                  <div className="flex items-center gap-3">
                    <span className="px-2.5 py-0.5 rounded-full bg-[#15370D] text-[#FCF9EA] font-extrabold text-xs">
                      {slot.day_of_week}
                    </span>
                    <span className="font-extrabold text-sm text-gray-900">
                      {slot.start_time} - {slot.end_time}
                    </span>
                  </div>

                  <p className="text-xs text-gray-600 flex items-center gap-1.5 pt-0.5">
                    <MapPin className="w-3.5 h-3.5 text-gray-400" />
                    <span>Location: <strong className="text-gray-900">{slot.location}</strong></span>
                    <span className="text-gray-400">•</span>
                    <span>Max Capacity: <strong className="text-[#F2842F]">{slot.max_bookings} students</strong></span>
                  </p>

                  <p className="text-[11px] text-gray-500 italic">
                    Note: {slot.instructions}
                  </p>
                </div>

                <button
                  onClick={() => handleDeleteSlot(slot.id)}
                  className="p-2 text-gray-400 hover:text-red-700 hover:bg-red-50 rounded-xl transition"
                  title="Remove this slot"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}

            {slots.length === 0 && !loading && (
              <div className="p-12 text-center bg-white rounded-3xl border border-dashed border-[#D8D2BA]">
                <Clock className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
                <p className="font-bold text-gray-800 text-sm">No consultation slots published</p>
                <p className="text-xs text-gray-500 mt-1">
                  Add your office/cabin hours on the left to allow students to book sessions.
                </p>
              </div>
            )}
          </div>
        </div>

      </div>

    </div>
  );
};
