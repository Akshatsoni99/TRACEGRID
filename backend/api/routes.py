import io
import json
import uuid
import datetime
import math
import numpy as np
import pandas as pd
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.core.database import get_db
from backend.models.models import (
    Investigation, Account, Transaction, Evidence, DigitalIntelligence, AnalysisResult, ActivityLog
)
from backend.schemas.schemas import (
    InvestigationResponse, InvestigationCreate, InvestigationUpdate,
    TransactionResponse, AccountResponse, GraphResponse,
    DigitalIntelligenceResponse, AIChatRequest, AIChatResponse, DashboardOverview
)
from backend.analytics.engine import TransactionAnalyticsEngine
from backend.graph.network import NetworkGraphService
from backend.intelligence.digital import DigitalIntelligenceService
from backend.services.cross_case import CrossCaseAnalysisService
from backend.services.ai_assistant import AIAssistantService
from backend.reports.pdf_generator import ReportPDFService
from backend.core.security import validate_uploaded_file, check_file_size

router = APIRouter()
intel_service = DigitalIntelligenceService()
analytics_engine = TransactionAnalyticsEngine()

# --- Health Check ---
@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "TRACEGRID Core API",
        "team": "CyboShield",
        "hackathon": "Rajasthan Police Hackathon 2026 - PS05",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
    }

# --- Dashboard Overview ---
@router.get("/dashboard/overview")
def get_dashboard_overview(db: Session = Depends(get_db)):
    cases = db.query(Investigation).all()
    transactions = db.query(Transaction).all()
    accounts = db.query(Account).all()

    total_vol = sum(t.amount for t in transactions)
    flagged_tx = [t for t in transactions if t.risk_flag != "NORMAL"]
    susp_vol = sum(t.amount for t in flagged_tx)

    risk_dist = {
        "NORMAL": len([t for t in transactions if t.risk_flag == "NORMAL"]),
        "SUSPICIOUS": len([t for t in transactions if t.risk_flag == "SUSPICIOUS"]),
        "HIGH_RISK": len([t for t in transactions if t.risk_flag == "HIGH_RISK"]),
        "MULE_INDICATOR": len([t for t in transactions if t.risk_flag == "MULE_INDICATOR"]),
        "CIRCULAR_HOP": len([t for t in transactions if t.risk_flag == "CIRCULAR_HOP"])
    }

    recent_cases_data = []
    for c in cases[:6]:
        c_txs = [t for t in transactions if t.case_id == c.id]
        c_flagged = [t for t in c_txs if t.risk_flag != "NORMAL"]
        recent_cases_data.append({
            "id": c.id,
            "case_number": c.case_number,
            "title": c.title,
            "priority": c.priority,
            "status": c.status,
            "lead_investigator": c.lead_investigator,
            "created_at": c.created_at.strftime("%Y-%m-%d"),
            "transaction_count": len(c_txs),
            "flagged_count": len(c_flagged),
            "total_volume": round(sum(t.amount for t in c_txs), 2)
        })

    # Timeline aggregation by day
    timeline_map = {}
    for t in transactions:
        d_str = t.timestamp.strftime("%Y-%m-%d")
        if d_str not in timeline_map:
            timeline_map[d_str] = {"date": d_str, "count": 0, "volume": 0.0, "flagged": 0}
        timeline_map[d_str]["count"] += 1
        timeline_map[d_str]["volume"] += t.amount
        if t.risk_flag != "NORMAL":
            timeline_map[d_str]["flagged"] += 1

    sorted_timeline = sorted(timeline_map.values(), key=lambda x: x["date"])

    return {
        "total_investigations": len(cases),
        "total_transactions_analyzed": len(transactions),
        "total_suspicious_flagged": len(flagged_tx),
        "high_priority_cases": len([c for c in cases if c.priority in ("CRITICAL", "HIGH")]),
        "accounts_requiring_review": len([a for a in accounts if a.risk_level in ("HIGH", "CRITICAL")]),
        "total_volume_analyzed": round(total_vol, 2),
        "total_suspicious_volume": round(susp_vol, 2),
        "risk_distribution": risk_dist,
        "timeline_activity": sorted_timeline,
        "recent_cases": recent_cases_data
    }

