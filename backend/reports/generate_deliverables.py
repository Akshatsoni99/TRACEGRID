import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)

def create_action_plan_pptx(output_path: str):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    c_navy = RGBColor(20, 34, 53)
    c_card = RGBColor(255, 255, 255)
    c_primary = RGBColor(36, 91, 136)
    c_text = RGBColor(23, 35, 51)
    c_secondary = RGBColor(104, 117, 134)
    c_amber = RGBColor(214, 154, 54)
    c_bg = RGBColor(244, 246, 248)

    def add_slide_header(slide, title_text, category_text="RAJASTHAN POLICE HACKATHON 2026 // PS05 // TEAM CYBOSHIELD"):
        top_bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(1.1))
        top_bar.fill.solid()
        top_bar.fill.fore_color.rgb = c_navy
        top_bar.line.fill.background()

        tb_cat = slide.shapes.add_textbox(Inches(0.8), Inches(0.15), Inches(11.5), Inches(0.3))
        tf_cat = tb_cat.text_frame
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = c_amber

        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.5), Inches(0.6))
        tf_title = tb_title.text_frame
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(20)
        p_title.font.bold = True
        p_title.font.color.rgb = RGBColor(255, 255, 255)

    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(1.1), Inches(13.333), Inches(6.4))
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_bg
        bg.line.fill.background()

    slides_data = [
        {
            "is_cover": True,
            "title": "TRACEGRID",
            "subtitle": "Connecting Financial Evidence. Revealing Hidden Relationships.",
            "team": "Team CyboShield | Rajasthan Police Hackathon 2026",
            "problem": "Problem Statement PS05 — Financial Crime Analytics",
            "lead": "Unified Forensic Investigation Workspace & Graph Intelligence Platform"
        },
        {
            "title": "01. Problem Statement & National Challenge",
            "bullets": [
                ("Proliferation of Mule Account Syndicates", "Organized cybercrime groups deploy layered networks of student, dormant, and fabricated KYC bank accounts to rapidly dissipate illicit funds."),
                ("Sub-Threshold Structuring (Smurfing)", "Fraudsters split proceeds into structured transfers under reporting limits (e.g. ₹40,000 to ₹1,95,000) to defeat static rule triggers."),
                ("Dispersed Multi-Domain Evidence", "Financial ledgers, SMS phish kits, hosting IPDRs, and crypto liquidation ramps remain siloed in separate spreadsheets."),
                ("Time-Critical Freezing Window", "Investigating officers have less than 4 hours to intercept stolen capital before it exits into offshore digital exchanges.")
            ]
        },
        {
            "title": "02. Existing Operational Challenges in Police Investigation",
            "bullets": [
                ("Manual Spreadsheet Stitching", "Officers waste days manually cross-referencing CSV statements from multiple commercial banks with inconsistent formats."),
                ("Blind Spots in Closed Cycles", "Linear examination fails to detect circular routing loops (A → B → C → A) designed to confuse ledger tracing."),
                ("Lack of Explainable Rationale", "Black-box AI models that output probabilistic guilt fail judicial scrutiny under Section 65B of the Indian Evidence Act."),
                ("Disjointed Cyber & Financial Clues", "No automated linkage between bank transaction timestamps and passive threat intelligence (malicious DNS, bulletproof hosting ASNs).")
            ]
        },
        {
            "title": "03. Proposed Solution: TRACEGRID by Team CyboShield",
            "bullets": [
                ("Unified Forensic Workspace", "A purpose-built enterprise investigation platform integrating bank statement parsing, anomaly detection, and graph visualization."),
                ("Hybrid Forensic Engine", "Combines deterministic rule breaches (velocity, nocturnal bursts, structuring) with Scikit-Learn IsolationForest anomaly detection."),
                ("NetworkX & React Flow Graph", "Interactive money-trail graph mapping accounts as nodes and transactions as directed weighted edges."),
                ("Court-Ready Certified Dossiers", "One-click generation of structured PDF investigation reports ready for Section 91 CrPC magistrate requisitions.")
            ]
        },
        {
            "title": "04. TRACEGRID Core Functional Capabilities",
            "bullets": [
                ("Multi-Bank Statement Parser", "Validates CSV and XLSX files, normalizes disparate bank headers, detects duplicate transactions and corrupt rows."),
                ("Pass-Through Mule Profiler", "Calculates throughput velocity to flag accounts where high-volume inflow is immediately drained with minimal retention."),
                ("Passive Digital Threat Correlator", "Maps bank accounts to suspicious domains, bulletproof hosting ASNs, and VPN proxy exit nodes without intrusive probing."),
                ("Cross-Case Syndicate Matching", "Automatically detects shared accounts, phone numbers, and domains across distinct active police cases.")
            ]
        },
        {
            "title": "05. End-to-End Investigation Workflow",
            "bullets": [
                ("Step 1: Case Registration", "Create a case dossier with FIR number, assigned investigating officer, and priority level."),
                ("Step 2: Bank Statement Ingestion", "Upload raw victim and suspected mule statements; auto-map headers and clean duplicates."),
                ("Step 3: Multi-Layer Analytics", "Run isolation forest and heuristics to detect bursts, off-hours execution, and circular loops."),
                ("Step 4: Interactive Graph Exploration", "Inspect account centrality, trace funds through intermediate conduits, and identify liquidation sinks."),
                ("Step 5: AI Forensic Assistant & Export", "Query evidentiary gaps using TRACEGRID AI Assistant and export certified PDF dossiers.")
            ]
        },
        {
            "title": "06. Technical Architecture & System Stack",
            "bullets": [
                ("Frontend Layer (Next.js 14 + React Flow)", "High-performance enterprise UI with TypeScript, Tailwind CSS, and custom interactive React Flow node renderers."),
                ("Backend Core (Python + FastAPI)", "Modular asynchronous REST API with Pydantic validation, structured services, and comprehensive test suite."),
                ("Analytics Engine", "Pandas & NumPy for vector calculations, Scikit-learn for Isolation Forest, and NetworkX for cycle detection."),
                ("Database & Reporting", "SQLAlchemy ORM with SQLite fallback (PostgreSQL ready) and ReportLab for court-admissible PDF generation.")
            ]
        },
        {
            "title": "07. AI/ML Approach: Explainable & Evidentiary Grounded",
            "bullets": [
                ("Isolation Forest Anomaly Detection", "Unsupervised tree ensemble detecting high-dimensional outliers across amount, time, velocity, and counterparty frequency."),
                ("Explainable Risk Leads (No Black Box)", "Outputs normalized anomaly scores (0.0 - 1.0) paired with human-readable evidentiary rationale."),
                ("Statutory Compliance Standard", "Risk tags are classified as 'Investigative Leads Requiring Human Verification' rather than autonomous proof of guilt."),
                ("Local Deterministic Fallback", "AI Assistant operates on grounded case records even when external LLM APIs are unreachable.")
            ]
        },
        {
            "title": "08. Digital Infrastructure & Threat Correlation",
            "bullets": [
                ("Passive DNS & WHOIS Inspection", "Extracts domain age, privacy shield status, and nameserver configurations linked to phishing scams."),
                ("IPDR & ASN Risk Profiling", "Flags transactions originating from bulletproof offshore data havens and TOR exit nodes."),
                ("Adapter-Based Architecture", "Clean interface allowing seamless integration with CERT-In, RBI Sachet, and Crime Multi-Agency Centre (Cri-MAC)."),
                ("Attribution Integrity", "Explicitly records data source, retrieval timestamp, and verification status for every digital indicator.")
            ]
        },
        {
            "title": "09. Money-Trail Graph Analytics (NetworkX + React Flow)",
            "bullets": [
                ("Directed Weighted Multigraph", "Accounts rendered as nodes with degree centrality; transaction streams rendered as directed edges."),
                ("Circular Hop Detection", "NetworkX simple_cycles algorithm detects closed wash-trading loops (length 3 to 6) in milliseconds."),
                ("Centrality & Flow Metrics", "Calculates in-degree, out-degree, and pass-through ratios to isolate nodal syndicates from retail victims."),
                ("Live Interactive Canvas", "Real-time pan/zoom, account search, minimum flow threshold sliders, and side drawer inspectors.")
            ]
        },
        {
            "title": "10. Enterprise UI Design System & Usability",
            "bullets": [
                ("Restrained Law Enforcement Aesthetics", "Deep navy sidebar (#142235), off-white canvas (#F4F6F8), and high-contrast typography designed for 10-hour shifts."),
                ("Zero Generic AI Fluff", "No distracting neon gradients, floating icons, or meaningless decorative cards."),
                ("High Data Density Tables", "Compact tabular views displaying UTR numbers, counterparty banks, and anomaly triggers in one view."),
                ("Context-Aware Workspaces", "Active case reference, lead investigator name, and statutory disclaimers pinned persistently across all screens.")
            ]
        },
        {
            "title": "11. Innovation & Unique Selling Propositions (USP)",
            "bullets": [
                ("Hybrid Rules + Graph + ML Ensemble", "Combines three distinct forensic paradigms to detect what individual techniques miss."),
                ("Cross-Case Syndicate Unmasking", "Automatically correlates accounts and hosting infrastructure across disparate police jurisdictions."),
                ("Section 91 CrPC Actionable Outputs", "Recommends exact statutory summons and account freeze notices based on detected conduit roles."),
                ("Full Offline / Air-Gapped Capable", "Runs entirely on localized runtimes without mandatory external cloud or LLM dependencies.")
            ]
        },
        {
            "title": "12. Implementation Roadmap & Police Rollout Plan",
            "bullets": [
                ("Phase 1: Hackathon Prototype (Completed)", "Core Next.js + FastAPI platform, statement parser, ML anomaly detector, NetworkX graph, and PDF report generator."),
                ("Phase 2: Pilot Deployment (Months 1-3)", "Trial testing across Jaipur & Jodhpur Cyber Police Stations with live sanitized banking feeds."),
                ("Phase 3: National Gateway Integration (Months 4-6)", "Direct API connectors for FIU-IND FINNET 2.0, I4C (Indian Cyber Crime Coordination Centre), and CCTNS."),
                ("Phase 4: State-Wide Rollout (Months 7-12)", "Deployment across all Rajasthan District Cyber Police Stations with role-based access control.")
            ]
        },
        {
            "title": "13. Expected Impact & Conclusion",
            "bullets": [
                ("80% Reduction in Triage Time", "Reduces preliminary statement collation from 48 hours to under 3 minutes."),
                ("Rapid Account Freezing", "Instant identification of exit sinks enables proactive requisition letters before funds leave India."),
                ("Trial-Ready Evidentiary Admissibility", "Certified dossiers streamline prosecution and improve conviction rates in cyber fraud trials."),
                ("Team CyboShield Commitment", "TRACEGRID delivers an operational, explainable, and scalable solution for Rajasthan Police Hackathon 2026.")
            ]
        }
    ]

    for slide_info in slides_data:
        slide = prs.slides.add_slide(blank_layout)

        if slide_info.get("is_cover"):
            bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
            bg.fill.solid()
            bg.fill.fore_color.rgb = c_navy
            bg.line.fill.background()

            tb = slide.shapes.add_textbox(Inches(1.2), Inches(1.5), Inches(11.0), Inches(4.5))
            tf = tb.text_frame
            tf.word_wrap = True

            p0 = tf.paragraphs[0]
            p0.text = "RAJASTHAN POLICE HACKATHON 2026 // PS05"
            p0.font.size = Pt(14)
            p0.font.bold = True
            p0.font.color.rgb = c_amber

            p1 = tf.add_paragraph()
            p1.text = "TRACEGRID"
            p1.font.size = Pt(54)
            p1.font.bold = True
            p1.font.color.rgb = RGBColor(255, 255, 255)
            p1.space_after = Pt(10)

            p2 = tf.add_paragraph()
            p2.text = "Connecting Financial Evidence. Revealing Hidden Relationships."
            p2.font.size = Pt(22)
            p2.font.color.rgb = RGBColor(200, 220, 240)
            p2.space_after = Pt(30)

            p3 = tf.add_paragraph()
            p3.text = "Developed by Team CyboShield  |  Problem Statement PS05 — Financial Crime Analytics"
            p3.font.size = Pt(14)
            p3.font.bold = True
            p3.font.color.rgb = RGBColor(255, 255, 255)

            p4 = tf.add_paragraph()
            p4.text = "A Unified Financial Intelligence Workspace, Mule Conduit Profiler & Money-Trail Graph Analytics Platform"
            p4.font.size = Pt(12)
            p4.font.color.rgb = c_secondary
        else:
            set_slide_background(slide)
            add_slide_header(slide, slide_info["title"], "RAJASTHAN POLICE HACKATHON 2026 // PS05 // TEAM CYBOSHIELD")

            bullets = slide_info.get("bullets", [])
            col_width = Inches(5.6)
            card_height = Inches(2.6)
            
            for idx, (b_title, b_desc) in enumerate(bullets[:4]):
                col_idx = idx % 2
                row_idx = idx // 2
                left = Inches(0.8 + col_idx * 6.0)
                top = Inches(1.5 + row_idx * 2.85)

                card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, col_width, card_height)
                card.fill.solid()
                card.fill.fore_color.rgb = c_card
                card.line.color.rgb = RGBColor(220, 226, 232)
                card.line.width = Pt(1)

                left_box = Inches(0.8 + col_idx * 6.0 + 0.2)
                top_box = Inches(1.5 + row_idx * 2.85 + 0.15)
                w_box = Inches(5.6 - 0.4)
                h_box = Inches(2.6 - 0.3)
                tb_inner = slide.shapes.add_textbox(left_box, top_box, w_box, h_box)
                tf_inner = tb_inner.text_frame
                tf_inner.word_wrap = True

                p_head = tf_inner.paragraphs[0]
                p_head.text = f"{idx + 1}. {b_title}"
                p_head.font.size = Pt(14)
                p_head.font.bold = True
                p_head.font.color.rgb = c_primary
                p_head.space_after = Pt(8)

                p_body = tf_inner.add_paragraph()
                p_body.text = b_desc
                p_body.font.size = Pt(11)
                p_body.font.color.rgb = c_text

    prs.save(output_path)
    print(f"Action plan presentation saved to {output_path}")

