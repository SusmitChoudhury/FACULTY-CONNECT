import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, HelpCircle, MessageSquare, BookOpen, 
  Calendar, Megaphone, Bookmark, BarChart3, Copy, 
  Sparkles, CheckCircle2, Clock, Users, ArrowRight, BookCheck
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ isOpen, onClose }) => {
  const { role, student, teacher } = useAuth();

  if (role === 'guest') return null;

  const studentLinks = [
    { to: '/student/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/student/ask', label: 'Ask a Doubt', icon: HelpCircle, badge: 'Smart' },
    { to: '/student/questions', label: 'My Questions', icon: MessageSquare },
    { to: '/student/answered', label: 'Answered Doubts', icon: BookCheck, badge: 'Verified' },
    { to: '/student/subjects', label: 'Explore Syllabus', icon: BookOpen },
    { to: '/student/availability', label: 'Faculty Availability', icon: Calendar },
    { to: '/student/bookmarks', label: 'Saved Answers', icon: Bookmark },
    { to: '/student/announcements', label: 'Announcements', icon: Megaphone }
  ];

  const teacherLinks = [
    { to: '/teacher/dashboard', label: 'Overview', icon: LayoutDashboard },
    { to: '/teacher/doubts', label: 'All Doubts', icon: MessageSquare },
    { to: '/teacher/doubts?tab=repeated', label: 'Repeated (+1)', icon: Copy, badge: 'High Impact' },
    { to: '/teacher/doubts?tab=ai', label: 'AI Answered (3h)', icon: Sparkles },
    { to: '/teacher/appointments', label: 'Appointments', icon: Users },
    { to: '/teacher/availability', label: 'My Availability', icon: Calendar },
    { to: '/teacher/analytics', label: 'Advanced Analytics', icon: BarChart3 },
    { to: '/teacher/announcements', label: 'Announcements', icon: Megaphone }
  ];

  const links = role === 'student' ? studentLinks : teacherLinks;

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div 
          onClick={onClose}
          className="fixed inset-0 bg-black/40 z-30 lg:hidden backdrop-blur-xs transition-opacity"
        />
      )}

      {/* Sidebar Surface */}
      <aside 
        className={`fixed lg:sticky top-16 left-0 z-40 h-[calc(100vh-4rem)] w-64 bg-[#FCF9EA] border-r border-[#D8D2BA] flex flex-col justify-between transition-transform duration-200 ease-in-out ${
          isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'
        }`}
      >
        <div className="p-4 overflow-y-auto">
          {/* User Role Card */}
          <div className="mb-4 p-3 rounded-xl bg-white border border-[#E5DFC8] shadow-xs">
            <span className="text-[10px] font-bold uppercase tracking-wider text-[#F2842F]">
              {role === 'student' ? 'Student Portal' : 'Faculty Console'}
            </span>
            <p className="text-sm font-bold text-[#000000] truncate">
              {role === 'student' ? student?.name : teacher?.name}
            </p>
            <p className="text-xs text-gray-600 truncate">
              {role === 'student' ? `Section ${student?.section}` : teacher?.department}
            </p>
          </div>

          {/* Navigation Links */}
          <nav className="space-y-1">
            {links.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink
                  key={link.to}
                  to={link.to}
                  onClick={onClose}
                  className={({ isActive }) =>
                    `flex items-center justify-between px-3 py-2.5 rounded-lg text-sm font-medium transition ${
                      isActive
                        ? 'bg-[#15370D] text-[#FCF9EA] shadow-xs'
                        : 'text-gray-800 hover:bg-[#EFEAD3] hover:text-[#000000]'
                    }`
                  }
                >
                  <div className="flex items-center gap-3">
                    <Icon className="w-4 h-4 shrink-0" />
                    <span>{link.label}</span>
                  </div>
                  {link.badge && (
                    <span className="px-1.5 py-0.2 rounded text-[10px] font-bold bg-[#F2842F] text-[#000000]">
                      {link.badge}
                    </span>
                  )}
                </NavLink>
              );
            })}
          </nav>
        </div>

        {/* Bottom System Status Badge */}
        <div className="p-4 border-t border-[#D8D2BA] bg-[#F7F3E2] text-xs">
          <div className="flex items-center gap-2 mb-1.5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="font-semibold text-gray-900">3-Hour AI Worker Active</span>
          </div>
          <p className="text-[11px] text-gray-600 leading-normal">
            LPU INT335 Project P09: Centralized Academic Assistance.
          </p>
        </div>
      </aside>
    </>
  );
};
