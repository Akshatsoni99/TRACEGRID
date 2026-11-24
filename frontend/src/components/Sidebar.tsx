'use client';

import React from 'react';
import {
  LayoutDashboard,
  Briefcase,
  UploadCloud,
  ListFilter,
  Network,
  Globe2,
  GitCompare,
  MessageSquareCode,
  FileCheck2,
  Sliders,
  ShieldAlert,
  ChevronDown,
  Layers
} from 'lucide-react';
import { Investigation } from '@/lib/types';

interface SidebarProps {
  currentView: string;
  onSelectView: (view: string) => void;
  cases: Investigation[];
  selectedCaseId: string;
  onSelectCase: (caseId: string) => void;
}

export default function Sidebar({
  currentView,
  onSelectView,
  cases,
  selectedCaseId,
  onSelectCase,
}: SidebarProps) {
  const navItems = [
    { id: 'overview', label: 'Overview', icon: LayoutDashboard },
    { id: 'investigations', label: 'Investigations', icon: Briefcase, count: cases.length },
    { id: 'upload', label: 'Statement Ingestion', icon: UploadCloud },
    { id: 'transactions', label: 'Transaction Analysis', icon: ListFilter },
    { id: 'graph', label: 'Money-Trail Graph', icon: Network, badge: 'React Flow' },
    { id: 'intelligence', label: 'Digital Intelligence', icon: Globe2 },
    { id: 'cross-case', label: 'Cross-Case Correlation', icon: GitCompare },
    { id: 'ai-assistant', label: 'AI Forensic Assistant', icon: MessageSquareCode, badge: 'AI' },
    { id: 'reports', label: 'Court Reports (PDF)', icon: FileCheck2 },
    { id: 'settings', label: 'System & Logs', icon: Sliders },
  ];

  const activeCase = cases.find((c) => c.id === selectedCaseId) || cases[0];

  return (
    <aside className="w-64 bg-tg-sidebar text-slate-200 flex flex-col flex-shrink-0 h-screen border-r border-[#1C2F47] select-none z-20">
      {/* Brand & Logo Header */}
      <div className="p-4 border-b border-[#1C2F47]">
        <div className="flex items-center space-x-2.5">
          {/* Connected Node Logo SVG */}
          <div className="w-9 h-9 rounded bg-tg-primary/30 border border-tg-primary flex items-center justify-center flex-shrink-0 shadow-inner">
            <svg
              className="w-5 h-5 text-sky-400"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2.2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <circle cx="6" cy="6" r="2.5" />
              <circle cx="18" cy="7" r="2.5" />
              <circle cx="8" cy="18" r="2.5" />
              <circle cx="18" cy="17" r="2" />
              <line x1="8.5" y1="6.5" x2="15.5" y2="7" />
              <line x1="7" y1="8.5" x2="8" y2="15.5" />
              <line x1="8.5" y1="16.5" x2="16" y2="17" />
              <line x1="16.5" y1="9" x2="9.5" y2="16" />
            </svg>
          </div>
          <div>
            <div className="flex items-center space-x-1.5">
              <span className="font-bold tracking-wider text-base text-white">TRACEGRID</span>
              <span className="text-[10px] bg-sky-950 text-sky-300 font-mono font-semibold px-1 py-0.2 rounded border border-sky-800">
                v1.0
              </span>
            </div>
            <p className="text-[10px] text-slate-400 tracking-tight font-medium">
              Team CyboShield &bull; PS05
            </p>
          </div>
        </div>

        {/* Hackathon Badge */}
        <div className="mt-3 px-2 py-1.5 rounded bg-[#101B2B] border border-[#1C2F47] flex items-center justify-between text-[11px]">
          <div className="flex items-center space-x-1.5 text-slate-300">
            <ShieldAlert className="w-3.5 h-3.5 text-amber-400 flex-shrink-0" />
            <span className="font-medium truncate">RJ Police Hackathon 2026</span>
          </div>
          <span className="text-[9px] bg-amber-900/50 text-amber-300 font-semibold px-1 rounded">
            DEMO
          </span>
        </div>
      </div>

      {/* Case Quick Selector Dropdown */}
      <div className="px-3 pt-3 pb-2 border-b border-[#1C2F47]">
        <label className="block text-[10px] uppercase tracking-wider text-slate-400 font-semibold mb-1 px-1">
          Active Investigation Case
        </label>
        <div className="relative">
          <select
            value={selectedCaseId}
            onChange={(e) => onSelectCase(e.target.value)}
            className="w-full bg-[#0D1826] border border-[#223955] text-white text-xs rounded px-2.5 py-1.5 appearance-none focus:outline-none focus:border-tg-primary font-mono cursor-pointer pr-7 truncate"
          >
            {cases.map((c) => (
              <option key={c.id} value={c.id}>
                {c.case_number} - {c.title.slice(0, 22)}...
              </option>
            ))}
          </select>
          <ChevronDown className="w-3.5 h-3.5 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
        </div>
        {activeCase && (
          <div className="mt-1.5 flex items-center justify-between px-1 text-[10px]">
            <span className="text-slate-400 truncate max-w-[140px]">{activeCase.title}</span>
            <span
              className={`font-semibold uppercase px-1 py-0.5 rounded text-[9px] ${
                activeCase.priority === 'CRITICAL'
                  ? 'bg-rose-950 text-rose-300 border border-rose-800'
                  : 'bg-amber-950 text-amber-300 border border-amber-800'
              }`}
            >
              {activeCase.priority}
            </span>
          </div>
        )}
      </div>

      {/* Main Navigation Items */}
      <nav className="flex-1 overflow-y-auto px-2 py-3 space-y-0.5">
        <div className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider px-2 py-1">
          Forensic Modules
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = currentView === item.id;
          return (
            <button
              key={item.id}
              onClick={() => onSelectView(item.id)}
              className={`w-full flex items-center justify-between px-2.5 py-2 rounded text-xs font-medium transition-colors ${
                isActive
                  ? 'bg-tg-primary text-white shadow-sm'
                  : 'text-slate-300 hover:bg-tg-sidebarHover hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-2.5 truncate">
                <Icon
                  className={`w-4 h-4 flex-shrink-0 ${
                    isActive ? 'text-white' : 'text-slate-400'
                  }`}
                />
                <span className="truncate">{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[9px] font-mono px-1 rounded ${
                    isActive
                      ? 'bg-white/20 text-white'
                      : 'bg-slate-800 text-sky-400 border border-sky-900/50'
                  }`}
                >
                  {item.badge}
                </span>
              )}
              {item.count !== undefined && (
                <span
                  className={`text-[10px] font-mono px-1.5 py-0.2 rounded-full ${
                    isActive ? 'bg-white/25 text-white' : 'bg-slate-800 text-slate-400'
                  }`}
                >
                  {item.count}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Footer Profile / Subpoena Tag */}
      <div className="p-3 border-t border-[#1C2F47] bg-[#0E1929]">
        <div className="flex items-center space-x-2.5">
          <div className="w-7 h-7 rounded-full bg-slate-700 border border-slate-600 flex items-center justify-center text-xs font-bold text-white flex-shrink-0">
            VR
          </div>
          <div className="truncate">
            <p className="text-xs font-medium text-white truncate">Insp. Vikram Rathore</p>
            <p className="text-[10px] text-slate-400 truncate">Cyber Crime Cell, EOW</p>
          </div>
        </div>
      </div>
    </aside>
  );
}

