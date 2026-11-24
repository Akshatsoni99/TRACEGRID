import datetime
import uuid
from typing import List, Optional
from sqlalchemy import String, Float, Integer, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.core.database import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

class Investigation(Base):
    __tablename__ = "investigations"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    case_number: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True, default="")
    priority: Mapped[str] = mapped_column(String, default="HIGH") # CRITICAL, HIGH, MEDIUM, LOW
    status: Mapped[str] = mapped_column(String, default="ACTIVE") # ACTIVE, IN_REVIEW, ESCALATED, CLOSED
    lead_investigator: Mapped[str] = mapped_column(String, default="Insp. Vikram Rathore (Cyber Crime EOW)")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utc_now)
    updated_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utc_now, onupdate=utc_now)

    # Relationships
    transactions: Mapped[List["Transaction"]] = relationship("Transaction", back_populates="case", cascade="all, delete-orphan")
    accounts: Mapped[List["Account"]] = relationship("Account", back_populates="case", cascade="all, delete-orphan")
    evidence: Mapped[List["Evidence"]] = relationship("Evidence", back_populates="case", cascade="all, delete-orphan")
    intelligence: Mapped[List["DigitalIntelligence"]] = relationship("DigitalIntelligence", back_populates="case", cascade="all, delete-orphan")
    analysis_results: Mapped[List["AnalysisResult"]] = relationship("AnalysisResult", back_populates="case", cascade="all, delete-orphan")
    logs: Mapped[List["ActivityLog"]] = relationship("ActivityLog", back_populates="case", cascade="all, delete-orphan")

class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    account_number: Mapped[str] = mapped_column(String, index=True, nullable=False)
    case_id: Mapped[str] = mapped_column(String, ForeignKey("investigations.id"), nullable=False, index=True)
    account_holder: Mapped[str] = mapped_column(String, nullable=False)
    bank_name: Mapped[str] = mapped_column(String, nullable=False)
    account_type: Mapped[str] = mapped_column(String, default="SAVINGS") # SAVINGS, CURRENT, DIGITAL_WALLET, NODAL, CRYPTO_RAMP
    risk_level: Mapped[str] = mapped_column(String, default="LOW") # LOW, MEDIUM, HIGH, CRITICAL
    risk_score: Mapped[float] = mapped_column(Float, default=0.0) # 0 to 100
    risk_tags: Mapped[str] = mapped_column(Text, default="[]") # JSON list of detected tags
    total_inflow: Mapped[float] = mapped_column(Float, default=0.0)
    total_outflow: Mapped[float] = mapped_column(Float, default=0.0)
    transaction_count: Mapped[int] = mapped_column(Integer, default=0)
    is_synthetic: Mapped[bool] = mapped_column(Boolean, default=True)

    case: Mapped["Investigation"] = relationship("Investigation", back_populates="accounts")

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(String, primary_key=True) # Transaction ID or Reference
    case_id: Mapped[str] = mapped_column(String, ForeignKey("investigations.id"), nullable=False, index=True)
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=False, default=utc_now)
    sender_account: Mapped[str] = mapped_column(String, index=True, nullable=False)
    sender_name: Mapped[str] = mapped_column(String, default="Unknown Sender")
    receiver_account: Mapped[str] = mapped_column(String, index=True, nullable=False)
    receiver_name: Mapped[str] = mapped_column(String, default="Unknown Receiver")
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    transaction_type: Mapped[str] = mapped_column(String, default="IMPS") # IMPS, NEFT, RTGS, UPI, WIRE, CASH
    description: Mapped[str] = mapped_column(String, default="")
    reference_number: Mapped[str] = mapped_column(String, default="")
    
    # Analytics flags
    risk_flag: Mapped[str] = mapped_column(String, default="NORMAL") # NORMAL, SUSPICIOUS, HIGH_RISK, MULE_INDICATOR, CIRCULAR_HOP
    anomaly_score: Mapped[float] = mapped_column(Float, default=0.0) # 0.0 to 1.0 (IsolationForest / rule calibrated)
    flag_reasons: Mapped[str] = mapped_column(Text, default="[]") # JSON list of reasons
    detection_method: Mapped[str] = mapped_column(String, default="RULE_BASED") # RULE_BASED, ISOLATION_FOREST, HYBRID_ENSEMBLE

    case: Mapped["Investigation"] = relationship("Investigation", back_populates="transactions")

class Evidence(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    case_id: Mapped[str] = mapped_column(String, ForeignKey("investigations.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    evidence_type: Mapped[str] = mapped_column(String, default="BANK_STATEMENT") # BANK_STATEMENT, IP_LOG, WHOIS_EXPORT, CDR, FORENSIC_DUMP
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_hash: Mapped[str] = mapped_column(String, default="") # SHA256 checksum
    uploaded_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utc_now)
    source: Mapped[str] = mapped_column(String, default="Internal Subpoena / CERT-In Dispatch")
    verification_status: Mapped[str] = mapped_column(String, default="VERIFIED") # VERIFIED, UNVERIFIED, CORROBORATED
    notes: Mapped[str] = mapped_column(Text, default="")

    case: Mapped["Investigation"] = relationship("Investigation", back_populates="evidence")

class DigitalIntelligence(Base):
    __tablename__ = "digital_intelligence"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    case_id: Mapped[str] = mapped_column(String, ForeignKey("investigations.id"), nullable=False, index=True)
    indicator_type: Mapped[str] = mapped_column(String, nullable=False) # DOMAIN, IP_ADDRESS, DNS, HOSTING_PROVIDER, ASN
    indicator_value: Mapped[str] = mapped_column(String, nullable=False, index=True)
    associated_account: Mapped[Optional[str]] = mapped_column(String, nullable=True) # Linked bank account
    lookup_source: Mapped[str] = mapped_column(String, default="Passive DNS / Threat Feed (DEMO)")
    metadata_json: Mapped[str] = mapped_column(Text, default="{}") # JSON details (ASN, Country, Registrar, DNS Records, etc.)
    risk_rating: Mapped[str] = mapped_column(String, default="SUSPICIOUS") # CLEAN, SUSPICIOUS, MALICIOUS
    verification_status: Mapped[str] = mapped_column(String, default="DEMO_SIMULATION") # VERIFIED_RECORD, CORROBORATED, DEMO_SIMULATION
    observed_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utc_now)

    case: Mapped["Investigation"] = relationship("Investigation", back_populates="intelligence")

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    case_id: Mapped[str] = mapped_column(String, ForeignKey("investigations.id"), nullable=False, index=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    total_volume: Mapped[float] = mapped_column(Float, default=0.0)
    suspicious_volume: Mapped[float] = mapped_column(Float, default=0.0)
    flagged_count: Mapped[int] = mapped_column(Integer, default=0)
    circular_paths_count: Mapped[int] = mapped_column(Integer, default=0)
    mule_candidates_count: Mapped[int] = mapped_column(Integer, default=0)
    metrics_json: Mapped[str] = mapped_column(Text, default="{}")
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=utc_now)

    case: Mapped["Investigation"] = relationship("Investigation", back_populates="analysis_results")

class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=generate_uuid)
    case_id: Mapped[str] = mapped_column(String, ForeignKey("investigations.id"), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String, nullable=False)
    actor: Mapped[str] = mapped_column(String, default="Lead Investigator")
    details: Mapped[str] = mapped_column(Text, default="")
    timestamp: Mapped[datetime.datetime] = mapped_column(DateTime, default=utc_now)

    case: Mapped["Investigation"] = relationship("Investigation", back_populates="logs")
