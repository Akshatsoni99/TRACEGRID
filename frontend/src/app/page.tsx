'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Sidebar from '@/components/Sidebar';
import Header from '@/components/Header';
import OverviewView from '@/components/views/OverviewView';
import InvestigationsView from '@/components/views/InvestigationsView';
import UploadView from '@/components/views/UploadView';
import TransactionAnalysisView from '@/components/views/TransactionAnalysisView';
import NetworkGraphView from '@/components/views/NetworkGraphView';
import DigitalIntelligenceView from '@/components/views/DigitalIntelligenceView';
import CrossCaseView from '@/components/views/CrossCaseView';
import AIAssistantView from '@/components/views/AIAssistantView';
import ReportsView from '@/components/views/ReportsView';
import SettingsView from '@/components/views/SettingsView';
import { Investigation } from '@/lib/types';
import { fetchCases } from '@/lib/api';
import { RefreshCw } from 'lucide-react';

export default function Home() {
  const [currentView, setCurrentView] = useState('overview');
  const [cases, setCases] = useState<Investigation[]>([]);
  const [selectedCaseId, setSelectedCaseId] = useState<string>('case-001');
  const [loading, setLoading] = useState(true);
  const [refreshKey, setRefreshKey] = useState(0);

  const loadCases = useCallback(async () => {
    try {
      const data = await fetchCases();
      setCases(data);
      if (data.length > 0 && (!selectedCaseId || !data.some((c: Investigation) => c.id === selectedCaseId))) {
        setSelectedCaseId(data[0].id);
      }
    } catch (err) {
      console.error('Failed to load cases:', err);
    } finally {
      setLoading(false);
    }
  }, [selectedCaseId]);

  useEffect(() => {
    loadCases();
  }, [loadCases, refreshKey]);

  const activeCase = cases.find((c) => c.id === selectedCaseId) || cases[0];

  const handleRefresh = () => {
    setRefreshKey((k) => k + 1);
  };

  if (loading && cases.length === 0) {
    return (
      <div className="h-screen w-screen bg-tg-sidebar flex flex-col items-center justify-center text-white space-y-4">
        <div className="w-12 h-12 rounded bg-tg-primary/30 border border-tg-primary flex items-center justify-center">
          <RefreshCw className="w-6 h-6 animate-spin text-sky-400" />
        </div>
        <div className="text-center">
          <h1 className="text-lg font-bold tracking-wider">TRACEGRID</h1>
          <p className="text-xs text-slate-400 mt-1">Connecting Financial Evidence. Revealing Hidden Relationships.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-tg-bg text-tg-text">
      {/* Deep Navy Left Sidebar */}
      <Sidebar
        currentView={currentView}
        onSelectView={setCurrentView}
        cases={cases}
        selectedCaseId={selectedCaseId}
        onSelectCase={setSelectedCaseId}
      />

      {/* Main Forensic Workspace */}
      <div className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Top Header */}
        <Header
          currentView={currentView}
          activeCase={activeCase}
          onRefresh={handleRefresh}
        />

        {/* View Content Area */}
        <main className="flex-1 overflow-hidden flex flex-col">
          {currentView === 'overview' && (
            <OverviewView
              onSelectCase={setSelectedCaseId}
              onNavigate={setCurrentView}
            />
          )}

          {currentView === 'investigations' && (
            <InvestigationsView
              cases={cases}
              selectedCaseId={selectedCaseId}
              onSelectCase={setSelectedCaseId}
              onNavigate={setCurrentView}
              onRefresh={handleRefresh}
            />
          )}

          {currentView === 'upload' && (
            <UploadView
              cases={cases}
              selectedCaseId={selectedCaseId}
              onSelectCase={setSelectedCaseId}
              onNavigate={setCurrentView}
              onRefresh={handleRefresh}
            />
          )}

          {currentView === 'transactions' && (
            <TransactionAnalysisView
              selectedCaseId={selectedCaseId}
            />
          )}

          {currentView === 'graph' && (
            <NetworkGraphView
              selectedCaseId={selectedCaseId}
            />
          )}

          {currentView === 'intelligence' && (
            <DigitalIntelligenceView
              selectedCaseId={selectedCaseId}
            />
          )}

          {currentView === 'cross-case' && (
            <CrossCaseView
              selectedCaseId={selectedCaseId}
              onSelectCase={setSelectedCaseId}
              onNavigate={setCurrentView}
            />
          )}

          {currentView === 'ai-assistant' && (
            <AIAssistantView
              activeCase={activeCase}
            />
          )}

          {currentView === 'reports' && (
            <ReportsView
              selectedCaseId={selectedCaseId}
            />
          )}

          {currentView === 'settings' && (
            <SettingsView
              selectedCaseId={selectedCaseId}
            />
          )}
        </main>
      </div>
    </div>
  );
}

