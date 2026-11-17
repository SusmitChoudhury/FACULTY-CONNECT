import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  X, Bell, CheckCircle2, Sparkles, Calendar, 
  AlertTriangle, Megaphone, CheckCheck, Inbox
} from 'lucide-react';
import { Notification } from '../types';
import { api } from '../api';
import { useAuth } from '../context/AuthContext';

interface NotificationModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export const NotificationModal: React.FC<NotificationModalProps> = ({ isOpen, onClose }) => {
  const { role, student, teacher } = useAuth();
  const navigate = useNavigate();
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [filter, setFilter] = useState<'all' | 'unread'>('all');
  const [loading, setLoading] = useState(false);

  const fetchNotifs = async () => {
    if (!isOpen) return;
    setLoading(true);
    try {
      if (role === 'student' && student) {
        const res = await api.getNotifications('student', student.name);
        setNotifications(res.notifications);
      } else if (role === 'teacher' && teacher) {
        const res = await api.getNotifications('teacher', teacher.id);
        setNotifications(res.notifications);
      }
    } catch (e) {
      console.warn('Failed to fetch notifications:', e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchNotifs();
  }, [isOpen, role, student, teacher]);

  if (!isOpen) return null;

  const handleMarkAsRead = async (id: number) => {
    try {
      await api.markNotificationRead(id);
      setNotifications(prev =>
        prev.map(n => n.id === id ? { ...n, is_read: true } : n)
      );
    } catch {
      // ignore
    }
  };

  const handleMarkAllRead = async () => {
    try {
      const id = role === 'student' ? student?.name : teacher?.id;
      if (id && (role === 'student' || role === 'teacher')) {
        await api.markAllNotificationsRead(role, id);
        setNotifications(prev => prev.map(n => ({ ...n, is_read: true })));
      }
    } catch {
      // ignore
    }
  };

  const handleClickItem = (n: Notification) => {
    handleMarkAsRead(n.id);
    onClose();
    if (n.notification_type === 'appointment_update') {
      navigate(role === 'student' ? '/student/availability' : '/teacher/appointments');
    } else if (n.notification_type === 'announcement') {
      navigate(role === 'student' ? '/student/announcements' : '/teacher/announcements');
    } else {
      navigate(role === 'student' ? '/student/questions' : '/teacher/doubts');
    }
  };

  const filteredNotifs = filter === 'unread' 
    ? notifications.filter(n => !n.is_read)
    : notifications;

  const getIcon = (type: string) => {
    switch (type) {
      case 'faculty_answer':
        return <CheckCircle2 className="w-5 h-5 text-[#15370D]" />;
      case 'ai_answer':
        return <Sparkles className="w-5 h-5 text-[#F2842F]" />;
      case 'appointment_update':
        return <Calendar className="w-5 h-5 text-blue-700" />;
      case 'high_volume_alert':
        return <AlertTriangle className="w-5 h-5 text-amber-600" />;
      case 'announcement':
        return <Megaphone className="w-5 h-5 text-[#15370D]" />;
      default:
        return <Bell className="w-5 h-5 text-gray-600" />;
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
      <div className="w-full max-w-lg bg-[#FCF9EA] border border-[#D8D2BA] rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[85vh] animate-fade-in">
        
        {/* Header */}
        <div className="px-6 py-4 bg-[#15370D] text-[#FCF9EA] flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Bell className="w-5 h-5 text-[#F2842F]" />
            <h2 className="text-base font-bold text-[#FCF9EA]">Notifications</h2>
          </div>
          <button 
            onClick={onClose}
            className="p-1 rounded-lg text-[#FCF9EA]/80 hover:text-white hover:bg-white/10 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Filter & Actions Bar */}
        <div className="px-6 py-3 bg-[#F4EFCF] border-b border-[#D8D2BA] flex items-center justify-between text-xs font-medium">
          <div className="flex gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-3 py-1 rounded-full transition ${
                filter === 'all' 
                  ? 'bg-[#15370D] text-[#FCF9EA] font-semibold' 
                  : 'bg-white/80 text-gray-700 hover:bg-white'
              }`}
            >
              All ({notifications.length})
            </button>
            <button
              onClick={() => setFilter('unread')}
              className={`px-3 py-1 rounded-full transition ${
                filter === 'unread' 
                  ? 'bg-[#15370D] text-[#FCF9EA] font-semibold' 
                  : 'bg-white/80 text-gray-700 hover:bg-white'
              }`}
            >
              Unread ({notifications.filter(n => !n.is_read).length})
            </button>
          </div>

          <button
            onClick={handleMarkAllRead}
            className="flex items-center gap-1 text-[#15370D] hover:text-[#F2842F] font-semibold"
          >
            <CheckCheck className="w-3.5 h-3.5" />
            Mark all read
          </button>
        </div>

        {/* Content List */}
        <div className="p-4 overflow-y-auto space-y-2.5 flex-1 divide-y divide-[#E5DFC8]/60">
          {loading && (
            <div className="text-center py-8 text-gray-500 text-sm">Loading notifications...</div>
          )}

          {!loading && filteredNotifs.length === 0 && (
            <div className="text-center py-12 px-4">
              <Inbox className="w-10 h-10 mx-auto text-gray-400 mb-2 stroke-1" />
              <p className="text-sm font-semibold text-gray-800">No notifications found</p>
              <p className="text-xs text-gray-500 mt-0.5">You are all caught up with your academic updates.</p>
            </div>
          )}

          {!loading && filteredNotifs.map((n) => (
            <div
              key={n.id}
              onClick={() => handleClickItem(n)}
              className={`pt-2.5 first:pt-0 p-3 rounded-xl cursor-pointer transition flex items-start gap-3.5 ${
                !n.is_read 
                  ? 'bg-white border-l-4 border-l-[#F2842F] shadow-xs' 
                  : 'bg-[#FAF6E4] hover:bg-white'
              }`}
            >
              <div className="mt-0.5 p-2 rounded-lg bg-[#FCF9EA] border border-[#E5DFC8]">
                {getIcon(n.notification_type)}
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center justify-between">
                  <h4 className="text-xs font-bold text-gray-900 truncate">{n.title}</h4>
                  <span className="text-[10px] text-gray-500">
                    {n.created_at ? new Date(n.created_at).toLocaleDateString([], { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : ''}
                  </span>
                </div>
                <p className="text-xs text-gray-700 mt-0.5 line-clamp-2 leading-relaxed">
                  {n.message}
                </p>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 bg-[#F4EFCF] border-t border-[#D8D2BA] text-center">
          <button
            onClick={onClose}
            className="w-full py-2 bg-[#15370D] text-[#FCF9EA] hover:bg-[#15370D]/90 rounded-lg text-xs font-bold transition"
          >
            Close
          </button>
        </div>

      </div>
    </div>
  );
};
