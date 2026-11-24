const API_BASE = '/api/v1';

export async function fetchDashboardOverview() {
  const res = await fetch(`${API_BASE}/dashboard/overview`);
  if (!res.ok) throw new Error('Failed to load dashboard overview');
  return res.json();
}

export async function fetchCases() {
  const res = await fetch(`${API_BASE}/cases`);
  if (!res.ok) throw new Error('Failed to load investigations');
  return res.json();
}

export async function fetchCaseDetails(caseId: string) {
  const res = await fetch(`${API_BASE}/cases/${caseId}`);
  if (!res.ok) throw new Error('Failed to load case details');
  return res.json();
}

export async function createCase(data: {
  case_number: string;
  title: string;
  description: string;
  priority: string;
  lead_investigator: string;
}) {
  const res = await fetch(`${API_BASE}/cases`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Creation failed' }));
    throw new Error(err.detail || 'Failed to create investigation');
  }
  return res.json();
}

export async function fetchTransactions(params: {
  case_id?: string;
  risk_flag?: string;
  min_amount?: number;
  max_amount?: number;
  account?: string;
}) {
  const query = new URLSearchParams();
  if (params.case_id) query.append('case_id', params.case_id);
  if (params.risk_flag && params.risk_flag !== 'ALL') query.append('risk_flag', params.risk_flag);
  if (params.min_amount) query.append('min_amount', params.min_amount.toString());
  if (params.max_amount) query.append('max_amount', params.max_amount.toString());
  if (params.account) query.append('account', params.account);

  const res = await fetch(`${API_BASE}/transactions?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to load transactions');
  return res.json();
}

export async function fetchAccounts(params: { case_id?: string; risk_level?: string }) {
  const query = new URLSearchParams();
  if (params.case_id) query.append('case_id', params.case_id);
  if (params.risk_level && params.risk_level !== 'ALL') query.append('risk_level', params.risk_level);

  const res = await fetch(`${API_BASE}/accounts?${query.toString()}`);
  if (!res.ok) throw new Error('Failed to load accounts');
  return res.json();
}

export async function fetchGraph(caseId: string, minAmount: number = 0) {
  const res = await fetch(`${API_BASE}/graph/${caseId}?min_amount=${minAmount}`);
  if (!res.ok) throw new Error('Failed to load network graph');
  return res.json();
}

export async function fetchDigitalIntelligence(caseId: string) {
  const res = await fetch(`${API_BASE}/intelligence/${caseId}`);
  if (!res.ok) throw new Error('Failed to load digital intelligence');
  return res.json();
}

export async function queryIntelLookup(indicator: string, indicator_type: string = 'AUTO') {
  const formData = new FormData();
  formData.append('indicator', indicator);
  formData.append('indicator_type', indicator_type);

  const res = await fetch(`${API_BASE}/intelligence/lookup`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Lookup failed');
  return res.json();
}

export async function fetchCrossCaseCorrelations(targetCaseId?: string) {
  const query = targetCaseId ? `?target_case_id=${targetCaseId}` : '';
  const res = await fetch(`${API_BASE}/cross-case/correlations${query}`);
  if (!res.ok) throw new Error('Failed to load cross-case correlations');
  return res.json();
}

export async function askAIAssistant(caseId: string, message: string) {
  const res = await fetch(`${API_BASE}/assistant/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ case_id: caseId, message }),
  });
  if (!res.ok) throw new Error('AI Assistant request failed');
  return res.json();
}

export async function uploadBankStatement(caseId: string, file: File) {
  const formData = new FormData();
  formData.append('file', file);

  const res = await fetch(`${API_BASE}/upload/statement/${caseId}`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(err.detail || 'Upload failed');
  }
  return res.json();
}

export async function resetDemoData() {
  const res = await fetch(`${API_BASE}/demo/reset`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to reset demo data');
  return res.json();
}

export function getReportDownloadUrl(caseId: string) {
  return `${API_BASE}/reports/pdf/${caseId}`;
}

