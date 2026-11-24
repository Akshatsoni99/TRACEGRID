export interface Investigation {
  id: string;
  case_number: string;
  title: string;
  description: string;
  priority: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW';
  status: 'ACTIVE' | 'IN_REVIEW' | 'ESCALATED' | 'CLOSED';
  lead_investigator: string;
  created_at: string;
  updated_at: string;
  transaction_count?: number;
  total_amount?: number;
  flagged_amount?: number;
  suspicious_count?: number;
}

export interface Transaction {
  id: string;
  case_id: string;
  timestamp: string;
  sender_account: string;
  sender_name: string;
  receiver_account: string;
  receiver_name: string;
  amount: number;
  transaction_type: string;
  description: string;
  reference_number: string;
  risk_flag: 'NORMAL' | 'SUSPICIOUS' | 'HIGH_RISK' | 'MULE_INDICATOR' | 'CIRCULAR_HOP';
  anomaly_score: number;
  flag_reasons: string[];
  detection_method: string;
}

export interface Account {
  id: string;
  account_number: string;
  case_id: string;
  account_holder: string;
  bank_name: string;
  account_type: string;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
  risk_score: number;
  risk_tags: string[];
  total_inflow: number;
  total_outflow: number;
  transaction_count: number;
  is_synthetic: boolean;
}

export interface GraphNodeData {
  account_number: string;
  account_holder: string;
  bank_name: string;
  in_degree: number;
  out_degree: number;
  total_degree: number;
  risk_level: string;
  risk_score: number;
  risk_tags: string[];
  is_mule_candidate: boolean;
  inflow: number;
  outflow: number;
  account_type: string;
}

export interface GraphEdgeData {
  total_amount: number;
  transaction_count: number;
  has_suspicious: boolean;
  last_timestamp: string;
  transaction_type: string;
  risk_flag: string;
  transactions: any[];
}

export interface DigitalIntelligence {
  id: string;
  case_id: string;
  indicator_type: 'DOMAIN' | 'IP_ADDRESS' | 'DNS' | 'HOSTING_PROVIDER' | 'ASN';
  indicator_value: string;
  associated_account?: string;
  lookup_source: string;
  metadata: Record<string, any>;
  risk_rating: 'CLEAN' | 'SUSPICIOUS' | 'MALICIOUS';
  verification_status: string;
  observed_at: string;
}

export interface CrossCaseMatch {
  indicator_type: string;
  indicator_value: string;
  matched_cases: Array<{
    case_id: string;
    case_number: string;
    case_title: string;
    holder?: string;
    bank?: string;
    risk_level?: string;
    risk_rating?: string;
    source?: string;
  }>;
  match_type: string;
  correlation_confidence: string;
  description: string;
}

export interface DashboardOverviewData {
  total_investigations: number;
  total_transactions_analyzed: number;
  total_suspicious_flagged: number;
  high_priority_cases: number;
  accounts_requiring_review: number;
  total_volume_analyzed: number;
  total_suspicious_volume: number;
  risk_distribution: Record<string, number>;
  timeline_activity: Array<{
    date: string;
    count: number;
    volume: number;
    flagged: number;
  }>;
  recent_cases: Array<{
    id: string;
    case_number: string;
    title: string;
    priority: string;
    status: string;
    lead_investigator: string;
    created_at: string;
    transaction_count: number;
    flagged_count: number;
    total_volume: number;
  }>;
}

export interface AIChatMessage {
  sender: 'user' | 'assistant';
  text: string;
  references?: string[];
  suggested_actions?: string[];
  confidence_level?: string;
  limitations_disclaimer?: string;
}

