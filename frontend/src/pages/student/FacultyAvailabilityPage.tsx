import React, { useState, useEffect } from 'react';
import { 
  Calendar, Clock, MapPin, User, CheckCircle2, 
  AlertCircle, ChevronRight, Send, X, AlertTriangle 
} from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Teacher, FacultyAvailability, Appointment } from '../../types';

export const FacultyAvailabilityPage: React.FC = () => {
  const { student } = useAuth();
  const [teachers, setTeachers] = useState<Teacher[]>([]);
  const [availabilities, setAvailabilities] = useState<FacultyAvailability[]>([]);
  const [myAppointments, setMyAppointments] = useState<Appointment[]>([]);
  const [activeTab, setActiveTab] = useState<'schedules' | 'my_bookings'>('schedules');
  
  // Booking Modal State
  const [selectedSlot, setSelectedSlot] = useState<FacultyAvailability | null>(null);
  const [selectedTeacher, setSelectedTeacher] = useState<Teacher | null>(null);
  const [bookingDate, setBookingDate] = useState<string>(() => {
    // Next 2 days default
    const d = new Date();
    d.setDate(d.getDate() + 2);
    return d.toISOString().split('T')[0];
  });
  const [consultationReason, setConsultationReason] = useState('');
  const [submittingBooking, setSubmittingBooking] = useState(false);
  const [bookingError, setBookingError] = useState('');
  const [bookingSuccess, setBookingSuccess] = useState('');

  const loadData = async () => {
    try {
      const [tList, avList] = await Promise.all([
        api.getAllTeachers(),
        api.getFacultyAvailability()
      ]);
      setTeachers(tList);
      setAvailabilities(avList);

      if (student) {
        const apps = await api.getAppointments({ student_name: student.name });
        setMyAppointments(apps);
      }
    } catch (e) {
      console.warn('Failed loading availability:', e);
    }
  };

  useEffect(() => {
    loadData();
  }, [student]);

  const handleOpenBooking = (slot: FacultyAvailability, teacher: Teacher) => {
    setSelectedSlot(slot);
    setSelectedTeacher(teacher);
    setBookingError('');
    setBookingSuccess('');
  };

  const handleSubmitBooking = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSlot || !selectedTeacher || !student) return;
    if (!consultationReason.trim()) {
      setBookingError('Please enter a specific reason for consultation.');
      return;
    }

    setSubmittingBooking(true);
    setBookingError('');
    try {
      const subjectId = selectedTeacher.assigned_subjects.length > 0 
        ? selectedTeacher.assigned_subjects[0].id 
        : undefined;

      await api.bookAppointment({
        teacher_id: selectedTeacher.id,
        student_name: student.name,
        student_section: student.section,
        subject_id: subjectId,
        availability_id: selectedSlot.id,
        appointment_date: bookingDate,
        time_slot: `${selectedSlot.start_time} - ${selectedSlot.end_time}`,
        location: selectedSlot.location,
        reason: consultationReason.trim()
      });

      setBookingSuccess('Consultation request submitted! Awaiting professor approval.');
      setConsultationReason('');
      await loadData();
      setTimeout(() => {
        setSelectedSlot(null);
        setActiveTab('my_bookings');
      }, 1500);
    } catch (err: any) {
      setBookingError(err.message || 'Slot already booked or unavailable.');
    } finally {
      setSubmittingBooking(false);
    }
  };

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
            <Calendar className="w-7 h-7 text-[#15370D]" />
            <span>Faculty Consultation &amp; Cabin Availability</span>
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Book official one-on-one consultation slots with professors outside lecture hours.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex bg-[#F4EFCF] p-1 rounded-2xl border border-[#D8D2BA]">
          <button
            onClick={() => setActiveTab('schedules')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition ${
              activeTab === 'schedules'
                ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
                : 'text-gray-700 hover:text-black'
            }`}
          >
            Faculty Schedules
          </button>
          <button
            onClick={() => setActiveTab('my_bookings')}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition ${
              activeTab === 'my_bookings'
                ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
                : 'text-gray-700 hover:text-black'
            }`}
          >
            My Appointments ({myAppointments.length})
          </button>
        </div>
      </div>

      {/* VIEW 1: FACULTY SCHEDULES */}
      {activeTab === 'schedules' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {teachers.map((t) => {
            const slots = availabilities.filter(a => a.teacher_id === t.id);
            return (
              <div 
                key={t.id}
                className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs hover:border-[#15370D] transition flex flex-col justify-between space-y-4"
              >
                <div>
                  <div className="flex items-start justify-between gap-3 mb-3">
                    <div>
                      <h3 className="text-base font-extrabold text-gray-900">{t.name}</h3>
                      <p className="text-xs text-[#F2842F] font-semibold">{t.department}</p>
                    </div>
                    <span className="px-2.5 py-1 rounded-full bg-[#15370D]/10 text-[#15370D] text-[11px] font-bold">
                      {slots.length} Slots Available
                    </span>
                  </div>

                  <div className="flex items-center gap-2 text-xs text-gray-600 mb-3">
                    <MapPin className="w-4 h-4 text-gray-400 shrink-0" />
                    <span>Cabin: <strong className="text-gray-900">{t.cabin_location}</strong></span>
                  </div>

                  {/* Assigned Subjects */}
                  <div className="flex flex-wrap gap-1.5 mb-4">
                    {t.assigned_subjects.map((sub) => (
                      <span key={sub.id} className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#FAF6E4] border border-[#D8D2BA] text-gray-800">
                        {sub.code}: {sub.title}
                      </span>
                    ))}
                  </div>

                  {/* Slots Schedule */}
                  <div className="space-y-2">
                    <h4 className="text-[11px] font-bold uppercase tracking-wider text-gray-400">
                      Weekly Consultation Hours
                    </h4>
                    {slots.map((slot) => (
                      <div
                        key={slot.id}
                        className="p-3 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] flex items-center justify-between gap-3 text-xs"
                      >
                        <div>
                          <p className="font-bold text-gray-900 flex items-center gap-1.5">
                            <Clock className="w-3.5 h-3.5 text-[#F2842F]" />
                            <span>{slot.day_of_week}: {slot.start_time} - {slot.end_time}</span>
                          </p>
                          <p className="text-[11px] text-gray-500 mt-0.5 line-clamp-1">
                            {slot.instructions || 'Bring course notes.'}
                          </p>
                        </div>

                        <button
                          onClick={() => handleOpenBooking(slot, t)}
                          className="px-3 py-1.5 rounded-lg bg-[#15370D] text-[#FCF9EA] hover:bg-[#15370D]/90 font-bold text-xs shrink-0 shadow-xs transition"
                        >
                          Book Slot
                        </button>
                      </div>
                    ))}

                    {slots.length === 0 && (
                      <p className="text-xs text-gray-500 italic py-2">
                        No active consultation slots published this week.
                      </p>
                    )}
                  </div>
                </div>

                <div className="pt-3 border-t border-gray-100 flex items-center justify-between text-[11px] text-gray-500">
                  <span>Sections: {t.assigned_sections.join(', ')}</span>
                  <span className="text-gray-400">{t.email}</span>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* VIEW 2: MY BOOKED APPOINTMENTS */}
      {activeTab === 'my_bookings' && (
        <div className="space-y-3">
          {myAppointments.map((app) => (
            <div
              key={app.id}
              className="p-5 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="font-extrabold text-sm text-gray-900">{app.teacher_name}</span>
                  <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold ${
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
                <p className="text-xs text-gray-700 font-semibold">
                  Date: {app.appointment_date} • Time: {app.time_slot}
                </p>
                <p className="text-xs text-gray-600">
                  Location: <strong className="text-gray-900">{app.location}</strong>
                </p>
                <p className="text-xs text-gray-600 italic mt-1">
                  Reason: "{app.reason}"
                </p>
                {app.teacher_notes && (
                  <p className="text-xs text-[#15370D] font-medium pt-1">
                    Professor's Note: {app.teacher_notes}
                  </p>
                )}
              </div>

              <div className="text-right text-[11px] text-gray-400 shrink-0">
                Booked on {new Date(app.created_at).toLocaleDateString()}
              </div>
            </div>
          ))}

          {myAppointments.length === 0 && (
            <div className="p-12 text-center bg-white rounded-2xl border border-dashed border-[#D8D2BA]">
              <Calendar className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
              <p className="font-bold text-gray-800 text-sm">No booked appointments yet</p>
              <p className="text-xs text-gray-500 mt-1">
                Switch to the "Faculty Schedules" tab above to book your first slot.
              </p>
            </div>
          )}
        </div>
      )}

      {/* BOOKING MODAL */}
      {selectedSlot && selectedTeacher && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
          <div className="w-full max-w-lg bg-[#FCF9EA] border border-[#D8D2BA] rounded-3xl shadow-2xl overflow-hidden animate-fade-in">
            
            {/* Header */}
            <div className="px-6 py-4 bg-[#15370D] text-[#FCF9EA] flex items-center justify-between">
              <div>
                <h3 className="text-base font-bold text-white">Book Consultation Slot</h3>
                <p className="text-xs text-[#F2842F]">{selectedTeacher.name}</p>
              </div>
              <button 
                onClick={() => setSelectedSlot(null)}
                className="p-1 text-white/80 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmitBooking} className="p-6 space-y-4">
              
              {bookingSuccess && (
                <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-300 text-xs font-bold text-emerald-900 flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0" />
                  <span>{bookingSuccess}</span>
                </div>
              )}

              {bookingError && (
                <div className="p-3.5 rounded-xl bg-red-50 border border-red-300 text-xs font-bold text-red-900 flex items-center gap-2">
                  <AlertTriangle className="w-5 h-5 text-red-600 shrink-0" />
                  <span>{bookingError}</span>
                </div>
              )}

              {/* Slot Details Summary */}
              <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] text-xs space-y-1.5">
                <p className="font-bold text-gray-900">
                  {selectedSlot.day_of_week} Slot: {selectedSlot.start_time} - {selectedSlot.end_time}
                </p>
                <p className="text-gray-600">Location: {selectedSlot.location}</p>
                <p className="text-[11px] text-gray-500">{selectedSlot.instructions}</p>
              </div>

              {/* Consultation Date Picker */}
              <div>
                <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
                  Select Appointment Date *
                </label>
                <input
                  type="date"
                  value={bookingDate}
                  min={new Date().toISOString().split('T')[0]}
                  onChange={(e) => setBookingDate(e.target.value)}
                  className="w-full px-4 py-2.5 bg-white border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs font-medium outline-hidden"
                  required
                />
              </div>

              {/* Reason For Consultation */}
              <div>
                <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
                  Academic Reason for Consultation *
                </label>
                <textarea
                  rows={3}
                  value={consultationReason}
                  onChange={(e) => setConsultationReason(e.target.value)}
                  placeholder="e.g. Need help reviewing the Coffman conditions for OS lab experiment 4, or discussing Project P09 design validation metrics."
                  className="w-full p-3 bg-white border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs font-medium outline-hidden"
                  required
                />
              </div>

              <div className="pt-2 flex justify-end gap-2">
                <button
                  type="button"
                  onClick={() => setSelectedSlot(null)}
                  className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 rounded-xl text-xs font-semibold"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submittingBooking}
                  className="px-5 py-2 bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-md disabled:opacity-50"
                >
                  <Send className="w-3.5 h-3.5 text-[#F2842F]" />
                  <span>{submittingBooking ? 'Submitting...' : 'Confirm Booking'}</span>
                </button>
              </div>

            </form>

          </div>
        </div>
      )}

    </div>
  );
};