# --- Investigations ---
@router.get("/cases", response_model=List[InvestigationResponse])
def list_cases(db: Session = Depends(get_db)):
    cases = db.query(Investigation).order_by(Investigation.created_at.desc()).all()
    results = []
    for c in cases:
        txs = db.query(Transaction).filter(Transaction.case_id == c.id).all()
        flagged = [t for t in txs if t.risk_flag != "NORMAL"]
        resp = InvestigationResponse(
            id=c.id,
            case_number=c.case_number,
            title=c.title,
            description=c.description or "",
            priority=c.priority,
            status=c.status,
            lead_investigator=c.lead_investigator or "Investigator",
            created_at=c.created_at,
            updated_at=c.updated_at,
            transaction_count=len(txs),
            total_amount=round(sum(t.amount for t in txs), 2),
            flagged_amount=round(sum(t.amount for t in flagged), 2),
            suspicious_count=len(flagged)
        )
        results.append(resp)
    return results

@router.post("/cases", response_model=InvestigationResponse)
def create_case(case_in: InvestigationCreate, db: Session = Depends(get_db)):
    existing = db.query(Investigation).filter(Investigation.case_number == case_in.case_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Case reference already exists in database.")

    new_id = f"case-{str(uuid.uuid4())[:8]}"
    case = Investigation(
        id=new_id,
        case_number=case_in.case_number,
        title=case_in.title,
        description=case_in.description,
        priority=case_in.priority,
        status="ACTIVE",
        lead_investigator=case_in.lead_investigator
    )
    db.add(case)
    
    # Audit log
    db.add(ActivityLog(
        case_id=new_id,
        action="CASE_CREATED",
        actor=case_in.lead_investigator or "Investigator",
        details=f"Created investigation case: {case_in.title}"
    ))
    db.commit()
    db.refresh(case)

    return InvestigationResponse(
        id=case.id,
        case_number=case.case_number,
        title=case.title,
        description=case.description or "",
        priority=case.priority,
        status=case.status,
        lead_investigator=case.lead_investigator,
        created_at=case.created_at,
        updated_at=case.updated_at,
        transaction_count=0,
        total_amount=0.0,
        flagged_amount=0.0,
        suspicious_count=0
    )

@router.get("/cases/{case_id}")
def get_case(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Investigation).filter(Investigation.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Investigation case not found")
    
    txs = db.query(Transaction).filter(Transaction.case_id == case_id).all()
    accounts = db.query(Account).filter(Account.case_id == case_id).all()
    evidence = db.query(Evidence).filter(Evidence.case_id == case_id).all()
    intel = db.query(DigitalIntelligence).filter(DigitalIntelligence.case_id == case_id).all()
    logs = db.query(ActivityLog).filter(ActivityLog.case_id == case_id).order_by(ActivityLog.timestamp.desc()).all()

    flagged = [t for t in txs if t.risk_flag != "NORMAL"]
    
    return {
        "case": {
            "id": case.id,
            "case_number": case.case_number,
            "title": case.title,
            "description": case.description,
            "priority": case.priority,
            "status": case.status,
            "lead_investigator": case.lead_investigator,
            "created_at": case.created_at.isoformat(),
            "updated_at": case.updated_at.isoformat(),
        },
        "stats": {
            "total_transactions": len(txs),
            "flagged_transactions": len(flagged),
            "total_volume": round(sum(t.amount for t in txs), 2),
            "flagged_volume": round(sum(t.amount for t in flagged), 2),
            "accounts_count": len(accounts),
            "evidence_count": len(evidence),
            "intel_count": len(intel)
        },
        "activity_logs": [
            {
                "id": l.id,
                "action": l.action,
                "actor": l.actor,
                "details": l.details,
                "timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M")
            } for l in logs
        ]
    }

@router.put("/cases/{case_id}")
def update_case(case_id: str, update_in: InvestigationUpdate, db: Session = Depends(get_db)):
    case = db.query(Investigation).filter(Investigation.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    
    if update_in.title is not None:
        case.title = update_in.title
    if update_in.description is not None:
        case.description = update_in.description
    if update_in.priority is not None:
        case.priority = update_in.priority
    if update_in.status is not None:
        case.status = update_in.status
    if update_in.lead_investigator is not None:
        case.lead_investigator = update_in.lead_investigator

    case.updated_at = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(case)
    return {"message": "Case updated successfully", "case_id": case.id}

# --- Bank Statement File Upload & Processing ---
@router.get("/sample/template.csv")
def download_sample_template():
    csv_content = (
        "Transaction ID,Date and timestamp,Sender account,Sender name,Receiver account,Receiver name,Amount,Transaction type,Description,Reference number\n"
        "TXN-DEMO-001,2026-02-15 02:30:00,ACC-SND-101,Ramesh Traders,ACC-RCV-202,Manoj Logistics,450000.00,RTGS,Consultancy invoice payment,RTGS9988110022\n"
        "TXN-DEMO-002,2026-02-15 03:00:00,ACC-RCV-202,Manoj Logistics,ACC-RCV-303,Deepak Bullion,445000.00,IMPS,Urgent bullion clearing,IMPS9988110044\n"
        "TXN-DEMO-003,2026-02-15 03:15:00,ACC-RCV-303,Deepak Bullion,ACC-SND-101,Ramesh Traders,50000.00,UPI,Security deposit rebate,UPI9988110055\n"
        "TXN-DEMO-004,2026-02-15 11:20:00,ACC-SND-404,Vikram Retail,ACC-RCV-505,Nodal Payment Escrow,12000.00,UPI,Stationery purchase,UPI9988110066\n"
    )
    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=TRACEGRID_Statement_Template.csv"}
    )

@router.post("/upload/statement/{case_id}")
async def upload_statement(
    case_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    case = db.query(Investigation).filter(Investigation.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Investigation case not found")

    filename = validate_uploaded_file(file)
    contents = await file.read()
    check_file_size(contents)

    # Parse CSV or Excel
    try:
        if filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(contents))
        else:
            df = pd.read_csv(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded statement file is empty.")

    # Normalize column headers
    col_map = {}
    for col in df.columns:
        c_low = str(col).lower().replace("_", " ").strip()
        if "id" in c_low or "txn" in c_low:
            col_map[col] = "id"
        elif "date" in c_low or "time" in c_low or "timestamp" in c_low:
            col_map[col] = "timestamp"
        elif "sender" in c_low and "acc" in c_low:
            col_map[col] = "sender_account"
        elif "sender" in c_low and "name" in c_low:
            col_map[col] = "sender_name"
        elif "sender" in c_low:
            col_map[col] = "sender_account"
        elif "receiver" in c_low and "acc" in c_low:
            col_map[col] = "receiver_account"
        elif "receiver" in c_low and "name" in c_low:
            col_map[col] = "receiver_name"
        elif "receiver" in c_low or "beneficiary" in c_low:
            col_map[col] = "receiver_account"
        elif "amount" in c_low or "debit" in c_low or "value" in c_low:
            col_map[col] = "amount"
        elif "type" in c_low or "mode" in c_low:
            col_map[col] = "transaction_type"
        elif "desc" in c_low or "remark" in c_low or "narration" in c_low:
            col_map[col] = "description"
        elif "ref" in c_low or "utr" in c_low:
            col_map[col] = "reference_number"

    df = df.rename(columns=col_map)

    # Validate essential columns
    required_cols = ["sender_account", "receiver_account", "amount"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing mandatory statement columns: {', '.join(missing)}. Download the sample template for reference."
        )

    # Process and detect duplicates
    existing_tx_ids = set(t[0] for t in db.query(Transaction.id).all())
    imported_count = 0
    duplicate_count = 0
    invalid_rows = 0

    new_tx_records = []
    discovered_accounts = set()

    for idx, row in df.iterrows():
        try:
            amt = float(str(row["amount"]).replace(",", "").strip())
            if amt <= 0:
                invalid_rows += 1
                continue

            tx_id = str(row.get("id", f"TXN-IMP-{uuid.uuid4().hex[:8]}"))
            if tx_id in existing_tx_ids:
                duplicate_count += 1
                continue

            s_acc = str(row["sender_account"]).strip()
            r_acc = str(row["receiver_account"]).strip()
            s_name = str(row.get("sender_name", "Account Holder"))
            r_name = str(row.get("receiver_name", "Beneficiary"))

            ts_raw = row.get("timestamp")
            if ts_raw is None or (isinstance(ts_raw, float) and np.isnan(ts_raw)) or str(ts_raw).strip() in ("", "nan", "NaT", "None"):
                tx_ts = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
            else:
                try:
                    parsed_dt = pd.to_datetime(str(ts_raw))
                    tx_ts = parsed_dt.to_pydatetime() if hasattr(parsed_dt, "to_pydatetime") else datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
                except Exception:
                    tx_ts = datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)

            discovered_accounts.add((s_acc, s_name))
            discovered_accounts.add((r_acc, r_name))

            new_tx = Transaction(
                id=tx_id,
                case_id=case_id,
                timestamp=tx_ts,
                sender_account=s_acc,
                sender_name=s_name,
                receiver_account=r_acc,
                receiver_name=r_name,
                amount=amt,
                transaction_type=str(row.get("transaction_type", "IMPS")),
                description=str(row.get("description", "")),
                reference_number=str(row.get("reference_number", "")),
                risk_flag="NORMAL",
                anomaly_score=0.0,
                flag_reasons=json.dumps([]),
                detection_method="RULE_BASED"
            )
            new_tx_records.append(new_tx)
            existing_tx_ids.add(tx_id)
            imported_count += 1
        except Exception:
            invalid_rows += 1

    # Bulk insert transactions
    for tx in new_tx_records:
        db.add(tx)

    # Create missing accounts
    for acc_num, holder_name in discovered_accounts:
        acc_exists = db.query(Account).filter(Account.account_number == acc_num, Account.case_id == case_id).first()
        if not acc_exists:
            new_acc = Account(
                id=f"{case_id}_{acc_num}",
                account_number=acc_num,
                case_id=case_id,
                account_holder=holder_name,
                bank_name="Scheduled Bank",
                account_type="SAVINGS",
                risk_level="LOW",
                risk_score=15.0,
                risk_tags=json.dumps([]),
                total_inflow=0.0,
                total_outflow=0.0,
                transaction_count=0,
                is_synthetic=True
            )
            db.add(new_acc)

    # Save evidence record
    import hashlib
    sha256 = hashlib.sha256(contents).hexdigest()
    ev = Evidence(
        case_id=case_id,
        title=f"Imported Statement: {filename}",
        evidence_type="BANK_STATEMENT",
        file_name=filename,
        file_hash=sha256,
        source="Authorized Ingestion Upload",
        verification_status="VERIFIED",
        notes=f"Parsed {imported_count} records. Duplicates: {duplicate_count}. Invalid: {invalid_rows}."
    )
    db.add(ev)

    # Log action
    db.add(ActivityLog(
        case_id=case_id,
        action="STATEMENT_INGESTED",
        actor="Investigator",
        details=f"File {filename} ingested. Imported: {imported_count}, Duplicates skipped: {duplicate_count}"
    ))

    db.commit()

    # Automatically trigger analytics engine on case transactions
    all_case_txs = db.query(Transaction).filter(Transaction.case_id == case_id).all()
    tx_dicts = [
        {
            "id": t.id,
            "case_id": t.case_id,
            "timestamp": t.timestamp,
            "sender_account": t.sender_account,
            "sender_name": t.sender_name,
            "receiver_account": t.receiver_account,
            "receiver_name": t.receiver_name,
            "amount": t.amount,
            "transaction_type": t.transaction_type,
            "description": t.description,
            "reference_number": t.reference_number
        }
        for t in all_case_txs
    ]

    analyzed_records, summary = analytics_engine.analyze_transactions(tx_dicts)

    # Update transactions with risk flags
    analysis_map = {r["id"]: r for r in analyzed_records}
    for t in all_case_txs:
        if t.id in analysis_map:
            t_data = analysis_map[t.id]
            t.risk_flag = t_data["risk_flag"]
            t.anomaly_score = t_data["anomaly_score"]
            t.flag_reasons = json.dumps(t_data["flag_reasons"])
            t.detection_method = t_data["detection_method"]

    # Update account flow metrics
    for acc in db.query(Account).filter(Account.case_id == case_id).all():
        in_sum = sum(t.amount for t in all_case_txs if t.receiver_account == acc.id)
        out_sum = sum(t.amount for t in all_case_txs if t.sender_account == acc.id)
        acc.total_inflow = round(in_sum, 2)
        acc.total_outflow = round(out_sum, 2)
        acc.transaction_count = len([t for t in all_case_txs if t.sender_account == acc.id or t.receiver_account == acc.id])

    db.commit()

    return {
        "status": "success",
        "file_name": filename,
        "imported_transactions": imported_count,
        "duplicate_transactions_skipped": duplicate_count,
        "invalid_rows_ignored": invalid_rows,
        "total_case_transactions": len(all_case_txs),
        "flagged_transactions": summary["flagged_count"],
        "suspicious_volume": summary["suspicious_volume"],
        "circular_paths_detected": len(summary["circular_paths"]),
        "mule_candidates_detected": len(summary["mule_candidates"])
    }

# --- Transactions & Analytics ---
@router.get("/transactions")
def list_transactions(
    case_id: Optional[str] = None,
    risk_flag: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    account: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Transaction)
    if case_id:
        query = query.filter(Transaction.case_id == case_id)
    if risk_flag and risk_flag != "ALL":
        query = query.filter(Transaction.risk_flag == risk_flag)
    if min_amount is not None:
        query = query.filter(Transaction.amount >= min_amount)
    if max_amount is not None:
        query = query.filter(Transaction.amount <= max_amount)
    if account:
        query = query.filter(
            (Transaction.sender_account == account) | (Transaction.receiver_account == account)
        )

    txs = query.order_by(Transaction.timestamp.desc()).all()
    results = []
    for t in txs:
        reasons = []
        try:
            reasons = json.loads(t.flag_reasons) if isinstance(t.flag_reasons, str) else t.flag_reasons
        except Exception:
            pass

        results.append({
            "id": t.id,
            "case_id": t.case_id,
            "timestamp": t.timestamp.isoformat(),
            "sender_account": t.sender_account,
            "sender_name": t.sender_name,
            "receiver_account": t.receiver_account,
            "receiver_name": t.receiver_name,
            "amount": t.amount,
            "transaction_type": t.transaction_type,
            "description": t.description,
            "reference_number": t.reference_number,
            "risk_flag": t.risk_flag,
            "anomaly_score": t.anomaly_score,
            "flag_reasons": reasons,
            "detection_method": t.detection_method
        })
    return results

@router.post("/analysis/run/{case_id}")
def run_case_analytics(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Investigation).filter(Investigation.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    txs = db.query(Transaction).filter(Transaction.case_id == case_id).all()
    tx_dicts = [
        {
            "id": t.id,
            "case_id": t.case_id,
            "timestamp": t.timestamp,
            "sender_account": t.sender_account,
            "sender_name": t.sender_name,
            "receiver_account": t.receiver_account,
            "receiver_name": t.receiver_name,
            "amount": t.amount,
            "transaction_type": t.transaction_type,
            "description": t.description,
            "reference_number": t.reference_number
        }
        for t in txs
    ]

    analyzed, summary = analytics_engine.analyze_transactions(tx_dicts)

    # Persist findings back to db
    analysis_map = {r["id"]: r for r in analyzed}
    for t in txs:
        if t.id in analysis_map:
            t_data = analysis_map[t.id]
            t.risk_flag = t_data["risk_flag"]
            t.anomaly_score = t_data["anomaly_score"]
            t.flag_reasons = json.dumps(t_data["flag_reasons"])
            t.detection_method = t_data["detection_method"]

    # Update account risk tags based on detected mule candidates
    mule_accs = {m["account"] for m in summary.get("mule_candidates", [])}
    for acc in db.query(Account).filter(Account.case_id == case_id).all():
        if acc.id in mule_accs:
            acc.risk_level = "CRITICAL"
            acc.risk_score = 92.0
            tags = []
            try:
                tags = json.loads(acc.risk_tags) if isinstance(acc.risk_tags, str) else acc.risk_tags
            except Exception:
                pass
            if "MULE_CONDUIT" not in tags:
                tags.append("MULE_CONDUIT")
            acc.risk_tags = json.dumps(tags)

    db.commit()

    return {
        "status": "completed",
        "case_id": case_id,
        "summary": summary
    }

# --- Accounts ---
@router.get("/accounts")
def list_accounts(case_id: Optional[str] = None, risk_level: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Account)
    if case_id:
        query = query.filter(Account.case_id == case_id)
    if risk_level and risk_level != "ALL":
        query = query.filter(Account.risk_level == risk_level)

    accs = query.all()
    results = []
    for a in accs:
        tags = []
        try:
            tags = json.loads(a.risk_tags) if isinstance(a.risk_tags, str) else a.risk_tags
        except Exception:
            pass
        results.append({
            "id": a.id,
            "account_number": a.account_number,
            "case_id": a.case_id,
            "account_holder": a.account_holder,
            "bank_name": a.bank_name,
            "account_type": a.account_type,
            "risk_level": a.risk_level,
            "risk_score": a.risk_score,
            "risk_tags": tags,
            "total_inflow": a.total_inflow,
            "total_outflow": a.total_outflow,
            "transaction_count": a.transaction_count,
            "is_synthetic": a.is_synthetic
        })
    return results

# --- Network Graph (React Flow) ---
@router.get("/graph/{case_id}")
def get_case_graph(case_id: str, min_amount: float = 0.0, db: Session = Depends(get_db)):
    txs = db.query(Transaction).filter(Transaction.case_id == case_id).all()
    accounts = db.query(Account).filter(Account.case_id == case_id).all()
    
    tx_dicts = [
        {
            "id": t.id,
            "sender_account": t.sender_account,
            "sender_name": t.sender_name,
            "receiver_account": t.receiver_account,
            "receiver_name": t.receiver_name,
            "amount": t.amount,
            "timestamp": t.timestamp.isoformat(),
            "transaction_type": t.transaction_type,
            "risk_flag": t.risk_flag
        }
        for t in txs
    ]

    accounts_map = {
        a.id: {
            "account_holder": a.account_holder,
            "bank_name": a.bank_name,
            "account_type": a.account_type,
            "risk_level": a.risk_level,
            "risk_score": a.risk_score,
            "risk_tags": a.risk_tags,
            "total_inflow": a.total_inflow,
            "total_outflow": a.total_outflow
        }
        for a in accounts
    }

    graph_data = NetworkGraphService.build_graph(tx_dicts, accounts_map, min_amount=min_amount)
    return {
        "case_id": case_id,
        "nodes": graph_data["nodes"],
        "edges": graph_data["edges"],
        "summary": graph_data["summary"]
    }

# --- Digital Intelligence ---
@router.get("/intelligence/{case_id}")
def get_case_intelligence(case_id: str, db: Session = Depends(get_db)):
    intel = db.query(DigitalIntelligence).filter(DigitalIntelligence.case_id == case_id).all()
    results = []
    for it in intel:
        meta = {}
        try:
            meta = json.loads(it.metadata_json) if isinstance(it.metadata_json, str) else it.metadata_json
        except Exception:
            pass
        results.append({
            "id": it.id,
            "case_id": it.case_id,
            "indicator_type": it.indicator_type,
            "indicator_value": it.indicator_value,
            "associated_account": it.associated_account,
            "lookup_source": it.lookup_source,
            "metadata": meta,
            "risk_rating": it.risk_rating,
            "verification_status": it.verification_status,
            "observed_at": it.observed_at.isoformat()
        })
    return results

@router.post("/intelligence/lookup")
def perform_intel_lookup(indicator: str = Form(...), indicator_type: str = Form("AUTO")):
    res = intel_service.query_indicator(indicator, indicator_type)
    return res

# --- Cross-Case Analysis ---
@router.get("/cross-case/correlations")
def get_cross_case_correlations(target_case_id: Optional[str] = None, db: Session = Depends(get_db)):
    matches = CrossCaseAnalysisService.find_cross_case_correlations(db, target_case_id)
    return {
        "total_correlations": len(matches),
        "target_case_id": target_case_id,
        "correlations": matches
    }

# --- AI Investigation Assistant ---
@router.post("/assistant/chat", response_model=AIChatResponse)
def chat_with_assistant(req: AIChatRequest, db: Session = Depends(get_db)):
    resp = AIAssistantService.query(db, req.case_id, req.message, req.history)
    return resp

# --- Reports & PDF Generation ---
@router.get("/reports/pdf/{case_id}")
def download_investigation_report(case_id: str, db: Session = Depends(get_db)):
    case = db.query(Investigation).filter(Investigation.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Investigation case not found")

    pdf_bytes = ReportPDFService.generate_case_pdf(db, case_id)
    safe_case_no = case.case_number.replace("/", "_").replace("-", "_")
    filename = f"TRACEGRID_Report_{safe_case_no}.pdf"

    return StreamingResponse(
        io.BytesIO(pdf_bytes),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

# --- Demo Reset ---
@router.post("/demo/reset")
def reset_demonstration_data(db: Session = Depends(get_db)):
    # Delete child records first
    db.query(ActivityLog).delete()
    db.query(AnalysisResult).delete()
    db.query(DigitalIntelligence).delete()
    db.query(Evidence).delete()
    db.query(Transaction).delete()
    db.query(Account).delete()
    db.query(Investigation).delete()
    db.commit()

    # Re-seed
    from backend.seed_data import seed_database
    seed_database()
    return {"status": "success", "message": "Demonstration database successfully re-initialized with standard scenarios."}
