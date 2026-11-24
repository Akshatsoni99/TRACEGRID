'use client';

import React, { useEffect, useState } from 'react';
import {
  ListFilter,
  Search,
  AlertTriangle,
  ArrowRight,
  Info,
  ShieldAlert,
  ChevronDown,
  ChevronRight,
  RefreshCw,
  Sparkles
} from 'lucide-react';
import { Transaction } from '@/lib/types';
import { fetchTransactions } from '@/lib/api';

interface TransactionAnalysisViewProps {
  selectedCaseId: string;
}

export default function TransactionAnalysisView({ selectedCaseId }: TransactionAnalysisViewProps) {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Filters
  const [riskFilter, setRiskFilter] = useState('ALL');
  const [searchAccount, setSearchAccount] = useState('');
  const [minAmount, setMinAmount] = useState<string>('');
  const [expandedTxId, setExpandedTxId] = useState<string | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetchTransactions({
        case_id: selectedCaseId,
        risk_flag: riskFilter,
        min_amount: minAmount ? parseFloat(minAmount) : undefined,
        account: searchAccount || undefined,
      });
      setTransactions(res);
    } catch (err: any) {
      setError(err.message || 'Failed to load transactions');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedCaseId, riskFilter]);

  const handleApplyFilters = (e: React.FormEvent) => {
    e.preventDefault();
    loadData();
  };

  const getRiskBadge = (flag: string) => {
    switch (flag) {
      case 'CIRCULAR_HOP':
        return (
          <span className="bg-purple-100 text-purple-800 border border-purple-200 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider font-mono">
            CIRCULAR HOP
          </span>
        );
      case 'MULE_INDICATOR':
        return (
          <span className="bg-indigo-100 text-indigo-800 border border-indigo-200 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider font-mono">
            MULE CONDUIT
          </span>
        );
      case 'HIGH_RISK':
        return (
          <span className="bg-rose-100 text-rose-800 border border-rose-200 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider font-mono">
            HIGH ANOMALY
          </span>
        );
      case 'SUSPICIOUS':
        return (
          <span className="bg-amber-100 text-amber-800 border border-amber-200 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider font-mono">
            SUSPICIOUS
          </span>
        );
      default:
        return (
          <span className="bg-slate-100 text-slate-600 border border-slate-200 px-2 py-0.5 rounded text-[10px] font-medium uppercase font-mono">
            NORMAL
          </span>
        );
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-5">
      {/* Statutory Guidance Banner */}
      <div className="bg-slate-50 border border-slate-200 rounded px-4 py-3 flex items-start space-x-3 text-xs text-slate-700">
        <Info className="w-4 h-4 text-tg-primary flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <strong className="text-tg-primary">EXPLAINABLE ANOMALY RATIONALE: </strong>
          Anomaly scores evaluate statistical divergence from empirical banking baselines. 
          They reflect heuristic criteria (nocturnal velocity, round-sum structuring, closed graph cycles). 
          Never present an anomaly score as a probability of criminal culpability.
        </div>
      </div>

      {/* Filter Toolbar */}
      <form
        onSubmit={handleApplyFilters}
        className="bg-white p-4 rounded border border-tg-border shadow-sm flex flex-wrap items-center gap-3 text-xs"
      >
        <div className="flex items-center space-x-2">
          <span className="font-semibold text-slate-700">Risk Filter:</span>
          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="border border-slate-300 rounded px-2.5 py-1.5 focus:outline-none focus:border-tg-primary bg-white text-slate-700 font-medium"
          >
            <option value="ALL">All Transactions</option>
            <option value="HIGH_RISK">High Anomaly (IsolationForest)</option>
            <option value="MULE_INDICATOR">Mule Conduit Profiles</option>
            <option value="CIRCULAR_HOP">Circular Closed Cycles</option>
            <option value="SUSPICIOUS">Suspicious Rule Hits</option>
            <option value="NORMAL">Normal Transactions</option>
          </select>
        </div>

        <div className="flex items-center space-x-2 flex-1 min-w-[200px]">
          <span className="font-semibold text-slate-700">Account:</span>
          <div className="relative flex-1">
            <input
              type="text"
              placeholder="Filter by Account Number..."
              value={searchAccount}
              onChange={(e) => setSearchAccount(e.target.value)}
              className="w-full px-2.5 py-1.5 border border-slate-300 rounded font-mono text-xs focus:outline-none focus:border-tg-primary"
            />
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <span className="font-semibold text-slate-700">Min Amount (₹):</span>
          <input
            type="number"
            placeholder="e.g. 50000"
            value={minAmount}
            onChange={(e) => setMinAmount(e.target.value)}
            className="w-28 px-2.5 py-1.5 border border-slate-300 rounded font-mono text-xs focus:outline-none focus:border-tg-primary"
          />
        </div>

        <button
          type="submit"
          className="px-4 py-1.5 bg-tg-primary text-white rounded font-medium hover:bg-tg-primaryHover shadow-sm"
        >
          Apply Filters
        </button>

        <button
          type="button"
          onClick={() => {
            setRiskFilter('ALL');
            setSearchAccount('');
            setMinAmount('');
            loadData();
          }}
          className="px-3 py-1.5 border border-slate-300 rounded text-slate-600 hover:bg-slate-50"
        >
          Reset
        </button>
      </form>

      {/* Transactions Data Table */}
      <div className="bg-white border border-tg-border rounded shadow-sm overflow-hidden">
        <div className="px-5 py-3 border-b border-tg-border flex items-center justify-between bg-slate-50">
          <div className="flex items-center space-x-2">
            <ListFilter className="w-4 h-4 text-tg-primary" />
            <h3 className="font-bold text-xs text-tg-text uppercase tracking-wider">
              Transaction Records ({transactions.length} entries)
            </h3>
          </div>
          <span className="text-[11px] font-mono text-slate-500">
            Click row to view explainable flag rationale
          </span>
        </div>

        {loading ? (
          <div className="p-8 text-center text-slate-500 text-xs flex items-center justify-center space-x-2">
            <RefreshCw className="w-4 h-4 animate-spin text-tg-primary" />
            <span>Scanning transaction anomalies...</span>
          </div>
        ) : transactions.length === 0 ? (
          <div className="p-8 text-center text-slate-500 text-xs">
            No transactions match the selected filter criteria for this investigation case.
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50/80 border-b border-tg-border text-slate-500 font-medium">
                <tr>
                  <th className="px-4 py-2.5 w-8"></th>
                  <th className="px-4 py-2.5">Tx ID / Timestamp</th>
                  <th className="px-4 py-2.5">Sender Account</th>
                  <th className="px-4 py-2.5">Beneficiary Account</th>
                  <th className="px-4 py-2.5">Amount (INR)</th>
                  <th className="px-4 py-2.5">Method</th>
                  <th className="px-4 py-2.5">Risk Indicator</th>
                  <th className="px-4 py-2.5 text-right">Anomaly Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {transactions.map((t) => {
                  const isExpanded = expandedTxId === t.id;
                  const reasons = Array.isArray(t.flag_reasons) ? t.flag_reasons : [];
                  const isHighAnomaly = t.risk_flag !== 'NORMAL';

                  return (
                    <React.Fragment key={t.id}>
                      <tr
                        onClick={() => setExpandedTxId(isExpanded ? null : t.id)}
                        className={`cursor-pointer transition-colors ${
                          isExpanded
                            ? 'bg-sky-50/50'
                            : isHighAnomaly
                            ? 'hover:bg-rose-50/30'
                            : 'hover:bg-slate-50'
                        }`}
                      >
                        <td className="px-4 py-3 text-slate-400">
                          {isExpanded ? (
                            <ChevronDown className="w-3.5 h-3.5 text-tg-primary" />
                          ) : (
                            <ChevronRight className="w-3.5 h-3.5" />
                          )}
                        </td>
                        <td className="px-4 py-3">
                          <span className="font-mono font-semibold text-slate-800 block">
                            {t.id}
                          </span>
                          <span className="text-[11px] text-slate-400 font-mono">
                            {new Date(t.timestamp).toLocaleString('en-GB', {
                              dateStyle: 'short',
                              timeStyle: 'medium',
                            })}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <span className="font-mono text-slate-800 block font-medium">
                            {t.sender_account}
                          </span>
                          <span className="text-[11px] text-slate-500">{t.sender_name}</span>
                        </td>
                        <td className="px-4 py-3">
                          <span className="font-mono text-slate-800 block font-medium">
                            {t.receiver_account}
                          </span>
                          <span className="text-[11px] text-slate-500">{t.receiver_name}</span>
                        </td>
                        <td className="px-4 py-3 font-mono">
                          <span className="font-bold text-tg-text block">
                            ₹{t.amount.toLocaleString('en-IN', { maximumFractionDigits: 2 })}
                          </span>
                          <span className="text-[10px] text-slate-400">{t.transaction_type}</span>
                        </td>
                        <td className="px-4 py-3 font-mono text-[11px]">
                          <span className="bg-slate-100 text-slate-700 px-1.5 py-0.5 rounded border border-slate-200">
                            {t.detection_method}
                          </span>
                        </td>
                        <td className="px-4 py-3">{getRiskBadge(t.risk_flag)}</td>
                        <td className="px-4 py-3 text-right font-mono">
                          <span
                            className={`font-bold ${
                              t.anomaly_score >= 0.8
                                ? 'text-tg-critical'
                                : t.anomaly_score >= 0.5
                                ? 'text-tg-warning'
                                : 'text-slate-500'
                            }`}
                          >
                            {t.anomaly_score > 0 ? `${t.anomaly_score.toFixed(2)}/1.00` : '—'}
                          </span>
                        </td>
                      </tr>

                      {/* Expandable Explanation Drawer */}
                      {isExpanded && (
                        <tr className="bg-sky-50/40">
                          <td colSpan={8} className="px-6 py-3.5 border-t border-sky-100">
                            <div className="space-y-2">
                              <div className="flex items-center space-x-2 text-xs font-bold text-tg-primary">
                                <Sparkles className="w-3.5 h-3.5" />
                                <span>Algorithmic Lead Rationale & Triggers:</span>
                              </div>
                              {reasons.length > 0 ? (
                                <ul className="list-disc list-inside space-y-1 text-xs text-slate-700 pl-1">
                                  {reasons.map((r, i) => (
                                    <li key={i} className="font-medium">
                                      {r}
                                    </li>
                                  ))}
                                </ul>
                              ) : (
                                <p className="text-xs text-slate-500 italic">
                                  Transaction within standard behavioral parameters. No rule or ML
                                  threshold triggered.
                                </p>
                              )}
                              <div className="flex items-center justify-between text-[11px] text-slate-500 pt-2 border-t border-sky-100/60 font-mono">
                                <span>Ref UTR: {t.reference_number || 'N/A'}</span>
                                <span>Narration: &ldquo;{t.description || 'N/A'}&rdquo;</span>
                              </div>
                            </div>
                          </td>
                        </tr>
                      )}
                    </React.Fragment>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

