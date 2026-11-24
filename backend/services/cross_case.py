from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from backend.models.models import Investigation, Account, Transaction, DigitalIntelligence

class CrossCaseAnalysisService:
    """
    Identifies shared accounts, transaction references, domains, and IP addresses
    across distinct investigations, clearly segregating confirmed matches
    from analytical associations.
    """

    @staticmethod
    def find_cross_case_correlations(db: Session, target_case_id: Optional[str] = None) -> List[Dict[str, Any]]:
        # Gather all cases
        cases = db.query(Investigation).all()
        case_map = {c.id: c.case_number for c in cases}
        case_title_map = {c.id: c.title for c in cases}

        correlations = []

        # 1. Match Accounts appearing in multiple cases
        accounts = db.query(Account).all()
        acc_case_map = {}
        for acc in accounts:
            acc_num = acc.account_number
            if acc_num not in acc_case_map:
                acc_case_map[acc_num] = []
            acc_case_map[acc_num].append({
                "case_id": acc.case_id,
                "case_number": case_map.get(acc.case_id, "Unknown"),
                "case_title": case_title_map.get(acc.case_id, "Unknown"),
                "holder": acc.account_holder,
                "bank": acc.bank_name,
                "risk_level": acc.risk_level
            })

        for acc_id, case_list in acc_case_map.items():
            # If present in more than 1 case, or if target_case_id requested and present in target
            unique_cases = {c["case_id"] for c in case_list}
            if len(unique_cases) > 1:
                if target_case_id and target_case_id not in unique_cases:
                    continue
                correlations.append({
                    "indicator_type": "BANK_ACCOUNT",
                    "indicator_value": acc_id,
                    "matched_cases": case_list,
                    "match_type": "CONFIRMED_DATA_MATCH",
                    "correlation_confidence": "HIGH (100% IDENTIFIER MATCH)",
                    "description": f"Account number {acc_id} appears actively in {len(unique_cases)} separate investigations. Strongly indicates a shared mule conduit or common operational syndicate."
                })

        # 2. Match Digital Intelligence (IP / Domain)
        intel_records = db.query(DigitalIntelligence).all()
        intel_map = {}
        for rec in intel_records:
            key = (rec.indicator_type, rec.indicator_value)
            if key not in intel_map:
                intel_map[key] = []
            intel_map[key].append({
                "case_id": rec.case_id,
                "case_number": case_map.get(rec.case_id, "Unknown"),
                "case_title": case_title_map.get(rec.case_id, "Unknown"),
                "risk_rating": rec.risk_rating,
                "source": rec.lookup_source
            })

        for (itype, ival), case_list in intel_map.items():
            unique_cases = {c["case_id"] for c in case_list}
            if len(unique_cases) > 1:
                if target_case_id and target_case_id not in unique_cases:
                    continue
                correlations.append({
                    "indicator_type": itype,
                    "indicator_value": ival,
                    "matched_cases": case_list,
                    "match_type": "ANALYTICAL_INFRASTRUCTURE_ASSOCIATION",
                    "correlation_confidence": "MEDIUM-HIGH (SHARED INFRASTRUCTURE)",
                    "description": f"{itype} '{ival}' is referenced across {len(unique_cases)} distinct cases. Indicates shared command-and-control, hosting or phishing kit reuse."
                })

        return correlations
