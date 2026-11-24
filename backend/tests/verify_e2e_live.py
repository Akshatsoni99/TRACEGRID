import urllib.request
import urllib.parse
import json
import os
import sys

BASE_URL = "http://127.0.0.1:8000/api/v1"
PROXY_URL = "http://127.0.0.1:3000/api/v1"

def test_endpoint(name: str, url: str, method: str = "GET", data: dict = None):
    print(f"Testing {name} at {url}...")
    headers = {"Content-Type": "application/json"} if data else {}
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8") if data else None,
        headers=headers,
        method=method
    )
    try:
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            content_type = resp.headers.get("Content-Type", "")
            raw = resp.read()
            if "application/json" in content_type:
                res_data = json.loads(raw.decode("utf-8"))
                print(f"  [PASS] Status: {status}, Keys: {list(res_data.keys()) if isinstance(res_data, dict) else len(res_data)}")
                return res_data
            elif "application/pdf" in content_type:
                print(f"  [PASS] Status: {status}, PDF Size: {len(raw)} bytes")
                return raw
            elif "text/csv" in content_type:
                print(f"  [PASS] Status: {status}, CSV Size: {len(raw)} bytes")
                return raw
            else:
                print(f"  [PASS] Status: {status}, Body length: {len(raw)}")
                return raw
    except Exception as e:
        print(f"  [FAIL] {e}")
        raise e

def run_all_checks():
    print("==================================================")
    print(" TRACEGRID E2E End-to-End Live Verification Suite ")
    print("==================================================")

    # 1. Health check via backend
    test_endpoint("Backend Health", f"{BASE_URL}/health")

    # 2. Health check via Next.js Proxy
    test_endpoint("Frontend Proxy Health", f"{PROXY_URL}/health")

    # 3. Dashboard overview
    test_endpoint("Dashboard Overview", f"{PROXY_URL}/dashboard/overview")

    # 4. List investigations
    cases = test_endpoint("List Cases", f"{PROXY_URL}/cases")
    assert len(cases) >= 3, "Expected at least 3 seeded cases"

    # 5. Case details
    test_endpoint("Case Details (case-001)", f"{PROXY_URL}/cases/case-001")

    # 6. Sample CSV template
    test_endpoint("Download Sample CSV Template", f"{PROXY_URL}/sample/template.csv")

    # 7. Upload CSV statement
    print("Testing Bank Statement CSV Upload & Ingestion...")
    sample_csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "sample_data", "sample_statement_layering_scam.csv")
    with open(sample_csv_path, "rb") as f:
        file_bytes = f.read()

    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="sample_statement_layering_scam.csv"\r\n'
        f"Content-Type: text/csv\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    upload_req = urllib.request.Request(
        f"{PROXY_URL}/upload/statement/case-001",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST"
    )
    with urllib.request.urlopen(upload_req) as resp:
        upload_res = json.loads(resp.read().decode("utf-8"))
        print(f"  [PASS] Upload Status: {resp.status}, Ingested: {upload_res.get('imported_count')}, Flags: {upload_res.get('flagged_count')}")

    # 8. Filtered transactions
    test_endpoint("Filtered Transactions (case-001)", f"{PROXY_URL}/transactions?case_id=case-001")

    # 9. Accounts listing
    test_endpoint("Accounts (case-001)", f"{PROXY_URL}/accounts?case_id=case-001")

    # 10. Interactive network graph
    graph = test_endpoint("Network Graph (case-001)", f"{PROXY_URL}/graph/case-001")
    assert "nodes" in graph and "edges" in graph, "Graph format mismatch"

    # 11. Digital Intelligence
    intel = test_endpoint("Digital Intelligence (case-001)", f"{PROXY_URL}/intelligence/case-001")

    # 12. Digital Intel passive lookup
    lookup_body = urllib.parse.urlencode({"indicator": "fast-payout-gateway.cc", "indicator_type": "DOMAIN"}).encode("utf-8")
    lookup_req = urllib.request.Request(
        f"{PROXY_URL}/intelligence/lookup",
        data=lookup_body,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST"
    )
    with urllib.request.urlopen(lookup_req) as resp:
        lookup_res = json.loads(resp.read().decode("utf-8"))
        print(f"  [PASS] Intel Lookup: {lookup_res.get('indicator')} -> {lookup_res.get('risk_rating')}")

    # 13. Cross-Case correlation
    cross = test_endpoint("Cross-Case Correlation (case-003)", f"{PROXY_URL}/cross-case/correlations?target_case_id=case-003")
    assert cross.get("total_correlations", 0) >= 1, "Cross-case correlation expected syndicate match"
    print(f"  Cross-case syndicate matches found: {cross.get('total_correlations')}")

    # 14. AI Assistant Chat
    ai_resp = test_endpoint(
        "AI Assistant Chat Query",
        f"{PROXY_URL}/assistant/chat",
        method="POST",
        data={"case_id": "case-001", "message": "Summarise this investigation and explain the flagged transactions."}
    )
    assert "reply" in ai_resp, "AI reply missing"
    print(f"  AI Reply Snippet: {ai_resp['reply'][:120]}...")

    # 15. PDF Report Generation & Download
    pdf_bytes = test_endpoint("Court PDF Report Generation", f"{PROXY_URL}/reports/pdf/case-001")
    assert len(pdf_bytes) > 2000, "PDF bytes insufficient"

    print("==================================================")
    print(" ALL 15 E2E INTEGRATION CHECKS PASSED (100% OK)   ")
    print("==================================================")

if __name__ == "__main__":
    run_all_checks()
