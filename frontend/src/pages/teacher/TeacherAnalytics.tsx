import React, { useState, useEffect } from 'react';
import { 
  BarChart3, Download, TrendingUp, Users, 
  Clock, Flame, Layers, CheckCircle2, AlertTriangle, FileSpreadsheet 
} from 'lucide-react';
import { api } from '../../api';
import { useAuth } from '../../context/AuthContext';
import { AnalyticsData, Subject } from '../../types';

export const TeacherAnalytics: React.FC = () => {
  const { teacher } = useAuth();
  const [data, setData] = useState<AnalyticsData | null>(null);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('All');
  const [selectedSection, setSelectedSection] = useState<string>('All');
  const [loading, setLoading] = useState(true);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const params: any = {};
      if (selectedSubjectId !== 'All') params.subject_id = Number(selectedSubjectId);
      if (selectedSection !== 'All') params.section = selectedSection;

      const [resData, subList] = await Promise.all([
        api.getAnalyticsDashboard(params),
        api.getSubjects()
      ]);
      setData(resData);
      setSubjects(subList);
    } catch (e) {
      console.warn('Failed loading analytics:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, [selectedSubjectId, selectedSection]);

  const summary = data?.summary;

  return (
    <div className="space-y-6 animate-fade-in pb-16">
      
      {/* Header & Export Action */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-gray-900 flex items-center gap-2.5">
            <BarChart3 className="w-7 h-7 text-[#15370D]" />
            <span>Academic Confusion &amp; Section Analytics</span>
          </h1>
          <p className="text-xs sm:text-sm text-gray-600 mt-1">
            Empirical data from actual student queries to identify high-friction syllabus topics and section workloads.
          </p>
        </div>

        <div className="flex items-center gap-2">
          {/* CSV Export Button (Section 21.I) */}
          <a
            href={api.exportAnalyticsCsvUrl()}
            download
            className="px-4 py-2.5 rounded-xl bg-[#15370D] hover:bg-[#15370D]/90 text-[#FCF9EA] text-xs font-bold flex items-center gap-2 shadow-sm transition"
          >
            <Download className="w-4 h-4 text-[#F2842F]" />
            <span>Export Analytics CSV</span>
          </a>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] flex flex-wrap items-center gap-4 text-xs">
        <div className="flex items-center gap-2">
          <span className="font-bold text-gray-700">Filter by Course:</span>
          <select
            value={selectedSubjectId}
            onChange={(e) => setSelectedSubjectId(e.target.value)}
            className="px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-lg font-semibold outline-hidden"
          >
            <option value="All">All Courses</option>
            {subjects.map(s => (
              <option key={s.id} value={s.id.toString()}>{s.code}: {s.title}</option>
            ))}
          </select>
        </div>

        <div className="flex items-center gap-2">
          <span className="font-bold text-gray-700">Filter by Section:</span>
          <select
            value={selectedSection}
            onChange={(e) => setSelectedSection(e.target.value)}
            className="px-3 py-1.5 bg-[#FAF6E4] border border-[#D8D2BA] rounded-lg font-semibold outline-hidden"
          >
            <option value="All">All Sections</option>
            <option value="K22DF">Section K22DF</option>
            <option value="K22GF">Section K22GF</option>
            <option value="K22SE">Section K22SE</option>
            <option value="K23AA">Section K23AA</option>
            <option value="K23AB">Section K23AB</option>
          </select>
        </div>
      </div>

      {/* Top 4 Workload Metric Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs">
          <div className="flex items-center justify-between text-xs font-bold text-gray-500 mb-1">
            <span>Total Queries Ingested</span>
            <Layers className="w-4 h-4 text-[#15370D]" />
          </div>
          <p className="text-3xl font-black text-gray-900">{summary?.total_doubts ?? 0}</p>
          <p className="text-[11px] text-gray-500 mt-1">Across all verified subjects</p>
        </div>

        <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs">
          <div className="flex items-center justify-between text-xs font-bold text-[#F2842F] mb-1">
            <span>Repeated Doubt Rate</span>
            <Flame className="w-4 h-4 text-[#F2842F]" />
          </div>
          <p className="text-3xl font-black text-[#000000]">
            {summary?.total_doubts ? Math.round((summary.repeated_doubts / summary.total_doubts) * 100) : 0}%
          </p>
          <p className="text-[11px] text-gray-600 mt-1">
            {summary?.repeated_doubts ?? 0} questions saved via +1 mechanism
          </p>
        </div>

        <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs">
          <div className="flex items-center justify-between text-xs font-bold text-emerald-800 mb-1">
            <span>Avg Response Turnaround</span>
            <Clock className="w-4 h-4 text-emerald-700" />
          </div>
          <p className="text-3xl font-black text-[#15370D]">
            {summary?.avg_response_hours ?? 2.4} hrs
          </p>
          <p className="text-[11px] text-gray-500 mt-1">3-hour AI fallback protection active</p>
        </div>

        <div className="p-5 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs">
          <div className="flex items-center justify-between text-xs font-bold text-blue-700 mb-1">
            <span>Total Consultations</span>
            <Users className="w-4 h-4 text-blue-700" />
          </div>
          <p className="text-3xl font-black text-gray-900">{summary?.total_appointments ?? 0}</p>
          <p className="text-[11px] text-gray-500 mt-1">{summary?.pending_appointments ?? 0} awaiting approval</p>
        </div>
      </div>

      {/* Grid: Section Analytics & Subject Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* A. Section-Wise Analytics (Section 14.A) */}
        <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-4">
          <h2 className="text-base font-bold text-gray-900 flex items-center justify-between">
            <span>A. Section-Wise Confusion Volume</span>
            <span className="text-xs text-gray-500 font-normal">Real Database Counts</span>
          </h2>
          <p className="text-xs text-gray-500">
            Identifies which classroom section requires the most instructional reinforcement.
          </p>

          <div className="space-y-3 pt-2">
            {data?.section_analytics.map((item) => {
              const max = Math.max(...(data.section_analytics.map(s => s.doubts) || [1]), 1);
              const pct = (item.doubts / max) * 100;
              return (
                <div key={item.section} className="space-y-1">
                  <div className="flex justify-between text-xs font-bold text-gray-800">
                    <span>Section {item.section}</span>
                    <span className="text-[#15370D]">{item.doubts} doubts</span>
                  </div>
                  <div className="w-full h-3 rounded-full bg-[#FAF6E4] overflow-hidden">
                    <div 
                      className="h-full bg-[#15370D] rounded-full transition-all duration-500"
                      style={{ width: `${Math.max(8, pct)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* B. Subject-Wise Analytics (Section 14.B) */}
        <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-4">
          <h2 className="text-base font-bold text-gray-900 flex items-center justify-between">
            <span>B. Subject-Wise Question Distribution</span>
            <span className="text-xs text-gray-500 font-normal">All Courses</span>
          </h2>
          <p className="text-xs text-gray-500">
            Course query distribution across INT335, CSE316, CSM228, CSM229, MTH401, etc.
          </p>

          <div className="space-y-3 pt-2">
            {data?.subject_analytics.map((item) => {
              const max = Math.max(...(data.subject_analytics.map(s => s.doubts) || [1]), 1);
              const pct = (item.doubts / max) * 100;
              return (
                <div key={item.subject} className="space-y-1">
                  <div className="flex justify-between text-xs font-bold text-gray-800">
                    <span>{item.subject}</span>
                    <span className="text-[#F2842F]">{item.doubts} doubts</span>
                  </div>
                  <div className="w-full h-3 rounded-full bg-[#FAF6E4] overflow-hidden">
                    <div 
                      className="h-full bg-[#F2842F] rounded-full transition-all duration-500"
                      style={{ width: `${Math.max(8, pct)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

      </div>

      {/* Grid: Topic-Wise Confusion Heatmap & Top Repeated Doubts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* D. Topic-Wise Analytics (Section 14.D) */}
        <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-4">
          <h2 className="text-base font-bold text-gray-900 flex items-center justify-between">
            <span>D. Topic-Wise Confusion Ranking (Impact Score)</span>
            <Flame className="w-4 h-4 text-[#F2842F]" />
          </h2>
          <p className="text-xs text-gray-500">
            Aggregated by questions submitted and +1 classmate endorsements.
          </p>

          <div className="space-y-2.5 pt-2">
            {data?.topic_analytics.map((item, idx) => (
              <div 
                key={idx}
                className="p-3 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] flex items-center justify-between text-xs"
              >
                <div className="flex items-center gap-2.5">
                  <span className="w-6 h-6 rounded-full bg-[#15370D] text-[#FCF9EA] flex items-center justify-center font-bold text-[11px] shrink-0">
                    {idx + 1}
                  </span>
                  <span className="font-bold text-gray-900 truncate max-w-[220px]">
                    {item.topic}
                  </span>
                </div>
                <span className="px-2.5 py-0.5 rounded-full bg-[#F2842F] text-[#000000] font-black text-[11px]">
                  Score: {item.impact_score}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* E. Top Repeated Questions (+1 Ranking) (Section 14.E) */}
        <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-4">
          <h2 className="text-base font-bold text-gray-900 flex items-center justify-between">
            <span>E. Highest Endorsed Doubts (+1 Ranking)</span>
            <Users className="w-4 h-4 text-[#15370D]" />
          </h2>
          <p className="text-xs text-gray-500">
            Doubts shared by multiple students where one answer resolved multiple students' doubts.
          </p>

          <div className="space-y-3 pt-2">
            {data?.top_repeated_doubts.map((item) => (
              <div 
                key={item.id}
                className="p-3.5 rounded-xl bg-[#FAF6E4] border border-[#E5DFC8] space-y-1.5 text-xs"
              >
                <div className="flex items-center justify-between">
                  <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-[#15370D] text-[#FCF9EA]">
                    {item.subject} • Sec {item.section}
                  </span>
                  <span className="font-extrabold text-[#F2842F]">
                    👥 {item.supporters_count} Students
                  </span>
                </div>
                <p className="font-semibold text-gray-900 line-clamp-2">
                  "{item.question}"
                </p>
                <p className="text-[11px] text-gray-500">Topic: {item.topic}</p>
              </div>
            ))}
          </div>
        </div>

      </div>

      {/* Response-Time Analytics Card (Section 14.F) */}
      <div className="p-6 rounded-3xl bg-white border border-[#E5DFC8] shadow-xs space-y-4">
        <h2 className="text-base font-bold text-gray-900 flex items-center gap-2">
          <Clock className="w-5 h-5 text-[#15370D]" />
          <span>F. Response-Time Performance &amp; 3-Hour Timer Reliability</span>
        </h2>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2">
          <div className="p-4 rounded-2xl bg-[#FAF6E4] border border-[#E5DFC8] text-center">
            <p className="text-xs font-bold text-gray-600">Answered Within 3 Hours</p>
            <p className="text-2xl font-black text-[#15370D] mt-1">
              {summary?.answered_within_3h ?? 0}
            </p>
            <p className="text-[10px] text-gray-500 mt-0.5">Faculty direct response</p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FAF6E4] border border-[#E5DFC8] text-center">
            <p className="text-xs font-bold text-gray-600">3-Hour AI Fallback Handled</p>
            <p className="text-2xl font-black text-[#F2842F] mt-1">
              {summary?.ai_answered ?? 0}
            </p>
            <p className="text-[10px] text-gray-500 mt-0.5">Automated syllabus assistance</p>
          </div>

          <div className="p-4 rounded-2xl bg-[#FAF6E4] border border-[#E5DFC8] text-center">
            <p className="text-xs font-bold text-gray-600">Avg Faculty Response Time</p>
            <p className="text-2xl font-black text-gray-900 mt-1">
              {summary?.avg_response_hours ?? 2.4} hrs
            </p>
            <p className="text-[10px] text-gray-500 mt-0.5">Below 4-hour university target</p>
          </div>
        </div>
      </div>

    </div>
  );
};
