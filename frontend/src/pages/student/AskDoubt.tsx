import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { 
  HelpCircle, Sparkles, CheckCircle2, AlertTriangle, 
  ArrowLeft, ArrowRight, BookOpen, Calendar, Clock, 
  RotateCcw, Send, Layers, ThumbsUp, ShieldCheck, User 
} from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Subject, Unit, Topic, Doubt } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export const AskDoubt: React.FC = () => {
  const { student } = useAuth();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  // Multi-step Form State
  const [step, setStep] = useState<1 | 2 | 3>(1); // Step 1: Subject/Unit/Topic/Date -> Step 2: Doubt Textarea -> Step 3: Duplicate Screen (if triggered)
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<number | ''>('');
  const [selectedUnitId, setSelectedUnitId] = useState<number | ''>('');
  const [selectedTopicId, setSelectedTopicId] = useState<number | ''>('');
  const [teachingDate, setTeachingDate] = useState<string>(() => {
    return new Date().toISOString().split('T')[0];
  });
  const [category, setCategory] = useState<string>('Conceptual Doubt');
  const [questionText, setQuestionText] = useState<string>('');
  
  // Loading & Error States
  const [loading, setLoading] = useState(false);
  const [checkingDuplicates, setCheckingDuplicates] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  // Duplicate Match Detection Result
  const [duplicateResult, setDuplicateResult] = useState<{
    is_duplicate: boolean;
    confidence: number;
    matched_doubt: Doubt | null;
    existing_answer: {
      type: 'faculty' | 'ai';
      author: string;
      text: string;
      quality_status?: string;
      created_at: string;
    } | null;
  } | null>(null);

  // Success State
  const [successInfo, setSuccessInfo] = useState<{
    title: string;
    message: string;
    doubtId?: number;
  } | null>(null);

  // Load subjects and handle query params
  useEffect(() => {
    const init = async () => {
      try {
        setLoading(true);
        const data = await api.getSubjects();
        setSubjects(data);

        // Prepopulate from URL params if arrived from Syllabus Explorer
        const qSub = searchParams.get('subject');
        const qUnit = searchParams.get('unit');
        const qTopic = searchParams.get('topic');

        if (qSub) {
          const sId = parseInt(qSub, 10);
          setSelectedSubjectId(sId);
          if (qUnit) setSelectedUnitId(parseInt(qUnit, 10));
          if (qTopic) setSelectedTopicId(parseInt(qTopic, 10));
        } else if (data.length > 0) {
          setSelectedSubjectId(data[0].id);
        }
      } catch (e: any) {
        setErrorMessage('Failed to load syllabus subjects.');
      } finally {
        setLoading(false);
      }
    };
    init();
  }, [searchParams]);

  // Derived current subject, units, topics
  const currentSubject = subjects.find(s => s.id === selectedSubjectId);
  const availableUnits = currentSubject?.units || [];
  const currentUnit = availableUnits.find(u => u.id === selectedUnitId);
  const availableTopics = currentUnit?.topics || [];

  // When subject changes, reset unit & topic
  const handleSubjectChange = (id: number) => {
    setSelectedSubjectId(id);
    setSelectedUnitId('');
    setSelectedTopicId('');
  };

  // When unit changes, reset topic
  const handleUnitChange = (id: number) => {
    setSelectedUnitId(id);
    setSelectedTopicId('');
  };

  // Step 1 to Step 2 Validation
  const handleProceedToQuestion = (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedSubjectId || !selectedUnitId || !selectedTopicId) {
      setErrorMessage('Please select Subject, Unit, and Topic to proceed.');
      return;
    }
    setErrorMessage('');
    setStep(2);
  };

  // Submit Doubt -> Triggers Smart Doubt Duplicate Detection
  const handleSubmitDoubt = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!questionText.trim()) {
      setErrorMessage('Please describe your academic doubt.');
      return;
    }
    if (questionText.trim().length < 15) {
      setErrorMessage('Please provide a slightly more descriptive question (at least 15 characters).');
      return;
    }

    setCheckingDuplicates(true);
    setErrorMessage('');

    try {
      // 1. Run semantic duplicate detection scoped by section, subject, unit, topic
      const checkRes = await api.checkDuplicateDoubt({
        question_text: questionText.trim(),
        subject_id: Number(selectedSubjectId),
        unit_id: Number(selectedUnitId),
        topic_id: Number(selectedTopicId),
        section: student?.section || 'K22DF'
      });

      if (checkRes.is_duplicate && checkRes.matched_doubt) {
        // DUPLICATE DETECTED! Show comparison screen
        setDuplicateResult(checkRes);
        setStep(3);
      } else {
        // No duplicate found -> Submit directly to faculty queue
        await executeDirectSubmission();
      }
    } catch (err: any) {
      setErrorMessage(err.message || 'Error checking for duplicates.');
    } finally {
      setCheckingDuplicates(false);
    }
  };

  // Direct Submission (Option 2 or when no duplicate detected)
  const executeDirectSubmission = async () => {
    if (!student) return;
    try {
      const res = await api.createDoubt({
        student_name: student.name,
        section: student.section,
        subject_id: Number(selectedSubjectId),
        unit_id: Number(selectedUnitId),
        topic_id: Number(selectedTopicId),
        teaching_date: teachingDate,
        category: category,
        question_text: questionText.trim()
      });

      setSuccessInfo({
        title: 'Academic Doubt Forwarded to Faculty Queue',
        message: 'Your doubt has been submitted. The 3-hour response timer has started. If faculty is engaged, our syllabus-grounded academic assistant will provide a preliminary answer automatically.',
        doubtId: res.doubt.id
      });
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to submit doubt.');
    }
  };

  // Option 1: "+1 – I HAVE THE SAME DOUBT"
  const handleSupportExisting = async () => {
    if (!duplicateResult?.matched_doubt || !student) return;
    setLoading(true);
    try {
      const res = await api.supportExistingDoubt(
        duplicateResult.matched_doubt.id,
        student.name,
        student.section
      );

      setSuccessInfo({
        title: 'Added Your +1 Support to this Doubt!',
        message: 'You have been linked to this query. You will receive an immediate notification as soon as the professor publishes the official answer.',
        doubtId: res.doubt.id
      });
    } catch (err: any) {
      setErrorMessage(err.message || 'Failed to add +1 support.');
    } finally {
      setLoading(false);
    }
  };

  // Option 2: "ASK A SEPARATE DOUBT"
  const handleConfirmSeparateDoubt = async () => {
    const confirmed = confirm(
      'Are you sure the existing doubt and answers do not cover your question? Click OK to submit this as an independent doubt into the faculty queue.'
    );
    if (!confirmed) return;

    setLoading(true);
    try {
      await executeDirectSubmission();
    } finally {
      setLoading(false);
    }
  };

  const handleResetForm = () => {
    setStep(1);
    setQuestionText('');
    setDuplicateResult(null);
    setSuccessInfo(null);
    setErrorMessage('');
  };

  // Categories per Section 21.J
  const categories = [
    'Conceptual Doubt',
    'Numerical Problem',
    'Assignment Related',
    'Lecture Clarification',
    'Examination Preparation',
    'Other'
  ];

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fade-in pb-16">
      
      {/* Top Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
          <HelpCircle className="w-7 h-7 text-[#15370D]" />
          <span>Ask an Academic Doubt</span>
        </h1>
        <p className="text-xs sm:text-sm text-gray-600 mt-1">
          Smart Question Submission with real-time duplicate detection &amp; 3-hour automatic assistance.
        </p>
      </div>

      {/* Step Indicator Progress Bar */}
      <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-black ${
            step >= 1 ? 'bg-[#15370D] text-[#FCF9EA]' : 'bg-gray-200 text-gray-600'
          }`}>
            1
          </span>
          <span className="text-xs font-bold text-gray-800 hidden sm:inline">Academic Scope</span>
        </div>
        <div className="flex-1 h-0.5 bg-[#D8D2BA] mx-3"></div>

        <div className="flex items-center gap-2">
          <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-black ${
            step >= 2 ? 'bg-[#15370D] text-[#FCF9EA]' : 'bg-gray-200 text-gray-600'
          }`}>
            2
          </span>
          <span className="text-xs font-bold text-gray-800 hidden sm:inline">Describe Doubt</span>
        </div>
        <div className="flex-1 h-0.5 bg-[#D8D2BA] mx-3"></div>

        <div className="flex items-center gap-2">
          <span className={`w-7 h-7 rounded-full flex items-center justify-center text-xs font-black ${
            step === 3 ? 'bg-[#F2842F] text-[#000000]' : 'bg-gray-200 text-gray-600'
          }`}>
            3
          </span>
          <span className="text-xs font-bold text-gray-800 hidden sm:inline">Smart Intelligence</span>
        </div>
      </div>

      {/* Error Banner */}
      {errorMessage && (
        <div className="p-4 rounded-2xl bg-red-50 border border-red-200 text-xs font-semibold text-red-800 flex items-center gap-2.5 animate-fade-in">
          <AlertTriangle className="w-5 h-5 text-red-600 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}

      {/* SUCCESS CONFIRMATION MODAL / SCREEN */}
      {successInfo && (
        <div className="p-8 rounded-3xl bg-white border-2 border-[#15370D] shadow-xl text-center space-y-4 animate-fade-in">
          <div className="w-14 h-14 mx-auto rounded-full bg-[#15370D]/10 text-[#15370D] flex items-center justify-center">
            <CheckCircle2 className="w-8 h-8 text-[#15370D]" />
          </div>
          <h2 className="text-xl sm:text-2xl font-black text-gray-900">{successInfo.title}</h2>
          <p className="text-xs sm:text-sm text-gray-600 max-w-lg mx-auto leading-relaxed">
            {successInfo.message}
          </p>

          <div className="pt-4 flex flex-col sm:flex-row gap-3 justify-center">
            <button
              onClick={() => navigate('/student/questions')}
              className="px-6 py-2.5 rounded-xl bg-[#15370D] text-[#FCF9EA] font-bold text-xs hover:bg-[#15370D]/90 shadow-md transition"
            >
              View My Questions
            </button>
            <button
              onClick={handleResetForm}
              className="px-6 py-2.5 rounded-xl bg-[#FAF6E4] text-[#000000] border border-[#D8D2BA] font-bold text-xs hover:bg-white transition"
            >
              Ask Another Doubt
            </button>
          </div>
        </div>
      )}

      {/* STEP 1: Academic Scope Selection Flow */}
      {!successInfo && step === 1 && (
        <form onSubmit={handleProceedToQuestion} className="p-6 sm:p-8 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-5 animate-fade-in">
          
          <div className="border-b border-gray-100 pb-3">
            <h2 className="text-base font-bold text-gray-900">Step 1: Select Academic Identifier</h2>
            <p className="text-xs text-gray-500 mt-0.5">
              Ties your doubt directly to the course lecture and syllabus topic.
            </p>
          </div>

          {/* Student Info Pill */}
          <div className="p-3 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] flex items-center justify-between text-xs">
            <div className="flex items-center gap-2">
              <User className="w-4 h-4 text-[#15370D]" />
              <span className="font-semibold text-gray-800">Student: {student?.name}</span>
            </div>
            <span className="px-2 py-0.5 rounded bg-[#15370D] text-[#FCF9EA] font-bold text-[11px]">
              Section {student?.section}
            </span>
          </div>

          {/* Subject Dropdown */}
          <div>
            <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
              Subject *
            </label>
            <select
              value={selectedSubjectId}
              onChange={(e) => handleSubjectChange(Number(e.target.value))}
              className="w-full px-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs sm:text-sm font-medium outline-hidden transition"
              required
            >
              <option value="">Select Course Subject...</option>
              {subjects.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.code}: {s.title}
                </option>
              ))}
            </select>
          </div>

          {/* Unit Dropdown */}
          <div>
            <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
              Course Unit *
            </label>
            <select
              value={selectedUnitId}
              onChange={(e) => handleUnitChange(Number(e.target.value))}
              disabled={!selectedSubjectId}
              className="w-full px-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs sm:text-sm font-medium outline-hidden transition disabled:opacity-50"
              required
            >
              <option value="">Select Unit...</option>
              {availableUnits.map((u) => (
                <option key={u.id} value={u.id}>
                  {u.unit_number}: {u.title}
                </option>
              ))}
            </select>
          </div>

          {/* Topic Dropdown */}
          <div>
            <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
              Specific Syllabus Topic *
            </label>
            <select
              value={selectedTopicId}
              onChange={(e) => setSelectedTopicId(Number(e.target.value))}
              disabled={!selectedUnitId}
              className="w-full px-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs sm:text-sm font-medium outline-hidden transition disabled:opacity-50"
              required
            >
              <option value="">Select Topic...</option>
              {availableTopics.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.title}
                </option>
              ))}
            </select>
          </div>

          {/* Date of Teaching */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
                Date of Teaching / Lecture Date *
              </label>
              <div className="relative">
                <Calendar className="w-4 h-4 text-gray-500 absolute left-3.5 top-3" />
                <input
                  type="date"
                  value={teachingDate}
                  onChange={(e) => setTeachingDate(e.target.value)}
                  className="w-full pl-10 pr-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs sm:text-sm font-medium outline-hidden transition"
                  required
                />
              </div>
              <p className="text-[10px] text-gray-500 mt-1">
                Helps faculty identify the exact lecture session.
              </p>
            </div>

            <div>
              <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5">
                Doubt Category
              </label>
              <select
                value={category}
                onChange={(e) => setCategory(e.target.value)}
                className="w-full px-4 py-2.5 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs sm:text-sm font-medium outline-hidden transition"
              >
                {categories.map((c) => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
          </div>

          <div className="pt-4 border-t border-gray-100 flex justify-end">
            <button
              type="submit"
              className="px-6 py-2.5 rounded-xl bg-[#15370D] text-[#FCF9EA] font-extrabold text-xs sm:text-sm hover:bg-[#15370D]/90 shadow-md flex items-center gap-2 transition"
            >
              <span>Next: Describe Doubt</span>
              <ArrowRight className="w-4 h-4 text-[#F2842F]" />
            </button>
          </div>

        </form>
      )}

      {/* STEP 2: Large Comfortable Textarea */}
      {!successInfo && step === 2 && (
        <form onSubmit={handleSubmitDoubt} className="p-6 sm:p-8 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-5 animate-fade-in">
          
          <div className="flex items-center justify-between border-b border-gray-100 pb-3">
            <div>
              <h2 className="text-base font-bold text-gray-900">Step 2: Describe Your Academic Doubt</h2>
              <p className="text-xs text-gray-500 mt-0.5">
                Explain what you are struggling with or need clarification on.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setStep(1)}
              className="text-xs font-bold text-[#15370D] hover:underline flex items-center gap-1"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Edit Scope
            </button>
          </div>

          {/* Scope Summary Card */}
          <div className="p-3.5 rounded-2xl bg-[#FAF6E4] border border-[#E5DFC8] text-xs space-y-1">
            <div className="flex items-center gap-2">
              <span className="font-bold text-[#15370D]">{currentSubject?.code}: {currentSubject?.title}</span>
              <span>•</span>
              <span className="text-gray-700">{currentUnit?.unit_number}</span>
            </div>
            <p className="text-gray-900 font-semibold">
              Topic: {availableTopics.find(t => t.id === selectedTopicId)?.title}
            </p>
            <p className="text-[11px] text-gray-500">
              Lecture Date: {teachingDate} • Section: {student?.section} • Category: {category}
            </p>
          </div>

          {/* Text Area */}
          <div>
            <label className="block text-xs font-bold text-gray-800 uppercase tracking-wider mb-1.5 flex items-center justify-between">
              <span>Describe Your Academic Doubt *</span>
              <span className="text-[11px] font-normal text-gray-500">
                {questionText.length} characters
              </span>
            </label>
            <textarea
              rows={6}
              value={questionText}
              onChange={(e) => setQuestionText(e.target.value)}
              placeholder="e.g. In Round Robin CPU scheduling, why does the operating system divide time into a fixed quantum slice? What happens to throughput if the quantum is set too low?"
              className="w-full p-4 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] focus:bg-white rounded-2xl text-xs sm:text-sm font-medium outline-hidden leading-relaxed transition"
              required
            />
            <p className="text-[11px] text-gray-500 mt-1">
              Be as specific as possible. Include problem constraints, compiler errors, or specific concepts.
            </p>
          </div>

          {/* Actions */}
          <div className="pt-4 border-t border-gray-100 flex items-center justify-between">
            <button
              type="button"
              onClick={() => setQuestionText('')}
              className="px-4 py-2 text-xs font-semibold text-gray-600 hover:text-black flex items-center gap-1.5 transition"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Clear</span>
            </button>

            <button
              type="submit"
              disabled={checkingDuplicates || !questionText.trim()}
              className="px-6 py-2.5 rounded-xl bg-[#15370D] text-[#FCF9EA] font-extrabold text-xs sm:text-sm hover:bg-[#15370D]/90 shadow-md flex items-center gap-2 transition disabled:opacity-50"
            >
              {checkingDuplicates ? (
                <>
                  <Sparkles className="w-4 h-4 text-[#F2842F] animate-spin" />
                  <span>Checking Duplicate Intelligence...</span>
                </>
              ) : (
                <>
                  <span>Next: Check &amp; Submit</span>
                  <ArrowRight className="w-4 h-4 text-[#F2842F]" />
                </>
              )}
            </button>
          </div>

        </form>
      )}

      {/* STEP 3: DUPLICATE QUESTION COMPARISON SCREEN (Section 8 Requirement) */}
      {!successInfo && step === 3 && duplicateResult?.matched_doubt && (
        <div className="p-6 sm:p-8 rounded-3xl bg-white border-2 border-[#F2842F] shadow-xl space-y-6 animate-fade-in">
          
          <div className="p-4 rounded-2xl bg-amber-50 border border-amber-200 flex items-start gap-3">
            <div className="p-2 rounded-xl bg-[#F2842F] text-[#000000] shrink-0">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-black text-gray-900">
                A similar doubt has already been submitted!
              </h2>
              <p className="text-xs text-gray-700 mt-0.5 leading-relaxed">
                Our Smart Doubt Intelligence Engine detected that a classmate in your section asked essentially the same question (Match confidence: {Math.round(duplicateResult.confidence * 100)}%).
              </p>
            </div>
          </div>

          {/* Side-by-Side or Stacked Comparison */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            
            {/* Matched Original Doubt */}
            <div className="p-4 rounded-2xl bg-[#FAF6E4] border border-[#D8D2BA] space-y-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-[#15370D] block">
                Existing Doubt Submitted by Classmate
              </span>
              <p className="text-xs font-bold text-gray-900">
                "{duplicateResult.matched_doubt.question_text}"
              </p>
              <div className="pt-2 border-t border-gray-200 text-[11px] text-gray-600 space-y-1">
                <p>Submitted: {new Date(duplicateResult.matched_doubt.created_at).toLocaleDateString([], { month: 'short', day: 'numeric' })}</p>
                <p>Status: <StatusBadge status={duplicateResult.matched_doubt.status} size="sm" /></p>
                <p className="font-semibold text-[#F2842F]">
                  👥 {duplicateResult.matched_doubt.duplicate_count} students already have this doubt
                </p>
              </div>
            </div>

            {/* Your Question */}
            <div className="p-4 rounded-2xl bg-white border border-[#D8D2BA] space-y-2">
              <span className="text-[10px] font-bold uppercase tracking-wider text-gray-500 block">
                Your Submitted Question
              </span>
              <p className="text-xs font-bold text-gray-900">
                "{questionText}"
              </p>
              <div className="pt-2 border-t border-gray-200 text-[11px] text-gray-600 space-y-1">
                <p>Section: {student?.section}</p>
                <p>Teaching Date: {teachingDate}</p>
                <p>Category: {category}</p>
              </div>
            </div>

          </div>

          {/* Existing Answer Preview if already answered! */}
          {duplicateResult.existing_answer && (
            <div className="p-5 rounded-2xl bg-white border border-[#15370D] space-y-2.5">
              <div className="flex items-center justify-between">
                <span className="text-xs font-extrabold text-[#15370D] flex items-center gap-1.5">
                  {duplicateResult.existing_answer.type === 'faculty' ? (
                    <>
                      <ShieldCheck className="w-4 h-4 text-[#F2842F]" />
                      Official Faculty Answer from {duplicateResult.existing_answer.author}
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-4 h-4 text-[#F2842F]" />
                      Automated Academic AI Answer
                    </>
                  )}
                </span>
                <span className="text-[10px] text-gray-500">
                  {duplicateResult.existing_answer.created_at ? new Date(duplicateResult.existing_answer.created_at).toLocaleDateString() : ''}
                </span>
              </div>

              <div className="p-3.5 rounded-xl bg-[#FAF6E4] text-xs text-gray-800 whitespace-pre-line leading-relaxed border border-[#E5DFC8] max-h-48 overflow-y-auto">
                {duplicateResult.existing_answer.text}
              </div>

              <p className="text-[11px] text-gray-600 italic">
                Does this existing answer resolve your doubt? If yes, click "+1" to save it. If not, you may submit a separate doubt.
              </p>
            </div>
          )}

          {/* Two Distinct Actions (Section 8 Requirement) */}
          <div className="pt-4 border-t border-gray-200 grid grid-cols-1 sm:grid-cols-2 gap-4">
            
            {/* OPTION 1 */}
            <button
              onClick={handleSupportExisting}
              disabled={loading}
              className="p-4 rounded-2xl bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] text-left shadow-md transition group disabled:opacity-50"
            >
              <div className="flex items-center gap-2 mb-1">
                <ThumbsUp className="w-5 h-5 text-[#F2842F] group-hover:scale-110 transition-transform" />
                <span className="font-black text-sm tracking-wide">
                  OPTION 1: +1 – I HAVE THE SAME DOUBT
                </span>
              </div>
              <p className="text-xs text-[#FCF9EA]/80 leading-relaxed">
                Connects your name to this question without creating duplicate notification workload for faculty. You will be alerted the moment an answer is posted.
              </p>
            </button>

            {/* OPTION 2 */}
            <button
              onClick={handleConfirmSeparateDoubt}
              disabled={loading}
              className="p-4 rounded-2xl bg-white hover:bg-gray-50 border-2 border-gray-300 text-left shadow-xs transition disabled:opacity-50"
            >
              <div className="flex items-center gap-2 mb-1">
                <Send className="w-5 h-5 text-gray-700" />
                <span className="font-black text-sm text-gray-900 tracking-wide">
                  OPTION 2: ASK A SEPARATE DOUBT
                </span>
              </div>
              <p className="text-xs text-gray-600 leading-relaxed">
                Confirm that the existing doubt or answer does not address your issue. Enters a new query into the faculty queue with a 3-hour timer.
              </p>
            </button>

          </div>

          <div className="text-center pt-2">
            <button
              type="button"
              onClick={() => setStep(2)}
              className="text-xs font-semibold text-gray-500 hover:text-black underline"
            >
              Back to edit question text
            </button>
          </div>

        </div>
      )}

    </div>
  );
};
