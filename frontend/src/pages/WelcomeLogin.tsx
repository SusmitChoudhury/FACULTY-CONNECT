import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  GraduationCap, BookOpen, Clock, Sparkles, 
  ShieldCheck, ArrowRight, CheckCircle2, User, 
  Lock, AlertCircle, Building2, HelpCircle 
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api';
import { Section } from '../types';
import { Footer } from '../components/Footer';

export const WelcomeLogin: React.FC = () => {
  const { loginStudent, loginTeacher, role } = useAuth();
  const navigate = useNavigate();

  // Active Tab: 'student' or 'teacher'
  const [activeTab, setActiveTab] = useState<'student' | 'teacher'>('student');

  // Student form state
  const [studentName, setStudentName] = useState('');
  const [studentSection, setStudentSection] = useState('K22DF');
  const [sections, setSections] = useState<Section[]>([]);
  const [studentLoading, setStudentLoading] = useState(false);
  const [studentError, setStudentError] = useState('');

  // Teacher form state
  const [teacherEmail, setTeacherEmail] = useState('');
  const [teacherPassword, setTeacherPassword] = useState('');
  const [teacherLoading, setTeacherLoading] = useState(false);
  const [teacherError, setTeacherError] = useState('');

  useEffect(() => {
    // If already logged in, redirect
    if (role === 'student') navigate('/student/dashboard');
    if (role === 'teacher') navigate('/teacher/dashboard');

    // Fetch available sections
    api.getSections().then(setSections).catch(() => {
      setSections([
        { id: 1, name: 'K22DF', department: 'CSE' },
        { id: 2, name: 'K22GF', department: 'CSE' },
        { id: 3, name: 'K22SE', department: 'CSE' },
        { id: 4, name: 'K23AA', department: 'CSE' },
        { id: 5, name: 'K23AB', department: 'CSE' }
      ]);
    });
  }, [role, navigate]);

  const handleStudentSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!studentName.trim()) {
      setStudentError('Please enter your full student name.');
      return;
    }
    setStudentLoading(true);
    setStudentError('');

    try {
      const res = await api.studentLogin(studentName.trim(), studentSection);
      loginStudent(res.student);
      navigate('/student/dashboard');
    } catch (err: any) {
      setStudentError(err.message || 'Login failed.');
    } finally {
      setStudentLoading(false);
    }
  };

  const handleTeacherSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teacherEmail.trim() || !teacherPassword) {
      setTeacherError('Please provide faculty email and password.');
      return;
    }
    setTeacherLoading(true);
    setTeacherError('');

    try {
      const res = await api.teacherLogin(teacherEmail.trim(), teacherPassword);
      loginTeacher(res.teacher, res.token);
      navigate('/teacher/dashboard');
    } catch (err: any) {
      setTeacherError(err.message || 'Invalid credentials.');
    } finally {
      setTeacherLoading(false);
    }
  };

  const fillTeacherQuickLogin = (email: string) => {
    setTeacherEmail(email);
    setTeacherPassword('faculty123');
    setTeacherError('');
  };

  return (
    <div className="min-h-screen bg-[#FCF9EA] text-[#000000] flex flex-col justify-between">
      
      {/* Top Banner / Hero */}
      <section className="bg-[#15370D] text-[#FCF9EA] border-b border-[#F2842F]/30 py-10 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto text-center space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#FCF9EA]/10 border border-[#F2842F]/40 text-xs font-semibold text-[#F2842F]">
            <span>LPU INT335 Design Thinking Project P09</span>
            <span>•</span>
            <span>Heard in Class, Lost After</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-black tracking-tight text-[#FCF9EA]">
            FACULTY <span className="text-[#F2842F]">CONNECT</span>
          </h1>

          <p className="max-w-2xl mx-auto text-sm sm:text-base text-[#FCF9EA]/80 font-normal leading-relaxed">
            Making Academic Communication Smarter, Faster and More Organised. 
            A unified academic platform solving outside-lecture communication barriers between students and faculty.
          </p>
        </div>
      </section>

      {/* Main Authentication Card Container */}
      <main className="flex-1 max-w-4xl w-full mx-auto p-4 sm:p-6 lg:p-8 flex flex-col items-center justify-center -mt-6">
        <div className="w-full bg-white rounded-3xl border border-[#D8D2BA] shadow-xl overflow-hidden">
          
          {/* Distinct Panel Switcher Tabs */}
          <div className="grid grid-cols-2 bg-[#F4EFCF] border-b border-[#D8D2BA] p-1.5 gap-2">
            <button
              type="button"
              onClick={() => setActiveTab('student')}
              className={`py-3.5 px-4 rounded-2xl font-bold text-sm sm:text-base flex items-center justify-center gap-2.5 transition ${
                activeTab === 'student'
                  ? 'bg-[#15370D] text-[#FCF9EA] shadow-md'
                  : 'text-gray-700 hover:text-black hover:bg-white/60'
              }`}
            >
              <User className="w-5 h-5 text-[#F2842F]" />
              <span>1. STUDENT PANEL</span>
            </button>

            <button
              type="button"
              onClick={() => setActiveTab('teacher')}
              className={`py-3.5 px-4 rounded-2xl font-bold text-sm sm:text-base flex items-center justify-center gap-2.5 transition ${
                activeTab === 'teacher'
                  ? 'bg-[#15370D] text-[#FCF9EA] shadow-md'
                  : 'text-gray-700 hover:text-black hover:bg-white/60'
              }`}
            >
              <ShieldCheck className="w-5 h-5 text-[#F2842F]" />
              <span>2. TEACHER PANEL</span>
            </button>
          </div>

          <div className="p-6 sm:p-10">
            {/* Student Panel */}
            {activeTab === 'student' && (
              <div className="animate-fade-in max-w-md mx-auto">
                <div className="text-center mb-6">
                  <h2 className="text-xl sm:text-2xl font-extrabold text-gray-900">
                    Student Academic Access
                  </h2>
                  <p className="text-xs sm:text-sm text-gray-600 mt-1">
                    Enter your name and select your section to ask doubts, explore syllabus, or book faculty appointments.
                  </p>
                </div>

                {studentError && (
                  <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-xs font-semibold text-red-700 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>{studentError}</span>
                  </div>
                )}

                <form onSubmit={handleStudentSubmit} className="space-y-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
                      Student Full Name *
                    </label>
                    <div className="relative">
                      <User className="w-4 h-4 text-gray-400 absolute left-3.5 top-3.5" />
                      <input
                        type="text"
                        value={studentName}
                        onChange={(e) => setStudentName(e.target.value)}
                        placeholder="e.g. Aman Choudhary"
                        className="w-full pl-10 pr-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] focus:bg-white rounded-xl text-sm font-medium outline-hidden transition"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
                      Class Section *
                    </label>
                    <select
                      value={studentSection}
                      onChange={(e) => setStudentSection(e.target.value)}
                      className="w-full px-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] focus:bg-white rounded-xl text-sm font-medium outline-hidden transition"
                    >
                      {sections.map((sec) => (
                        <option key={sec.id} value={sec.name}>
                          Section {sec.name} ({sec.department || 'CSE'})
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Quick Student Suggestions */}
                  <div className="pt-2">
                    <p className="text-[11px] font-semibold text-gray-500 mb-1.5">Quick Demo Profiles:</p>
                    <div className="flex flex-wrap gap-2">
                      <button
                        type="button"
                        onClick={() => { setStudentName('Aman Choudhary'); setStudentSection('K22DF'); }}
                        className="px-2.5 py-1 text-xs rounded-lg bg-[#FAF6E4] border border-[#D8D2BA] hover:border-[#15370D] font-medium transition"
                      >
                        Aman Choudhary (K22DF)
                      </button>
                      <button
                        type="button"
                        onClick={() => { setStudentName('Priya Sharma'); setStudentSection('K22DF'); }}
                        className="px-2.5 py-1 text-xs rounded-lg bg-[#FAF6E4] border border-[#D8D2BA] hover:border-[#15370D] font-medium transition"
                      >
                        Priya Sharma (K22DF)
                      </button>
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={studentLoading}
                    className="w-full mt-4 py-3 bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] font-extrabold rounded-xl shadow-md flex items-center justify-center gap-2 transition disabled:opacity-50"
                  >
                    <span>{studentLoading ? 'Entering Student Portal...' : 'Enter Student Portal'}</span>
                    <ArrowRight className="w-4 h-4 text-[#F2842F]" />
                  </button>
                </form>
              </div>
            )}

            {/* Teacher Panel */}
            {activeTab === 'teacher' && (
              <div className="animate-fade-in max-w-md mx-auto">
                <div className="text-center mb-6">
                  <h2 className="text-xl sm:text-2xl font-extrabold text-gray-900">
                    Faculty Authentication
                  </h2>
                  <p className="text-xs sm:text-sm text-gray-600 mt-1">
                    Authorized faculty access for academic doubt management and consultation schedules.
                  </p>
                </div>

                {teacherError && (
                  <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-xs font-semibold text-red-700 flex items-center gap-2">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>{teacherError}</span>
                  </div>
                )}

                <form onSubmit={handleTeacherSubmit} className="space-y-4">
                  <div>
                    <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
                      Faculty Official Email *
                    </label>
                    <div className="relative">
                      <User className="w-4 h-4 text-gray-400 absolute left-3.5 top-3.5" />
                      <input
                        type="email"
                        value={teacherEmail}
                        onChange={(e) => setTeacherEmail(e.target.value)}
                        placeholder="e.g. dr.rajesh@lpu.co.in"
                        className="w-full pl-10 pr-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] focus:bg-white rounded-xl text-sm font-medium outline-hidden transition"
                        required
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
                      Password *
                    </label>
                    <div className="relative">
                      <Lock className="w-4 h-4 text-gray-400 absolute left-3.5 top-3.5" />
                      <input
                        type="password"
                        value={teacherPassword}
                        onChange={(e) => setTeacherPassword(e.target.value)}
                        placeholder="Enter faculty password"
                        className="w-full pl-10 pr-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] focus:bg-white rounded-xl text-sm font-medium outline-hidden transition"
                        required
                      />
                    </div>
                  </div>

                  {/* Quick Faculty Click for Evaluation */}
                  <div className="pt-2">
                    <p className="text-[11px] font-semibold text-gray-500 mb-1.5">Quick Evaluation Pre-Sets (Default pwd: faculty123):</p>
                    <div className="space-y-1.5">
                      <button
                        type="button"
                        onClick={() => fillTeacherQuickLogin('dr.rajesh@lpu.co.in')}
                        className="w-full px-2.5 py-1.5 text-xs rounded-lg bg-[#FAF6E4] border border-[#D8D2BA] hover:border-[#15370D] text-left font-medium transition flex items-center justify-between"
                      >
                        <span>Dr. Rajesh Sharma (INT335 Design Thinking)</span>
                        <span className="text-[10px] text-[#F2842F] font-bold">Use</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => fillTeacherQuickLogin('dr.harpreet@lpu.co.in')}
                        className="w-full px-2.5 py-1.5 text-xs rounded-lg bg-[#FAF6E4] border border-[#D8D2BA] hover:border-[#15370D] text-left font-medium transition flex items-center justify-between"
                      >
                        <span>Dr. Harpreet Kaur (CSE316 Operating Systems)</span>
                        <span className="text-[10px] text-[#F2842F] font-bold">Use</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => fillTeacherQuickLogin('prof.verma@lpu.co.in')}
                        className="w-full px-2.5 py-1.5 text-xs rounded-lg bg-[#FAF6E4] border border-[#D8D2BA] hover:border-[#15370D] text-left font-medium transition flex items-center justify-between"
                      >
                        <span>Prof. Amit Verma (CSM228 Data Structures)</span>
                        <span className="text-[10px] text-[#F2842F] font-bold">Use</span>
                      </button>
                    </div>
                  </div>

                  <button
                    type="submit"
                    disabled={teacherLoading}
                    className="w-full mt-4 py-3 bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] font-extrabold rounded-xl shadow-md flex items-center justify-center gap-2 transition disabled:opacity-50"
                  >
                    <span>{teacherLoading ? 'Verifying Faculty Credentials...' : 'Sign In to Faculty Console'}</span>
                    <ArrowRight className="w-4 h-4 text-[#F2842F]" />
                  </button>
                </form>
              </div>
            )}
          </div>
        </div>

        {/* Feature Highlights Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 mt-8 w-full">
          <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs flex items-start gap-3">
            <div className="p-2 rounded-xl bg-[#15370D]/10 text-[#15370D] shrink-0">
              <Sparkles className="w-5 h-5 text-[#F2842F]" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-gray-900">Smart Duplicate Engine</h3>
              <p className="text-[11px] text-gray-600 mt-0.5 leading-relaxed">
                Prevents repetitive questions. Supports +1 to notify students together when answered.
              </p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs flex items-start gap-3">
            <div className="p-2 rounded-xl bg-[#15370D]/10 text-[#15370D] shrink-0">
              <Clock className="w-5 h-5 text-[#F2842F]" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-gray-900">3-Hour AI Mechanism</h3>
              <p className="text-[11px] text-gray-600 mt-0.5 leading-relaxed">
                Server-side timer triggers syllabus-grounded academic explanations if faculty is busy.
              </p>
            </div>
          </div>

          <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs flex items-start gap-3">
            <div className="p-2 rounded-xl bg-[#15370D]/10 text-[#15370D] shrink-0">
              <BookOpen className="w-5 h-5 text-[#F2842F]" />
            </div>
            <div>
              <h3 className="text-xs font-bold text-gray-900">Verified Syllabus Core</h3>
              <p className="text-[11px] text-gray-600 mt-0.5 leading-relaxed">
                Built strictly on LPU course units, topics, subtopics, and approved textbooks.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Global Academic Project Footer */}
      <Footer />

    </div>
  );
};
