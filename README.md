# TRACEGRID
**Connecting Financial Evidence. Revealing Hidden Relationships.**

Developed by **Team CyboShield** for the **Rajasthan Police Hackathon 2026**  
**Problem Statement PS05 — Financial Crime Analytics**

---

## 1. Executive Overview

**TRACEGRID** is a unified financial crime analytics and forensic investigation platform designed specifically for authorized law enforcement officers, Economic Offences Wings (EOW), and State Cyber Police Stations.

Traditional financial investigations are hindered by disparate bank statement formats, delayed intelligence sharing, and the sheer velocity of modern mule account syndicates. TRACEGRID bridges these gaps by providing:

1. **Automated Statement Ingestion**: Ingests, normalizes, and validates heterogeneous bank statements (CSV/XLSX) from SBI, HDFC, ICICI, PNB, and payment gateways.
2. **Hybrid Anomaly Detection**: Combines deterministic forensic rules (velocity bursts, nocturnal transfers, round-sum structuring) with Scikit-learn's `IsolationForest` unsupervised outlier scoring.
3. **Mule Conduit Profiling**: Automatically flags pass-through accounts where high-volume funds enter and are immediately drained with zero legitimate retention.
4. **Interactive Money-Trail Graph**: NetworkX-driven topological analysis rendered via high-performance React Flow to visually expose multi-hop layering and closed circular wash cycles.
5. **Passive Digital Infrastructure Correlation**: Correlates bank accounts with suspicious phishing domains, bulletproof hosting ASNs, and VPN/TOR proxy nodes without active probing.
6. **Cross-Case Syndicate Unmasking**: Discovers shared accounts, infrastructure, and entities across distinct FIR dossiers.
7. **AI Forensic Assistant**: Context-grounded investigation assistant that explains anomalous patterns and proposes Section 91 CrPC statutory summons.
8. **Court-Ready Certified PDF Dossiers**: Generates court-admissible forensic reports using ReportLab with SHA256 checksums and Section 65B Indian Evidence Act disclaimers.

> **Statutory Integrity Standard**: TRACEGRID operates strictly on explainable investigative leads. All anomaly scores and flags represent indicators to guide human inquiry, never autonomous declarations of guilt.

---

## 2. System Architecture

TRACEGRID is built on a high-density, air-gappable architecture:

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS, React Flow (`reactflow`), Lucide Icons.
- **Backend API**: Python 3.14 / 3.11+, FastAPI, Pydantic V2, Uvicorn.
- **Analytics & ML**: Scikit-Learn (`IsolationForest`), Pandas, NumPy, NetworkX (`DiGraph`).
- **Database**: Relational SQLite development database (configured for seamless PostgreSQL production deployment via SQLAlchemy ORM).
- **Reporting Engine**: ReportLab (Python) producing vector-quality PDF dossiers with custom enterprise styling.
- **Deliverables**: PowerPoint presentation (`python-pptx`), wireframe schematics, and standalone offline HTML prototype.

---

## 3. Quickstart & Installation Guide

### Prerequisites
- Python 3.10+ (Tested on Python 3.14)
- Node.js 18+ & npm 9+

### A. Backend Setup & Startup
```powershell
# Navigate to project root
cd "c:\Users\Akshat Soni\Desktop\TRACEGRID"

# Install Python requirements
python -m pip install -r backend/requirements.txt

# Run automated tests to verify analytics and APIs
python -m pytest backend/tests/

# Launch the FastAPI backend server (Runs on port 8000)
python backend/main.py
```
*API Swagger Documentation is available live at: `http://127.0.0.1:8000/docs`*

### B. Frontend Setup & Startup
```powershell
# In a new terminal, navigate to frontend/
cd "c:\Users\Akshat Soni\Desktop\TRACEGRID\frontend"

# Launch Next.js development server (Runs on port 3000)
npm run dev
```
*Access the TRACEGRID Workspace in your browser at: `http://localhost:3000`*

---

## 4. Demonstration Scenarios (Pre-Loaded in Database)

TRACEGRID comes pre-populated with realistic synthetic criminal investigation scenarios:

