import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, ConfigDict

# --- Investigation Schemas ---
class InvestigationBase(BaseModel):
    case_number: str
    title: str
    description: Optional[str] = ""
    priority: str = "HIGH"
    status: str = "ACTIVE"
    lead_investigator: Optional[str] = "Insp. Vikram Rathore (Cyber Crime EOW)"

class InvestigationCreate(BaseModel):
    case_number: str
    title: str
    description: Optional[str] = ""
    priority: str = "HIGH"
    lead_investigator: Optional[str] = "Investigator"

class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    lead_investigator: Optional[str] = None

class InvestigationResponse(InvestigationBase):
    id: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    transaction_count: Optional[int] = 0
    total_amount: Optional[float] = 0.0
    flagged_amount: Optional[float] = 0.0
    suspicious_count: Optional[int] = 0

    model_config = ConfigDict(from_attributes=True)

# --- Transaction Schemas ---
class TransactionBase(BaseModel):
    id: str
    timestamp: datetime.datetime
    sender_account: str
    sender_name: Optional[str] = "Unknown"
    receiver_account: str
    receiver_name: Optional[str] = "Unknown"
    amount: float
    transaction_type: str = "IMPS"
    description: Optional[str] = ""
    reference_number: Optional[str] = ""

class TransactionCreate(TransactionBase):
    case_id: str

class TransactionResponse(TransactionBase):
    case_id: str
    risk_flag: str
    anomaly_score: float
    flag_reasons: List[str] = []
    detection_method: str

    model_config = ConfigDict(from_attributes=True)

# --- Account Schemas ---
class AccountResponse(BaseModel):
    id: str
    account_number: str
    case_id: str
    account_holder: str
    bank_name: str
    account_type: str
    risk_level: str
    risk_score: float
    risk_tags: List[str] = []
    total_inflow: float
    total_outflow: float
    transaction_count: int
    is_synthetic: bool

    model_config = ConfigDict(from_attributes=True)

# --- Graph Schemas (for React Flow) ---
class GraphNode(BaseModel):
    id: str
    label: str
    bank_name: str
    risk_level: str
    risk_score: float
    risk_tags: List[str]
    inflow: float
    outflow: float
    degree: int
    is_mule_candidate: bool

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    amount: float
    timestamp: str
    transaction_type: str
    risk_flag: str
    count: int = 1

class GraphResponse(BaseModel):
    case_id: str
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    summary: Dict[str, Any]

# --- Digital Intelligence Schemas ---
class DigitalIntelligenceBase(BaseModel):
    indicator_type: str
    indicator_value: str
    associated_account: Optional[str] = None
    lookup_source: str = "Passive DNS / Threat Feed (DEMO)"
    metadata: Dict[str, Any] = {}
    risk_rating: str = "SUSPICIOUS"
    verification_status: str = "DEMO_SIMULATION"

class DigitalIntelligenceResponse(DigitalIntelligenceBase):
    id: str
    case_id: str
    observed_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)

# --- Cross-case Schemas ---
class CrossCaseMatch(BaseModel):
    indicator_type: str # ACCOUNT, DOMAIN, IP, ENTITY
    indicator_value: str
    matched_cases: List[Dict[str, Any]]
    correlation_confidence: str
    description: str

# --- AI Assistant Schemas ---
class AIChatRequest(BaseModel):
    case_id: str
    message: str
    history: Optional[List[Dict[str, str]]] = None

class AIChatResponse(BaseModel):
    reply: str
    evidence_references: List[str]
    suggested_actions: List[str]
    confidence_level: str
    limitations_disclaimer: str

# --- Dashboard Stats ---
class DashboardOverview(BaseModel):
    total_investigations: int
    total_transactions_analyzed: int
    total_suspicious_flagged: int
    high_priority_cases: int
    accounts_requiring_review: int
    total_volume_analyzed: float
    total_suspicious_volume: float
    risk_distribution: Dict[str, int]
    timeline_activity: List[Dict[str, Any]]
    recent_cases: List[Dict[str, Any]]
