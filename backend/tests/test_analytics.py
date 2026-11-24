import pytest
import datetime
from backend.analytics.engine import TransactionAnalyticsEngine

def test_analytics_large_transaction_detection():
    engine = TransactionAnalyticsEngine(large_tx_threshold=100000.0)
    txs = [
        {
            "id": "TX-01",
            "timestamp": datetime.datetime(2026, 2, 10, 14, 0),
            "sender_account": "ACC-A",
            "receiver_account": "ACC-B",
            "amount": 250000.0,
            "transaction_type": "RTGS"
        },
        {
            "id": "TX-02",
            "timestamp": datetime.datetime(2026, 2, 10, 14, 10),
            "sender_account": "ACC-B",
            "receiver_account": "ACC-C",
            "amount": 15000.0,
            "transaction_type": "UPI"
        }
    ]
    analyzed, summary = engine.analyze_transactions(txs)
    assert len(analyzed) == 2
    assert analyzed[0]["risk_flag"] in ("SUSPICIOUS", "HIGH_RISK")
    assert any("High-Value" in r for r in analyzed[0]["flag_reasons"])
    assert analyzed[1]["risk_flag"] == "NORMAL"

def test_circular_cycle_detection():
    engine = TransactionAnalyticsEngine()
    # Closed 3-hop loop: ACC-1 -> ACC-2 -> ACC-3 -> ACC-1
    t0 = datetime.datetime(2026, 2, 10, 10, 0)
    txs = [
        {"id": "T1", "timestamp": t0, "sender_account": "ACC-1", "receiver_account": "ACC-2", "amount": 50000.0, "transaction_type": "IMPS"},
        {"id": "T2", "timestamp": t0 + datetime.timedelta(minutes=10), "sender_account": "ACC-2", "receiver_account": "ACC-3", "amount": 50000.0, "transaction_type": "IMPS"},
        {"id": "T3", "timestamp": t0 + datetime.timedelta(minutes=20), "sender_account": "ACC-3", "receiver_account": "ACC-1", "amount": 50000.0, "transaction_type": "IMPS"}
    ]
    analyzed, summary = engine.analyze_transactions(txs)
    assert len(summary["circular_paths"]) >= 1
    assert any(t["risk_flag"] == "CIRCULAR_HOP" for t in analyzed)

