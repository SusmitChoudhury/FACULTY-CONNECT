import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { 
  MessageSquare, Search, Filter, Sparkles, CheckCircle2, 
  Send, X, User, Clock, AlertTriangle, Layers, ThumbsUp, 
  Flame, Check, Edit3, ArrowRight, ShieldCheck, Loader2 
} from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { Doubt, Subject } from '../../types';
import { StatusBadge } from '../../components/StatusBadge';

export const TeacherDoubtManagement: React.FC = () => {
  const { teacher } = useAuth();
  const [searchParams] = useSearchParams();

  const [doubts, setDoubts] = useState<Doubt[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [activeTab, setActiveTab] = useState<'all' | 'pending' | 'repeated' | 'ai' | 'answered'>('all');
  
  // Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [sectionFilter, setSectionFilter] = useState('All');
  const [subjectFilter, setSubjectFilter] = useState('All');
  const [statusFilter, setStatusFilter] = useState('All');

  // Selected Doubt for Detailed Answering Drawer / Modal
  const [selectedDoubt, setSelectedDoubt] = useState<Doubt | null>(null);
  const [answerDraft, setAnswerDraft] = useState('');
  const [isSubmittingAnswer, setIsSubmittingAnswer] = useState(false);
  const [actionSuccess, setActionSuccess] = useState('');
  const [actionError, setActionError] = useState('');

  // AI Quality Feedback State
  const [aiQuality, setAiQuality] = useState<'Correct' | 'Needs Correction' | 'Incorrect' | 'Requires Additional Explanation'>('Correct');
  const [aiQualityNotes, setAiQualityNotes] = useState('');
  const [submittingQuality, setSubmittingQuality] = useState(false);
  const [isGeneratingAi, setIsGeneratingAi] = useState(false);
  const [quickAiLoadingId, setQuickAiLoadingId] = useState<number | null>(null);

  // Initialize
  const loadData = async () => {
    try {
      const [doubtsData, subjectsData] = await Promise.all([
        api.getDoubts(),
        api.getSubjects()
      ]);
      setDoubts(doubtsData);
      setSubjects(subjectsData);
    } catch (e) {
      console.warn('Failed loading teacher doubts:', e);
    }
  };

  useEffect(() => {
    loadData();

    // Check tab query param
    const qTab = searchParams.get('tab');
    if (qTab === 'pending') setActiveTab('pending');
    else if (qTab === 'repeated') setActiveTab('repeated');
    else if (qTab === 'ai') setActiveTab('ai');
    else if (qTab === 'answered') setActiveTab('answered');
  }, [searchParams]);

  // Open doubt modal
  const handleOpenDoubt = (d: Doubt) => {
    setSelectedDoubt(d);
    setAnswerDraft(d.faculty_answers && d.faculty_answers.length > 0 ? d.faculty_answers[0].answer_text : '');
    setActionSuccess('');
    setActionError('');
  };

  // Publish Faculty Answer
  const handlePublishAnswer = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedDoubt || !teacher) return;
    if (!answerDraft.trim()) {
      setActionError('Answer text cannot be empty.');
      return;
    }

    setIsSubmittingAnswer(true);
    setActionError('');
    try {
      const res = await api.postFacultyAnswer(selectedDoubt.id, {
        teacher_id: teacher.id,
        teacher_name: teacher.name,
        answer_text: answerDraft.trim()
      });

      // Automatically close drawer and mark resolved
      setSelectedDoubt(null);
      setAnswerDraft('');
      setActionSuccess('Official Faculty Answer published! Question marked as Resolved.');
      await loadData();
    } catch (err: any) {
      setActionError(err.message || 'Failed to publish answer.');
    } finally {
      setIsSubmittingAnswer(false);
    }
  };

  // Submit AI Quality Feedback (Section 21.F)
  const handleSubmitAiQuality = async () => {
    if (!selectedDoubt) return;
    setSubmittingQuality(true);
    try {
      await api.submitAiQualityFeedback(selectedDoubt.id, {
        quality_status: aiQuality,
        notes: aiQualityNotes
      });
      setActionSuccess('AI answer quality evaluation recorded.');
      await loadData();
    } catch (err: any) {
      setActionError(err.message || 'Failed recording feedback.');
    } finally {
      setSubmittingQuality(false);
    }
  };

  // Give Answer by AI
  const handleGiveAnsByAi = async (publishImmediately: boolean) => {
    if (!selectedDoubt || !teacher) return;
    setIsGeneratingAi(true);
    setActionError('');
    setActionSuccess('');

    try {
      const res = await api.generateAiAnswer(selectedDoubt.id, {
        publish_immediately: publishImmediately,
        teacher_id: teacher.id,
        teacher_name: teacher.name
      });

      if (publishImmediately) {
        // Automatically close drawer and mark resolved
        setSelectedDoubt(null);
        setAnswerDraft('');
        setActionSuccess(`AI answer successfully published to ${selectedDoubt.student_name}! Question marked as Resolved.`);
        await loadData();
      } else {
        if (res.ai_text) {
          setAnswerDraft(res.ai_text);
          setActionSuccess('Syllabus AI answer inserted into editor below! You can customize and publish.');
        }
      }
    } catch (err: any) {
      setActionError(err.message || 'Failed generating AI answer.');
    } finally {
      setIsGeneratingAi(false);
    }
  };

  // Quick One-Click Give Answer by AI from card list
  const handleQuickAiAnswer = async (doubtId: number) => {
    if (!teacher) return;
    setQuickAiLoadingId(doubtId);
    try {
      await api.generateAiAnswer(doubtId, {
        publish_immediately: true,
        teacher_id: teacher.id,
        teacher_name: teacher.name
      });
      await loadData();
    } catch (err: any) {
      alert(err.message || 'Failed generating AI answer.');
    } finally {
      setQuickAiLoadingId(null);
    }
  };

  // Update Status
  const handleStatusChange = async (newStatus: string) => {
    if (!selectedDoubt) return;
    try {
      const res = await api.updateDoubtStatus(selectedDoubt.id, newStatus);
      setSelectedDoubt(res.doubt);
      setActionSuccess(`Status changed to ${newStatus}`);
      await loadData();
    } catch (err: any) {
      setActionError(err.message || 'Failed updating status.');
    }
  };

  // Filtering Logic
  const filteredDoubts = doubts.filter(d => {
    // Tab filter
    if (activeTab === 'pending' && !['Pending', 'Under Review'].includes(d.status)) return false;
    if (activeTab === 'repeated' && d.duplicate_count <= 1) return false;
    if (activeTab === 'ai' && (!d.ai_responses || d.ai_responses.length === 0)) return false;
    if (activeTab === 'answered' && (!d.faculty_answers || d.faculty_answers.length === 0)) return false;

    // Dropdown filters
    if (sectionFilter !== 'All' && d.section !== sectionFilter) return false;
    if (subjectFilter !== 'All' && d.subject_code !== subjectFilter) return false;
    if (statusFilter !== 'All' && d.status !== statusFilter) return false;

    // Search query
    if (searchQuery.trim()) {
      const q = searchQuery.toLowerCase();
      return (
        d.question_text.toLowerCase().includes(q) ||
        d.student_name.toLowerCase().includes(q) ||
        d.topic_title?.toLowerCase().includes(q)
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
            <MessageSquare className="w-7 h-7 text-[#15370D]" />
            <span>Academic Doubt &amp; Answer Console</span>
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Resolve queries, identify repeated confusion patterns (+1), and review syllabus-grounded AI responses.
          </p>
        </div>

        {/* Search Bar */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by student, topic, keyword..."
            className="w-full pl-10 pr-4 py-2 bg-white border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs font-medium outline-hidden shadow-xs transition"
          />
        </div>
      </div>

      {/* Tabs Row */}
      <div className="flex gap-2 overflow-x-auto pb-1 scrollbar-none">
        <button
          onClick={() => setActiveTab('all')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold whitespace-nowrap transition ${
            activeTab === 'all'
              ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
              : 'bg-white text-gray-700 hover:bg-[#EFEAD3] border border-[#E5DFC8]'
          }`}
        >
          All Doubts ({doubts.length})
        </button>

        <button
          onClick={() => setActiveTab('pending')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold whitespace-nowrap transition ${
            activeTab === 'pending'
              ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
              : 'bg-white text-gray-700 hover:bg-[#EFEAD3] border border-[#E5DFC8]'
          }`}
        >
          Pending Queue ({doubts.filter(d => ['Pending', 'Under Review'].includes(d.status)).length})
        </button>

        <button
          onClick={() => setActiveTab('repeated')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold whitespace-nowrap transition flex items-center gap-1.5 ${
            activeTab === 'repeated'
              ? 'bg-[#F2842F] text-[#000000] shadow-xs'
              : 'bg-white text-gray-700 hover:bg-[#EFEAD3] border border-[#E5DFC8]'
          }`}
        >
          <Flame className="w-3.5 h-3.5" />
          <span>Repeated (+1) ({doubts.filter(d => d.duplicate_count > 1).length})</span>
        </button>

        <button
          onClick={() => setActiveTab('ai')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold whitespace-nowrap transition flex items-center gap-1.5 ${
            activeTab === 'ai'
              ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
              : 'bg-white text-gray-700 hover:bg-[#EFEAD3] border border-[#E5DFC8]'
          }`}
        >
          <Sparkles className="w-3.5 h-3.5 text-[#F2842F]" />
          <span>3-Hour AI Answered ({doubts.filter(d => d.ai_responses && d.ai_responses.length > 0).length})</span>
        </button>

        <button
          onClick={() => setActiveTab('answered')}
          className={`px-4 py-2 rounded-2xl text-xs font-bold whitespace-nowrap transition ${
            activeTab === 'answered'
              ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
              : 'bg-white text-gray-700 hover:bg-[#EFEAD3] border border-[#E5DFC8]'
          }`}
        >
          Faculty Answered ({doubts.filter(d => d.faculty_answers && d.faculty_answers.length > 0).length})
        </button>
      </div>

      {/* Filter Bar */}
      <div className="p-3.5 rounded-2xl bg-white border border-[#E5DFC8] flex flex-wrap items-center gap-3 text-xs">
        <span className="font-bold text-gray-500 uppercase tracking-wider text-[10px] flex items-center gap-1">
          <Filter className="w-3.5 h-3.5" />
          Filters:
        </span>

        {/* Section Filter */}
        <select
          value={sectionFilter}
          onChange={(e) => setSectionFilter(e.target.value)}
          className="px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-lg font-medium outline-hidden"
        >
          <option value="All">All Sections</option>
          <option value="K22DF">Section K22DF</option>
          <option value="K22GF">Section K22GF</option>
          <option value="K22SE">Section K22SE</option>
          <option value="K23AA">Section K23AA</option>
        </select>

        {/* Subject Filter */}
        <select
          value={subjectFilter}
          onChange={(e) => setSubjectFilter(e.target.value)}
          className="px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-lg font-medium outline-hidden"
        >
          <option value="All">All Subjects</option>
          {subjects.map(s => (
            <option key={s.id} value={s.code}>{s.code}: {s.title}</option>
          ))}
        </select>

        {/* Status Filter */}
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-lg font-medium outline-hidden"
        >
          <option value="All">All Statuses</option>
          <option value="Pending">Pending</option>
          <option value="Under Review">Under Review</option>
          <option value="AI Answered">AI Answered</option>
          <option value="Faculty Answered">Faculty Answered</option>
          <option value="Faculty Verified">Faculty Verified</option>
          <option value="Resolved">Resolved</option>
        </select>

        {(sectionFilter !== 'All' || subjectFilter !== 'All' || statusFilter !== 'All' || searchQuery) && (
          <button
            onClick={() => {
              setSectionFilter('All');
              setSubjectFilter('All');
              setStatusFilter('All');
              setSearchQuery('');
            }}
            className="text-[11px] font-bold text-red-600 hover:underline ml-auto"
          >
            Reset Filters
          </button>
        )}
      </div>

      {/* Doubts Table / Card List */}
      <div className="space-y-3">
        {filteredDoubts.map((doubt) => {
          const isHighVolume = doubt.duplicate_count >= 3;
          return (
            <div
              key={doubt.id}
              onClick={() => handleOpenDoubt(doubt)}
              className={`p-5 rounded-3xl bg-white border cursor-pointer transition flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-xs hover:shadow-md ${
                isHighVolume 
                  ? 'border-2 border-[#F2842F] bg-amber-50/20' 
                  : 'border-[#E5DFC8] hover:border-[#15370D]'
              }`}
            >
              <div className="space-y-2 flex-1">
                <div className="flex items-center gap-2 flex-wrap">
                  <span className="px-2 py-0.5 rounded text-[11px] font-black bg-[#15370D] text-[#FCF9EA]">
                    {doubt.subject_code}
                  </span>
                  <span className="text-xs font-bold text-gray-800">
                    Section {doubt.section}
                  </span>
                  <span className="text-gray-400">•</span>
                  <span className="text-xs text-gray-600 truncate max-w-[200px]">
                    {doubt.unit_title} - {doubt.topic_title}
                  </span>
                  <StatusBadge status={doubt.status} size="sm" />
                </div>

                <h3 className="text-sm font-bold text-gray-900 leading-snug">
                  "{doubt.question_text}"
                </h3>

                <div className="flex items-center gap-3 text-[11px] text-gray-500 flex-wrap">
                  <span>Student: <strong>{doubt.student_name}</strong></span>
                  <span>Teaching Date: {doubt.teaching_date || 'N/A'}</span>
                  <span>Category: {doubt.category}</span>
                  {doubt.duplicate_count > 1 && (
                    <span className="font-extrabold text-[#F2842F] flex items-center gap-1">
                      <Flame className="w-3.5 h-3.5" />
                      +{doubt.duplicate_count - 1} Classmates Share This Doubt
                    </span>
                  )}
                </div>
              </div>

              {/* Action Pill */}
              <div className="flex items-center gap-2 shrink-0 md:pl-4 md:border-l border-gray-100 flex-wrap">
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    handleQuickAiAnswer(doubt.id);
                  }}
                  disabled={quickAiLoadingId === doubt.id}
                  className="px-3.5 py-2 bg-[#F2842F] hover:bg-[#d86d1d] text-[#000000] border border-[#d86d1d] rounded-xl text-xs font-black flex items-center gap-1.5 shadow-sm transition active:scale-95 disabled:opacity-50"
                  title="Synthesize and publish verified AI answer immediately to this student doubt"
                >
                  {quickAiLoadingId === doubt.id ? (
                    <>
                      <Loader2 className="w-3.5 h-3.5 animate-spin text-[#000000]" />
                      <span>Generating AI...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles className="w-3.5 h-3.5 text-[#000000]" />
                      <span>Give Ans by AI</span>
                    </>
                  )}
                </button>
                <button
                  onClick={(e) => { e.stopPropagation(); handleOpenDoubt(doubt); }}
                  className="px-4 py-2 bg-[#15370D] text-[#FCF9EA] hover:bg-[#15370D]/90 rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-sm transition active:scale-95"
                >
                  <Edit3 className="w-3.5 h-3.5 text-[#F2842F]" />
                  <span>{doubt.faculty_answers && doubt.faculty_answers.length > 0 ? 'Edit Answer' : 'Answer Question'}</span>
                </button>
              </div>
            </div>
          );
        })}

        {filteredDoubts.length === 0 && (
          <div className="p-12 text-center bg-white rounded-3xl border border-dashed border-[#D8D2BA]">
            <MessageSquare className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
            <p className="font-bold text-gray-800 text-sm">No doubts found matching current filter</p>
            <p className="text-xs text-gray-500 mt-1">Adjust filters or select another subject.</p>
          </div>
        )}
      </div>

      {/* FULL QUESTION DETAIL & ANSWERING MODAL (Section 13) */}
      {selectedDoubt && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
          <div className="w-full max-w-3xl bg-[#FCF9EA] border border-[#D8D2BA] rounded-3xl shadow-2xl overflow-hidden flex flex-col max-h-[92vh] animate-fade-in">
            
            {/* Modal Header */}
            <div className="px-6 py-4 bg-[#15370D] text-[#FCF9EA] flex items-center justify-between">
              <div>
                <span className="text-[10px] font-bold text-[#F2842F] uppercase tracking-wider">
                  {selectedDoubt.subject_code}: {selectedDoubt.subject_title}
                </span>
                <h2 className="text-base font-bold text-white">
                  {selectedDoubt.unit_title} • {selectedDoubt.topic_title}
                </h2>
              </div>
              <button
                onClick={() => setSelectedDoubt(null)}
                className="p-1.5 rounded-lg text-white/80 hover:text-white hover:bg-white/10 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Scrollable Body */}
            <div className="p-6 overflow-y-auto space-y-6 flex-1">
              
              {actionSuccess && (
                <div className="p-3.5 rounded-xl bg-emerald-50 border border-emerald-300 text-xs font-bold text-emerald-900 flex items-center gap-2">
                  <Check className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>{actionSuccess}</span>
                </div>
              )}

              {actionError && (
                <div className="p-3.5 rounded-xl bg-red-50 border border-red-300 text-xs font-bold text-red-900 flex items-center gap-2">
                  <AlertTriangle className="w-4 h-4 text-red-600 shrink-0" />
                  <span>{actionError}</span>
                </div>
              )}

              {/* Student Query Details Card */}
              <div className="p-5 rounded-2xl bg-white border border-[#E5DFC8] shadow-xs space-y-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <User className="w-4 h-4 text-[#15370D]" />
                    <span className="text-xs font-bold text-gray-900">
                      {selectedDoubt.student_name} (Section {selectedDoubt.section})
                    </span>
                  </div>
                  <StatusBadge status={selectedDoubt.status} />
                </div>

                <div className="p-4 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8]">
                  <p className="text-sm font-bold text-gray-900 leading-relaxed">
                    "{selectedDoubt.question_text}"
                  </p>
                </div>

                <div className="flex items-center justify-between text-xs text-gray-500 pt-1">
                  <span>Lecture Date: {selectedDoubt.teaching_date || 'N/A'}</span>
                  <span>Category: {selectedDoubt.category}</span>
                  <span className="font-extrabold text-[#F2842F]">
                    👥 Total Supporters (+1): {selectedDoubt.duplicate_count} students
                  </span>
                </div>

                {/* Supporters List */}
                {selectedDoubt.supporters && selectedDoubt.supporters.length > 1 && (
                  <div className="pt-2 border-t border-gray-100">
                    <p className="text-[11px] font-bold text-gray-500 mb-1">Students sharing this query:</p>
                    <div className="flex flex-wrap gap-1.5">
                      {selectedDoubt.supporters.map((sup, idx) => (
                        <span key={idx} className="px-2 py-0.5 rounded text-[10px] font-semibold bg-gray-100 text-gray-700">
                          {sup.student_name} ({sup.student_section})
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* AI Generated Answer Review (Section 10 & 21.F) */}
              {selectedDoubt.ai_responses && selectedDoubt.ai_responses.length > 0 && (
                <div className="p-5 rounded-2xl bg-white border-2 border-[#F2842F] shadow-xs space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-black text-gray-900 flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4 text-[#F2842F]" />
                      3-Hour Automated AI Response ({selectedDoubt.ai_responses[0].model_name})
                    </span>
                    <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#15370D]/10 font-bold text-[#15370D]">
                      Quality: {selectedDoubt.ai_responses[0].faculty_quality_status}
                    </span>
                  </div>

                  <div className="p-4 rounded-xl bg-[#FAF6E4] text-xs sm:text-sm text-gray-800 leading-relaxed whitespace-pre-line border border-[#E5DFC8] max-h-48 overflow-y-auto">
                    {selectedDoubt.ai_responses[0].response_text}
                  </div>

                  {/* AI Quality Control Controls (Section 21.F) */}
                  <div className="pt-3 border-t border-gray-100 space-y-2">
                    <p className="text-[11px] font-bold text-gray-700">
                      Faculty Quality Review for AI Answer:
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {(['Correct', 'Needs Correction', 'Incorrect', 'Requires Additional Explanation'] as const).map((q) => (
                        <button
                          key={q}
                          type="button"
                          onClick={() => setAiQuality(q)}
                          className={`px-2.5 py-1 rounded-lg text-xs font-semibold transition ${
                            aiQuality === q
                              ? 'bg-[#15370D] text-[#FCF9EA]'
                              : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                          }`}
                        >
                          {q}
                        </button>
                      ))}
                    </div>

                    <div className="flex gap-2 pt-1">
                      <input
                        type="text"
                        value={aiQualityNotes}
                        onChange={(e) => setAiQualityNotes(e.target.value)}
                        placeholder="Add faculty feedback note on this AI explanation..."
                        className="flex-1 px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-lg text-xs outline-hidden"
                      />
                      <button
                        type="button"
                        onClick={handleSubmitAiQuality}
                        disabled={submittingQuality}
                        className="px-3 py-1.5 bg-[#15370D] text-[#FCF9EA] text-xs font-bold rounded-lg hover:bg-[#15370D]/90 disabled:opacity-50"
                      >
                        Save Evaluation
                      </button>
                    </div>
                  </div>
                </div>
              )}

              {/* Rich Faculty Answering Form */}
              <form onSubmit={handlePublishAnswer} className="p-5 rounded-2xl bg-white border border-[#15370D] shadow-xs space-y-3.5">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-extrabold text-[#15370D] flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-[#F2842F]" />
                    <span>Official Faculty Answer (Published by {teacher?.name})</span>
                  </h3>
                  <span className="text-[11px] text-gray-500">Supports Markdown &amp; Math</span>
                </div>

                {/* AI Assistant Quick Generator Banner */}
                <div className="p-3.5 rounded-xl bg-[#FAF6E4] border-2 border-[#F2842F] flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-xs">
                  <div>
                    <h4 className="text-xs font-black text-gray-900 flex items-center gap-1.5">
                      <Sparkles className="w-4 h-4 text-[#F2842F]" />
                      <span>AI Academic Answer Assistant</span>
                    </h4>
                    <p className="text-[11px] text-gray-700 mt-0.5">
                      Auto-generate syllabus-grounded answer directly into this editor to review, or publish immediately.
                    </p>
                  </div>

                  <div className="flex items-center gap-2 flex-wrap">
                    <button
                      type="button"
                      onClick={() => handleGiveAnsByAi(false)}
                      disabled={isGeneratingAi}
                      className="px-3.5 py-1.5 bg-white hover:bg-gray-100 border border-gray-400 text-gray-900 text-xs font-bold rounded-lg shadow-xs flex items-center gap-1.5 transition disabled:opacity-50"
                      title="Generates curriculum explanation and fills it into the editor below for review or customization"
                    >
                      <Edit3 className="w-3.5 h-3.5 text-[#15370D]" />
                      <span>{isGeneratingAi ? 'Writing Answer...' : '✨ Auto-Fill with AI'}</span>
                    </button>

                    <button
                      type="button"
                      onClick={() => handleGiveAnsByAi(true)}
                      disabled={isGeneratingAi}
                      className="px-3.5 py-1.5 bg-[#F2842F] hover:bg-[#d86d1d] text-[#000000] text-xs font-black rounded-lg shadow-xs flex items-center gap-1.5 transition disabled:opacity-50"
                      title="Immediately publishes verified AI answer to student doubt and delivers notifications"
                    >
                      <Sparkles className="w-3.5 h-3.5 text-[#000000]" />
                      <span>{isGeneratingAi ? 'Publishing AI Answer...' : 'Give Ans by AI (Publish)'}</span>
                    </button>
                  </div>
                </div>

                <textarea
                  rows={6}
                  value={answerDraft}
                  onChange={(e) => setAnswerDraft(e.target.value)}
                  placeholder="Type the authoritative explanation, key textbook references, or problem-solving steps here (or click '✨ Auto-Fill with AI' above)..."
                  className="w-full p-4 bg-[#FAF6E4] border border-[#D8D2BA] focus:border-[#15370D] focus:bg-white rounded-xl text-xs sm:text-sm font-medium outline-hidden leading-relaxed"
                  required
                />

                <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                  <div className="flex items-center gap-2">
                    <span className="text-[11px] font-bold text-gray-500">Quick Status:</span>
                    <button
                      type="button"
                      onClick={() => handleStatusChange('Resolved')}
                      className="px-2.5 py-1 rounded bg-emerald-100 hover:bg-emerald-200 text-emerald-900 font-bold text-[11px]"
                    >
                      Mark Resolved
                    </button>
                    <button
                      type="button"
                      onClick={() => handleStatusChange('Escalated')}
                      className="px-2.5 py-1 rounded bg-red-100 hover:bg-red-200 text-red-900 font-bold text-[11px]"
                    >
                      Escalate
                    </button>
                  </div>

                  <div className="flex items-center gap-2.5">
                    <button
                      type="button"
                      onClick={() => handleGiveAnsByAi(true)}
                      disabled={isGeneratingAi}
                      className="px-5 py-2.5 bg-[#F2842F] hover:bg-[#d86d1d] text-[#000000] font-black rounded-xl text-xs sm:text-sm flex items-center gap-2 shadow-sm transition active:scale-95 disabled:opacity-50"
                      title="Instantly generate academic AI response and publish to student"
                    >
                      {isGeneratingAi ? (
                        <>
                          <Loader2 className="w-4 h-4 animate-spin text-[#000000]" />
                          <span>Generating AI...</span>
                        </>
                      ) : (
                        <>
                          <Sparkles className="w-4 h-4 text-[#000000]" />
                          <span>Give Ans by AI</span>
                        </>
                      )}
                    </button>

                    <button
                      type="submit"
                      disabled={isSubmittingAnswer}
                      className="px-6 py-2.5 bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] font-extrabold rounded-xl text-xs sm:text-sm flex items-center gap-2 shadow-md transition active:scale-95 disabled:opacity-50"
                    >
                      <Send className="w-4 h-4 text-[#F2842F]" />
                      <span>{isSubmittingAnswer ? 'Publishing...' : 'Publish Official Answer'}</span>
                    </button>
                  </div>
                </div>
              </form>

            </div>

            {/* Modal Footer */}
            <div className="px-6 py-3 bg-[#F4EFCF] border-t border-[#D8D2BA] text-right">
              <button
                onClick={() => setSelectedDoubt(null)}
                className="px-5 py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-xl text-xs font-bold transition"
              >
                Close Drawer
              </button>
            </div>

          </div>
        </div>
      )}

    </div>
  );
};
