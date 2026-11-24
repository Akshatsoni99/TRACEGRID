'use client';

import React, { useEffect, useState } from 'react';
import {
  GitCompare,
  Link2,
  Building,
  Globe2,
  AlertTriangle,
  CheckCircle2,
  ArrowRight,
  ShieldAlert,
  RefreshCw,
  FolderOpen
} from 'lucide-react';
import { CrossCaseMatch } from '@/lib/types';
import { fetchCrossCaseCorrelations } from '@/lib/api';

interface CrossCaseViewProps {
  selectedCaseId: string;
  onSelectCase: (caseId: string) => void;
  onNavigate: (view: string) => void;
}

export default function CrossCaseView({
  selectedCaseId,
  onSelectCase,
  onNavigate,
}: CrossCaseViewProps) {
  const [correlations, setCorrelations] = useState<CrossCaseMatch[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filterMode, setFilterMode] = useState<'ALL' | 'ACTIVE_ONLY'>('ACTIVE_ONLY');

  const loadCorrelations = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCrossCaseCorrelations(filterMode === 'ACTIVE_ONLY' ? selectedCaseId : undefined);
      setCorrelations(data.correlations || []);
    } catch (err: any) {
      setError(err.message || 'Failed to load cross-case correlations');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadCorrelations();
  }, [selectedCaseId, filterMode]);

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-5xl mx-auto">
      {/* Evidence Separation Banner */}
      <div className="bg-slate-50 border border-slate-200 rounded p-4 flex items-start space-x-3 text-xs text-slate-700">
        <ShieldAlert className="w-4 h-4 text-tg-primary flex-shrink-0 mt-0.5" />
        <div className="flex-1 space-y-1">
          <p className="font-semibold text-tg-primary">
            EVIDENTIARY DISTINCTION: CONFIRMED MATCHES VS. ANALYTICAL ASSOCIATIONS
          </p>
          <p>
            - <strong className="text-emerald-800">CONFIRMED DATA MATCH (100%):</strong> Explicit identity match on exact account numbers across bank statements under Section 91 CrPC.<br/>
            - <strong className="text-amber-800">ANALYTICAL INFRASTRUCTURE ASSOCIATION:</strong> Shared bulletproof hosting ASNs, reverse DNS resolvers, or proxy IP clusters indicating possible common toolkits or syndicates.
          </p>
        </div>
      </div>

      {/* Control Bar */}
      <div className="bg-white border border-tg-border rounded p-4 shadow-sm flex items-center justify-between">
        <div>
          <h2 className="text-sm font-bold text-tg-text">Cross-Case Correlation Engine</h2>
          <p className="text-xs text-tg-secondary">
            Cross-referencing {correlations.length} multi-case syndicate intersections
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setFilterMode('ACTIVE_ONLY')}
            className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
              filterMode === 'ACTIVE_ONLY'
                ? 'bg-tg-primary text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            Intersecting Current Case
          </button>
          <button
            onClick={() => setFilterMode('ALL')}
            className={`px-3 py-1.5 rounded text-xs font-medium transition-colors ${
              filterMode === 'ALL'
                ? 'bg-tg-primary text-white'
                : 'bg-slate-100 text-slate-700 hover:bg-slate-200'
            }`}
          >
            All Database Cases
          </button>
        </div>
      </div>

      {/* Correlation Cards */}
      {loading ? (
        <div className="p-12 text-center text-slate-500 text-xs flex items-center justify-center space-x-2">
          <RefreshCw className="w-4 h-4 animate-spin text-tg-primary" />
          <span>Cross-indexing multi-case identifiers...</span>
        </div>
      ) : correlations.length === 0 ? (
        <div className="bg-white border border-tg-border rounded p-8 text-center text-slate-500 text-xs">
          No cross-case commonalities detected for the selected filter.
        </div>
      ) : (
        <div className="space-y-4">
          {correlations.map((match, idx) => {
            const isConfirmed = match.match_type === 'CONFIRMED_DATA_MATCH';

            return (
              <div
                key={idx}
                className={`bg-white rounded border shadow-sm p-5 space-y-4 transition-all ${
                  isConfirmed ? 'border-emerald-300 ring-1 ring-emerald-100' : 'border-amber-300'
                }`}
              >
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2.5">
                    <div
                      className={`w-8 h-8 rounded flex items-center justify-center ${
                        isConfirmed
                          ? 'bg-emerald-50 text-emerald-700'
                          : 'bg-amber-50 text-amber-700'
                      }`}
                    >
                      {match.indicator_type === 'BANK_ACCOUNT' ? (
                        <Building className="w-4 h-4" />
                      ) : (
                        <Globe2 className="w-4 h-4" />
                      )}
                    </div>
                    <div>
                      <span className="text-[10px] font-mono uppercase tracking-wider text-slate-400 font-bold block">
                        {match.indicator_type} INTERSECTION
                      </span>
                      <h3 className="font-mono text-sm font-bold text-slate-900">
                        {match.indicator_value}
                      </h3>
                    </div>
                  </div>

                  <span
                    className={`text-[10px] font-bold px-2.5 py-1 rounded font-mono ${
                      isConfirmed
                        ? 'bg-emerald-100 text-emerald-800 border border-emerald-200'
                        : 'bg-amber-100 text-amber-800 border border-amber-200'
                    }`}
                  >
                    {match.match_type}
                  </span>
                </div>

                {/* Description */}
                <p className="text-xs text-slate-700 leading-relaxed font-medium">
                  {match.description}
                </p>

                {/* Matched Cases Grid */}
                <div>
                  <span className="text-[10px] font-mono text-slate-400 uppercase tracking-wider block mb-2 font-semibold">
                    Corroborating Investigation Records ({match.matched_cases.length} cases):
                  </span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    {match.matched_cases.map((mc, mIdx) => (
                      <div
                        key={mIdx}
                        className="p-3 rounded bg-slate-50 border border-slate-200 flex items-center justify-between text-xs"
                      >
                        <div>
                          <span className="font-mono font-bold text-slate-800 block">
                            {mc.case_number}
                          </span>
                          <span className="text-slate-600 truncate block max-w-[200px]">
                            {mc.case_title}
                          </span>
                          {mc.holder && (
                            <span className="text-[10px] text-slate-400 font-mono block">
                              Holder: {mc.holder} ({mc.bank})
                            </span>
                          )}
                        </div>

                        <button
                          onClick={() => {
                            onSelectCase(mc.case_id);
                            onNavigate('graph');
                          }}
                          className="px-2 py-1 text-[11px] bg-white border border-slate-300 rounded text-tg-primary font-medium hover:bg-slate-100 flex items-center space-x-1"
                        >
                          <span>Open</span>
                          <ArrowRight className="w-3 h-3" />
                        </button>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Confidence Bar */}
                <div className="pt-2 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-500">
                  <span>Confidence Metric:</span>
                  <span className="font-mono font-bold text-slate-700">
                    {match.correlation_confidence}
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

