'use client';

import React, { useEffect, useState } from 'react';
import {
  Globe2,
  Server,
  ShieldAlert,
  Search,
  ExternalLink,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  Clock,
  Layers,
  FileText
} from 'lucide-react';
import { DigitalIntelligence } from '@/lib/types';
import { fetchDigitalIntelligence, queryIntelLookup } from '@/lib/api';

interface DigitalIntelligenceViewProps {
  selectedCaseId: string;
}

export default function DigitalIntelligenceView({ selectedCaseId }: DigitalIntelligenceViewProps) {
  const [intelList, setIntelList] = useState<DigitalIntelligence[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Live lookup query state
  const [lookupQuery, setLookupQuery] = useState('');
  const [lookupType, setLookupType] = useState('AUTO');
  const [lookingUp, setLookingUp] = useState(false);
  const [lookupResult, setLookupResult] = useState<any | null>(null);

  const loadIntel = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchDigitalIntelligence(selectedCaseId);
      setIntelList(data);
    } catch (err: any) {
      setError(err.message || 'Failed to load intelligence records');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadIntel();
  }, [selectedCaseId]);

  const handleLookup = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!lookupQuery.trim()) return;
    setLookingUp(true);
    try {
      const res = await queryIntelLookup(lookupQuery.trim(), lookupType);
      setLookupResult(res);
    } catch (err: any) {
      alert(`Lookup failed: ${err.message}`);
    } finally {
      setLookingUp(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-6xl mx-auto">
      {/* Attribution & Verification Boundary Banner */}
      <div className="bg-amber-50/80 border border-amber-200/80 rounded px-4 py-3 flex items-start space-x-3 text-xs text-amber-900">
        <ShieldAlert className="w-4 h-4 text-amber-700 flex-shrink-0 mt-0.5" />
        <div className="flex-1">
          <strong className="text-amber-800">DIGITAL INTELLIGENCE ATTRIBUTION BOUNDARY: </strong>
          Domain, DNS, and IP records are gathered strictly via safe passive lookups and demonstrative synthetic threat archives. 
          TRACEGRID never invents real-world attribution, ownership or criminal associations. Every record below displays its source, 
          retrieval timestamp, and verification status.
        </div>
      </div>

      {/* Interactive Passive Lookup Console */}
      <div className="bg-white border border-tg-border rounded p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-2 border-b border-slate-100">
          <div>
            <h2 className="text-sm font-bold text-tg-text">Passive Infrastructure Lookup Console</h2>
            <p className="text-xs text-tg-secondary">
              Query DNS records, ASN routing, WHOIS creation dates and bulletproof hosting signatures
            </p>
          </div>
          <span className="text-[11px] font-mono bg-sky-50 text-tg-primary px-2 py-0.5 rounded border border-sky-200 font-semibold">
            ADAPTER: PASSIVE RESOLVER
          </span>
        </div>

        <form onSubmit={handleLookup} className="flex flex-wrap items-center gap-3">
          <div className="relative flex-1 min-w-[240px]">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="e.g. fast-payout-gateway.cc or 185.220.101.44"
              value={lookupQuery}
              onChange={(e) => setLookupQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded border border-slate-300 focus:outline-none focus:border-tg-primary font-mono"
            />
          </div>

          <select
            value={lookupType}
            onChange={(e) => setLookupType(e.target.value)}
            className="text-xs border border-slate-300 rounded px-2.5 py-1.5 focus:outline-none focus:border-tg-primary bg-white text-slate-700"
          >
            <option value="AUTO">Auto Detect Indicator</option>
            <option value="DOMAIN">Domain Name</option>
            <option value="IP_ADDRESS">IP Address / ASN</option>
          </select>

          <button
            type="submit"
            disabled={lookingUp || !lookupQuery.trim()}
            className="px-4 py-1.5 bg-tg-primary text-white rounded text-xs font-semibold hover:bg-tg-primaryHover shadow-sm flex items-center space-x-1.5 disabled:bg-slate-300"
          >
            {lookingUp ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Querying...</span>
              </>
            ) : (
              <>
                <Globe2 className="w-3.5 h-3.5" />
                <span>Execute Passive Lookup</span>
              </>
            )}
          </button>
        </form>

        {/* Live Lookup Result Display */}
        {lookupResult && (
          <div className="mt-3 p-4 bg-slate-50 border border-slate-200 rounded font-mono text-xs space-y-2">
            <div className="flex items-center justify-between pb-2 border-b border-slate-200">
              <span className="font-bold text-slate-800 text-sm">
                Target: {lookupResult.indicator} ({lookupResult.type})
              </span>
              <span
                className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase ${
                  lookupResult.risk_rating === 'MALICIOUS'
                    ? 'bg-rose-100 text-rose-800'
                    : lookupResult.risk_rating === 'SUSPICIOUS'
                    ? 'bg-amber-100 text-amber-800'
                    : 'bg-emerald-100 text-emerald-800'
                }`}
              >
                {lookupResult.risk_rating || 'OBSERVED'}
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-[11px] pt-1">
              <div>
                <span className="text-slate-400 block text-[10px]">ASN / HOSTING</span>
                <span className="text-slate-800">{lookupResult.asn || lookupResult.asn_org || 'Standard Cloud ISP'}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">GEO LOCATION</span>
                <span className="text-slate-800">{lookupResult.country || 'International / Anycast'}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">INTELLIGENCE SOURCE</span>
                <span className="text-tg-primary font-medium">{lookupResult.lookup_source}</span>
              </div>
              <div>
                <span className="text-slate-400 block text-[10px]">VERIFICATION STATUS</span>
                <span className="text-emerald-700">{lookupResult.verification_status}</span>
              </div>
            </div>

            {lookupResult.risk_signals && (
              <div className="pt-2 border-t border-slate-200">
                <span className="text-[10px] text-slate-400 block mb-1">OBSERVED SIGNALS:</span>
                <ul className="list-disc list-inside space-y-0.5 text-slate-700 text-[11px]">
                  {lookupResult.risk_signals.map((sig: string, idx: number) => (
                    <li key={idx}>{sig}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Case-Linked Infrastructure Records */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-sm font-bold text-tg-text">
            Correlated Case Digital Infrastructure ({intelList.length} records)
          </h3>
          <span className="text-xs text-tg-secondary font-mono">
            Linked to Target Bank Accounts in Case
          </span>
        </div>

        {loading ? (
          <div className="p-8 text-center text-slate-500 text-xs flex items-center justify-center space-x-2">
            <RefreshCw className="w-4 h-4 animate-spin text-tg-primary" />
            <span>Loading corroborated threat records...</span>
          </div>
        ) : intelList.length === 0 ? (
          <div className="bg-white border border-tg-border rounded p-8 text-center text-slate-500 text-xs">
            No digital intelligence records currently attached to this case.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {intelList.map((item) => {
              const meta = item.metadata || {};
              const isMalicious = item.risk_rating === 'MALICIOUS';

              return (
                <div
                  key={item.id}
                  className={`bg-white border rounded p-4 shadow-sm space-y-3 transition-all ${
                    isMalicious ? 'border-rose-200 hover:border-rose-400' : 'border-tg-border'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <span className="text-[10px] font-mono uppercase bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded font-bold">
                        {item.indicator_type}
                      </span>
                      <h4 className="font-mono text-sm font-bold text-slate-900 mt-1">
                        {item.indicator_value}
                      </h4>
                    </div>
                    <span
                      className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase font-mono ${
                        isMalicious
                          ? 'bg-rose-100 text-rose-800 border border-rose-200'
                          : 'bg-amber-100 text-amber-800 border border-amber-200'
                      }`}
                    >
                      {item.risk_rating}
                    </span>
                  </div>

                  {/* Metadata fields */}
                  <div className="bg-slate-50 p-3 rounded border border-slate-200 text-xs font-mono space-y-1">
                    {meta.resolved_ip && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">Resolved IP:</span>
                        <span className="font-semibold text-slate-800">{meta.resolved_ip}</span>
                      </div>
                    )}
                    {meta.asn && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">ASN:</span>
                        <span className="text-slate-800 truncate max-w-[200px]">{meta.asn}</span>
                      </div>
                    )}
                    {meta.country && (
                      <div className="flex justify-between">
                        <span className="text-slate-400">Geo / Haven:</span>
                        <span className="text-slate-800">{meta.country}</span>
                      </div>
                    )}
                    {item.associated_account && (
                      <div className="flex justify-between pt-1 border-t border-slate-200 text-tg-primary font-bold">
                        <span>Linked Account:</span>
                        <span>{item.associated_account}</span>
                      </div>
                    )}
                  </div>

                  {/* Source and Verification Metadata */}
                  <div className="pt-2 border-t border-slate-100 flex flex-col space-y-1 text-[11px] text-slate-500">
                    <div className="flex justify-between">
                      <span>Source:</span>
                      <span className="font-medium text-slate-700">{item.lookup_source}</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Verification Status:</span>
                      <span className="font-mono text-emerald-700 font-semibold">
                        {item.verification_status}
                      </span>
                    </div>
                    <div className="flex justify-between text-[10px] text-slate-400">
                      <span>Observed:</span>
                      <span>{new Date(item.observed_at).toLocaleString('en-GB')}</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

