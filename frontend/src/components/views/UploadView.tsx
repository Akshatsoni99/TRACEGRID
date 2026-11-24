'use client';

import React, { useState, useRef } from 'react';
import {
  UploadCloud,
  FileSpreadsheet,
  Download,
  CheckCircle2,
  AlertTriangle,
  FileCheck,
  RefreshCw,
  FolderOpen,
  ArrowRight,
  ShieldCheck
} from 'lucide-react';
import { Investigation } from '@/lib/types';
import { uploadBankStatement } from '@/lib/api';

interface UploadViewProps {
  cases: Investigation[];
  selectedCaseId: string;
  onSelectCase: (caseId: string) => void;
  onNavigate: (view: string) => void;
  onRefresh: () => void;
}

export default function UploadView({
  cases,
  selectedCaseId,
  onSelectCase,
  onNavigate,
  onRefresh,
}: UploadViewProps) {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const activeCase = cases.find((c) => c.id === selectedCaseId) || cases[0];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selected = e.target.files[0];
      const ext = selected.name.split('.').pop()?.toLowerCase();
      if (ext !== 'csv' && ext !== 'xlsx' && ext !== 'xls') {
        setError('Unsupported file type. Please upload a CSV or XLSX bank statement.');
        return;
      }
      setFile(selected);
      setError(null);
      setUploadResult(null);
    }
  };

  const handleUpload = async () => {
    if (!file || !activeCase) return;
    setUploading(true);
    setError(null);
    try {
      const res = await uploadBankStatement(activeCase.id, file);
      setUploadResult(res);
      onRefresh();
    } catch (err: any) {
      setError(err.message || 'File upload and ingestion failed');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="flex-1 overflow-y-auto p-6 space-y-6 max-w-4xl mx-auto">
      {/* Upload Instructions & Target Case */}
      <div className="bg-white border border-tg-border rounded p-5 shadow-sm space-y-4">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100">
          <div>
            <h2 className="text-sm font-bold text-tg-text">Target Investigation Dossier</h2>
            <p className="text-xs text-tg-secondary">
              Transactions will be ingested, mapped, and linked directly to this case.
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-semibold text-slate-700">Select Case:</span>
            <select
              value={selectedCaseId}
              onChange={(e) => onSelectCase(e.target.value)}
              className="text-xs border border-slate-300 rounded px-2.5 py-1.5 focus:outline-none focus:border-tg-primary font-mono bg-white"
            >
              {cases.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.case_number} - {c.title.slice(0, 30)}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Drag & Drop Area */}
        <div
          onClick={() => fileInputRef.current?.click()}
          className="border-2 border-dashed border-slate-300 hover:border-tg-primary rounded-lg p-8 text-center cursor-pointer transition-colors bg-slate-50/50 hover:bg-slate-50"
        >
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            accept=".csv, .xlsx, .xls"
            className="hidden"
          />
          <div className="w-12 h-12 rounded-full bg-sky-50 text-tg-primary mx-auto flex items-center justify-center mb-3">
            <UploadCloud className="w-6 h-6" />
          </div>
          <h3 className="text-sm font-semibold text-slate-800">
            {file ? file.name : 'Choose bank statement or drag & drop here'}
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Supports official CSV or XLSX statement exports (up to 25MB)
          </p>
          {file && (
            <div className="mt-3 inline-flex items-center space-x-1.5 bg-emerald-50 text-emerald-700 border border-emerald-200 px-3 py-1 rounded text-xs font-mono">
              <FileCheck className="w-3.5 h-3.5" />
              <span>{(file.size / 1024).toFixed(1)} KB &bull; Ready to Ingest</span>
            </div>
          )}
        </div>

        {/* Error notification */}
        {error && (
          <div className="p-3 rounded bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start space-x-2">
            <AlertTriangle className="w-4 h-4 text-rose-600 flex-shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Ingestion Error</p>
              <p>{error}</p>
            </div>
          </div>
        )}

        {/* Actions Bar */}
        <div className="flex items-center justify-between pt-2">
          <a
            href="/api/v1/sample/template.csv"
            download
            className="text-xs text-tg-primary hover:text-tg-primaryHover font-medium flex items-center space-x-1.5"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Download Normalized Sample CSV Template</span>
          </a>

          <button
            onClick={handleUpload}
            disabled={!file || uploading}
            className={`px-5 py-2 rounded text-xs font-semibold text-white flex items-center space-x-2 shadow-sm transition-all ${
              !file || uploading
                ? 'bg-slate-400 cursor-not-allowed'
                : 'bg-tg-primary hover:bg-tg-primaryHover'
            }`}
          >
            {uploading ? (
              <>
                <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                <span>Parsing & Running Analytics Engine...</span>
              </>
            ) : (
              <>
                <FileSpreadsheet className="w-4 h-4" />
                <span>Parse & Run Anomaly Detection</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Ingestion Results Summary */}
      {uploadResult && (
        <div className="bg-white border border-emerald-200 rounded p-5 shadow-sm space-y-4">
          <div className="flex items-center space-x-2 text-emerald-700">
            <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
            <h3 className="font-bold text-sm">Statement Ingested & Analyzed Successfully</h3>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="bg-slate-50 p-3 rounded border border-slate-200">
              <span className="text-slate-400 block text-[10px] uppercase">New Transactions</span>
              <span className="text-base font-bold font-mono text-slate-800">
                {uploadResult.imported_transactions}
              </span>
            </div>
            <div className="bg-slate-50 p-3 rounded border border-slate-200">
              <span className="text-slate-400 block text-[10px] uppercase">Duplicates Skipped</span>
              <span className="text-base font-bold font-mono text-slate-500">
                {uploadResult.duplicate_transactions_skipped}
              </span>
            </div>
            <div className="bg-slate-50 p-3 rounded border border-slate-200">
              <span className="text-slate-400 block text-[10px] uppercase">Flagged Suspicious</span>
              <span className="text-base font-bold font-mono text-tg-critical">
                {uploadResult.flagged_transactions}
              </span>
            </div>
            <div className="bg-slate-50 p-3 rounded border border-slate-200">
              <span className="text-slate-400 block text-[10px] uppercase">Mule Leads Found</span>
              <span className="text-base font-bold font-mono text-tg-warning">
                {uploadResult.mule_candidates_detected}
              </span>
            </div>
          </div>

          <div className="p-3 bg-amber-50/70 border border-amber-200 rounded text-xs text-amber-900">
            <strong>Automated Forensic Result: </strong>
            The analytics engine flagged {uploadResult.flagged_transactions} transactions totalling ₹
            {uploadResult.suspicious_volume?.toLocaleString('en-IN', { maximumFractionDigits: 2 })}{' '}
            and detected {uploadResult.circular_paths_detected} circular flow loop(s).
          </div>

          <div className="flex items-center justify-end space-x-3 pt-2">
            <button
              onClick={() => onNavigate('transactions')}
              className="px-3 py-1.5 border border-slate-300 rounded text-xs font-medium text-slate-700 hover:bg-slate-50"
            >
              View Flagged Transactions
            </button>
            <button
              onClick={() => onNavigate('graph')}
              className="px-4 py-1.5 bg-tg-primary text-white rounded text-xs font-medium hover:bg-tg-primaryHover flex items-center space-x-1"
            >
              <span>Explore Money-Trail Graph</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

      {/* Normalized Column Guide */}
      <div className="bg-white border border-tg-border rounded p-5 shadow-sm space-y-3">
        <h3 className="font-bold text-xs text-slate-700 uppercase tracking-wider">
          Normalized Field Requirements
        </h3>
        <p className="text-xs text-tg-secondary">
          TRACEGRID&apos;s intelligent column mapper recognizes standard Indian banking headers across SBI,
          HDFC, ICICI, PNB, Axis, and Razorpay/Paytm nodal statements:
        </p>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-[11px] font-mono">
          <div className="p-2 bg-slate-50 rounded border border-slate-200">
            <strong className="text-slate-800 block">Transaction ID</strong>
            <span className="text-slate-500">Txn ID, Ref, UTR</span>
          </div>
          <div className="p-2 bg-slate-50 rounded border border-slate-200">
            <strong className="text-slate-800 block">Sender Account</strong>
            <span className="text-slate-500">Debit A/c, From A/c</span>
          </div>
          <div className="p-2 bg-slate-50 rounded border border-slate-200">
            <strong className="text-slate-800 block">Receiver Account</strong>
            <span className="text-slate-500">Credit A/c, Beneficiary</span>
          </div>
          <div className="p-2 bg-slate-50 rounded border border-slate-200">
            <strong className="text-slate-800 block">Amount (INR)</strong>
            <span className="text-slate-500">Amount, Value, Debit</span>
          </div>
        </div>
      </div>
    </div>
  );
}

