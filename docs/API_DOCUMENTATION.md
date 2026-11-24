# TRACEGRID REST API Specification
**Team CyboShield | Rajasthan Police Hackathon 2026 | PS05**

Base URL: `http://127.0.0.1:8000/api/v1`

---

## 1. System & Health Endpoints

### `GET /health`
Verifies backend connectivity, active database status, and hackathon team metadata.
- **Response `200 OK`**:
```json
{
  "status": "healthy",
  "service": "TRACEGRID Core API",
  "team": "CyboShield",
  "hackathon": "Rajasthan Police Hackathon 2026 - PS05",
  "timestamp": "2026-02-15T12:00:00Z"
}
```

### `GET /dashboard/overview`
Retrieves aggregated executive metrics, risk distribution breakdowns, daily volume timelines, and active priority cases.

---

## 2. Investigation Case Management

### `GET /cases`
Lists all active investigation dossiers sorted by creation date descending.

### `POST /cases`
Creates a new persistent investigation dossier in the database.
- **Request Body**:
```json
{
  "case_number": "RJ-POL-EOW-2026-0099",
  "title": "Operation Thar-Shield: Hawala Diversion",
  "description": "Multi-tier layering through digital payment conduits.",
  "priority": "CRITICAL",
  "lead_investigator": "Insp. Vikram Rathore"
}
```

### `GET /cases/{case_id}`
Retrieves complete case profile, summary statistics, and immutable activity logs.

---

## 3. Bank Statement Ingestion

### `GET /sample/template.csv`
Downloads the official normalized bank statement CSV template.

### `POST /upload/statement/{case_id}`
Uploads and parses a CSV or XLSX statement file. Validates headers, filters duplicates, stores SHA256 evidence checksum, and automatically triggers anomaly detection.

---

## 4. Transaction Analytics & Graph

### `GET /transactions`
Queries transaction records with optional filters:
- `case_id`: Filter by case
- `risk_flag`: `ALL`, `NORMAL`, `SUSPICIOUS`, `HIGH_RISK`, `MULE_INDICATOR`, `CIRCULAR_HOP`
- `min_amount`, `max_amount`: Value range
- `account`: Account number substring match

### `POST /analysis/run/{case_id}`
Explicitly re-runs the hybrid analytics engine (IsolationForest + Rule triggers + Graph cycles) across all transactions of a case.

### `GET /graph/{case_id}?min_amount=0`
Generates directed graph topology serialized specifically for React Flow:
- `nodes`: Account nodes with degrees, flow sums, and risk badges.
- `edges`: Transaction directed edges with aggregated flow sums and anomaly markers.
- `summary`: High-level graph topology metrics.

---

## 5. Intelligence & Cross-Case Correlator

### `GET /intelligence/{case_id}`
Retrieves passive threat infrastructure linked to the case.

### `POST /intelligence/lookup`
Executes live passive lookup on any domain name or IP address.

### `GET /cross-case/correlations?target_case_id={case_id}`
Identifies shared accounts and infrastructure indicators across separate cases.

---

## 6. AI Assistant & Forensic Reporting

### `POST /assistant/chat`
Context-grounded query endpoint answering specific investigative questions using actual case database holdings.
- **Request Body**:
```json
{
  "case_id": "case-001",
  "message": "Summarise this investigation and explain the flagged transactions."
}
```

### `GET /reports/pdf/{case_id}`
Generates and streams a court-admissible certified forensic PDF dossier created dynamically with ReportLab.

