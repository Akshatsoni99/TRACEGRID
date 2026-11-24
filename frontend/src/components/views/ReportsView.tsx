'use client';

import React, { useEffect, useState } from 'react';
import {
  FileCheck2,
  FileDown,
  Printer,
  ShieldCheck,
  Building,
  CheckCircle2,
  Calendar,
  User,
  AlertTriangle,
  RefreshCw
} from 'lucide-react';
import { Investigation } from '@/lib/types';
import { fetchCaseDetails, getReportDownloadUrl } from '@/lib/api';

interface ReportsViewProps {
  selectedCaseId: string;
}

export default function ReportsView({ selectedCaseId }: ReportsViewProps) {
  const [caseData, setCaseData] = useState<any | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadCase = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCaseDetails(selectedCaseId);
      setCaseData(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load case data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCase();
  }, [selectedCaseId]);

  if (loading) {
    return (
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="flex items-center space-x-2 text-slate-500 text-xs">
          <RefreshCw className="w-4 h-4 animate-spin text-tg-primary" />
          <span>Generating forensic report preview...</span>
        </div>
      </div>
    );
  }

  if (error || !caseData) {
    return (
      <div className="flex-1 p-8 text-center text-rose-600 text-xs">
        {error || 'Case records unavailable'}
      </div>
    );
  }

  const { case: c, stats } = caseData;
  const downloadUrl = getReportDownloadUrl(c.id);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-4xl mx-auto">
      {/* Top Action Header */}
      <div className="bg-white border border-tg-border rounded p-4 shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-sm font-bold text-tg-text">Investigation Dossier & Court Report</h2>
          <p className="text-xs text-tg-secondary">
            Generated via ReportLab for official law enforcement submission
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <a
            href={downloadUrl}
            target="_blank"
            rel="noreferrer"
            className="flex items-center space-x-2 px-4 py-2 bg-tg-primary hover:bg-tg-primaryHover text-white rounded text-xs font-semibold shadow-sm transition-colors"
          >
            <FileDown className="w-4 h-4" />
            <span>Download Certified PDF Report</span>
          </a>
        </div>
      </div>

      {/* Simulated Document Preview Card */}
      <div className="bg-white border-2 border-slate-300 rounded-lg shadow-lg p-8 space-y-6 font-sans text-xs">
        {/* Dossier Header Banner */}
        <div className="border-b-2 border-tg-primary pb-4 flex items-start justify-between">
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-extrabold text-xl tracking-wider text-tg-sidebar">TRACEGRID</span>
              <span className="text-slate-300 text-lg">|</span>
              <span className="text-xs font-semibold text-tg-primary uppercase tracking-wide">
                Financial Crime Intelligence Dossier
              </span>
            </div>
            <p className="text-[11px] text-slate-500 mt-1">
              Team CyboShield &bull; Rajasthan Police Hackathon 2026 &bull; Problem Statement PS05
            </p>
          </div>

          <div className="text-right">
            <span className="font-mono text-xs font-bold text-rose-800 bg-rose-50 border border-rose-200 px-2 py-0.5 rounded uppercase">
              CONFIDENTIAL // LAW ENFORCEMENT
            </span>
            <p className="text-[11px] font-mono text-slate-500 mt-1">
              Ref: <strong>{c.case_number}</strong>
            </p>
          </div>
        </div>

        {/* Section 1: Investigation Profile */}
        <div className="space-y-2">
          <h3 className="font-bold text-xs uppercase tracking-wider text-tg-primary flex items-center space-x-1.5">
            <span>1. Investigation Profile & Executive Summary</span>
          </h3>
          <div className="bg-slate-50 border border-slate-200 rounded p-4 grid grid-cols-2 gap-3 text-xs">
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Case Title</span>
              <span className="font-bold text-slate-800">{c.title}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Priority</span>
              <span className="font-bold text-rose-700 uppercase">{c.priority}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Lead Investigator</span>
              <span className="font-medium text-slate-800">{c.lead_investigator}</span>
            </div>
            <div>
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Registration Date</span>
              <span className="font-mono text-slate-700">{new Date(c.created_at).toLocaleDateString()}</span>
            </div>
            <div className="col-span-2 pt-2 border-t border-slate-200">
              <span className="text-slate-400 block text-[10px] uppercase font-semibold">Modus Operandi Brief</span>
              <p className="text-slate-700 mt-0.5 leading-relaxed">{c.description}</p>
            </div>
          </div>
        </div>

        {/* Section 2: Quantitative Metrics */}
        <div className="space-y-2">
          <h3 className="font-bold text-xs uppercase tracking-wider text-tg-primary">
            2. Quantitative Forensic Ledger Metrics
          </h3>
          <div className="grid grid-cols-4 gap-3 font-mono">
            <div className="p-3 bg-slate-50 border border-slate-200 rounded">
              <span className="text-slate-400 text-[10px] block uppercase">Transactions</span>
              <span className="text-base font-bold text-slate-800">{stats.total_transactions}</span>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded">
              <span className="text-slate-400 text-[10px] block uppercase">Total Volume</span>
              <span className="text-sm font-bold text-slate-800">₹{stats.total_volume?.toLocaleString('en-IN')}</span>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded">
              <span className="text-slate-400 text-[10px] block uppercase">Flagged Entries</span>
              <span className="text-base font-bold text-tg-critical">{stats.flagged_transactions}</span>
            </div>
            <div className="p-3 bg-slate-50 border border-slate-200 rounded">
              <span className="text-slate-400 text-[10px] block uppercase">Suspicious Volume</span>
              <span className="text-sm font-bold text-tg-critical">₹{stats.flagged_volume?.toLocaleString('en-IN')}</span>
            </div>
          </div>
        </div>

        {/* Section 3: Statutory Verification Limitations */}
        <div className="space-y-2">
          <h3 className="font-bold text-xs uppercase tracking-wider text-tg-primary">
            3. Evidentiary Integrity & Statutory Limitations Notice
          </h3>
          <div className="bg-slate-50 border border-slate-200 rounded p-3 text-slate-600 text-[11px] leading-relaxed italic space-y-1">
            <p>
              This investigation dossier is generated automatically by TRACEGRID (Team CyboShield) for the Rajasthan Police Hackathon 2026.
            </p>
            <p>
              All anomaly scores, mule flow tags, and circular hop detections represent algorithmic intelligence leads synthesized from bank records. 
              No finding in this dossier constitutes autonomous proof of guilt. Sworn human officer verification, formal Section 91 CrPC requisitions, 
              and certified core-banking certificates under Section 65B of the Indian Evidence Act are required before trial submission.
            </p>
          </div>
        </div>

        {/* Footer Signature Block */}
        <div className="pt-6 border-t border-slate-200 grid grid-cols-2 gap-8 text-[11px] font-mono">
          <div>
            <span className="text-slate-400 block mb-4">PREPARED BY:</span>
            <div className="border-b border-slate-400 pb-1 mb-1 font-bold text-slate-800">
              {c.lead_investigator}
            </div>
            <span className="text-slate-500">Authorized Investigating Officer</span>
          </div>

          <div>
            <span className="text-slate-400 block mb-4">SYSTEM GENERATION AUDIT:</span>
            <div className="border-b border-slate-400 pb-1 mb-1 font-bold text-slate-800">
              TRACEGRID Engine v1.0 [SHA256 Certified]
            </div>
            <span className="text-slate-500">Timestamp: {new Date().toUTCString()}</span>
          </div>
        </div>
      </div>
    </div>
  );
}

