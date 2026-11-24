import datetime
import json
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Tuple
import networkx as nx

class TransactionAnalyticsEngine:
    """
    TRACEGRID Financial Crime Analytics Engine.
    Combines rule-based indicators, behavioral heuristics, graph cycle analysis,
    and Scikit-learn IsolationForest anomaly detection.
    
    Principles:
    - Never declares guilt; produces explainable investigative leads.
    - Clearly distinguishes between deterministic rule breaches, statistical anomalies, and graph topology flags.
    """

    def __init__(
        self,
        large_tx_threshold: float = 200000.0,
        burst_threshold_count: int = 4,
        burst_window_minutes: int = 60,
        mule_in_out_ratio_threshold: float = 0.85,
        isolation_forest_contamination: float = 0.08
    ):
        self.large_tx_threshold = large_tx_threshold
        self.burst_threshold_count = burst_threshold_count
        self.burst_window_minutes = burst_window_minutes
        self.mule_in_out_ratio_threshold = mule_in_out_ratio_threshold
        self.contamination = isolation_forest_contamination

    def analyze_transactions(
        self, transactions: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
        if not transactions:
            return [], {
                "total_records": 0,
                "flagged_count": 0,
                "total_volume": 0.0,
                "suspicious_volume": 0.0,
                "circular_paths": [],
                "mule_candidates": [],
                "clean_percentage": 100.0
            }

        records: List[Dict[str, Any]] = [dict(t) for t in transactions]

        # Ensure datetime on timestamp
        for r in records:
            ts = r.get("timestamp")
            if isinstance(ts, str):
                try:
                    r["timestamp"] = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except Exception:
                    r["timestamp"] = datetime.datetime.now(datetime.timezone.utc)
            elif not isinstance(ts, (datetime.datetime, pd.Timestamp)):
                r["timestamp"] = datetime.datetime.now(datetime.timezone.utc)

        # Sort by timestamp
        records.sort(key=lambda x: x["timestamp"])

        # Initialize tracking fields
        for r in records:
            r["risk_flag"] = "NORMAL"
            r["anomaly_score"] = 0.0
            r["flag_reasons"] = list(r.get("flag_reasons", []))
            r["detection_method"] = "RULE_BASED"

        # -------------------------------------------------------------
        # 1. Rule-Based Indicators
        # -------------------------------------------------------------
        for r in records:
            reasons: List[str] = []
            amt = float(r.get("amount", 0.0))
            dt: datetime.datetime = r["timestamp"]

            # Large value spike
            if amt >= self.large_tx_threshold:
                reasons.append(
                    f"High-Value Transaction: Amount ₹{amt:,.2f} exceeds standard reporting threshold (₹{self.large_tx_threshold:,.2f})"
                )

            # Nocturnal execution (12:00 AM - 05:00 AM)
            if 0 <= dt.hour < 5:
                reasons.append(
                    f"Off-Hours Activity: Transaction initiated at {dt.strftime('%H:%M:%S')} (irregular processing window)"
                )

            # Round sum structuring
            if amt >= 20000 and amt % 10000 == 0:
                reasons.append(
                    f"Round-Sum Structuring Pattern: Exactly ₹{amt:,.2f} with zero fractional variance"
                )

            if reasons:
                r["flag_reasons"].extend(reasons)
                r["risk_flag"] = "SUSPICIOUS"

        # -------------------------------------------------------------
        # 2. Velocity / Burst Detection
        # -------------------------------------------------------------
        sender_buckets: Dict[str, List[datetime.datetime]] = {}
        for r in records:
            s_acc = str(r["sender_account"])
            if s_acc not in sender_buckets:
                sender_buckets[s_acc] = []
            sender_buckets[s_acc].append(r["timestamp"])

        for r in records:
            s_acc = str(r["sender_account"])
            t = r["timestamp"]
            # Count transactions from same sender within burst window
            count_in_window = sum(
                1 for other_t in sender_buckets.get(s_acc, [])
                if 0 <= (other_t - t).total_seconds() <= self.burst_window_minutes * 60
            )
            if count_in_window >= self.burst_threshold_count:
                reason = f"High Velocity Burst: {count_in_window} transactions in < {self.burst_window_minutes} mins for sender {s_acc}"
                if reason not in r["flag_reasons"]:
                    r["flag_reasons"].append(reason)
                    r["risk_flag"] = "HIGH_RISK"

        # -------------------------------------------------------------
        # 3. Account-Level Flow & Pass-through Mule Candidate Detection
        # -------------------------------------------------------------
        inflows: Dict[str, float] = {}
        outflows: Dict[str, float] = {}
        for r in records:
            s_acc = str(r["sender_account"])
            r_acc = str(r["receiver_account"])
            amt = float(r.get("amount", 0.0))
            outflows[s_acc] = outflows.get(s_acc, 0.0) + amt
            inflows[r_acc] = inflows.get(r_acc, 0.0) + amt

        all_accounts = set(inflows.keys()).union(set(outflows.keys()))
        mule_accounts: List[Dict[str, Any]] = []

        for acc in all_accounts:
            in_amt = inflows.get(acc, 0.0)
            out_amt = outflows.get(acc, 0.0)
            if in_amt > 25000 and out_amt > 25000:
                min_flow = min(in_amt, out_amt)
                max_flow = max(in_amt, out_amt)
                ratio = min_flow / max_flow if max_flow > 0 else 0.0
                if ratio >= self.mule_in_out_ratio_threshold:
                    mule_accounts.append({
                        "account": acc,
                        "inflow": in_amt,
                        "outflow": out_amt,
                        "ratio": round(ratio, 3),
                        "lead_reason": f"Mule Conduit Profile: Inflow ₹{in_amt:,.2f} rapidly drained by Outflow ₹{out_amt:,.2f} ({ratio*100:.1f}% throughput)"
                    })

        mule_acc_set = {m["account"] for m in mule_accounts}
        for r in records:
            if str(r["sender_account"]) in mule_acc_set or str(r["receiver_account"]) in mule_acc_set:
                reason = "Linked to Pass-Through Mule Account Profile"
                if reason not in r["flag_reasons"]:
                    r["flag_reasons"].append(reason)
                    if r["risk_flag"] == "NORMAL":
                        r["risk_flag"] = "MULE_INDICATOR"

        # -------------------------------------------------------------
        # 4. Graph Cycle Detection (Circular Fund Routing / Wash Layering)
        # -------------------------------------------------------------
        G = nx.DiGraph()
        for r in records:
            u, v = str(r["sender_account"]), str(r["receiver_account"])
            amt = float(r.get("amount", 0.0))
            if G.has_edge(u, v):
                G[u][v]["weight"] += amt
            else:
                G.add_edge(u, v, weight=amt)

        circular_paths: List[Dict[str, Any]] = []
        try:
            cycles = list(nx.simple_cycles(G))
            for cycle in cycles:
                if 2 < len(cycle) <= 6:
                    cycle_str = " -> ".join(cycle) + f" -> {cycle[0]}"
                    circular_paths.append({
                        "length": len(cycle),
                        "path": cycle,
                        "path_display": cycle_str
                    })
                    for i in range(len(cycle)):
                        c_u = cycle[i]
                        c_v = cycle[(i + 1) % len(cycle)]
                        for r in records:
                            if str(r["sender_account"]) == c_u and str(r["receiver_account"]) == c_v:
                                reason = f"Circular Routing Loop: Part of {len(cycle)}-hop closed cycle ({cycle_str})"
                                if reason not in r["flag_reasons"]:
                                    r["flag_reasons"].append(reason)
                                    r["risk_flag"] = "CIRCULAR_HOP"
        except Exception:
            pass

        # -------------------------------------------------------------
        # 5. Isolation Forest Anomaly Detection (Statistical Model)
        # -------------------------------------------------------------
        if len(records) >= 6:
            try:
                amounts = np.array([float(r.get("amount", 0.0)) for r in records], dtype=float)
                hours = np.array([r["timestamp"].hour for r in records], dtype=float)
                log_amounts = np.log1p(amounts)
                feature_matrix = np.column_stack((amounts, log_amounts, hours))

                try:
                    from sklearn.ensemble import IsolationForest
                    forest_kwargs: Dict[str, Any] = {
                        "contamination": float(self.contamination),
                        "random_state": 42,
                        "n_estimators": 50
                    }
                    model = IsolationForest(**forest_kwargs)
                    model.fit(feature_matrix)
                    raw_scores = model.decision_function(feature_matrix)
                    predictions = model.predict(feature_matrix)
                    min_s, max_s = float(raw_scores.min()), float(raw_scores.max())
                    if max_s > min_s:
                        norm_scores = 1.0 - ((raw_scores - min_s) / (max_s - min_s))
                    else:
                        norm_scores = np.zeros(len(raw_scores))
                except Exception:
                    med = float(np.median(amounts))
                    q75, q25 = np.percentile(amounts, [75, 25])
                    iqr = max(float(q75 - q25), 1.0)
                    z_scores = np.abs((amounts - med) / iqr)
                    norm_scores = np.clip(z_scores / 3.0, 0.0, 1.0)
                    predictions = np.where(norm_scores >= 0.75, -1, 1)

                for idx, r in enumerate(records):
                    score = float(norm_scores[idx])
                    r["anomaly_score"] = round(score, 3)

                    if predictions[idx] == -1 and score >= 0.70:
                        reason = f"ML Isolation Forest Anomaly: Deviates from baseline transaction distribution (Anomaly Score: {score:.2f}/1.00)"
                        if reason not in r["flag_reasons"]:
                            r["flag_reasons"].append(reason)

                        if r["detection_method"] == "RULE_BASED" and len(r["flag_reasons"]) > 1:
                            r["detection_method"] = "HYBRID_ENSEMBLE"
                        elif r["detection_method"] == "RULE_BASED":
                            r["detection_method"] = "ISOLATION_FOREST"

                        if r["risk_flag"] in ("NORMAL", "SUSPICIOUS"):
                            r["risk_flag"] = "HIGH_RISK" if score >= 0.85 else "SUSPICIOUS"
            except Exception:
                pass

        # Calculate final summary
        flagged_count = sum(1 for r in records if r["risk_flag"] != "NORMAL")
        total_vol = sum(float(r.get("amount", 0.0)) for r in records)
        susp_vol = sum(float(r.get("amount", 0.0)) for r in records if r["risk_flag"] != "NORMAL")

        summary = {
            "total_records": len(records),
            "flagged_count": flagged_count,
            "total_volume": round(total_vol, 2),
            "suspicious_volume": round(susp_vol, 2),
            "circular_paths": circular_paths[:5],
            "mule_candidates": mule_accounts[:10],
            "clean_percentage": round(((len(records) - flagged_count) / len(records)) * 100, 1) if records else 100.0
        }

        # Format output list
        output_records: List[Dict[str, Any]] = []
        for r in records:
            ts = r["timestamp"]
            ts_str = ts.isoformat() if hasattr(ts, "isoformat") else str(ts)
            output_records.append({
                "id": str(r.get("id", "")),
                "case_id": str(r.get("case_id", "")),
                "timestamp": ts_str,
                "sender_account": str(r.get("sender_account", "")),
                "sender_name": str(r.get("sender_name", "Unknown")),
                "receiver_account": str(r.get("receiver_account", "")),
                "receiver_name": str(r.get("receiver_name", "Unknown")),
                "amount": float(r.get("amount", 0.0)),
                "transaction_type": str(r.get("transaction_type", "IMPS")),
                "description": str(r.get("description", "")),
                "reference_number": str(r.get("reference_number", "")),
                "risk_flag": str(r.get("risk_flag", "NORMAL")),
                "anomaly_score": float(r.get("anomaly_score", 0.0)),
                "flag_reasons": list(r.get("flag_reasons", [])),
                "detection_method": str(r.get("detection_method", "RULE_BASED"))
            })

        return output_records, summary
