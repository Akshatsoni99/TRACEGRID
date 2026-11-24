'use client';

import React, { useEffect, useState } from 'react';
import {
  ShieldAlert,
  AlertTriangle,
  TrendingUp,
  CreditCard,
  Briefcase,
  Users,
  ArrowUpRight,
  ArrowDownLeft,
  CheckCircle2,
  ExternalLink,
  RefreshCw,
  Info
} from 'lucide-react';
import { DashboardOverviewData } from '@/lib/types';
import { fetchDashboardOverview } from '@/lib/api';

interface OverviewViewProps {
  onSelectCase: (caseId: string) => void;
  onNavigate: (view: string) => void;
}

export default function OverviewView({ onSelectCase, onNavigate }: OverviewViewProps) {
  const [data, setData] = useState<DashboardOverviewData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchDashboardOverview();
      setData(res);
    } catch (err: any) {
      setError(err.message || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  if (loading) {
    return (
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="flex items-center space-x-2 text-slate-500 text-sm">
          <RefreshCw className="w-4 h-4 animate-spin text-tg-primary" />
          <span>Aggregating financial forensic metrics...</span>
        </div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex-1 p-8 flex items-center justify-center">
        <div className="bg-rose-50 border border-rose-200 text-rose-700 px-4 py-3 rounded text-sm max-w-md">
          <p className="font-semibold">Unable to connect to TRACEGRID Analytics Engine</p>
          <p className="text-xs mt-1 text-rose-600">{error}</p>
          <button
            onClick={loadData}
            className="mt-3 px-3 py-1 bg-rose-600 text-white rounded text-xs hover:bg-rose-700"
          >
            Retry Connection
          </button>
        </div>
      </div>
    );
  }

  // Calculate percentages
  const totalTx = data.total_transactions_analyzed || 1;
  const flaggedRatio = ((data.total_suspicious_flagged / totalTx) * 100).toFixed(1);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6">
      {/* Human Verification Statutory Banner */}
      <div className="bg-amber-50/80 border border-amber-200/80 rounded px-4 py-2.5 flex items-start space-x-3 text-xs text-amber-900">
        <ShieldAlert className="w-4 h-4 text-amber-600 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <span className="font-semibold text-amber-800">INVESTIGATIVE INTEGRITY DIRECTIVE: </span>
          Risk indicators, anomaly scores and mule profile tags are algorithmic intelligence leads to guide human inquiry. 
          No score autonomously establishes criminal liability. Independent verification via Section 91 CrPC notices is mandatory.
        </div>
      </div>

      {/* Top Forensic KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Card 1: Total Volume */}
        <div className="bg-white border border-tg-border rounded p-4 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-tg-secondary">Total Processed Volume</span>
            <div className="w-7 h-7 rounded bg-slate-100 flex items-center justify-center text-tg-primary">
              <CreditCard className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-2">
            <div className="text-xl font-bold font-mono text-tg-text">
              ₹{data.total_volume_analyzed.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
            </div>
            <p className="text-[11px] text-tg-secondary mt-0.5">
              Across {data.total_transactions_analyzed} parsed ledger entries
            </p>
          </div>
        </div>

        {/* Card 2: Suspicious Volume */}
        <div className="bg-white border border-tg-border rounded p-4 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-tg-secondary">Suspicious / Flagged Flow</span>
            <div className="w-7 h-7 rounded bg-rose-50 flex items-center justify-center text-tg-critical">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-2">
            <div className="text-xl font-bold font-mono text-tg-critical">
              ₹{data.total_suspicious_volume.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
            </div>
            <p className="text-[11px] text-rose-600 mt-0.5">
              {data.total_suspicious_flagged} transactions ({flaggedRatio}% anomaly rate)
            </p>
          </div>
        </div>

        {/* Card 3: Target Accounts under Review */}
        <div className="bg-white border border-tg-border rounded p-4 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-tg-secondary">High-Priority Mule Candidates</span>
            <div className="w-7 h-7 rounded bg-amber-50 flex items-center justify-center text-tg-warning">
              <Users className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-2">
            <div className="text-xl font-bold font-mono text-tg-text">
              {data.accounts_requiring_review}
            </div>
            <p className="text-[11px] text-tg-secondary mt-0.5">
              Rapid throughput & circular conduits
            </p>
          </div>
        </div>

        {/* Card 4: Active Investigations */}
        <div className="bg-white border border-tg-border rounded p-4 shadow-sm flex flex-col justify-between">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-tg-secondary">Active Case Dossiers</span>
            <div className="w-7 h-7 rounded bg-blue-50 flex items-center justify-center text-tg-primary">
              <Briefcase className="w-4 h-4" />
            </div>
          </div>
          <div className="mt-2">
            <div className="text-xl font-bold font-mono text-tg-text">
              {data.total_investigations}
            </div>
            <p className="text-[11px] text-tg-primary font-medium mt-0.5">
              {data.high_priority_cases} prioritized as Critical / High
            </p>
          </div>
        </div>
      </div>

      {/* Middle Row: Risk Distribution & Daily Volume Breakdown */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution Box */}
        <div className="bg-white border border-tg-border rounded p-5 shadow-sm">
          <h2 className="text-sm font-bold text-tg-text mb-1">Transaction Risk Distribution</h2>
          <p className="text-xs text-tg-secondary mb-4">
            Classification breakdown across loaded investigative records
          </p>

          <div className="space-y-3">
            {[
              {
                label: 'Normal Flow',
                count: data.risk_distribution.NORMAL || 0,
                color: 'bg-emerald-500',
                border: 'border-emerald-200',
              },
              {
                label: 'High-Value / Structuring Spike',
                count: data.risk_distribution.SUSPICIOUS || 0,
                color: 'bg-amber-500',
                border: 'border-amber-200',
              },
              {
                label: 'Statistical ML Anomaly (IsolationForest)',
                count: data.risk_distribution.HIGH_RISK || 0,
                color: 'bg-rose-500',
                border: 'border-rose-200',
              },
              {
                label: 'Pass-Through Mule Indicator',
                count: data.risk_distribution.MULE_INDICATOR || 0,
                color: 'bg-indigo-600',
                border: 'border-indigo-200',
              },
              {
                label: 'Closed Circular Hop (Wash Layering)',
                count: data.risk_distribution.CIRCULAR_HOP || 0,
                color: 'bg-purple-600',
                border: 'border-purple-200',
              },
            ].map((item) => {
              const pct = ((item.count / totalTx) * 100).toFixed(1);
              return (
                <div key={item.label} className="space-y-1">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="text-slate-700">{item.label}</span>
                    <span className="font-mono text-slate-500">
                      {item.count} <span className="text-[10px] text-slate-400">({pct}%)</span>
                    </span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div
                      className={`${item.color} h-2 rounded-full transition-all duration-500`}
                      style={{ width: `${Math.max(parseFloat(pct), 2)}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>

          <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-tg-secondary">
            <span>Detection Framework:</span>
            <span className="font-mono font-medium text-tg-primary">Hybrid Rules + Scikit-Learn</span>
          </div>
        </div>

        {/* Timeline Volume Activity */}
        <div className="lg:col-span-2 bg-white border border-tg-border rounded p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-1">
              <h2 className="text-sm font-bold text-tg-text">Transaction Activity Timeline</h2>
              <span className="text-[11px] font-mono text-slate-500">Daily Aggregation</span>
            </div>
            <p className="text-xs text-tg-secondary mb-4">
              Temporal distribution highlighting off-hours and synchronized burst clusters
            </p>

            {/* Timeline Bars */}
            <div className="space-y-3">
              {data.timeline_activity.map((t) => {
                const maxVol = Math.max(...data.timeline_activity.map((a) => a.volume), 1);
                const barWidth = Math.min(100, Math.max(12, (t.volume / maxVol) * 100));

                return (
                  <div key={t.date} className="flex items-center space-x-3 text-xs">
                    <span className="w-24 font-mono text-slate-600 flex-shrink-0 text-[11px]">
                      {t.date}
                    </span>
                    <div className="flex-1 bg-slate-100 rounded h-6 relative overflow-hidden flex items-center">
                      <div
                        className="bg-tg-primary/80 h-full rounded transition-all flex items-center px-2"
                        style={{ width: `${barWidth}%` }}
                      >
                        <span className="text-[10px] font-mono text-white font-medium truncate">
                          ₹{t.volume.toLocaleString('en-IN', { maximumFractionDigits: 0 })}
                        </span>
                      </div>
                    </div>
                    <div className="w-20 text-right font-mono text-[11px] text-slate-500">
                      {t.count} txns
                      {t.flagged > 0 && (
                        <span className="text-rose-600 font-semibold ml-1">({t.flagged} ⚠)</span>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
            <span className="text-slate-500">Evidence Source: Core Banking Transaction Feeds</span>
            <button
              onClick={() => onNavigate('transactions')}
              className="text-tg-primary hover:text-tg-primaryHover font-medium flex items-center space-x-1"
            >
              <span>View All Transactions</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>

      {/* Priority Investigations Table */}
      <div className="bg-white border border-tg-border rounded shadow-sm overflow-hidden">
        <div className="px-5 py-4 border-b border-tg-border flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold text-tg-text">Active Priority Investigation Cases</h2>
            <p className="text-xs text-tg-secondary">
              Case dossiers loaded from persistent relational storage
            </p>
          </div>
          <button
            onClick={() => onNavigate('investigations')}
            className="text-xs font-medium text-tg-primary hover:text-tg-primaryHover flex items-center space-x-1"
          >
            <span>Manage All Cases</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-50 border-b border-tg-border text-slate-500 font-medium">
              <tr>
                <th className="px-4 py-2.5">Case Reference</th>
                <th className="px-4 py-2.5">Title & Scope</th>
                <th className="px-4 py-2.5">Priority</th>
                <th className="px-4 py-2.5">Status</th>
                <th className="px-4 py-2.5">Transactions</th>
                <th className="px-4 py-2.5">Suspicious Volume</th>
                <th className="px-4 py-2.5 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 text-slate-700">
              {data.recent_cases.map((c) => (
                <tr key={c.id} className="hover:bg-slate-50/75 transition-colors">
                  <td className="px-4 py-3 font-mono font-semibold text-slate-800">
                    {c.case_number}
                  </td>
                  <td className="px-4 py-3">
                    <p className="font-semibold text-tg-text">{c.title}</p>
                    <p className="text-[11px] text-slate-400 font-mono">Lead: {c.lead_investigator}</p>
                  </td>
                  <td className="px-4 py-3">
                    <span
                      className={`inline-block px-1.5 py-0.5 rounded text-[10px] font-bold uppercase ${
                        c.priority === 'CRITICAL'
                          ? 'bg-rose-100 text-rose-700 border border-rose-200'
                          : 'bg-amber-100 text-amber-700 border border-amber-200'
                      }`}
                    >
                      {c.priority}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="font-mono text-[11px] text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                      {c.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 font-mono">
                    {c.transaction_count} <span className="text-slate-400">({c.flagged_count} flagged)</span>
                  </td>
                  <td className="px-4 py-3 font-mono font-medium text-tg-critical">
                    ₹{c.total_volume.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button
                      onClick={() => {
                        onSelectCase(c.id);
                        onNavigate('graph');
                      }}
                      className="px-2.5 py-1 text-xs font-medium text-tg-primary hover:bg-slate-100 rounded border border-slate-200"
                    >
                      Open Graph
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

