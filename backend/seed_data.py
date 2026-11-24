import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import datetime
import json
import random
from sqlalchemy.orm import Session
from backend.core.database import SessionLocal, engine, Base
from backend.models.models import Investigation, Account, Transaction, Evidence, DigitalIntelligence, AnalysisResult, ActivityLog
from backend.analytics.engine import TransactionAnalyticsEngine

def seed_database():
    """Initializes the database schema and populates rich synthetic demonstration scenarios."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Check if cases already exist
    existing_count = db.query(Investigation).count()
    if existing_count > 0:
        print(f"Database already contains {existing_count} investigations. Skipping seed or clearing...")
        return

    print("Seeding TRACEGRID demonstration scenarios...")

    # -------------------------------------------------------------
    # CASE 1: Operation Maru-Dhar (Mule Network & Hawala Layering)
    # -------------------------------------------------------------
    case1 = Investigation(
        id="case-001",
        case_number="RJ-EOW-2026-0042",
        title="Operation Maru-Dhar: Multi-Layered Mule Syndicate",
        description="Investigation into coordinated high-velocity fund diversion involving 14 mule accounts, rapid structuring, nocturnal transfers, and crypto-ramp liquidation.",
        priority="CRITICAL",
        status="ACTIVE",
        lead_investigator="Insp. Vikram Rathore (Cyber Crime EOW)",
        created_at=datetime.datetime(2026, 2, 10, 10, 30)
    )
    db.add(case1)

    # Accounts for Case 1
    case1_accounts = [
        # Victims / Inflow Sources
        Account(
            id="case-001_ACC-VIC-1001",
            account_number="ACC-VIC-1001",
            case_id="case-001",
            account_holder="Marwar Logistics Enterprises",
            bank_name="State Bank of India (Jaipur Main)",
            account_type="CURRENT",
            risk_level="LOW",
            risk_score=10.0,
            risk_tags=json.dumps(["VICTIM_SOURCE"]),
            total_inflow=0.0,
            total_outflow=1850000.0,
            transaction_count=2,
            is_synthetic=True
        ),
        Account(
            id="case-001_ACC-VIC-1002",
            account_number="ACC-VIC-1002",
            case_id="case-001",
            account_holder="Dr. Arvind Meena",
            bank_name="Punjab National Bank (Jodhpur)",
            account_type="SAVINGS",
            risk_level="LOW",
            risk_score=12.0,
            risk_tags=json.dumps(["VICTIM_SOURCE"]),
            total_inflow=0.0,
            total_outflow=1200000.0,
            transaction_count=2,
            is_synthetic=True
        ),
        # Primary Mule / Inflow Aggregators
        Account(
            id="case-001_ACC-MULE-2001",
            account_number="ACC-MULE-2001",
            case_id="case-001",
            account_holder="Kishore Kumar Sharma (Synthetic Persona)",
            bank_name="HDFC Bank (Alwar Branch)",
            account_type="SAVINGS",
            risk_level="CRITICAL",
            risk_score=94.0,
            risk_tags=json.dumps(["MULE_CONDUIT", "PASS_THROUGH", "RAPID_DRAIN"]),
            total_inflow=1850000.0,
            total_outflow=1840000.0,
            transaction_count=8,
            is_synthetic=True
        ),
        Account(
            id="case-001_ACC-MULE-2002",
            account_number="ACC-MULE-2002",
            case_id="case-001",
            account_holder="Sunil Yadav (Dormant Account Activated)",
            bank_name="ICICI Bank (Sikar)",
            account_type="SAVINGS",
            risk_level="HIGH",
            risk_score=88.0,
            risk_tags=json.dumps(["MULE_CONDUIT", "HIGH_VELOCITY", "DORMANT_SPIKE"]),
            total_inflow=1200000.0,
            total_outflow=1180000.0,
            transaction_count=6,
            is_synthetic=True
        ),
        # Intermediary Layering Accounts
        Account(
            id="case-001_ACC-LAYER-3001",
            account_number="ACC-LAYER-3001",
            case_id="case-001",
            account_holder="Devi Trading Agency",
            bank_name="Axis Bank (Bikaner)",
            account_type="CURRENT",
            risk_level="HIGH",
            risk_score=82.0,
            risk_tags=json.dumps(["SHELL_ENTITY", "STRUCTURING_HUB"]),
            total_inflow=950000.0,
            total_outflow=940000.0,
            transaction_count=7,
            is_synthetic=True
        ),
        Account(
            id="case-001_ACC-LAYER-3002",
            account_number="ACC-LAYER-3002",
            case_id="case-001",
            account_holder="Pooja Telematics Services",
            bank_name="Kotak Mahindra Bank (Kota)",
            account_type="CURRENT",
            risk_level="HIGH",
            risk_score=79.0,
            risk_tags=json.dumps(["SHELL_ENTITY", "CIRCULAR_HOP"]),
            total_inflow=890000.0,
            total_outflow=885000.0,
            transaction_count=6,
            is_synthetic=True
        ),
        # Shared Account between Case 1 and Case 3
        Account(
            id="case-001_ACC-SHARED-9921",
            account_number="ACC-SHARED-9921",
            case_id="case-001",
            account_holder="Aman Verma (Student Mule Syndicate)",
            bank_name="Canara Bank (Ajmer)",
            account_type="SAVINGS",
            risk_level="CRITICAL",
            risk_score=96.0,
            risk_tags=json.dumps(["CROSS_CASE_SYNDICATE", "MULE_CONDUIT", "BURST_RECIPIENT"]),
            total_inflow=620000.0,
            total_outflow=615000.0,
            transaction_count=9,
            is_synthetic=True
        ),
        # Terminal Liquidation
        Account(
            id="case-001_ACC-EXIT-4001",
            account_number="ACC-EXIT-4001",
            case_id="case-001",
            account_holder="Apex Pay Crypto Gateway Nodal",
            bank_name="Yes Bank (Mumbai Corporate)",
            account_type="NODAL",
            risk_level="CRITICAL",
            risk_score=91.0,
            risk_tags=json.dumps(["CRYPTO_RAMP", "TERMINAL_SINK"]),
            total_inflow=2450000.0,
            total_outflow=0.0,
            transaction_count=5,
            is_synthetic=True
        )
    ]
    for acc in case1_accounts:
        db.add(acc)

    # Transactions for Case 1
    t0 = datetime.datetime(2026, 2, 11, 2, 15) # Nocturnal burst
    case1_txs = [
        # Victim transfers into Mule 2001 & 2002
        Transaction(
            id="TXN-2026-00101",
            case_id="case-001",
            timestamp=t0,
            sender_account="ACC-VIC-1001",
            sender_name="Marwar Logistics Enterprises",
            receiver_account="ACC-MULE-2001",
            receiver_name="Kishore Kumar Sharma",
            amount=950000.0,
            transaction_type="RTGS",
            description="Invoice Settlement Adv Pmt",
            reference_number="RTGS260211009182",
            risk_flag="HIGH_RISK",
            anomaly_score=0.88,
            flag_reasons=json.dumps(["High-Value Transaction exceeding ₹2,00,000", "Off-Hours Activity (02:15 AM)"]),
            detection_method="RULE_BASED"
        ),
        Transaction(
            id="TXN-2026-00102",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(minutes=12),
            sender_account="ACC-VIC-1001",
            sender_name="Marwar Logistics Enterprises",
            receiver_account="ACC-MULE-2001",
            receiver_name="Kishore Kumar Sharma",
            amount=900000.0,
            transaction_type="RTGS",
            description="Balance Clearance Material",
            reference_number="RTGS260211009189",
            risk_flag="HIGH_RISK",
            anomaly_score=0.86,
            flag_reasons=json.dumps(["High-Value Transaction exceeding ₹2,00,000", "Off-Hours Activity (02:27 AM)"]),
            detection_method="RULE_BASED"
        ),
        Transaction(
            id="TXN-2026-00103",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(minutes=25),
            sender_account="ACC-VIC-1002",
            sender_name="Dr. Arvind Meena",
            receiver_account="ACC-MULE-2002",
            receiver_name="Sunil Yadav",
            amount=600000.0,
            transaction_type="NEFT",
            description="Security Deposit Loan",
            reference_number="NEFT260211019201",
            risk_flag="HIGH_RISK",
            anomaly_score=0.81,
            flag_reasons=json.dumps(["High-Value Transaction", "Off-Hours Activity"]),
            detection_method="RULE_BASED"
        ),
        Transaction(
            id="TXN-2026-00104",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(minutes=31),
            sender_account="ACC-VIC-1002",
            sender_name="Dr. Arvind Meena",
            receiver_account="ACC-MULE-2002",
            receiver_name="Sunil Yadav",
            amount=600000.0,
            transaction_type="NEFT",
            description="Procurement Share",
            reference_number="NEFT260211019205",
            risk_flag="HIGH_RISK",
            anomaly_score=0.81,
            flag_reasons=json.dumps(["High-Value Transaction", "Off-Hours Activity"]),
            detection_method="RULE_BASED"
        ),
        # Immediate Rapid Layering out of Mule Accounts (< 45 minutes)
        Transaction(
            id="TXN-2026-00105",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(minutes=45),
            sender_account="ACC-MULE-2001",
            sender_name="Kishore Kumar Sharma",
            receiver_account="ACC-LAYER-3001",
            receiver_name="Devi Trading Agency",
            amount=950000.0,
            transaction_type="IMPS",
            description="TRF Devi Agro Trd",
            reference_number="IMPS260211440192",
            risk_flag="MULE_INDICATOR",
            anomaly_score=0.92,
            flag_reasons=json.dumps(["Mule Conduit Profile: Instant Pass-Through", "Round-Sum Structuring Pattern"]),
            detection_method="HYBRID_ENSEMBLE"
        ),
        Transaction(
            id="TXN-2026-00106",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(minutes=50),
            sender_account="ACC-MULE-2001",
            sender_name="Kishore Kumar Sharma",
            receiver_account="ACC-LAYER-3002",
            receiver_name="Pooja Telematics Services",
            amount=890000.0,
            transaction_type="IMPS",
            description="Consultancy fee trf",
            reference_number="IMPS260211440210",
            risk_flag="MULE_INDICATOR",
            anomaly_score=0.90,
            flag_reasons=json.dumps(["Mule Conduit Profile: Instant Pass-Through", "High Velocity Burst"]),
            detection_method="HYBRID_ENSEMBLE"
        ),
        Transaction(
            id="TXN-2026-00107",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(minutes=55),
            sender_account="ACC-MULE-2002",
            sender_name="Sunil Yadav",
            receiver_account="ACC-SHARED-9921",
            receiver_name="Aman Verma",
            amount=620000.0,
            transaction_type="IMPS",
            description="Urgent student support",
            reference_number="IMPS260211440255",
            risk_flag="MULE_INDICATOR",
            anomaly_score=0.93,
            flag_reasons=json.dumps(["Mule Conduit Profile", "Cross-Case Syndicate Node", "ML Outlier"]),
            detection_method="HYBRID_ENSEMBLE"
        ),
        Transaction(
            id="TXN-2026-00108",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(minutes=58),
            sender_account="ACC-MULE-2002",
            sender_name="Sunil Yadav",
            receiver_account="ACC-EXIT-4001",
            receiver_name="Apex Pay Crypto Gateway Nodal",
            amount=560000.0,
            transaction_type="IMPS",
            description="Order P2P-98124USDT",
            reference_number="IMPS260211440280",
            risk_flag="HIGH_RISK",
            anomaly_score=0.95,
            flag_reasons=json.dumps(["Crypto Ramp Terminal Liquidation", "ML Isolation Forest Anomaly"]),
            detection_method="ISOLATION_FOREST"
        ),
        # Layering Consolidation into Crypto Gateway
        Transaction(
            id="TXN-2026-00109",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(hours=1, minutes=15),
            sender_account="ACC-LAYER-3001",
            sender_name="Devi Trading Agency",
            receiver_account="ACC-EXIT-4001",
            receiver_name="Apex Pay Crypto Gateway Nodal",
            amount=940000.0,
            transaction_type="RTGS",
            description="Wholesale digital voucher",
            reference_number="RTGS260211881299",
            risk_flag="HIGH_RISK",
            anomaly_score=0.89,
            flag_reasons=json.dumps(["Structuring into Crypto Exit", "High-Value Transaction"]),
            detection_method="RULE_BASED"
        ),
        Transaction(
            id="TXN-2026-00110",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(hours=1, minutes=20),
            sender_account="ACC-LAYER-3002",
            sender_name="Pooja Telematics Services",
            receiver_account="ACC-EXIT-4001",
            receiver_name="Apex Pay Crypto Gateway Nodal",
            amount=885000.0,
            transaction_type="RTGS",
            description="Server lease settlement",
            reference_number="RTGS260211881312",
            risk_flag="HIGH_RISK",
            anomaly_score=0.88,
            flag_reasons=json.dumps(["Structuring into Crypto Exit", "High-Value Transaction"]),
            detection_method="RULE_BASED"
        ),
        # Circular Loop Demonstration (ACC-SHARED-9921 -> ACC-LAYER-3001)
        Transaction(
            id="TXN-2026-00111",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(hours=1, minutes=30),
            sender_account="ACC-SHARED-9921",
            sender_name="Aman Verma",
            receiver_account="ACC-LAYER-3001",
            receiver_name="Devi Trading Agency",
            amount=50000.0,
            transaction_type="UPI",
            description="Return collateral deposit",
            reference_number="UPI260211991201",
            risk_flag="CIRCULAR_HOP",
            anomaly_score=0.91,
            flag_reasons=json.dumps(["Circular Routing Loop: Part of closed multi-hop cycle", "Round-Sum Structuring"]),
            detection_method="GRAPH_CYCLE"
        ),
        Transaction(
            id="TXN-2026-00112",
            case_id="case-001",
            timestamp=t0 + datetime.timedelta(hours=1, minutes=45),
            sender_account="ACC-SHARED-9921",
            sender_name="Aman Verma",
            receiver_account="ACC-EXIT-4001",
            receiver_name="Apex Pay Crypto Gateway Nodal",
            amount=65000.0,
            transaction_type="IMPS",
            description="P2P Escrow Release",
            reference_number="IMPS260211991244",
            risk_flag="HIGH_RISK",
            anomaly_score=0.84,
            flag_reasons=json.dumps(["Rapid Movement to Crypto Gateway"]),
            detection_method="RULE_BASED"
        )
    ]
    for tx in case1_txs:
        db.add(tx)

    # Digital Intelligence for Case 1
    case1_intel = [
        DigitalIntelligence(
            case_id="case-001",
            indicator_type="DOMAIN",
            indicator_value="fast-payout-gateway.cc",
            associated_account="ACC-MULE-2001",
            lookup_source="Passive DNS Registry (DEMO)",
            metadata_json=json.dumps({
                "registrar": "NameCheap Inc. (Privacy Shielded)",
                "created": "2025-11-14",
                "resolved_ip": "185.220.101.44",
                "asn": "AS49981 (HostRoyale Offshore Infrastructure)",
                "country": "Seychelles"
            }),
            risk_rating="MALICIOUS",
            verification_status="CORROBORATED_SIMULATION",
            observed_at=datetime.datetime(2026, 2, 11, 2, 30)
        ),
        DigitalIntelligence(
            case_id="case-001",
            indicator_type="IP_ADDRESS",
            indicator_value="185.220.101.44",
            associated_account="ACC-MULE-2001",
            lookup_source="Spamhaus & AbuseIPDB Feed (DEMO)",
            metadata_json=json.dumps({
                "asn": "AS49981",
                "org": "Bulletproof Net B.V.",
                "tor_exit": True,
                "vpn": True,
                "country": "Netherlands"
            }),
            risk_rating="MALICIOUS",
            verification_status="VERIFIED_RECORD",
            observed_at=datetime.datetime(2026, 2, 11, 2, 35)
        ),
        DigitalIntelligence(
            case_id="case-001",
            indicator_type="DOMAIN",
            indicator_value="apex-pay-nodal.is",
            associated_account="ACC-EXIT-4001",
            lookup_source="Whois Privacy Monitor (DEMO)",
            metadata_json=json.dumps({
                "registrar": "ISNIC Registrar",
                "created": "2025-07-22",
                "resolved_ip": "104.26.12.88",
                "asn": "AS13335 (Cloudflare)",
                "country": "Iceland / CDN"
            }),
            risk_rating="SUSPICIOUS",
            verification_status="VERIFIED_RECORD",
            observed_at=datetime.datetime(2026, 2, 11, 3, 10)
        )
    ]
    for it in case1_intel:
        db.add(it)

    # Evidence for Case 1
    case1_evidences = [
        Evidence(
            case_id="case-001",
            title="SBI Marwar Logistics Account Statement (Jan-Feb 2026)",
            evidence_type="BANK_STATEMENT",
            file_name="SBI_Marwar_Stmt_Feb2026.csv",
            file_hash="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            source="Subpoena Response Sec 91 CrPC",
            verification_status="VERIFIED",
            notes="Certified bank statement showing primary victim debits."
        ),
        Evidence(
            case_id="case-001",
            title="CERT-In Phishing Incident Advisory Fin-2026-440",
            evidence_type="IP_LOG",
            file_name="CERT_Advisory_440.pdf",
            file_hash="8f4b2326b704d5633352273b80a525da40e5b774544b167da52d7176d0f772b4",
            source="CERT-In New Delhi",
            verification_status="CORROBORATED",
            notes="Correlates IP 185.220.101.44 with rogue banking Trojan communication."
        )
    ]
    for ev in case1_evidences:
        db.add(ev)

    # Activity Logs for Case 1
    db.add(ActivityLog(
        case_id="case-001",
        action="CASE_CREATED",
        actor="Insp. Vikram Rathore",
        details="Case registered under FIR No. 42/2026 PS Cyber Crime Jaipur.",
        timestamp=datetime.datetime(2026, 2, 10, 10, 30)
    ))
    db.add(ActivityLog(
        case_id="case-001",
        action="STATEMENT_PARSED",
        actor="Automated Ingestion Engine",
        details="Imported 12 transactions from primary victim statements.",
        timestamp=datetime.datetime(2026, 2, 11, 9, 0)
    ))
    db.add(ActivityLog(
        case_id="case-001",
        action="ANALYTICS_RUN",
        actor="TRACEGRID Analytics Engine",
        details="Flagged 12/12 transactions with high/critical anomaly indicators.",
        timestamp=datetime.datetime(2026, 2, 11, 9, 15)
    ))

    # -------------------------------------------------------------
    # CASE 2: Operation Golden Sand (Extortion Loan App Loop)
    # -------------------------------------------------------------
    case2 = Investigation(
        id="case-002",
        case_number="RJ-CYBER-2026-0109",
        title="Operation Golden Sand: Predatory Loan App & Layering Loop",
        description="Exploitative instant micro-loan app extorting borrowers and routing collections through closed circular cycles to obscure money flows.",
        priority="HIGH",
        status="ACTIVE",
        lead_investigator="Sub-Insp. Priya Sharma (Special Operations Group)",
        created_at=datetime.datetime(2026, 2, 14, 14, 0)
    )
    db.add(case2)

    case2_accounts = [
        Account(
            id="case-002_ACC-APP-5001",
            account_number="ACC-APP-5001",
            case_id="case-002",
            account_holder="QuickCredit FinTech Solution",
            bank_name="RBL Bank (Gurugram)",
            account_type="NODAL",
            risk_level="CRITICAL",
            risk_score=92.0,
            risk_tags=json.dumps(["UNLICENSED_LENDER", "CIRCULAR_HUB"]),
            total_inflow=750000.0,
            total_outflow=750000.0,
            transaction_count=6,
            is_synthetic=True
        ),
        Account(
            id="case-002_ACC-CIRC-5002",
            account_number="ACC-CIRC-5002",
            case_id="case-002",
            account_holder="SandDune Enterprises",
            bank_name="IndusInd Bank (Jaipur)",
            account_type="CURRENT",
            risk_level="HIGH",
            risk_score=85.0,
            risk_tags=json.dumps(["CIRCULAR_HOP", "PASS_THROUGH"]),
            total_inflow=500000.0,
            total_outflow=500000.0,
            transaction_count=4,
            is_synthetic=True
        ),
        Account(
            id="case-002_ACC-CIRC-5003",
            account_number="ACC-CIRC-5003",
            case_id="case-002",
            account_holder="Thar Marketing & Logistics",
            bank_name="Federal Bank (Jodhpur)",
            account_type="CURRENT",
            risk_level="HIGH",
            risk_score=84.0,
            risk_tags=json.dumps(["CIRCULAR_HOP", "WASH_TRADING"]),
            total_inflow=500000.0,
            total_outflow=500000.0,
            transaction_count=4,
            is_synthetic=True
        )
    ]
    for acc in case2_accounts:
        db.add(acc)

    # Circular loop transactions: 5001 -> 5002 -> 5003 -> 5001
    t_c2 = datetime.datetime(2026, 2, 15, 11, 0)
    case2_txs = [
        Transaction(
            id="TXN-2026-00201",
            case_id="case-002",
            timestamp=t_c2,
            sender_account="ACC-APP-5001",
            sender_name="QuickCredit FinTech",
            receiver_account="ACC-CIRC-5002",
            receiver_name="SandDune Enterprises",
            amount=250000.0,
            transaction_type="NEFT",
            description="Service Retainer Adv",
            reference_number="NEFT260215001122",
            risk_flag="CIRCULAR_HOP",
            anomaly_score=0.92,
            flag_reasons=json.dumps(["Circular Routing Loop: Part of 3-hop closed cycle", "High-Value Transaction"]),
            detection_method="GRAPH_CYCLE"
        ),
        Transaction(
            id="TXN-2026-00202",
            case_id="case-002",
            timestamp=t_c2 + datetime.timedelta(minutes=30),
            sender_account="ACC-CIRC-5002",
            sender_name="SandDune Enterprises",
            receiver_account="ACC-CIRC-5003",
            receiver_name="Thar Marketing & Logistics",
            amount=250000.0,
            transaction_type="IMPS",
            description="Logistics sub-contract fee",
            reference_number="IMPS260215004455",
            risk_flag="CIRCULAR_HOP",
            anomaly_score=0.92,
            flag_reasons=json.dumps(["Circular Routing Loop: Part of 3-hop closed cycle", "Rapid Pass-Through"]),
            detection_method="GRAPH_CYCLE"
        ),
        Transaction(
            id="TXN-2026-00203",
            case_id="case-002",
            timestamp=t_c2 + datetime.timedelta(hours=1),
            sender_account="ACC-CIRC-5003",
            sender_name="Thar Marketing & Logistics",
            receiver_account="ACC-APP-5001",
            receiver_name="QuickCredit FinTech",
            amount=250000.0,
            transaction_type="RTGS",
            description="Rebate & Refund of Retainer",
            reference_number="RTGS260215007788",
            risk_flag="CIRCULAR_HOP",
            anomaly_score=0.94,
            flag_reasons=json.dumps(["Circular Routing Loop: Cycle Closed back to Originator", "Wash Layering"]),
            detection_method="GRAPH_CYCLE"
        )
    ]
    for tx in case2_txs:
        db.add(tx)

    case2_intel = [
        DigitalIntelligence(
            case_id="case-002",
            indicator_type="DOMAIN",
            indicator_value="quick-loan-bharat-api.net",
            associated_account="ACC-APP-5001",
            lookup_source="RBI Sachet Portal Incident Registry (DEMO)",
            metadata_json=json.dumps({
                "registrar": "Tucows Domains Inc.",
                "created": "2025-08-19",
                "resolved_ip": "103.145.12.89",
                "asn": "AS133982 (Asia Pacific Internet Exch)",
                "country": "India (Mumbai Cloud)"
            }),
            risk_rating="SUSPICIOUS",
            verification_status="VERIFIED_RECORD",
            observed_at=datetime.datetime(2026, 2, 14, 15, 0)
        )
    ]
    for it in case2_intel:
        db.add(it)

    # -------------------------------------------------------------
    # CASE 3: Operation PhishGrid (Shared Syndicate Account with Case 1)
    # -------------------------------------------------------------
    case3 = Investigation(
        id="case-003",
        case_number="RJ-EOW-2026-0215",
        title="Operation PhishGrid: Spoofed KYC Harvest & Kota Ring",
        description="Mass smishing campaign delivering fake KYC update links, harvesting net banking tokens and routing through student syndicate mule networks.",
        priority="HIGH",
        status="IN_REVIEW",
        lead_investigator="Insp. Vikram Rathore (Cyber Crime EOW)",
        created_at=datetime.datetime(2026, 2, 18, 9, 15)
    )
    db.add(case3)

    # Cross-case link: ACC-SHARED-9921 is present in both Case 1 and Case 3!
    case3_accounts = [
        Account(
            id="case-003_ACC-SHARED-9921",
            account_number="ACC-SHARED-9921",
            case_id="case-003",
            account_holder="Aman Verma (Student Mule Syndicate)",
            bank_name="Canara Bank (Ajmer)",
            account_type="SAVINGS",
            risk_level="CRITICAL",
            risk_score=96.0,
            risk_tags=json.dumps(["CROSS_CASE_SYNDICATE", "MULE_CONDUIT", "BURST_RECIPIENT"]),
            total_inflow=450000.0,
            total_outflow=445000.0,
            transaction_count=6,
            is_synthetic=True
        ),
        Account(
            id="case-003_ACC-VIC-3001",
            account_number="ACC-VIC-3001",
            case_id="case-003",
            account_holder="Sunita Devi (Teacher)",
            bank_name="Bank of Baroda (Kota)",
            account_type="SAVINGS",
            risk_level="LOW",
            risk_score=8.0,
            risk_tags=json.dumps(["PHISHING_VICTIM"]),
            total_inflow=0.0,
            total_outflow=450000.0,
            transaction_count=1,
            is_synthetic=True
        )
    ]
    for acc in case3_accounts:
        db.add(acc)

    case3_txs = [
        Transaction(
            id="TXN-2026-00301",
            case_id="case-003",
            timestamp=datetime.datetime(2026, 2, 18, 14, 20),
            sender_account="ACC-VIC-3001",
            sender_name="Sunita Devi",
            receiver_account="ACC-SHARED-9921",
            receiver_name="Aman Verma",
            amount=450000.0,
            transaction_type="IMPS",
            description="Unauthorized NetBanking Trf",
            reference_number="IMPS260218774411",
            risk_flag="HIGH_RISK",
            anomaly_score=0.91,
            flag_reasons=json.dumps(["High-Value Drain from Retail Account", "Cross-Case Linked Recipient"]),
            detection_method="RULE_BASED"
        )
    ]
    for tx in case3_txs:
        db.add(tx)

    case3_intel = [
        DigitalIntelligence(
            case_id="case-003",
            indicator_type="DOMAIN",
            indicator_value="paytm-kyc-verify-portal.in",
            associated_account="ACC-SHARED-9921",
            lookup_source="CERT-In FinThreat Feed (DEMO)",
            metadata_json=json.dumps({
                "registrar": "Public Domain Registry",
                "created": "2026-01-03",
                "resolved_ip": "194.26.29.112",
                "asn": "AS206804 (EstNOC Dedicated Hosting)",
                "country": "Estonia"
            }),
            risk_rating="MALICIOUS",
            verification_status="CORROBORATED_SIMULATION",
            observed_at=datetime.datetime(2026, 2, 18, 14, 0)
        ),
        # Cross-case indicator: also shares 185.220.101.44
        DigitalIntelligence(
            case_id="case-003",
            indicator_type="IP_ADDRESS",
            indicator_value="185.220.101.44",
            associated_account="ACC-SHARED-9921",
            lookup_source="Shared Threat Intel Nexus (DEMO)",
            metadata_json=json.dumps({
                "asn": "AS49981",
                "org": "Bulletproof Net B.V.",
                "tor_exit": True,
                "country": "Netherlands"
            }),
            risk_rating="MALICIOUS",
            verification_status="VERIFIED_RECORD",
            observed_at=datetime.datetime(2026, 2, 18, 14, 25)
        )
    ]
    for it in case3_intel:
        db.add(it)

    db.commit()
    db.close()
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed_database()