def create_action_plan_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    c_navy = colors.HexColor("#142235")
    c_primary = colors.HexColor("#245B88")
    c_text = colors.HexColor("#172333")
    c_light = colors.HexColor("#F4F6F8")
    c_border = colors.HexColor("#DCE2E8")
    c_amber = colors.HexColor("#D69A36")

    title_style = ParagraphStyle(
        'SlideTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=18, leading=22, textColor=c_navy
    )
    cat_style = ParagraphStyle(
        'SlideCat', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12, textColor=c_amber
    )
    head_style = ParagraphStyle(
        'CardHead', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14, textColor=c_primary
    )
    body_style = ParagraphStyle(
        'CardBody', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13, textColor=c_text
    )

    slides = [
        ("01. Executive Overview & Problem Statement", [
            ("Mule Syndicate Expansion", "Criminal networks deploy structured layering through multi-tiered accounts to dissipate stolen funds."),
            ("Static Filter Evasion", "Sub-threshold transactions bypass conventional static rules, masking significant systemic losses."),
            ("Multi-Domain Disconnect", "Financial, DNS, IP and victim data remain separated in disparate unstructured formats."),
            ("Critical Interception Window", "First 4 hours are critical before funds exit into offshore crypto conduits.")
        ]),
        ("02. Operational Challenges in Cyber Police Stations", [
            ("Manual Data Processing", "Manual parsing of varied CSV and Excel statements consumes days of investigative time."),
            ("Circular Loop Invisibility", "Complex laundering loops (A->B->C->A) evade traditional linear scrutiny."),
            ("Admissibility Demands", "Forensic findings must meet statutory standards under Section 65B of the Indian Evidence Act."),
            ("Resource Constraints", "Police teams handle high caseloads requiring rapid, explainable automated triage.")
        ]),
        ("03. TRACEGRID Architectural Solution", [
            ("Unified Workspace", "Single pane of glass combining statement ingestion, graph exploration, and digital correlation."),
            ("Hybrid Analytics", "Ensemble of Scikit-Learn IsolationForest anomaly detection and deterministic forensic rules."),
            ("Directed Graph Canvas", "NetworkX-driven topological analysis rendered via high-performance React Flow."),
            ("Certified Dossier Export", "Court-admissible PDF generation containing structured findings and CrPC statutory guidance.")
        ]),
        ("04. Machine Learning & Explainability Approach", [
            ("Unsupervised Isolation Forest", "Detects multi-dimensional feature outliers (amount, hour, velocity, counterparty frequency)."),
            ("Explainable Rationale", "Every score is linked to plain-language forensic reasons; never probabilistic guilt."),
            ("Heuristic Calibration", "Calculates pass-through velocity ratios to isolate mule conduits from legitimate commerce."),
            ("Air-Gapped Operation", "Deterministic analytical fallback guarantees zero operational disruption offline.")
        ]),
        ("05. Implementation Plan & Police Rollout", [
            ("Prototype Completed", "Full Next.js + FastAPI implementation with synthetic database, testing, and report generation."),
            ("Field Trial Phase", "Testing with cyber police stations using sanitized real-world fraud statement logs."),
            ("National Integration", "Connectors for FIU-IND FINNET 2.0, I4C portal, and state CCTNS platforms."),
            ("Statewide Expansion", "Rollout to all district cyber crime units with automated Section 91 CrPC export.")
        ])
    ]

    story = []
    # Cover page
    story.append(Spacer(1, 40))
    story.append(Paragraph("RAJASTHAN POLICE HACKATHON 2026 // PS05", cat_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>TRACEGRID: ACTION PLAN & TECHNICAL DOSSIER</b>", ParagraphStyle('CoverT', parent=title_style, fontSize=26, leading=30)))
    story.append(Paragraph("Connecting Financial Evidence. Revealing Hidden Relationships.", ParagraphStyle('CoverSub', parent=head_style, fontSize=14, leading=18, textColor=c_primary)))
    story.append(Spacer(1, 20))
    story.append(Paragraph("<b>Team CyboShield</b> | Problem Statement PS05 — Financial Crime Analytics", body_style))
    story.append(Paragraph("A Unified Forensic Investigation Workspace, Mule Profiler & Money-Trail Graph Platform", body_style))
    story.append(PageBreak())

    for title, cards in slides:
        story.append(Paragraph("RAJASTHAN POLICE HACKATHON 2026 // PS05 // TEAM CYBOSHIELD", cat_style))
        story.append(Paragraph(f"<b>{title}</b>", title_style))
        story.append(HRFlowable(width="100%", thickness=1, color=c_primary, spaceBefore=4, spaceAfter=14))

        t_data = [
            [
                Paragraph(f"<b>1. {cards[0][0]}</b><br/><br/>{cards[0][1]}", body_style),
                Paragraph(f"<b>2. {cards[1][0]}</b><br/><br/>{cards[1][1]}", body_style),
            ],
            [
                Paragraph(f"<b>3. {cards[2][0]}</b><br/><br/>{cards[2][1]}", body_style),
                Paragraph(f"<b>4. {cards[3][0]}</b><br/><br/>{cards[3][1]}", body_style),
            ]
        ]
        t = Table(t_data, colWidths=[350, 350], rowHeights=[140, 140])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), c_light),
            ('BOX', (0,0), (-1,-1), 1, c_border),
            ('INNERGRID', (0,0), (-1,-1), 1, c_border),
            ('TOPPADDING', (0,0), (-1,-1), 14),
            ('BOTTOMPADDING', (0,0), (-1,-1), 14),
            ('LEFTPADDING', (0,0), (-1,-1), 16),
            ('RIGHTPADDING', (0,0), (-1,-1), 16),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        story.append(t)
        story.append(PageBreak())

    doc.build(story)
    print(f"Action plan PDF saved to {output_path}")

