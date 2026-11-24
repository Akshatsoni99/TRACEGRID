# TRACEGRID Hackathon Demonstration Guide
**Team CyboShield | Rajasthan Police Hackathon 2026 | PS05**

Follow this structured 5-minute walkthrough to demonstrate TRACEGRID's complete functional capabilities to the jury.

---

## 1. Startup & Pre-Flight Check (30 Seconds)

1. Open a terminal in `TRACEGRID/`:
   ```powershell
   python backend/main.py
   ```
   *Terminal confirms: `TRACEGRID Backend Engine Initializing... Database seeding completed.`*
2. Open a second terminal in `TRACEGRID/frontend/`:
   ```powershell
   npm run dev
   ```
   *Terminal confirms: `Ready in localhost:3000`*
3. Open Google Chrome at `http://localhost:3000`.

---

## 2. Walkthrough Script (4.5 Minutes)

### Step 1: Executive Overview Dashboard
- Point out the **Statutory Guidance Banner**: Emphasize that TRACEGRID operates strictly on explainable investigative leads, never claiming autonomous criminal guilt.
- Highlight the **Real Forensic KPIs**: ₹42,50,000 processed volume, ₹37,85,000 flagged flow, 4 high-priority mule candidates.
- Review the **Risk Distribution Breakdown**: Show that the dataset separates normal flow, structuring spikes, ML isolation forest outliers, pass-through mule profiles, and circular wash loops.

### Step 2: Investigation Case Dossiers
- Click **Investigations** in the sidebar.
- Open **Case RJ-EOW-2026-0042 (`Operation Maru-Dhar`)**: Explain the premise — high-velocity diversion from victim accounts into mule accounts and crypto liquidation ramps.
- Demonstrate **New Case Creation**: Click `+ New Case`, enter reference `RJ-POL-2026-DEMO`, Title `Operation Sand-Storm`, and submit. Show that it instantly creates a persistent case record in SQLite.

### Step 3: Bank Statement CSV/XLSX Ingestion
- Click **Statement Ingestion** in the sidebar.
- Click **Download Normalized Sample CSV Template**: Show that TRACEGRID provides official downloadable templates.
- Demonstrate upload: Select a statement file or click Parse. Explain how the column mapper recognizes SBI, HDFC, ICICI, and payment gateway headers, eliminates duplicate UTRs, and immediately triggers anomaly scoring.

### Step 4: Transaction Analytics & Explainable Rationale
- Click **Transaction Analysis** in the sidebar.
- Filter by `HIGH_RISK` or `MULE_INDICATOR`.
- **Click on row `TXN-2026-00101`**: Expand the drawer to show the **Explainable Rationale**:
  - *Trigger 1*: High-Value Transaction exceeding ₹2,00,000 reporting threshold.
  - *Trigger 2*: Off-Hours nocturnal execution at 02:15 AM.
  - *ML Anomaly Score*: 0.88 / 1.00 via Scikit-Learn IsolationForest.
- Show `TXN-2026-00111`: Explain how the **Circular Routing Loop** was detected.

### Step 5: Interactive Money-Trail Graph (React Flow)
- Click **Money-Trail Graph** in the sidebar.
- Demonstrate interactive Canvas:
  - **Zoom & Pan**: Smooth navigation across the multi-hop network.
  - **Node Selection**: Click on `ACC-MULE-2001 (Kishore Sharma)`. The right drawer reveals a 98% pass-through drain ratio, degree centrality, and recommended Section 91 CrPC notice to HDFC Bank.
  - **Directed Red Edges**: Highlight animated red edges showing the direction of illicit fund movement.
  - **Threshold Slider**: Drag the `Min Amount` slider to ₹5,00,000 to isolate primary trunk flows from micro-transfers.

### Step 6: Digital Infrastructure Threat Intelligence
- Click **Digital Intelligence** in the sidebar.
- Show correlated threat records: `fast-payout-gateway.cc` (phishing gateway) resolved to bulletproof hosting IP `185.220.101.44` (Tor exit node).
- Demonstrate **Live Passive Lookup**: Enter `paytm-kyc-verify-portal.in` in the search bar and click `Execute Passive Lookup`. The engine instantly resolves registrar, ASN, and risk signals.

### Step 7: Cross-Case Syndicate Correlation
- Click **Cross-Case Correlation** in the sidebar.
- Highlight the **Confirmed Data Match**: Show that student mule account `ACC-SHARED-9921 (Aman Verma)` appears in both **Case 0042** and **Case 0215**.
- Explain how this unmasks organized multi-jurisdictional syndicate operations that individual police stations investigating in isolation would miss.

### Step 8: TRACEGRID AI Forensic Assistant
- Click **AI Forensic Assistant** in the sidebar.
- Click the prompt chip: *"Summarise this investigation."*
- Show the detailed response grounded in actual case evidence: breakdown of victim debits, pass-through conduit accounts, crypto liquidation sinks, and suggested Section 91 CrPC summons.

### Step 9: Court-Ready PDF Dossier Export
- Click **Court Reports (PDF)** in the sidebar.
- Click **Download Certified PDF Report**: Show the downloaded multi-page PDF generated via ReportLab containing TRACEGRID branding, quantitative metrics, flagged transaction tables, and Section 65B Indian Evidence Act statutory disclaimers.

---

## 3. Summary of Offline Deliverables
If demonstrating without internet connectivity or standalone:
- Double-click `docs/TRACEGRID_HTML_Prototype/index.html` to run the zero-dependency interactive prototype in any browser.
- Open `docs/TRACEGRID_Action_Plan.pptx` for the 14-slide jury presentation.
- Open `docs/TRACEGRID_Action_Plan.pdf` for the printable action plan dossier.
- Open `docs/TRACEGRID_Wireframe.pdf` for the architectural UI wireframe schematics.

