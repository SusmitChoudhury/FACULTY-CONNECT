import React from 'react';
import { GraduationCap, Users, Award, ShieldCheck } from 'lucide-react';

export const Footer: React.FC = () => {
  const teamMembers = [
    { name: 'Aryan Singh', regNo: '12516621', role: 'Team Member' },
    { name: 'Kaya Hamir Reddy', regNo: '12516680', role: 'Team Member' },
    { name: 'Aditya Tiwari', regNo: '12516873', role: 'Team Member' },
    { name: 'Susmit Choudhury', regNo: '12517025', role: 'Team Member' }
  ];

  return (
    <footer className="bg-[#15370D] text-[#FCF9EA] border-t-2 border-[#F2842F]/40 pt-10 pb-16 lg:pb-10 transition-colors">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-8">
        
        {/* Top Header & Project Identity */}
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6 pb-6 border-b border-[#FCF9EA]/15">
          <div className="space-y-2">
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-[#FCF9EA] text-[#15370D] flex items-center justify-center font-black shadow-sm">
                <GraduationCap className="w-5 h-5 text-[#15370D]" />
              </div>
              <span className="text-xl font-black tracking-tight text-[#FCF9EA]">
                FACULTY<span className="text-[#F2842F]">CONNECT</span>
              </span>
              <span className="px-2 py-0.5 rounded text-[11px] font-black bg-[#F2842F] text-[#000000] uppercase tracking-wider">
                Project ID: P09
              </span>
            </div>
            
            <p className="text-sm font-bold text-[#FCF9EA]/90">
              FACULTY CONNECT © 2026 • Lovely Professional University (LPU)
            </p>
            <p className="text-xs text-[#FCF9EA]/70">
              INT335 Design Thinking Innovation Group Project (ID: P09) • Project Domain: Faculty-Student Academic Communication
            </p>
          </div>

          <div className="flex items-center gap-3 bg-[#FCF9EA]/10 border border-[#F2842F]/30 px-4 py-2.5 rounded-2xl">
            <Award className="w-5 h-5 text-[#F2842F] shrink-0" />
            <div className="text-xs">
              <span className="font-bold text-[#FCF9EA] block">LPU INT335 Innovation</span>
              <span className="text-[11px] text-[#FCF9EA]/70">Heard in Class, Lost After</span>
            </div>
          </div>
        </div>

        {/* Project Team Members Showcase */}
        <div className="space-y-3">
          <div className="flex items-center gap-2 text-xs font-black uppercase tracking-wider text-[#F2842F]">
            <Users className="w-4 h-4" />
            <span>Group Innovation Project Team Members</span>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {teamMembers.map((member) => (
              <div
                key={member.regNo}
                className="p-4 rounded-2xl bg-[#FCF9EA]/5 border border-[#F2842F]/20 hover:border-[#F2842F] hover:bg-[#FCF9EA]/10 transition group"
              >
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl bg-[#F2842F] text-[#000000] font-black flex items-center justify-center text-sm shadow-xs group-hover:scale-105 transition-transform">
                    {member.name.charAt(0)}
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm font-black text-[#FCF9EA] truncate">
                      {member.name}
                    </p>
                    <p className="text-xs text-[#F2842F] font-semibold">
                      Reg. No: <span className="font-mono text-[#FCF9EA]">{member.regNo}</span>
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bottom Tagline & Academic Disclaimer */}
        <div className="pt-4 border-t border-[#FCF9EA]/15 flex flex-col sm:flex-row items-center justify-between gap-3 text-center sm:text-left text-xs text-[#FCF9EA]/60">
          <p>
            Making Academic Communication Smarter, Faster and More Organised.
          </p>
          <p className="flex items-center gap-1.5 justify-center">
            <ShieldCheck className="w-4 h-4 text-[#F2842F]" />
            <span>Official INT335 Design Thinking Prototype • LPU 2026</span>
          </p>
        </div>

      </div>
    </footer>
  );
};