def create_wireframe_pdf(output_path: str):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    c_wire_bg = colors.HexColor("#F8FAFC")
    c_wire_border = colors.HexColor("#94A3B8")
    c_dark = colors.HexColor("#1E293B")
    c_gray = colors.HexColor("#64748B")

    title_style = ParagraphStyle(
        'WireTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14, leading=18, textColor=c_dark
    )
    meta_style = ParagraphStyle(
        'WireMeta', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=11, textColor=c_gray
    )
    box_style = ParagraphStyle(
        'WireBox', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11, textColor=c_dark
    )

    wireframes = [
        ("WIREFRAME 01: OVERVIEW DASHBOARD", "High-density executive metrics, real-time risk distribution bar, temporal burst timeline, priority investigations table."),
        ("WIREFRAME 02: INVESTIGATION CASE REGISTRY & CREATION MODAL", "Case dossier listing with FIR number, lead investigator, priority badges, and Section 91 CrPC requisition generator."),
        ("WIREFRAME 03: BANK STATEMENT CSV/XLSX INGESTION CONSOLE", "Drag-and-drop file upload, automated column header mapping, duplicate detection, and instant anomaly scan triggers."),
        ("WIREFRAME 04: TRANSACTION ANALYTICS & EXPLAINABLE ANOMALIES", "Tabular ledger view with multi-variable filters (Risk, Mode, Amount), expandable explainable lead drawer, and ML anomaly score."),
        ("WIREFRAME 05: MONEY-TRAIL NETWORK GRAPH (REACT FLOW)", "Directed multigraph canvas with degree centrality, minimum flow threshold slider, node inspector drawer, and circular loop isolation."),
        ("WIREFRAME 06: DIGITAL INFRASTRUCTURE INTELLIGENCE CONSOLE", "Passive WHOIS / DNS lookup query bar, bulletproof hosting ASN cross-correlations, and verified threat feed cards."),
        ("WIREFRAME 07: AI FORENSIC ASSISTANT CHAT INTERFACE", "Conversational investigation assistant with pre-canned prompts, grounded case citations, statutory notices, and uncertainty disclaimers."),
        ("WIREFRAME 08: COURT-READY EVIDENCE DOSSIER & PDF PREVIEW", "Branded forensic dossier preview with Section 65B Indian Evidence Act certification, signature blocks, and official export button.")
    ]

    story = []

    for name, desc in wireframes:
        story.append(Paragraph(f"<b>TRACEGRID UI WIREFRAME // LOW-FIDELITY SCHEMATIC</b>", meta_style))
        story.append(Paragraph(f"<b>{name}</b>", title_style))
        story.append(Paragraph(desc, meta_style))
        story.append(Spacer(1, 8))

        wire_table_data = [
            [
                Paragraph("<b>[SIDEBAR NAV]</b><br/><br/>&bull; Overview<br/>&bull; Cases<br/>&bull; Upload<br/>&bull; Ledger<br/>&bull; Graph<br/>&bull; Intel<br/>&bull; Cross-Case<br/>&bull; AI Chat<br/>&bull; Reports<br/>&bull; Settings<br/><br/><b>[ACTIVE CASE]</b><br/>RJ-EOW-2026-0042<br/>[CRITICAL]", box_style),
                Paragraph(f"<b>[HEADER BAR: {name}]</b> &bull; Status: Online &bull; Active Officer: Insp. Vikram Rathore<br/><br/>"
                          f"<b>+---------------------------------------------------------------------------------------------------+</b><br/>"
                          f"| <b>PRIMARY VIEW CONTENT REGION</b>                                                                 |<br/>"
                          f"| [KPI Metric Card 1]   [KPI Metric Card 2]   [KPI Metric Card 3]   [KPI Metric Card 4]         |<br/>"
                          f"| ₹42,50,000 Analyzed   ₹37,85,000 Suspicious  4 Mule Accounts       Case Priority: CRITICAL    |<br/>"
                          f"|                                                                                                   |<br/>"
                          f"| <b>[DATA DENSITY VISUALIZATION / INTERACTIVE CANVAS]</b>                                            |<br/>"
                          f"| +-----------------------------------------------------------------------------------------------+ |<br/>"
                          f"| | [Search Toolbar] [Filter Dropdown] [Sort Criteria] [Export Button]                            | |<br/>"
                          f"| |                                                                                               | |<br/>"
                          f"| | (Data Table / React Flow Directed Graph Nodes / Evidence Breakdown / Inspection Panel)         | |<br/>"
                          f"| |                                                                                               | |<br/>"
                          f"| | Record 1: TXN-00101 &bull; ACC-VIC-1001 -&gt; ACC-MULE-2001 &bull; ₹9,50,000 [HIGH_RISK]           | |<br/>"
                          f"| | Record 2: TXN-00105 &bull; ACC-MULE-2001 -&gt; ACC-LAYER-3001 &bull; ₹9,50,000 [MULE_CONDUIT]       | |<br/>"
                          f"| | Record 3: TXN-00111 &bull; ACC-SHARED-9921 -&gt; ACC-LAYER-3001 &bull; ₹50,000 [CIRCULAR_HOP]        | |<br/>"
                          f"| +-----------------------------------------------------------------------------------------------+ |<br/>"
                          f"| <i>Statutory Disclaimer: Investigative leads requiring Section 91 CrPC officer verification.</i>  |<br/>"
                          f"<b>+---------------------------------------------------------------------------------------------------+</b>", box_style)
            ]
        ]

        wt = Table(wire_table_data, colWidths=[130, 580], rowHeights=[360])
        wt.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (0,0), colors.HexColor("#E2E8F0")),
            ('BACKGROUND', (1,0), (1,0), c_wire_bg),
            ('BOX', (0,0), (-1,-1), 1, c_wire_border),
            ('INNERGRID', (0,0), (-1,-1), 1, c_wire_border),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))

        story.append(wt)
        story.append(PageBreak())

    doc.build(story)
    print(f"Wireframe PDF saved to {output_path}")

if __name__ == "__main__":
    os.makedirs("docs", exist_ok=True)
    create_action_plan_pptx("docs/TRACEGRID_Action_Plan.pptx")
    create_action_plan_pdf("docs/TRACEGRID_Action_Plan.pdf")
    create_wireframe_pdf("docs/TRACEGRID_Wireframe.pdf")
    print("Deliverables generation completed!")
