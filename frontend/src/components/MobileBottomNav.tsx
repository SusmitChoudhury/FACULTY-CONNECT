import React from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, HelpCircle, MessageSquare, 
  Calendar, BarChart3, Users, BookOpen
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';

export const MobileBottomNav: React.FC = () => {
  const { role } = useAuth();

  if (role === 'guest') return null;

  return (
    <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-40 bg-[#15370D] border-t border-[#F2842F]/30 text-[#FCF9EA] px-2 py-1 safe-area-bottom shadow-lg">
      <div className="flex items-center justify-around h-14">
        {role === 'student' ? (
          <>
            <NavLink
              to="/student/dashboard"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <LayoutDashboard className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Home</span>
            </NavLink>

            <NavLink
              to="/student/ask"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <div className="relative">
                <HelpCircle className="w-5 h-5 mb-0.5" />
                <span className="absolute -top-1 -right-1 w-2 h-2 bg-[#F2842F] rounded-full"></span>
              </div>
              <span className="text-[10px]">Ask Doubt</span>
            </NavLink>

            <NavLink
              to="/student/questions"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <MessageSquare className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Doubts</span>
            </NavLink>

            <NavLink
              to="/student/subjects"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <BookOpen className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Syllabus</span>
            </NavLink>

            <NavLink
              to="/student/availability"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <Calendar className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Book Slot</span>
            </NavLink>
          </>
        ) : (
          <>
            <NavLink
              to="/teacher/dashboard"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <LayoutDashboard className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Home</span>
            </NavLink>

            <NavLink
              to="/teacher/doubts"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <MessageSquare className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Doubts</span>
            </NavLink>

            <NavLink
              to="/teacher/appointments"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <Users className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Bookings</span>
            </NavLink>

            <NavLink
              to="/teacher/availability"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <Calendar className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Schedule</span>
            </NavLink>

            <NavLink
              to="/teacher/analytics"
              className={({ isActive }) =>
                `flex flex-col items-center justify-center w-14 py-1 rounded-md transition ${
                  isActive ? 'text-[#F2842F] font-bold' : 'text-[#FCF9EA]/75 hover:text-[#FCF9EA]'
                }`
              }
            >
              <BarChart3 className="w-5 h-5 mb-0.5" />
              <span className="text-[10px]">Analytics</span>
            </NavLink>
          </>
        )}
      </div>
    </nav>
  );
};
