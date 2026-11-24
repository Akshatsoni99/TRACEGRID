# TRACEGRID Technical Architecture Specification
**Team CyboShield | Rajasthan Police Hackathon 2026 | PS05**

---

## 1. High-Level Architectural Diagram

```
+---------------------------------------------------------------------------------------+
|                                    PRESENTATION LAYER                                 |
|                                                                                       |
|   Next.js 14 App Router  |  TypeScript  |  Tailwind CSS  |  React Flow Directed Canvas |
|   - Overview Dashboard       - Case Dossiers Registry    - Bank Statement Ingestor    |
|   - Transaction Ledger       - Money-Trail Graph View    - Digital Threat Intel       |
|   - Cross-Case Syndicate     - AI Forensic Assistant     - ReportLab Dossier Viewer   |
+-------------------------------------------+-------------------------------------------+
                                            |
                                            | REST API / JSON Streaming (/api/v1)
                                            v
+-------------------------------------------+-------------------------------------------+
|                                   APPLICATION API LAYER                               |
|                                                                                       |
|   FastAPI Core Framework (Python 3.14 / 3.11+)                                        |
|   - Input Validation & Sanitization (Pydantic V2)                                     |
|   - File Security Guard (Safe Extensions, Size Throttling, Memory Streaming)          |
|   - Asynchronous Execution & CORS Controller                                          |
+-------------------------------------------+-------------------------------------------+
                                            |
        +-----------------------------------+-----------------------------------+
        |                                   |                                   |
        v                                   v                                   v
+-----------------------+   +-------------------------------+   +-----------------------+
|   FORENSIC ANALYTICS  |   |    MONEY-TRAIL GRAPH ENGINE   |   | DIGITAL THREAT INTEL  |
|                       |   |                               |   |                       |
| - Rule Indicator Base |   | - NetworkX DiGraph Model      |   | - Passive DNS Adapter |
| - Velocity Burst Scan |   | - Simple Cycles Detection     |   | - WHOIS Privacy Check |
| - Mule Profiling (IQR)|   | - Degree Centrality Calculus  |   | - IP / ASN Threat Map |
| - Scikit-Learn Model  |   | - 2D Canvas Auto-Positioning  |   | - Synthetic Archive   |
|   (IsolationForest)   |   | - React Flow Node Serializer  |   |   (Safe Attribution)  |
+-----------------------+   +-------------------------------+   +-----------------------+
        |                                   |                                   |
        +-----------------------------------+-----------------------------------+
                                            |
                                            v
+-------------------------------------------+-------------------------------------------+
|                             PERSISTENCE & REPORTING LAYER                             |
|                                                                                       |
|   SQLAlchemy 2.0 ORM                                                                  |
|   - SQLite (Embedded Zero-Config Dev/Demo) / PostgreSQL (Enterprise Production)       |
|   - Relational Tables: Investigations, Accounts, Transactions, Evidence, Intel, Logs  |
|                                                                                       |
|   ReportLab Document Generator                                                        |
|   - Court-Admissible Forensic Dossier Export (PDF)                                    |
|   - Section 65B Indian Evidence Act Compliance & Cryptographic Integrity Checksums    |
+---------------------------------------------------------------------------------------+
```

---

## 2. Forensic Analytics & Anomaly Detection Pipeline

TRACEGRID replaces opaque probabilistic models with an explainable, multi-tiered forensic pipeline:

### 2.1 Tier 1: Deterministic Heuristic Indicators
- **High-Value Spikes**: Identifies transactions exceeding ₹2,00,000 threshold or case-defined parameters.
- **Nocturnal Processing Windows**: Flags transactions initiated between 12:00 AM and 05:00 AM.
- **Round-Sum Structuring (Smurfing)**: Detects zero-fractional round numbers (e.g., ₹50,000, ₹1,00,000) deployed to stay below mandatory reporting limits.
- **Velocity Bursts**: Detects clusters of $\ge 4$ transactions within a rolling 60-minute window for a single originator.

### 2.2 Tier 2: Pass-Through Mule Account Identification
Mule conduits are characterized by rapid turnover with negligible retained balance. TRACEGRID computes the **Pass-Through Ratio**:
$$\text{Throughput Ratio} = \frac{\min(\text{Inflow}, \text{Outflow})}{\max(\text{Inflow}, \text{Outflow})}$$
When $\text{Throughput Ratio} \ge 0.85$ on high volumes within short holding windows, the account is tagged as a `MULE_CONDUIT` and prioritized for Section 91 CrPC debits freezing.

### 2.3 Tier 3: Graph Topology & Circular Cycle Detection
Using NetworkX directed multigraphs, the engine evaluates closed directed cycles:
$$A \longrightarrow B \longrightarrow C \longrightarrow A$$
Circular hops are typically deployed to inflate ledger volume, simulate commercial trading, or confuse linear accounting. Transactions within simple directed cycles ($3 \le \text{length} \le 6$) are flagged with the `CIRCULAR_HOP` indicator.

### 2.4 Tier 4: Unsupervised Statistical Isolation Forest
When $\ge 6$ transactions exist, TRACEGRID fits a Scikit-Learn `IsolationForest` model on feature vectors:
$$\mathbf{x} = [\text{Amount}, \ln(1 + \text{Amount}), \text{Hour}, \text{DayOfWeek}]$$
Decision function values are normalized to a calibrated Anomaly Score between $0.00$ and $1.00$. If score $\ge 0.70$, the transaction is flagged as a high-priority anomaly with clear human-readable divergence explanations.

---

## 3. Statutory Admissibility & Judicial Safeguards
- **Explainability Standard**: No black-box classifications. Every alert pairs the anomaly score with concrete evidentiary triggers.
- **Audit Logging**: Every statement upload, case status update, and analytics execution is recorded in `activity_logs`.
- **Integrity Verification**: File uploads generate SHA256 checksums to maintain chain of custody under Section 65B of the Indian Evidence Act.

