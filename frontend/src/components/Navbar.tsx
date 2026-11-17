import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
  GraduationCap, Bell, Download, LogOut, User, 
  Menu, X, Sparkles, BookOpen, Layers, Key, CheckCircle2, AlertCircle, Loader2
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { api } from '../api';

interface NavbarProps {
  onOpenNotifications: () => void;
  onToggleSidebar?: () => void;
  isSidebarOpen?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({ 
  onOpenNotifications, 
  onToggleSidebar, 
  isSidebarOpen 
}) => {
  const { role, student, teacher, logout } = useAuth();
  const navigate = useNavigate();
  const [unreadCount, setUnreadCount] = useState(0);
  const [deferredPrompt, setDeferredPrompt] = useState<any>(null);
  const [isInstalled, setIsInstalled] = useState(false);

  // AI Configuration Modal State
  const [isAiModalOpen, setIsAiModalOpen] = useState(false);
  const [aiConfig, setAiConfig] = useState<{ provider: string; has_gemini_key: boolean; model_name: string } | null>(null);
  const [inputKey, setInputKey] = useState('');
  const [savingAi, setSavingAi] = useState(false);
  const [aiMsg, setAiMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  useEffect(() => {
    if (role === 'teacher') {
      api.getAiConfig().then(setAiConfig).catch(() => {});
    }
  }, [role]);

  const handleSaveKey = async (keyToSave: string) => {
    try {
      setSavingAi(true);
      setAiMsg(null);
      const res = await api.saveAiConfig(keyToSave);
      const updated = await api.getAiConfig();
      setAiConfig(updated);
      setAiMsg({ type: 'success', text: res.message });
      if (!keyToSave) setInputKey('');
    } catch (err: any) {
      setAiMsg({ type: 'error', text: err?.response?.data?.error || err.message || 'Failed to update AI key.' });
    } finally {
      setSavingAi(false);
    }
  };

  // Poll notifications
  useEffect(() => {
    const fetchUnread = async () => {
      if (role === 'student' && student) {
        try {
          const res = await api.getNotifications('student', student.name);
          setUnreadCount(res.unread_count);
        } catch {
          // ignore
        }
      } else if (role === 'teacher' && teacher) {
        try {
          const res = await api.getNotifications('teacher', teacher.id);
          setUnreadCount(res.unread_count);
        } catch {
          // ignore
        }
      }
    };

    fetchUnread();
    const interval = setInterval(fetchUnread, 15000);
    return () => clearInterval(interval);
  }, [role, student, teacher]);

  // Listen for Chrome PWA install prompt
  useEffect(() => {
    const handleBeforeInstall = (e: any) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstall);
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setIsInstalled(true);
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstall);
    };
  }, []);

  const handleInstallClick = async () => {
    if (deferredPrompt) {
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      if (outcome === 'accepted') {
        setIsInstalled(true);
      }
      setDeferredPrompt(null);
    } else {
      alert('To install Faculty Connect on Chrome: click the install icon (⊕) on the right side of your browser URL address bar.');
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <header className="sticky top-0 z-40 bg-[#15370D] text-[#FCF9EA] shadow-md border-b border-[#F2842F]/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
        
        {/* Left: Mobile Menu Toggle & Brand */}
        <div className="flex items-center gap-3">
          {role !== 'guest' && onToggleSidebar && (
            <button 
              onClick={onToggleSidebar}
              className="lg:hidden p-2 rounded-lg text-[#FCF9EA] hover:bg-[#FCF9EA]/10 transition"
              aria-label="Toggle navigation"
            >
              {isSidebarOpen ? <X className="w-5 h-5 text-[#F2842F]" /> : <Menu className="w-5 h-5 text-[#FCF9EA]" />}
            </button>
          )}

          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-lg bg-[#FCF9EA] text-[#15370D] flex items-center justify-center font-black shadow group-hover:scale-105 transition-transform">
              <GraduationCap className="w-6 h-6 text-[#15370D]" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="font-extrabold tracking-tight text-lg sm:text-xl text-[#FCF9EA]">
                  FACULTY<span className="text-[#F2842F]">CONNECT</span>
                </span>
                <span className="hidden sm:inline-block px-1.5 py-0.5 rounded text-[10px] font-bold bg-[#F2842F] text-[#000000] tracking-wider uppercase">
                  P09 • INT335
                </span>
              </div>
              <p className="text-[10px] text-[#FCF9EA]/70 hidden md:block tracking-wide">
                Making Academic Communication Smarter, Faster and More Organised
              </p>
            </div>
          </Link>
        </div>

        {/* Right Action Controls */}
        <div className="flex items-center gap-2 sm:gap-4">
          
          {/* PWA Install Button */}
          {!isInstalled && (
            <button
              onClick={handleInstallClick}
              className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-[#F2842F] bg-[#F2842F]/10 hover:bg-[#F2842F] hover:text-[#000000] text-xs font-semibold text-[#FCF9EA] transition"
              title="Install Faculty Connect as Chrome App (PWA)"
            >
              <Download className="w-3.5 h-3.5 text-[#F2842F] group-hover:text-[#000000]" />
              <span>Install App</span>
            </button>
          )}

          {/* Teacher AI Engine Pill */}
          {role === 'teacher' && (
            <button
              onClick={() => setIsAiModalOpen(true)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-[#F2842F] bg-[#F2842F]/15 hover:bg-[#F2842F] text-[#FCF9EA] hover:text-[#000000] text-xs font-black shadow-xs transition"
              title="Configure AI Engine (Google Gemini Cloud LLM or Local Academic Synthesizer)"
            >
              <Sparkles className="w-3.5 h-3.5 text-[#F2842F]" />
              <span className="hidden sm:inline">
                {aiConfig?.has_gemini_key ? '⚡ Gemini AI Active' : '✨ Academic AI Engine'}
              </span>
              <span className="sm:hidden">AI</span>
            </button>
          )}

          {/* Notifications Button */}
          {role !== 'guest' && (
            <button
              onClick={onOpenNotifications}
              className="relative p-2 rounded-lg text-[#FCF9EA] hover:bg-[#FCF9EA]/10 transition"
              aria-label="View notifications"
            >
              <Bell className="w-5 h-5" />
              {unreadCount > 0 && (
                <span className="absolute top-1 right-1 w-4 h-4 bg-[#F2842F] text-[#000000] text-[10px] font-black rounded-full flex items-center justify-center animate-pulse">
                  {unreadCount > 9 ? '9+' : unreadCount}
                </span>
              )}
            </button>
          )}

          {/* User Profile Pill */}
          {role === 'student' && student && (
            <div className="flex items-center gap-2 pl-2 border-l border-[#FCF9EA]/20">
              <div className="w-8 h-8 rounded-full bg-[#FCF9EA]/10 border border-[#F2842F]/50 flex items-center justify-center text-xs font-bold text-[#FCF9EA]">
                {student.name.charAt(0)}
              </div>
              <div className="hidden md:block text-left text-xs leading-tight">
                <p className="font-semibold text-[#FCF9EA]">{student.name}</p>
                <p className="text-[#F2842F] text-[10px] font-medium">{student.section}</p>
              </div>
              <button
                onClick={handleLogout}
                className="p-1.5 text-[#FCF9EA]/70 hover:text-[#F2842F] transition ml-1"
                title="Switch User / Logout"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )}

          {role === 'teacher' && teacher && (
            <div className="flex items-center gap-2 pl-2 border-l border-[#FCF9EA]/20">
              <div className="w-8 h-8 rounded-full bg-[#F2842F] text-[#000000] font-bold flex items-center justify-center text-xs">
                {teacher.name.replace('Dr. ', '').replace('Prof. ', '').charAt(0)}
              </div>
              <div className="hidden md:block text-left text-xs leading-tight">
                <p className="font-semibold text-[#FCF9EA]">{teacher.name}</p>
                <p className="text-[#F2842F] text-[10px] font-medium">{teacher.cabin_location}</p>
              </div>
              <button
                onClick={handleLogout}
                className="p-1.5 text-[#FCF9EA]/70 hover:text-[#F2842F] transition ml-1"
                title="Sign Out"
              >
                <LogOut className="w-4 h-4" />
              </button>
            </div>
          )}

          {role === 'guest' && (
            <Link
              to="/"
              className="px-3.5 py-1.5 rounded-lg bg-[#F2842F] text-[#000000] text-xs font-bold hover:bg-[#F2842F]/90 transition"
            >
              Sign In
            </Link>
          )}

        </div>
      </div>

      {/* AI Configuration Modal */}
      {isAiModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs">
          <div className="w-full max-w-lg bg-[#FCF9EA] border-2 border-[#15370D] rounded-3xl shadow-2xl overflow-hidden animate-fade-in text-gray-900">
            <div className="p-5 bg-[#15370D] text-[#FCF9EA] flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-[#F2842F]" />
                <h3 className="text-base font-black">AI Doubt Resolution Engine Settings</h3>
              </div>
              <button
                onClick={() => setIsAiModalOpen(false)}
                className="p-1 rounded-lg text-[#FCF9EA]/70 hover:text-[#FCF9EA] hover:bg-white/10 transition"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 space-y-4 text-xs sm:text-sm">
              <div className="p-4 rounded-2xl bg-white border border-[#E5DFC8] space-y-2">
                <div className="flex items-center justify-between">
                  <span className="font-bold text-gray-700">Active Engine:</span>
                  <span className={`px-2.5 py-0.5 rounded-full font-black text-xs ${
                    aiConfig?.has_gemini_key 
                      ? 'bg-purple-100 text-purple-900 border border-purple-300' 
                      : 'bg-emerald-100 text-emerald-900 border border-emerald-300'
                  }`}>
                    {aiConfig?.model_name || 'Loading...'}
                  </span>
                </div>
                <p className="text-[11px] text-gray-500">
                  {aiConfig?.has_gemini_key
                    ? 'Connected to Google Gemini Live API. Generates unique, dynamic solutions in real time.'
                    : 'Running the built-in Deep Academic Knowledge Synthesizer grounded in all 7 LPU course syllabi.'}
                </p>
              </div>

              {aiMsg && (
                <div className={`p-3 rounded-xl border text-xs font-bold flex items-center gap-2 ${
                  aiMsg.type === 'success'
                    ? 'bg-emerald-50 border-emerald-300 text-emerald-900'
                    : 'bg-red-50 border-red-300 text-red-900'
                }`}>
                  {aiMsg.type === 'success' ? (
                    <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  ) : (
                    <AlertCircle className="w-4 h-4 text-red-600 shrink-0" />
                  )}
                  <span>{aiMsg.text}</span>
                </div>
              )}

              <div className="space-y-2">
                <label className="block text-xs font-black text-gray-800">
                  Google Gemini API Key (Optional Cloud LLM):
                </label>
                <div className="relative">
                  <Key className="w-4 h-4 text-gray-400 absolute left-3 top-3" />
                  <input
                    type="password"
                    value={inputKey}
                    onChange={(e) => setInputKey(e.target.value)}
                    placeholder={aiConfig?.has_gemini_key ? '••••••••••••••••••••••••••••••••' : 'Enter Gemini API Key from Google AI Studio...'}
                    className="w-full pl-9 pr-3 py-2.5 bg-white border border-[#D8D2BA] focus:border-[#15370D] rounded-xl text-xs outline-hidden"
                  />
                </div>
                <p className="text-[11px] text-gray-500">
                  You can obtain a 100% free Gemini API key with no credit card at{' '}
                  <a
                    href="https://aistudio.google.com/app/apikey"
                    target="_blank"
                    rel="noreferrer"
                    className="text-[#15370D] font-bold underline hover:text-[#F2842F]"
                  >
                    Google AI Studio
                  </a>.
                </p>
              </div>

              <div className="pt-3 border-t border-gray-200 flex flex-wrap items-center justify-between gap-2">
                {aiConfig?.has_gemini_key && (
                  <button
                    type="button"
                    onClick={() => handleSaveKey('')}
                    disabled={savingAi}
                    className="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 font-bold rounded-xl text-xs transition"
                  >
                    Disconnect Gemini (Use Local)
                  </button>
                )}

                <div className="flex items-center gap-2 ml-auto">
                  <button
                    type="button"
                    onClick={() => setIsAiModalOpen(false)}
                    className="px-4 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold rounded-xl text-xs transition"
                  >
                    Close
                  </button>
                  <button
                    type="button"
                    onClick={() => handleSaveKey(inputKey)}
                    disabled={savingAi || !inputKey.trim()}
                    className="px-5 py-2 bg-[#F2842F] hover:bg-[#d86d1d] text-[#000000] font-black rounded-xl text-xs flex items-center gap-1.5 transition disabled:opacity-50"
                  >
                    {savingAi ? (
                      <>
                        <Loader2 className="w-3.5 h-3.5 animate-spin text-[#000000]" />
                        <span>Verifying...</span>
                      </>
                    ) : (
                      <>
                        <Sparkles className="w-3.5 h-3.5 text-[#000000]" />
                        <span>Connect &amp; Save Key</span>
                      </>
                    )}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </header>
  );
};
