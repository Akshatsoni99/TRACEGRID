# TRACEGRID Data Dictionary & Schema Specification
**Team CyboShield | Rajasthan Police Hackathon 2026 | PS05**

---

## 1. Relational Database Tables

### 1.1 `investigations` (Case Dossiers)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | VARCHAR | PRIMARY KEY | Unique case identifier (e.g. `case-001` or UUID). |
| `case_number` | VARCHAR | UNIQUE, NOT NULL, INDEX | Official police reference or FIR number (e.g. `RJ-EOW-2026-0042`). |
| `title` | VARCHAR | NOT NULL | Descriptive title of the investigation. |
| `description` | TEXT | NULLABLE | Case brief, reported victim modus operandi, and scope. |
| `priority` | VARCHAR | DEFAULT 'HIGH' | Priority rating: `CRITICAL`, `HIGH`, `MEDIUM`, `LOW`. |
| `status` | VARCHAR | DEFAULT 'ACTIVE' | Case workflow status: `ACTIVE`, `IN_REVIEW`, `ESCALATED`, `CLOSED`. |
| `lead_investigator`| VARCHAR | NOT NULL | Sworn investigating officer name and unit. |
| `created_at` | DATETIME| DEFAULT UTC_NOW | Date and timestamp when the case was initiated. |
| `updated_at` | DATETIME| DEFAULT UTC_NOW | Timestamp of latest case ledger modification. |

### 1.2 `accounts` (Bank Accounts & Wallets)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | VARCHAR | PRIMARY KEY | Composite key: `{case_id}_{account_number}`. |
| `account_number` | VARCHAR | NOT NULL, INDEX | Core banking account number or virtual payment address. |
| `case_id` | VARCHAR | FOREIGN KEY (`investigations.id`)| Associated case reference. |
| `account_holder` | VARCHAR | NOT NULL | Holder name or synthetic persona identifier. |
| `bank_name` | VARCHAR | NOT NULL | Financial institution or payment switch branch. |
| `account_type` | VARCHAR | DEFAULT 'SAVINGS' | Account type: `SAVINGS`, `CURRENT`, `NODAL`, `CRYPTO_RAMP`. |
| `risk_level` | VARCHAR | DEFAULT 'LOW' | Categorization: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`. |
| `risk_score` | FLOAT | DEFAULT 0.0 | Normalized risk metric from 0.0 to 100.0. |
| `risk_tags` | TEXT | DEFAULT '[]' | JSON list of detected leads (e.g. `["MULE_CONDUIT", "PASS_THROUGH"]`). |
| `total_inflow` | FLOAT | DEFAULT 0.0 | Cumulative credited funds in INR. |
| `total_outflow` | FLOAT | DEFAULT 0.0 | Cumulative debited funds in INR. |
| `transaction_count`| INTEGER| DEFAULT 0 | Total ledger records involving this account. |
| `is_synthetic` | BOOLEAN | DEFAULT TRUE | Synthetic data marker. |

### 1.3 `transactions` (Ledger Entries)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | VARCHAR | PRIMARY KEY | Transaction reference ID or UTR number. |
| `case_id` | VARCHAR | FOREIGN KEY (`investigations.id`)| Associated case reference. |
| `timestamp` | DATETIME| NOT NULL | Execution date and time. |
| `sender_account` | VARCHAR | NOT NULL, INDEX | Debited source account number. |
| `sender_name` | VARCHAR | DEFAULT 'Unknown' | Name of sending entity or remitter. |
| `receiver_account`| VARCHAR | NOT NULL, INDEX | Credited beneficiary account number. |
| `receiver_name` | VARCHAR | DEFAULT 'Unknown' | Beneficiary name. |
| `amount` | FLOAT | NOT NULL | Transfer value in Indian Rupees (INR). |
| `transaction_type`| VARCHAR | DEFAULT 'IMPS' | Transfer rail: `IMPS`, `NEFT`, `RTGS`, `UPI`, `WIRE`. |
| `description` | VARCHAR | DEFAULT '' | Bank narration or remarks string. |
| `reference_number`| VARCHAR | DEFAULT '' | Official banking UTR / reference string. |
| `risk_flag` | VARCHAR | DEFAULT 'NORMAL' | Enum: `NORMAL`, `SUSPICIOUS`, `HIGH_RISK`, `MULE_INDICATOR`, `CIRCULAR_HOP`. |
| `anomaly_score` | FLOAT | DEFAULT 0.0 | Scaled anomaly score (0.00 to 1.00). |
| `flag_reasons` | TEXT | DEFAULT '[]' | JSON list of human-readable rationale strings. |
| `detection_method`| VARCHAR | DEFAULT 'RULE_BASED' | Method: `RULE_BASED`, `ISOLATION_FOREST`, `HYBRID_ENSEMBLE`, `GRAPH_CYCLE`. |

### 1.4 `digital_intelligence` (Infrastructure Observations)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | VARCHAR | PRIMARY KEY | Unique intelligence observation UUID. |
| `case_id` | VARCHAR | FOREIGN KEY (`investigations.id`)| Associated case reference. |
| `indicator_type` | VARCHAR | NOT NULL | Type: `DOMAIN`, `IP_ADDRESS`, `DNS`, `HOSTING_PROVIDER`, `ASN`. |
| `indicator_value`| VARCHAR | NOT NULL, INDEX | Observed value (e.g. `fast-payout-gateway.cc` or `185.220.101.44`). |
| `associated_account`| VARCHAR | NULLABLE | Linked target account number from bank statements. |
| `lookup_source` | VARCHAR | NOT NULL | Origin: `Passive DNS Archive (DEMO)`, `CERT-In FinThreat Feed`. |
| `metadata_json` | TEXT | DEFAULT '{}' | JSON dictionary containing ASN, Registrar, Age, PTR records. |
| `risk_rating` | VARCHAR | DEFAULT 'SUSPICIOUS' | Rating: `CLEAN`, `SUSPICIOUS`, `MALICIOUS`. |
| `verification_status`| VARCHAR| DEFAULT 'DEMO' | Verification: `VERIFIED_RECORD`, `CORROBORATED_SIMULATION`, `DEMO_SIMULATION`. |

### 1.5 `evidence` (Chain of Custody Files)
| Column | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `id` | VARCHAR | PRIMARY KEY | Evidence item UUID. |
| `case_id` | VARCHAR | FOREIGN KEY (`investigations.id`)| Associated case reference. |
| `title` | VARCHAR | NOT NULL | Descriptive title of ingested artifact. |
| `evidence_type` | VARCHAR | DEFAULT 'BANK_STATEMENT'| Category: `BANK_STATEMENT`, `IP_LOG`, `CDR`, `FORENSIC_DUMP`. |
| `file_name` | VARCHAR | NOT NULL | Ingested filename. |
| `file_hash` | VARCHAR | NOT NULL | SHA256 cryptographic checksum for legal admissibility. |
| `source` | VARCHAR | NOT NULL | Ingestion origin or subpoena response reference. |
| `verification_status`| VARCHAR| DEFAULT 'VERIFIED' | Status: `VERIFIED`, `UNVERIFIED`, `CORROBORATED`. |

