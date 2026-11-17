import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  BookOpen, Search, ChevronRight, ChevronDown, 
  HelpCircle, Award, CheckCircle2, FileText, Layers 
} from 'lucide-react';
import { api } from '../../api';
import { Subject } from '../../types';

export const SubjectExplorer: React.FC = () => {
  const navigate = useNavigate();
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<Subject | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [expandedUnit, setExpandedUnit] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadSubjects = async () => {
      try {
        setLoading(true);
        const data = await api.getSubjects();
        setSubjects(data);
        if (data.length > 0) {
          // Default to INT335 Design Thinking
          const int335 = data.find(s => s.code === 'INT335') || data[0];
          const fullSubject = await api.getSubjectDetails(int335.id);
          setSelectedSubject(fullSubject);
          if (fullSubject.units.length > 0) {
            setExpandedUnit(fullSubject.units[0].id);
          }
        }
      } catch (e) {
        console.warn('Failed loading subjects:', e);
      } finally {
        setLoading(false);
      }
    };
    loadSubjects();
  }, []);

  const handleSelectSubject = async (sub: Subject) => {
    try {
      const full = await api.getSubjectDetails(sub.id);
      setSelectedSubject(full);
      setSearchQuery('');
      setSearchResults([]);
      if (full.units.length > 0) {
        setExpandedUnit(full.units[0].id);
      }
    } catch (e) {
      console.warn('Failed to load full subject details:', e);
    }
  };

  const handleSearch = async (query: string) => {
    setSearchQuery(query);
    if (!query.trim()) {
      setSearchResults([]);
      return;
    }
    try {
      const res = await api.searchSyllabus(query.trim());
      setSearchResults(res);
    } catch {
      // ignore
    }
  };

  const handleAskDoubtOnTopic = (subjectId: number, unitId: number, topicId: number) => {
    navigate(`/student/ask?subject=${subjectId}&unit=${unitId}&topic=${topicId}`);
  };

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
            <BookOpen className="w-7 h-7 text-[#15370D]" />
            <span>Official Syllabus & Subject Explorer</span>
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Grounded in the verified Lovely Professional University course curriculum.
          </p>
        </div>

        {/* Global Syllabus Search */}
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-gray-400 absolute left-3.5 top-3" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => handleSearch(e.target.value)}
            placeholder="Search topics, units, keywords..."
            className="w-full pl-10 pr-4 py-2 bg-white border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs font-medium outline-hidden shadow-xs transition"
          />
          {searchQuery && (
            <button
              onClick={() => { setSearchQuery(''); setSearchResults([]); }}
              className="absolute right-3 top-2.5 text-xs text-gray-400 hover:text-gray-600"
            >
              Clear
            </button>
          )}
        </div>
      </div>

      {/* Search Results Display */}
      {searchQuery && (
        <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] shadow-md space-y-2">
          <p className="text-xs font-bold text-gray-900">
            Search Results for "{searchQuery}" ({searchResults.length} matches found)
          </p>
          <div className="divide-y divide-gray-100 max-h-80 overflow-y-auto">
            {searchResults.map((item, idx) => (
              <div key={idx} className="py-2.5 flex items-start justify-between gap-3">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#15370D] text-[#FCF9EA]">
                      {item.subject_code}
                    </span>
                    <span className="text-xs font-semibold text-gray-700">{item.unit_title}</span>
                  </div>
                  <p className="text-xs font-bold text-gray-900">{item.topic_title}</p>
                  <p className="text-[11px] text-gray-500 line-clamp-1">{item.subtopics}</p>
                </div>
                <button
                  onClick={() => handleAskDoubtOnTopic(item.subject_id, item.unit_id, item.topic_id)}
                  className="px-3 py-1.5 rounded-lg bg-[#F2842F] hover:bg-[#F2842F]/90 text-[#000000] text-xs font-bold shrink-0 transition"
                >
                  Ask Doubt
                </button>
              </div>
            ))}
            {searchResults.length === 0 && (
              <p className="text-xs text-gray-500 py-4 text-center">No matching topics found in the official syllabus.</p>
            )}
          </div>
        </div>
      )}

      {/* Subject Selector Tabs */}
      <div className="flex gap-2 overflow-x-auto pb-2 scrollbar-none">
        {subjects.map((sub) => {
          const isSelected = selectedSubject?.id === sub.id;
          return (
            <button
              key={sub.id}
              onClick={() => handleSelectSubject(sub)}
              className={`px-4 py-2.5 rounded-2xl text-xs font-bold whitespace-nowrap transition flex items-center gap-2 ${
                isSelected
                  ? 'bg-[#15370D] text-[#FCF9EA] shadow-md border border-[#15370D]'
                  : 'bg-white text-gray-700 hover:bg-[#EFEAD3] border border-[#E5DFC8]'
              }`}
            >
              <span className={`px-1.5 py-0.5 rounded text-[10px] ${isSelected ? 'bg-[#F2842F] text-[#000000]' : 'bg-gray-100 text-gray-800'}`}>
                {sub.code}
              </span>
              <span>{sub.title}</span>
            </button>
          );
        })}
      </div>

      {/* Selected Subject Detail View */}
      {selectedSubject && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left 2 Cols: Units & Topics Accordion */}
          <div className="lg:col-span-2 space-y-4">
            <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs">
              <div className="flex items-start justify-between gap-4 mb-4">
                <div>
                  <span className="text-xs font-bold text-[#F2842F] uppercase tracking-wider">
                    Course Code: {selectedSubject.code}
                  </span>
                  <h2 className="text-xl sm:text-2xl font-black text-gray-900 mt-0.5">
                    {selectedSubject.title}
                  </h2>
                  <p className="text-xs text-gray-500 mt-1">
                    Credits: {selectedSubject.credits} • Distribution: {selectedSubject.lecture_hours}
                  </p>
                </div>

                <button
                  onClick={() => navigate(`/student/ask?subject=${selectedSubject.id}`)}
                  className="px-4 py-2 bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] rounded-xl text-xs font-bold flex items-center gap-1.5 shadow-sm transition"
                >
                  <HelpCircle className="w-4 h-4 text-[#F2842F]" />
                  <span>Ask Question</span>
                </button>
              </div>

              {/* Units List */}
              <div className="space-y-3 mt-6">
                <h3 className="text-xs font-bold uppercase tracking-wider text-gray-500 mb-2">
                  Course Units &amp; Learning Modules
                </h3>

                {selectedSubject.units.map((unit) => {
                  const isExpanded = expandedUnit === unit.id;
                  return (
                    <div
                      key={unit.id}
                      className="rounded-2xl border border-[#D8D2BA] bg-[#FAF6E4] overflow-hidden transition"
                    >
                      <button
                        onClick={() => setExpandedUnit(isExpanded ? null : unit.id)}
                        className="w-full p-4 text-left flex items-center justify-between gap-3 hover:bg-[#F2EDD3] transition"
                      >
                        <div className="flex items-center gap-3">
                          <span className="px-2 py-1 rounded bg-[#15370D] text-[#FCF9EA] text-xs font-black shrink-0">
                            {unit.unit_number}
                          </span>
                          <span className="font-bold text-sm text-gray-900">{unit.title}</span>
                        </div>
                        {isExpanded ? (
                          <ChevronDown className="w-4 h-4 text-gray-500 shrink-0" />
                        ) : (
                          <ChevronRight className="w-4 h-4 text-gray-500 shrink-0" />
                        )}
                      </button>

                      {isExpanded && (
                        <div className="p-4 pt-1 bg-white border-t border-[#D8D2BA] divide-y divide-gray-100 space-y-2">
                          {unit.topics.map((topic) => (
                            <div key={topic.id} className="pt-3 first:pt-1 flex items-start justify-between gap-4">
                              <div className="flex-1">
                                <h4 className="text-xs font-bold text-gray-900 flex items-center gap-1.5">
                                  <span className="w-1.5 h-1.5 rounded-full bg-[#F2842F]"></span>
                                  {topic.title}
                                </h4>
                                {topic.subtopics && (
                                  <p className="text-[11px] text-gray-600 mt-1 pl-3 leading-relaxed">
                                    {topic.subtopics}
                                  </p>
                                )}
                              </div>
                              <button
                                onClick={() => handleAskDoubtOnTopic(selectedSubject.id, unit.id, topic.id)}
                                className="px-2.5 py-1 text-[11px] font-bold rounded-lg border border-[#F2842F] text-[#000000] bg-[#F2842F]/10 hover:bg-[#F2842F] hover:text-[#000000] shrink-0 transition"
                              >
                                Ask Doubt
                              </button>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Right Col: Course Outcomes & Textbooks */}
          <div className="space-y-6">
            
            {/* Course Outcomes */}
            <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3">
              <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
                <Award className="w-4 h-4 text-[#15370D]" />
                <span>Course Outcomes (COs)</span>
              </h3>
              <div className="space-y-2.5">
                {selectedSubject.course_outcomes?.map((co) => (
                  <div key={co.id} className="p-2.5 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] text-xs">
                    <span className="font-extrabold text-[#15370D] block mb-0.5">{co.co_code}</span>
                    <p className="text-gray-700 text-[11px] leading-relaxed">{co.description}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* Prescribed Textbooks */}
            <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-3">
              <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
                <FileText className="w-4 h-4 text-[#F2842F]" />
                <span>Prescribed Textbooks</span>
              </h3>
              <div className="p-3 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] text-xs font-mono text-gray-800 whitespace-pre-line leading-relaxed">
                {selectedSubject.textbooks || 'Standard university reference materials.'}
              </div>
            </div>

          </div>

        </div>
      )}

    </div>
  );
};