1. **Case RJ-EOW-2026-0042 (`Operation Maru-Dhar`)**:
   - High-velocity fund diversion of ₹42,50,000 from victim accounts (`ACC-VIC-1001`, `ACC-VIC-1002`) into 2 primary pass-through mule conduits.
   - Immediate 45-minute splitting into shell accounts and a cross-case student mule node (`ACC-SHARED-9921`).
   - Closed circular hop returning collateral funds to layer accounts.
   - Terminal liquidation into offshore crypto-ramp nodal wallet (`ACC-EXIT-4001`).
   - Digital correlation with bulletproof hosting domain `fast-payout-gateway.cc` and Tor proxy IP `185.220.101.44`.

2. **Case RJ-CYBER-2026-0109 (`Operation Golden Sand`)**:
   - Predatory micro-lending app extortion loop (`quick-loan-bharat-api.net`).
   - Closed 3-hop wash layering cycle: `ACC-APP-5001 -> ACC-CIRC-5002 -> ACC-CIRC-5003 -> ACC-APP-5001`.

3. **Case RJ-EOW-2026-0215 (`Operation PhishGrid`)**:
   - Phishing KYC SMS credential theft ring targeting teacher retail savings.
   - Cross-case syndication: Intersects with Case 0042 through shared student mule `ACC-SHARED-9921` and proxy hosting IP `185.220.101.44`.

---

## 5. Hackathon Deliverables Summary

All required documentation and project deliverables are organized inside `docs/`:

| Deliverable | Location | Description |
| :--- | :--- | :--- |
| **Action Plan Presentation (PPTX)** | [`docs/TRACEGRID_Action_Plan.pptx`](file:///c:/Users/Akshat%20Soni/Desktop/TRACEGRID/docs/TRACEGRID_Action_Plan.pptx) | 14-slide widescreen presentation detailing architecture, problem statement, ML approach, and rollout. |
| **Action Plan Document (PDF)** | [`docs/TRACEGRID_Action_Plan.pdf`](file:///c:/Users/Akshat%20Soni/Desktop/TRACEGRID/docs/TRACEGRID_Action_Plan.pdf) | Landscape PDF export of the action plan. |
| **UI Wireframes (PDF)** | [`docs/TRACEGRID_Wireframe.pdf`](file:///c:/Users/Akshat%20Soni/Desktop/TRACEGRID/docs/TRACEGRID_Wireframe.pdf) | Multi-page low-fidelity schematic wireframes covering all 8 core views. |
| **Standalone HTML Prototype** | [`docs/TRACEGRID_HTML_Prototype/index.html`](file:///c:/Users/Akshat%20Soni/Desktop/TRACEGRID/docs/TRACEGRID_HTML_Prototype/index.html) | Single-file zero-dependency prototype demonstrating complete workflow offline. |
| **Architecture Specification** | [`docs/ARCHITECTURE.md`](file:///c:/Users/Akshat%20Soni/Desktop/TRACEGRID/docs/ARCHITECTURE.md) | Technical deep-dive into backend pipelines, data flow, and ML scoring. |
| **Data Dictionary** | [`docs/DATA_DICTIONARY.md`](file:///c:/Users/Akshat%20Soni/Desktop/TRACEGRID/docs/DATA_DICTIONARY.md) | Relational schema definitions, enum states, and forensic metadata fields. |
| **API Documentation** | [`docs/API_DOCUMENTATION.md`](file:///c:/Users/Akshat%20Soni/Desktop/TRACEGRID/docs/API_DOCUMENTATION.md) | Comprehensive REST endpoint catalog with request/response schemas. |
| **Demonstration Guide** | [`docs/DEMO_GUIDE.md`](file:///c:/Users/Akshat%20Soni/Desktop/TRACEGRID/docs/DEMO_GUIDE.md) | Step-by-step 5-minute walkthrough script for hackathon jury evaluation. |

---

## 6. Team & Hackathon Details

- **Team Name**: CyboShield
- **Event**: Rajasthan Police Hackathon 2026
- **Problem Statement**: PS05 — Financial Crime Analytics
- **Lead Contact**: Cyber Crime Analytics & Full-Stack Engineering Unit
- **Status**: Complete, Functional, Fully Tested Prototype

