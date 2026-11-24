'use client';

import React, { useState } from 'react';
import {
  Briefcase,
  Plus,
  Search,
  ExternalLink,
  FileDown,
  CheckCircle2,
  Clock,
  AlertCircle,
  FolderOpen
} from 'lucide-react';
import { Investigation } from '@/lib/types';
import { createCase, getReportDownloadUrl } from '@/lib/api';

interface InvestigationsViewProps {
  cases: Investigation[];
  selectedCaseId: string;
  onSelectCase: (caseId: string) => void;
  onNavigate: (view: string) => void;
  onRefresh: () => void;
}

export default function InvestigationsView({
  cases,
  selectedCaseId,
  onSelectCase,
  onNavigate,
  onRefresh,
}: InvestigationsViewProps) {
  const [search, setSearch] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('ALL');
  const [isModalOpen, setIsModalOpen] = useState(false);

  // New Case Form State
  const [caseNumber, setCaseNumber] = useState('');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('HIGH');
  const [leadInvestigator, setLeadInvestigator] = useState('Insp. Vikram Rathore (Cyber Crime EOW)');
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState<string | null>(null);

  const filteredCases = cases.filter((c) => {
    const matchesSearch =
      c.case_number.toLowerCase().includes(search.toLowerCase()) ||
      c.title.toLowerCase().includes(search.toLowerCase()) ||
      c.lead_investigator.toLowerCase().includes(search.toLowerCase());
    const matchesPriority = priorityFilter === 'ALL' || c.priority === priorityFilter;
    return matchesSearch && matchesPriority;
  });

  const handleCreateCase = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!caseNumber.trim() || !title.trim()) {
      setFormError('Case reference number and title are required.');
      return;
    }
    setSubmitting(true);
    setFormError(null);
    try {
      const newCase = await createCase({
        case_number: caseNumber.trim(),
        title: title.trim(),
        description: description.trim(),
        priority,
        lead_investigator: leadInvestigator.trim(),
      });
      setIsModalOpen(false);
      setCaseNumber('');
      setTitle('');
      setDescription('');
      onRefresh();
      onSelectCase(newCase.id);
    } catch (err: any) {
      setFormError(err.message || 'Failed to create case');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6">
      {/* Top Filter & Creation Action Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-4 rounded border border-tg-border shadow-sm">
        <div className="flex items-center space-x-3 flex-1">
          <div className="relative flex-1 max-w-sm">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search case reference, title, investigator..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded border border-slate-300 focus:outline-none focus:border-tg-primary"
            />
          </div>

          <select
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
            className="text-xs border border-slate-300 rounded px-2.5 py-1.5 focus:outline-none focus:border-tg-primary text-slate-700 bg-white"
          >
            <option value="ALL">All Priorities</option>
            <option value="CRITICAL">Critical Priority</option>
            <option value="HIGH">High Priority</option>
            <option value="MEDIUM">Medium Priority</option>
            <option value="LOW">Low Priority</option>
          </select>
        </div>

        <button
          onClick={() => setIsModalOpen(true)}
          className="flex items-center justify-center space-x-1.5 px-3 py-1.5 rounded text-xs font-medium text-white bg-tg-primary hover:bg-tg-primaryHover shadow-sm transition-colors"
        >
          <Plus className="w-4 h-4" />
          <span>New Investigation Case</span>
        </button>
      </div>

      {/* Cases Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {filteredCases.map((c) => {
          const isSelected = c.id === selectedCaseId;
          return (
            <div
              key={c.id}
              className={`bg-white rounded border transition-all shadow-sm flex flex-col justify-between ${
                isSelected
                  ? 'border-tg-primary ring-1 ring-tg-primary'
                  : 'border-tg-border hover:border-slate-300'
              }`}
            >
              <div className="p-4">
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div>
                    <span className="font-mono text-xs font-bold text-slate-800 bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                      {c.case_number}
                    </span>
                    <h3 className="font-bold text-sm text-tg-text mt-2 line-clamp-1">{c.title}</h3>
                  </div>
                  <span
                    className={`text-[10px] font-bold px-1.5 py-0.5 rounded uppercase ${
                      c.priority === 'CRITICAL'
                        ? 'bg-rose-100 text-rose-700 border border-rose-200'
                        : 'bg-amber-100 text-amber-700 border border-amber-200'
                    }`}
                  >
                    {c.priority}
                  </span>
                </div>

                <p className="text-xs text-tg-secondary mt-2 line-clamp-2 leading-relaxed">
                  {c.description || 'Comprehensive financial intelligence and ledger analysis.'}
                </p>

                {/* Metrics */}
                <div className="mt-4 pt-3 border-t border-slate-100 grid grid-cols-2 gap-2 text-xs">
                  <div>
                    <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                      Total Ledger Flow
                    </span>
                    <span className="font-mono font-semibold text-slate-800">
                      ₹{(c.total_amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                    </span>
                  </div>
                  <div>
                    <span className="text-[10px] text-slate-400 uppercase tracking-wider block">
                      Suspicious Volume
                    </span>
                    <span className="font-mono font-semibold text-tg-critical">
                      ₹{(c.flagged_amount || 0).toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                    </span>
                  </div>
                </div>

                {/* Sub-info */}
                <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400">
                  <span>Transactions: {c.transaction_count || 0}</span>
                  <span>Status: <strong className="text-emerald-700">{c.status}</strong></span>
                </div>
              </div>

              {/* Card Footer Actions */}
              <div className="bg-slate-50 px-4 py-2.5 border-t border-slate-100 flex items-center justify-between text-xs">
                <button
                  onClick={() => {
                    onSelectCase(c.id);
                    onNavigate('graph');
                  }}
                  className="font-medium text-tg-primary hover:text-tg-primaryHover flex items-center space-x-1"
                >
                  <FolderOpen className="w-3.5 h-3.5" />
                  <span>Open in Graph</span>
                </button>

                <div className="flex items-center space-x-2">
                  <button
                    onClick={() => {
                      onSelectCase(c.id);
                      onNavigate('transactions');
                    }}
                    className="text-slate-600 hover:text-slate-900 font-medium"
                  >
                    Ledger
                  </button>
                  <span className="text-slate-300">|</span>
                  <a
                    href={getReportDownloadUrl(c.id)}
                    target="_blank"
                    rel="noreferrer"
                    className="text-slate-600 hover:text-tg-primary flex items-center space-x-1 font-medium"
                  >
                    <FileDown className="w-3.5 h-3.5" />
                    <span>PDF</span>
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Create Case Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 bg-slate-900/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-white rounded-lg border border-slate-200 shadow-xl max-w-lg w-full overflow-hidden">
            <div className="px-5 py-4 border-b border-slate-200 flex items-center justify-between bg-slate-50">
              <div className="flex items-center space-x-2">
                <Briefcase className="w-4 h-4 text-tg-primary" />
                <h3 className="font-bold text-sm text-tg-text">Initiate New Investigation Dossier</h3>
              </div>
              <button
                onClick={() => setIsModalOpen(false)}
                className="text-slate-400 hover:text-slate-600 text-lg leading-none"
              >
                &times;
              </button>
            </div>

            <form onSubmit={handleCreateCase} className="p-5 space-y-4 text-xs">
              {formError && (
                <div className="p-2.5 rounded bg-rose-50 border border-rose-200 text-rose-700">
                  {formError}
                </div>
              )}

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  Case Reference Number (FIR / Subpoena Ref) *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. RJ-POL-EOW-2026-0099"
                  value={caseNumber}
                  onChange={(e) => setCaseNumber(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded font-mono focus:outline-none focus:border-tg-primary"
                />
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  Investigation Title *
                </label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Operation Thar-Shield: Hawala Diversion"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded focus:outline-none focus:border-tg-primary"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Priority Level</label>
                  <select
                    value={priority}
                    onChange={(e) => setPriority(e.target.value)}
                    className="w-full px-2.5 py-2 border border-slate-300 rounded focus:outline-none focus:border-tg-primary bg-white"
                  >
                    <option value="CRITICAL">Critical (High Volume / Threat)</option>
                    <option value="HIGH">High (Active Layering)</option>
                    <option value="MEDIUM">Medium</option>
                    <option value="LOW">Low</option>
                  </select>
                </div>
                <div>
                  <label className="block font-semibold text-slate-700 mb-1">Lead Investigator</label>
                  <input
                    type="text"
                    value={leadInvestigator}
                    onChange={(e) => setLeadInvestigator(e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded focus:outline-none focus:border-tg-primary"
                  />
                </div>
              </div>

              <div>
                <label className="block font-semibold text-slate-700 mb-1">
                  Case Brief & Evidentiary Scope
                </label>
                <textarea
                  rows={3}
                  placeholder="Provide context regarding reported victim transactions, alleged layering modus operandi..."
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  className="w-full px-3 py-2 border border-slate-300 rounded focus:outline-none focus:border-tg-primary"
                />
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="px-3 py-1.5 border border-slate-300 rounded text-slate-600 hover:bg-slate-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-1.5 bg-tg-primary text-white rounded font-medium hover:bg-tg-primaryHover shadow-sm flex items-center space-x-1"
                >
                  <span>{submitting ? 'Registering...' : 'Register Investigation'}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

