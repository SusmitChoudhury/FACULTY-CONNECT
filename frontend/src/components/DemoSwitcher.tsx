import React, { useState } from 'react';
import { 
  Sliders, UserCheck, Shield, RotateCcw, 
  Sparkles, Check, ChevronUp, ChevronDown 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api';

export const DemoSwitcher: React.FC = () => {
  const { loginStudent, loginTeacher } = useAuth();
  const [isOpen, setIsOpen] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const showToast = (msg: string) => {
    setMessage(msg);
    setTimeout(() => setMessage(null), 3000);
  };

  const handleSelectStudent = async (name: string, section: string) => {
    try {
      const res = await api.studentLogin(name, section);
      loginStudent(res.student);
      showToast(`Switched to student: ${res.student.name} (${section})`);
    } catch (e: any) {
      showToast(e.message);
    }
  };

  const handleSelectTeacher = async (email: string) => {
    try {
      const res = await api.teacherLogin(email, 'faculty123');
      loginTeacher(res.teacher, res.token);
      showToast(`Switched to faculty: ${res.teacher.name}`);
    } catch (e: any) {
      showToast(e.message);
    }
  };

  const handleTriggerTimer = async () => {
    try {
      const res = await api.triggerTimerCheck();
      showToast(`Scan complete: ${res.processed_count} doubts answered by AI worker.`);
    } catch (e: any) {
      showToast(e.message);
    }
  };

  const handleResetDemo = async () => {
    if (!confirm('Reset all demo data to INT335 original presentation state?')) return;
    try {
      await api.resetDemoData();
      showToast('Demonstration data successfully reset!');
      window.location.reload();
    } catch (e: any) {
      showToast(e.message);
    }
  };

  return (
    <div className="fixed bottom-16 lg:bottom-4 right-4 z-50">
      {/* Toast Notification */}
      {message && (
        <div className="mb-2 px-3.5 py-2 rounded-xl bg-[#15370D] text-[#FCF9EA] text-xs font-semibold shadow-xl border border-[#F2842F] animate-fade-in flex items-center gap-2">
          <Check className="w-4 h-4 text-[#F2842F]" />
          <span>{message}</span>
        </div>
      )}

      {/* Accordion Box */}
      <div className="bg-[#FCF9EA] border border-[#15370D] rounded-2xl shadow-xl overflow-hidden transition-all duration-200">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-full px-3 py-2 bg-[#15370D] text-[#FCF9EA] flex items-center justify-between gap-3 text-xs font-bold hover:bg-[#15370D]/95 transition"
        >
          <div className="flex items-center gap-1.5">
            <Sliders className="w-3.5 h-3.5 text-[#F2842F]" />
            <span>INT335 Demo Bar</span>
          </div>
          {isOpen ? <ChevronDown className="w-3.5 h-3.5 text-[#F2842F]" /> : <ChevronUp className="w-3.5 h-3.5 text-[#F2842F]" />}
        </button>

        {isOpen && (
          <div className="p-3 w-72 space-y-3 text-xs bg-[#FAF6E4]">
            
            {/* Quick Students */}
            <div>
              <p className="font-bold text-gray-800 flex items-center gap-1 mb-1.5 text-[11px] uppercase tracking-wider">
                <UserCheck className="w-3.5 h-3.5 text-[#15370D]" />
                Switch Student Account
              </p>
              <div className="grid grid-cols-2 gap-1.5">
                <button
                  onClick={() => handleSelectStudent('Aman Choudhary', 'K22DF')}
                  className="px-2 py-1.5 bg-white border border-[#D8D2BA] rounded-lg text-left hover:border-[#15370D] hover:bg-[#15370D]/5 transition"
                >
                  <p className="font-semibold text-gray-900 truncate">Aman C.</p>
                  <p className="text-[10px] text-gray-500">Sec K22DF</p>
                </button>
                <button
                  onClick={() => handleSelectStudent('Priya Sharma', 'K22DF')}
                  className="px-2 py-1.5 bg-white border border-[#D8D2BA] rounded-lg text-left hover:border-[#15370D] hover:bg-[#15370D]/5 transition"
                >
                  <p className="font-semibold text-gray-900 truncate">Priya S.</p>
                  <p className="text-[10px] text-gray-500">Sec K22DF</p>
                </button>
              </div>
            </div>

            {/* Quick Teachers */}
            <div>
              <p className="font-bold text-gray-800 flex items-center gap-1 mb-1.5 text-[11px] uppercase tracking-wider">
                <Shield className="w-3.5 h-3.5 text-[#F2842F]" />
                Switch Faculty Account
              </p>
              <div className="space-y-1">
                <button
                  onClick={() => handleSelectTeacher('dr.rajesh@lpu.co.in')}
                  className="w-full px-2 py-1.5 bg-white border border-[#D8D2BA] rounded-lg text-left hover:border-[#15370D] hover:bg-[#15370D]/5 transition flex justify-between items-center"
                >
                  <div>
                    <p className="font-semibold text-gray-900 truncate">Dr. Rajesh Sharma</p>
                    <p className="text-[10px] text-[#F2842F]">INT335 Design Thinking</p>
                  </div>
                  <span className="text-[10px] px-1 py-0.5 rounded bg-[#15370D]/10 font-bold text-[#15370D]">Cabin 601</span>
                </button>

                <button
                  onClick={() => handleSelectTeacher('dr.harpreet@lpu.co.in')}
                  className="w-full px-2 py-1.5 bg-white border border-[#D8D2BA] rounded-lg text-left hover:border-[#15370D] hover:bg-[#15370D]/5 transition flex justify-between items-center"
                >
                  <div>
                    <p className="font-semibold text-gray-900 truncate">Dr. Harpreet Kaur</p>
                    <p className="text-[10px] text-[#F2842F]">CSE316 Operating Systems</p>
                  </div>
                  <span className="text-[10px] px-1 py-0.5 rounded bg-[#15370D]/10 font-bold text-[#15370D]">Cabin 402</span>
                </button>

                <button
                  onClick={() => handleSelectTeacher('prof.verma@lpu.co.in')}
                  className="w-full px-2 py-1.5 bg-white border border-[#D8D2BA] rounded-lg text-left hover:border-[#15370D] hover:bg-[#15370D]/5 transition flex justify-between items-center"
                >
                  <div>
                    <p className="font-semibold text-gray-900 truncate">Prof. Amit Verma</p>
                    <p className="text-[10px] text-[#F2842F]">CSM228 Data Structures</p>
                  </div>
                  <span className="text-[10px] px-1 py-0.5 rounded bg-[#15370D]/10 font-bold text-[#15370D]">Cabin 405</span>
                </button>
              </div>
            </div>

            {/* Test Actions */}
            <div className="pt-2 border-t border-[#D8D2BA] space-y-1.5">
              <button
                onClick={handleTriggerTimer}
                className="w-full py-1.5 px-2 bg-[#15370D] text-[#FCF9EA] hover:bg-[#15370D]/90 rounded-lg font-bold flex items-center justify-center gap-1.5 transition text-[11px]"
                title="Runs the background 3-hour timer check immediately"
              >
                <Sparkles className="w-3.5 h-3.5 text-[#F2842F]" />
                Trigger 3-Hour AI Check
              </button>

              <button
                onClick={handleResetDemo}
                className="w-full py-1.5 px-2 bg-white text-gray-700 hover:text-red-700 hover:border-red-300 border border-[#D8D2BA] rounded-lg font-medium flex items-center justify-center gap-1.5 transition text-[11px]"
              >
                <RotateCcw className="w-3.5 h-3.5 text-gray-500" />
                Reset Demonstration Data
              </button>
            </div>

          </div>
        )}
      </div>
    </div>
  );
};
