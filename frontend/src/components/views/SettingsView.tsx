'use client';

import React, { useEffect, useState } from 'react';
import {
  Sliders,
  Database,
  Shield,
  Activity,
  CheckCircle2,
  Lock,
  Cpu,
  RefreshCw,
  FileText
} from 'lucide-react';
import { fetchCaseDetails } from '@/lib/api';

interface SettingsViewProps {
  selectedCaseId: string;
}

export default function SettingsView({ selectedCaseId }: SettingsViewProps) {
  const [logs, setLogs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCaseDetails(selectedCaseId)
      .then((data) => setLogs(data.activity_logs || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [selectedCaseId]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-5xl mx-auto text-xs">
      {/* System Status Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white border border-tg-border rounded p-4 shadow-sm space-y-2">
          <div className="flex items-center space-x-2 text-tg-primary font-bold">
            <Database className="w-4 h-4" />
            <span>Relational Database</span>
          </div>
          <div className="space-y-1 text-slate-600 font-mono text-[11px]">
            <p>Engine: <strong>SQLite (Local Development Fallback)</strong></p>
            <p>Storage: <strong>tracegrid.db</strong></p>
            <p className="text-emerald-700 font-bold">Status: Online & Connected</p>
          </div>
        </div>

        <div className="bg-white border border-tg-border rounded p-4 shadow-sm space-y-2">
          <div className="flex items-center space-x-2 text-tg-primary font-bold">
            <Cpu className="w-4 h-4" />
            <span>Analytics & ML Engine</span>
          </div>
          <div className="space-y-1 text-slate-600 font-mono text-[11px]">
            <p>Model: <strong>IsolationForest (Scikit-Learn)</strong></p>
            <p>Graph Engine: <strong>NetworkX 3.x DiGraph</strong></p>
            <p>Contamination Param: <strong>0.08 (8% Outlier Expectation)</strong></p>
          </div>
        </div>

        <div className="bg-white border border-tg-border rounded p-4 shadow-sm space-y-2">
          <div className="flex items-center space-x-2 text-tg-primary font-bold">
            <Shield className="w-4 h-4" />
            <span>Security & Data Safeguards</span>
          </div>
          <div className="space-y-1 text-slate-600 font-mono text-[11px]">
            <p>Max Upload Size: <strong>25 MB</strong></p>
            <p>Sanitization: <strong>Safe ORM Querying Only</strong></p>
            <p>Data Label: <strong>SYNTHETIC DEMONSTRATION</strong></p>
          </div>
        </div>
      </div>

      {/* Audit Log Trail */}
      <div className="bg-white border border-tg-border rounded shadow-sm overflow-hidden">
        <div className="px-5 py-3 border-b border-tg-border bg-slate-50 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Activity className="w-4 h-4 text-tg-primary" />
            <h3 className="font-bold text-tg-text uppercase tracking-wider text-xs">
              Case Forensic Audit Trail
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-500">
            Immutable operation timeline
          </span>
        </div>

        {loading ? (
          <div className="p-8 text-center text-slate-500">
            Loading audit events...
          </div>
        ) : logs.length === 0 ? (
          <div className="p-8 text-center text-slate-500">
            No audit records logged for this case yet.
          </div>
        ) : (
          <div className="divide-y divide-slate-100">
            {logs.map((log) => (
              <div key={log.id} className="p-4 flex items-start justify-between hover:bg-slate-50/60">
                <div className="space-y-0.5">
                  <div className="flex items-center space-x-2 font-mono">
                    <span className="font-bold text-slate-800 bg-slate-100 px-1.5 py-0.5 rounded text-[10px]">
                      {log.action}
                    </span>
                    <span className="text-slate-500">&bull;</span>
                    <span className="text-slate-600 text-[11px]">{log.actor}</span>
                  </div>
                  <p className="text-slate-700 text-xs">{log.details}</p>
                </div>
                <span className="text-[11px] font-mono text-slate-400 flex-shrink-0">
                  {log.timestamp}
                </span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Hackathon Submission Credentials & Metadata */}
      <div className="bg-white border border-tg-border rounded p-5 shadow-sm space-y-3">
        <h3 className="font-bold text-tg-text text-xs uppercase tracking-wider">
          Hackathon Project Submission Credentials
        </h3>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs font-mono">
          <div className="p-2.5 bg-slate-50 rounded border border-slate-200">
            <span className="text-slate-400 block text-[10px]">PROJECT</span>
            <strong className="text-slate-800">TRACEGRID</strong>
          </div>
          <div className="p-2.5 bg-slate-50 rounded border border-slate-200">
            <span className="text-slate-400 block text-[10px]">TEAM</span>
            <strong className="text-slate-800">CyboShield</strong>
          </div>
          <div className="p-2.5 bg-slate-50 rounded border border-slate-200">
            <span className="text-slate-400 block text-[10px]">PROBLEM STATEMENT</span>
            <strong className="text-slate-800">PS05 (Financial Crime)</strong>
          </div>
          <div className="p-2.5 bg-slate-50 rounded border border-slate-200">
            <span className="text-slate-400 block text-[10px]">EVENT</span>
            <strong className="text-slate-800">RJ Police Hackathon 2026</strong>
          </div>
        </div>
      </div>
    </div>
  );
}

