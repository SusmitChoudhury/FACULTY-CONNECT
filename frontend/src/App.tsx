import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { Sidebar } from './components/Sidebar';
import { MobileBottomNav } from './components/MobileBottomNav';
import { NotificationModal } from './components/NotificationModal';
import { DemoSwitcher } from './components/DemoSwitcher';
import { Footer } from './components/Footer';

// Pages
import { WelcomeLogin } from './pages/WelcomeLogin';
import { StudentDashboard } from './pages/student/StudentDashboard';
import { AskDoubt } from './pages/student/AskDoubt';
import { MyQuestions } from './pages/student/MyQuestions';
import { SubjectExplorer } from './pages/student/SubjectExplorer';
import { FacultyAvailabilityPage } from './pages/student/FacultyAvailabilityPage';
import { BookmarksPage } from './pages/student/BookmarksPage';
import { AnnouncementsPage } from './pages/student/AnnouncementsPage';
import { AnsweredDoubtsPage } from './pages/student/AnsweredDoubtsPage';

import { TeacherDashboard } from './pages/teacher/TeacherDashboard';
import { TeacherDoubtManagement } from './pages/teacher/TeacherDoubtManagement';
import { TeacherAppointments } from './pages/teacher/TeacherAppointments';
import { TeacherAvailability } from './pages/teacher/TeacherAvailability';
import { TeacherAnalytics } from './pages/teacher/TeacherAnalytics';
import { TeacherAnnouncements } from './pages/teacher/TeacherAnnouncements';

// Protected Route Guards
const StudentRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { role } = useAuth();
  if (role !== 'student') return <Navigate to="/" replace />;
  return <>{children}</>;
};

const TeacherRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { role } = useAuth();
  if (role !== 'teacher') return <Navigate to="/" replace />;
  return <>{children}</>;
};

const MainLayout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { role } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [isNotifOpen, setIsNotifOpen] = useState(false);

  return (
    <div className="min-h-screen flex flex-col bg-[#FCF9EA] text-[#000000]">
      {/* Top Navigation */}
      <Navbar
        onOpenNotifications={() => setIsNotifOpen(true)}
        onToggleSidebar={() => setIsSidebarOpen(!isSidebarOpen)}
        isSidebarOpen={isSidebarOpen}
      />

      <div className="flex-1 flex max-w-7xl w-full mx-auto">
        {/* Desktop / Mobile Collapsible Sidebar */}
        {role !== 'guest' && (
          <Sidebar
            isOpen={isSidebarOpen}
            onClose={() => setIsSidebarOpen(false)}
          />
        )}

        {/* Main Content Viewport */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-full overflow-x-hidden min-h-[calc(100vh-4rem)] pb-20 lg:pb-8">
          {children}
        </main>
      </div>

      {/* Global Academic Project Footer */}
      <Footer />

      {/* Mobile Touch-Friendly Bottom Navigation */}
      <MobileBottomNav />

      {/* Notification Center Modal */}
      <NotificationModal
        isOpen={isNotifOpen}
        onClose={() => setIsNotifOpen(false)}
      />

      {/* INT335 Demonstration Assistant Bar */}
      <DemoSwitcher />
    </div>
  );
};

export function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Welcome and Login Screen */}
          <Route path="/" element={<WelcomeLogin />} />

          {/* Student Protected Routes */}
          <Route path="/student/dashboard" element={<StudentRoute><MainLayout><StudentDashboard /></MainLayout></StudentRoute>} />
          <Route path="/student/ask" element={<StudentRoute><MainLayout><AskDoubt /></MainLayout></StudentRoute>} />
          <Route path="/student/questions" element={<StudentRoute><MainLayout><MyQuestions /></MainLayout></StudentRoute>} />
          <Route path="/student/answered" element={<StudentRoute><MainLayout><AnsweredDoubtsPage /></MainLayout></StudentRoute>} />
          <Route path="/student/subjects" element={<StudentRoute><MainLayout><SubjectExplorer /></MainLayout></StudentRoute>} />
          <Route path="/student/availability" element={<StudentRoute><MainLayout><FacultyAvailabilityPage /></MainLayout></StudentRoute>} />
          <Route path="/student/bookmarks" element={<StudentRoute><MainLayout><BookmarksPage /></MainLayout></StudentRoute>} />
          <Route path="/student/announcements" element={<StudentRoute><MainLayout><AnnouncementsPage /></MainLayout></StudentRoute>} />

          {/* Teacher Protected Routes */}
          <Route path="/teacher/dashboard" element={<TeacherRoute><MainLayout><TeacherDashboard /></MainLayout></TeacherRoute>} />
          <Route path="/teacher/doubts" element={<TeacherRoute><MainLayout><TeacherDoubtManagement /></MainLayout></TeacherRoute>} />
          <Route path="/teacher/appointments" element={<TeacherRoute><MainLayout><TeacherAppointments /></MainLayout></TeacherRoute>} />
          <Route path="/teacher/availability" element={<TeacherRoute><MainLayout><TeacherAvailability /></MainLayout></TeacherRoute>} />
          <Route path="/teacher/analytics" element={<TeacherRoute><MainLayout><TeacherAnalytics /></MainLayout></TeacherRoute>} />
          <Route path="/teacher/announcements" element={<TeacherRoute><MainLayout><TeacherAnnouncements /></MainLayout></TeacherRoute>} />

          {/* Fallback */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
