import React from 'react';
import { 
  Clock, CheckCircle, Sparkles, ShieldCheck, 
  AlertTriangle, HelpCircle, FileCheck 
} from 'lucide-react';

interface StatusBadgeProps {
  status: string;
  size?: 'sm' | 'md';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, size = 'md' }) => {
  const isSm = size === 'sm';
  const sizeClasses = isSm ? 'text-xs px-2 py-0.5' : 'text-xs font-medium px-2.5 py-1';

  switch (status) {
    case 'Pending':
      return (
        <span className={`inline-flex items-center gap-1 rounded-full border border-[#F2842F] bg-[#F2842F]/10 text-[#000000] font-semibold ${sizeClasses}`}>
          <Clock className={isSm ? "w-3 h-3 text-[#F2842F]" : "w-3.5 h-3.5 text-[#F2842F]"} />
          Pending
        </span>
      );
    case 'Under Review':
      return (
        <span className={`inline-flex items-center gap-1 rounded-full border border-gray-400 bg-gray-100 text-gray-800 ${sizeClasses}`}>
          <HelpCircle className={isSm ? "w-3 h-3 text-gray-600" : "w-3.5 h-3.5 text-gray-600"} />
          Under Review
        </span>
      );
    case 'AI Answered':
      return (
        <span className={`inline-flex items-center gap-1 rounded-full border border-[#15370D] bg-[#15370D]/10 text-[#15370D] font-bold ${sizeClasses}`}>
          <Sparkles className={isSm ? "w-3 h-3 text-[#F2842F]" : "w-3.5 h-3.5 text-[#F2842F]"} />
          AI Answered
        </span>
      );
    case 'Faculty Answered':
      return (
        <span className={`inline-flex items-center gap-1 rounded-full border border-[#15370D] bg-[#15370D] text-[#FCF9EA] font-semibold ${sizeClasses}`}>
          <CheckCircle className={isSm ? "w-3 h-3 text-[#F2842F]" : "w-3.5 h-3.5 text-[#F2842F]"} />
          Faculty Answered
        </span>
      );
    case 'Faculty Verified':
      return (
        <span className={`inline-flex items-center gap-1 rounded-full border border-[#15370D] bg-[#15370D] text-[#FCF9EA] font-bold ${sizeClasses}`}>
          <ShieldCheck className={isSm ? "w-3 h-3 text-[#F2842F]" : "w-3.5 h-3.5 text-[#F2842F]"} />
          Faculty Verified
        </span>
      );
    case 'Resolved':
      return (
        <span className={`inline-flex items-center gap-1 rounded-full border border-[#15370D]/30 bg-emerald-50 text-emerald-900 ${sizeClasses}`}>
          <FileCheck className={isSm ? "w-3 h-3 text-emerald-700" : "w-3.5 h-3.5 text-emerald-700"} />
          Resolved
        </span>
      );
    case 'Escalated':
      return (
        <span className={`inline-flex items-center gap-1 rounded-full border border-red-500 bg-red-50 text-red-800 ${sizeClasses}`}>
          <AlertTriangle className={isSm ? "w-3 h-3 text-red-600" : "w-3.5 h-3.5 text-red-600"} />
          Escalated
        </span>
      );
    default:
      return (
        <span className={`inline-flex items-center gap-1 rounded-full border border-gray-300 bg-gray-50 text-gray-700 ${sizeClasses}`}>
          {status}
        </span>
      );
  }
};
