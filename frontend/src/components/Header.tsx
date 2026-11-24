'use client';

import React, { useState } from 'react';
import {
  FileDown,
  RotateCcw,
  CheckCircle2,
  AlertTriangle,
  FolderOpen,
  UserCheck,
  ShieldCheck
} from 'lucide-react';
import { Investigation } from '@/lib/types';
import { getReportDownloadUrl, resetDemoData } from '@/lib/api';

interface HeaderProps {
  currentView: string;
  activeCase?: Investigation;
  onRefresh: () => void;
}

export default function Header({
  currentView,
  activeCase,
  onRefresh,
}: HeaderProps) {
  const [resetting, setResetting] = useState(false);

  const viewTitles: Record<string, { title: string; subtitle: string }> = {
    overview: {
      title: 'Investigation Overview Dashboard',
      subtitle: 'High-level metrics, active threat levels, transaction velocity and recent case intake.',
    },
    investigations: {
      title: 'Investigation Dossier Registry',
      subtitle: 'Create, search, prioritize and manage active financial crime cases with full evidentiary links.',
    },
    upload: {
      title: 'Bank Statement Ingestion & Parsing',
      subtitle: 'Secure CSV/Excel parser with column mapping, duplicate detection, and automated anomaly flagging.',
    },
    transactions: {
      title: 'Financial Transaction Analytics',
      subtitle: 'Algorithmic indicators, structuring detection, pass-through mule profiling and anomaly scores.',
    },
    graph: {
      title: 'Money-Trail Network Graph',
      subtitle: 'Interactive directed relationship graph powered by NetworkX & React Flow to expose circular hops.',
    },
    intelligence: {
      title: 'Digital Infrastructure Intelligence',
      subtitle: 'Correlating passive WHOIS, DNS records, IP lookups and hosting ASNs with target bank accounts.',
    },
    'cross-case': {
      title: 'Cross-Case Correlation & Syndicate Linking',
      subtitle: 'Identifies accounts, infrastructure and entities appearing across multiple separate police cases.',
    },
    'ai-assistant': {
      title: 'TRACEGRID AI Forensic Assistant',
      subtitle: 'Context-grounded investigative query assistant explaining anomalies and recommending Section 91 CrPC requisitions.',
    },
    reports: {
      title: 'Evidence Dossier & Court Reports',
      subtitle: 'Generate verifiable, branded, timestamped PDF investigation dossiers for judicial submission.',
    },
    settings: {
      title: 'System Settings, API Connectivity & Audit Logs',
      subtitle: 'Review backend database status, operational logs, and machine learning engine configuration.',
    },
  };

  const currentMeta = viewTitles[currentView] || {
    title: 'TRACEGRID Forensic Console',
    subtitle: 'Unified Financial Crime Analytics Workspace',
  };

  const handleResetDemo = async () => {
    if (!confirm('Re-seed demonstration database with fresh synthetic crime scenarios?')) return;
    setResetting(true);
    try {
      await resetDemoData();
      alert('Demonstration database re-seeded successfully.');
      onRefresh();
    } catch (err: any) {
      alert(`Reset error: ${err.message}`);
    } finally {
      setResetting(false);
    }
  };

  const handleDownloadReport = () => {
    if (!activeCase) return;
    window.open(getReportDownloadUrl(activeCase.id), '_blank');
  };

  return (
    <header className="h-16 bg-white border-b border-tg-border px-6 flex items-center justify-between flex-shrink-0 z-10">
      {/* Title & Active Case Context */}
      <div className="flex items-center space-x-4">
        <div>
          <div className="flex items-center space-x-2.5">
            <h1 className="text-base font-bold text-tg-text">{currentMeta.title}</h1>
            {activeCase && (
              <span className="inline-flex items-center space-x-1 font-mono text-[11px] bg-slate-100 text-slate-700 px-2 py-0.5 rounded border border-slate-300 font-semibold">
                <FolderOpen className="w-3 h-3 text-tg-primary" />
                <span>{activeCase.case_number}</span>
              </span>
            )}
            {activeCase && (
              <span
                className={`text-[10px] font-bold px-1.5 py-0.5 rounded uppercase ${
                  activeCase.priority === 'CRITICAL'
                    ? 'bg-rose-100 text-rose-700 border border-rose-200'
                    : 'bg-amber-100 text-amber-700 border border-amber-200'
                }`}
              >
                {activeCase.priority}
              </span>
            )}
          </div>
          <p className="text-xs text-tg-secondary line-clamp-1">{currentMeta.subtitle}</p>
        </div>
      </div>

      {/* Right Controls */}
      <div className="flex items-center space-x-3">
        {/* Backend Status indicator */}
        <div className="hidden lg:flex items-center space-x-1.5 px-2.5 py-1 rounded bg-slate-50 border border-slate-200 text-[11px] text-slate-600 font-mono">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span>API 8000 LIVE</span>
        </div>

        {/* Reset Demo Data Button */}
        <button
          onClick={handleResetDemo}
          disabled={resetting}
          className="flex items-center space-x-1.5 px-2.5 py-1.5 rounded text-xs font-medium text-slate-700 bg-slate-100 hover:bg-slate-200 border border-slate-300 transition-colors"
          title="Reset demonstration database to standard scenarios"
        >
          <RotateCcw className={`w-3.5 h-3.5 text-slate-500 ${resetting ? 'animate-spin' : ''}`} />
          <span className="hidden sm:inline">Reset Demo</span>
        </button>

        {/* PDF Export Button */}
        {activeCase && (
          <button
            onClick={handleDownloadReport}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded text-xs font-medium text-white bg-tg-primary hover:bg-tg-primaryHover shadow-sm transition-colors"
          >
            <FileDown className="w-3.5 h-3.5" />
            <span>Export Case PDF</span>
          </button>
        )}
      </div>
    </header>
  );
}

