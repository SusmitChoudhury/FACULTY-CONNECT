import React, { createContext, useContext, useState, useEffect } from 'react';
import { Student, Teacher } from '../types';

interface AuthContextType {
  role: 'guest' | 'student' | 'teacher';
  student: Student | null;
  teacher: Teacher | null;
  token: string | null;
  loginStudent: (student: Student) => void;
  loginTeacher: (teacher: Teacher, token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [role, setRole] = useState<'guest' | 'student' | 'teacher'>('guest');
  const [student, setStudent] = useState<Student | null>(null);
  const [teacher, setTeacher] = useState<Teacher | null>(null);
  const [token, setToken] = useState<string | null>(null);

  useEffect(() => {
    // Restore session from localStorage
    try {
      const savedRole = localStorage.getItem('fc_role') as 'student' | 'teacher' | null;
      if (savedRole === 'student') {
        const savedStudent = localStorage.getItem('fc_student');
        if (savedStudent) {
          setStudent(JSON.parse(savedStudent));
          setRole('student');
        }
      } else if (savedRole === 'teacher') {
        const savedTeacher = localStorage.getItem('fc_teacher');
        const savedToken = localStorage.getItem('fc_token');
        if (savedTeacher && savedToken) {
          setTeacher(JSON.parse(savedTeacher));
          setToken(savedToken);
          setRole('teacher');
        }
      }
    } catch (e) {
      console.warn('Failed to restore auth session:', e);
    }
  }, []);

  const loginStudent = (newStudent: Student) => {
    setStudent(newStudent);
    setRole('student');
    setTeacher(null);
    setToken(null);
    localStorage.setItem('fc_role', 'student');
    localStorage.setItem('fc_student', JSON.stringify(newStudent));
    localStorage.removeItem('fc_teacher');
    localStorage.removeItem('fc_token');
  };

  const loginTeacher = (newTeacher: Teacher, newToken: string) => {
    setTeacher(newTeacher);
    setToken(newToken);
    setRole('teacher');
    setStudent(null);
    localStorage.setItem('fc_role', 'teacher');
    localStorage.setItem('fc_teacher', JSON.stringify(newTeacher));
    localStorage.setItem('fc_token', newToken);
    localStorage.removeItem('fc_student');
  };

  const logout = () => {
    setRole('guest');
    setStudent(null);
    setTeacher(null);
    setToken(null);
    localStorage.removeItem('fc_role');
    localStorage.removeItem('fc_student');
    localStorage.removeItem('fc_teacher');
    localStorage.removeItem('fc_token');
  };

  return (
    <AuthContext.Provider value={{ role, student, teacher, token, loginStudent, loginTeacher, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within an AuthProvider');
  return context;
};
