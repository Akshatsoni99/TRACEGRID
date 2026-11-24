import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.core.database import SessionLocal
from backend.models.models import Investigation

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["team"] == "CyboShield"

def test_cases_listing():
    response = client.get("/api/v1/cases")
    assert response.status_code == 200
    cases = response.json()
    assert len(cases) >= 3
    assert any(c["case_number"] == "RJ-EOW-2026-0042" for c in cases)

def test_dashboard_overview():
    response = client.get("/api/v1/dashboard/overview")
    assert response.status_code == 200
    stats = response.json()
    assert stats["total_investigations"] >= 3
    assert stats["total_transactions_analyzed"] > 0
    assert stats["total_suspicious_flagged"] > 0
    assert "risk_distribution" in stats

def test_graph_endpoint():
    response = client.get("/api/v1/graph/case-001")
    assert response.status_code == 200
    graph = response.json()
    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) > 0

def test_ai_assistant():
    payload = {
        "case_id": "case-001",
        "message": "Summarise this investigation and show flagged transactions"
    }
    response = client.post("/api/v1/assistant/chat", json=payload)
    assert response.status_code == 200
    chat_resp = response.json()
    assert "reply" in chat_resp
    assert len(chat_resp["reply"]) > 50
    assert len(chat_resp["suggested_actions"]) > 0

def test_pdf_report_generation():
    response = client.get("/api/v1/reports/pdf/case-001")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert len(response.content) > 1000 # Valid non-empty PDF binary

