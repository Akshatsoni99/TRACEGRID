import pytest
from backend.graph.network import NetworkGraphService

def test_graph_construction():
    txs = [
        {"sender_account": "ACC-101", "receiver_account": "ACC-102", "amount": 50000.0, "timestamp": "2026-02-10T10:00:00", "risk_flag": "NORMAL"},
        {"sender_account": "ACC-102", "receiver_account": "ACC-103", "amount": 49000.0, "timestamp": "2026-02-10T10:15:00", "risk_flag": "SUSPICIOUS"},
        {"sender_account": "ACC-103", "receiver_account": "ACC-104", "amount": 48000.0, "timestamp": "2026-02-10T10:30:00", "risk_flag": "MULE_INDICATOR"}
    ]
    graph = NetworkGraphService.build_graph(txs)
    assert len(graph["nodes"]) == 4
    assert len(graph["edges"]) == 3
    assert graph["summary"]["total_nodes"] == 4
    assert graph["summary"]["total_edges"] == 3
    # Verify node structure conforms to React Flow
    for node in graph["nodes"]:
        assert "id" in node
        assert "position" in node
        assert "data" in node

