import io
import datetime
import json
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether, HRFlowable
)
from sqlalchemy.orm import Session
from backend.models.models import Investigation, Account, Transaction, Evidence, DigitalIntelligence

class ReportPDFService:
    """
    Generates structured, court-ready, evidence-backed forensic investigation
    dossiers in PDF format using ReportLab.
    """

    @classmethod
    def generate_case_pdf(cls, db: Session, case_id: str) -> bytes:
        case = db.query(Investigation).filter(Investigation.id == case_id).first()
        if not case:
            raise ValueError("Case not found")

        tx_list = db.query(Transaction).filter(Transaction.case_id == case_id).all()
        acc_list = db.query(Account).filter(Account.case_id == case_id).all()
        evidence_list = db.query(Evidence).filter(Evidence.case_id == case_id).all()
        intel_list = db.query(DigitalIntelligence).filter(DigitalIntelligence.case_id == case_id).all()

        flagged_tx = [t for t in tx_list if t.risk_flag != "NORMAL"]
        total_vol = sum(t.amount for t in tx_list)
        flagged_vol = sum(t.amount for t in flagged_tx)

        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Enterprise Styles
        c_navy = colors.HexColor("#142235")
        c_primary = colors.HexColor("#245B88")
        c_dark = colors.HexColor("#172333")
        c_gray = colors.HexColor("#687586")
        c_light = colors.HexColor("#F4F6F8")
        c_critical = colors.HexColor("#BD4A4A")
        c_warning = colors.HexColor("#D69A36")
        c_border = colors.HexColor("#DCE2E8")

        title_style = ParagraphStyle(
            'DocTitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=18,
            leading=22,
            textColor=c_navy
        )
        subtitle_style = ParagraphStyle(
            'DocSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=c_gray
        )
        section_style = ParagraphStyle(
            'SectionHead',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=c_primary,
            spaceBefore=12,
            spaceAfter=6
        )
        body_style = ParagraphStyle(
            'Body',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=c_dark
        )
        badge_style = ParagraphStyle(
            'Badge',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=8,
            leading=10,
            textColor=colors.white
        )
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=11,
            textColor=c_gray
        )

        story = []

        # 1. Header & Branding Banner
        header_table_data = [
            [
                Paragraph("<b>TRACEGRID</b> | Financial Crime Intelligence", title_style),
                Paragraph(f"<b>OFFICIAL USE ONLY</b><br/>Ref: {case.case_number}", ParagraphStyle('RightRef', parent=subtitle_style, alignment=2))
            ],
            [
                Paragraph("Team CyboShield &bull; Rajasthan Police Hackathon 2026 &bull; Problem Statement PS05", subtitle_style),
                Paragraph(f"Generated: {datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}", ParagraphStyle('RightDate', parent=subtitle_style, alignment=2))
            ]
        ]
        header_table = Table(header_table_data, colWidths=[340, 200])
        header_table.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        story.append(header_table)
        story.append(Spacer(1, 8))
        story.append(HRFlowable(width="100%", thickness=1.5, color=c_primary, spaceBefore=2, spaceAfter=10))

        # 2. Case Overview Card
        story.append(Paragraph("1. INVESTIGATION PROFILE & EXECUTIVE SUMMARY", section_style))
        overview_data = [
            [
                Paragraph("<b>Case Title:</b>", body_style), Paragraph(case.title, body_style),
                Paragraph("<b>Case Priority:</b>", body_style), Paragraph(f"<font color='{c_critical.hexval()}'><b>{case.priority}</b></font>", body_style)
            ],
            [
                Paragraph("<b>Case Reference:</b>", body_style), Paragraph(case.case_number, body_style),
                Paragraph("<b>Status:</b>", body_style), Paragraph(case.status, body_style)
            ],
            [
                Paragraph("<b>Lead Investigator:</b>", body_style), Paragraph(case.lead_investigator, body_style),
                Paragraph("<b>Opened:</b>", body_style), Paragraph(case.created_at.strftime('%Y-%m-%d'), body_style)
            ],
            [
                Paragraph("<b>Description:</b>", body_style),
                Paragraph(case.description or "Comprehensive financial intelligence analysis of suspected fund layering network.", body_style),
                "", ""
            ]
        ]
        overview_table = Table(overview_data, colWidths=[90, 200, 90, 160])
        overview_table.setStyle(TableStyle([
            ('SPAN', (1, 3), (3, 3)),
            ('BACKGROUND', (0, 0), (-1, -1), c_light),
            ('BOX', (0, 0), (-1, -1), 0.5, c_border),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(overview_table)
        story.append(Spacer(1, 10))

        # 3. Key Financial Metrics Box
        story.append(Paragraph("2. QUANTITATIVE FORENSIC METRICS", section_style))
        metrics_data = [
            [
                Paragraph(f"<b>Total Transactions:</b><br/>{len(tx_list)}", body_style),
                Paragraph(f"<b>Total Volume Analyzed:</b><br/>₹{total_vol:,.2f}", body_style),
                Paragraph(f"<b>Flagged Transactions:</b><br/><font color='{c_critical.hexval()}'><b>{len(flagged_tx)} ({len(flagged_tx)/len(tx_list)*100 if tx_list else 0:.1f}%)</b></font>", body_style),
                Paragraph(f"<b>Suspicious Volume:</b><br/><font color='{c_critical.hexval()}'><b>₹{flagged_vol:,.2f}</b></font>", body_style)
            ]
        ]
        metrics_table = Table(metrics_data, colWidths=[135, 135, 135, 135])
        metrics_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF1F6")),
            ('BOX', (0, 0), (-1, -1), 1, c_primary),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ]))
        story.append(metrics_table)
        story.append(Spacer(1, 10))

        # 4. High-Priority Flagged Transactions Table
        story.append(Paragraph("3. FLAGGED TRANSACTIONS REQUIRING HUMAN SCRUTINY", section_style))
        tx_rows = [
            [
                Paragraph("<b>Tx ID / Time</b>", body_style),
                Paragraph("<b>Sender Account</b>", body_style),
                Paragraph("<b>Receiver Account</b>", body_style),
                Paragraph("<b>Amount (INR)</b>", body_style),
                Paragraph("<b>Risk Lead & Reasons</b>", body_style)
            ]
        ]
        
        for t in flagged_tx[:8]: # Display top 8 in report
            reasons = []
            try:
                reasons = json.loads(t.flag_reasons) if isinstance(t.flag_reasons, str) else t.flag_reasons
            except Exception:
                pass
            first_reason = reasons[0] if reasons else "Anomalous velocity indicator"
            
            tx_rows.append([
                Paragraph(f"<b>{t.id}</b><br/>{t.timestamp.strftime('%d-%b %H:%M')}", body_style),
                Paragraph(f"{t.sender_account}<br/><i>{t.sender_name}</i>", body_style),
                Paragraph(f"{t.receiver_account}<br/><i>{t.receiver_name}</i>", body_style),
                Paragraph(f"<b>₹{t.amount:,.2f}</b><br/>{t.transaction_type}", body_style),
                Paragraph(f"<b>[{t.risk_flag}]</b> {first_reason}", body_style)
            ])

        if len(tx_rows) == 1:
            empty_cell = Paragraph("", body_style)
            tx_rows.append([Paragraph("No transactions flagged in this dataset.", body_style), empty_cell, empty_cell, empty_cell, empty_cell])

        tx_table = Table(tx_rows, colWidths=[80, 110, 110, 85, 155])
        tx_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_navy),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BOX', (0, 0), (-1, -1), 0.5, c_border),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(tx_table)
        story.append(Spacer(1, 10))

        # 5. Accounts Under Review
        story.append(Paragraph("4. TARGET ACCOUNTS & MULE CONDUIT PROFILES", section_style))
        acc_rows = [
            [
                Paragraph("<b>Account Number</b>", body_style),
                Paragraph("<b>Holder / Bank</b>", body_style),
                Paragraph("<b>Inflow / Outflow</b>", body_style),
                Paragraph("<b>Risk Rating</b>", body_style),
                Paragraph("<b>Observed Lead Tags</b>", body_style)
            ]
        ]
        sorted_accs = sorted(acc_list, key=lambda a: a.risk_score, reverse=True)[:5]
        for a in sorted_accs:
            tags = []
            try:
                tags = json.loads(a.risk_tags) if isinstance(a.risk_tags, str) else a.risk_tags
            except Exception:
                pass
            tag_str = ", ".join(tags) if tags else "STANDARD_MONITORING"
            color_hex = c_critical.hexval() if a.risk_level in ("HIGH", "CRITICAL") else c_warning.hexval()

            acc_rows.append([
                Paragraph(f"<b>{a.id}</b><br/>Type: {a.account_type}", body_style),
                Paragraph(f"{a.account_holder}<br/><i>{a.bank_name}</i>", body_style),
                Paragraph(f"In: ₹{a.total_inflow:,.2f}<br/>Out: ₹{a.total_outflow:,.2f}", body_style),
                Paragraph(f"<font color='{color_hex}'><b>{a.risk_level}</b> ({a.risk_score:.0f}/100)</font>", body_style),
                Paragraph(f"<i>{tag_str}</i>", body_style)
            ])

        acc_table = Table(acc_rows, colWidths=[100, 130, 110, 80, 120])
        acc_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), c_primary),
            ('BOX', (0, 0), (-1, -1), 0.5, c_border),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        story.append(acc_table)
        story.append(Spacer(1, 10))

        # 6. Digital Infrastructure & Corroborating Evidence
        story.append(Paragraph("5. DIGITAL INFRASTRUCTURE EVIDENCE & CROSS-CORRELATION", section_style))
        intel_rows = [
            [
                Paragraph("<b>Indicator</b>", body_style),
                Paragraph("<b>Type</b>", body_style),
                Paragraph("<b>Provider / ASN / Hosting</b>", body_style),
                Paragraph("<b>Risk Rating</b>", body_style),
                Paragraph("<b>Verification Status</b>", body_style)
            ]
        ]
        for it in intel_list[:4]:
            meta = {}
            try:
                meta = json.loads(it.metadata_json) if isinstance(it.metadata_json, str) else it.metadata_json
            except Exception:
                pass
            asn_info = meta.get("asn", meta.get("registrar", "Commercial Hosting"))
            intel_rows.append([
                Paragraph(f"<b>{it.indicator_value}</b>", body_style),
                Paragraph(it.indicator_type, body_style),
                Paragraph(str(asn_info)[:40], body_style),
                Paragraph(f"<b>{it.risk_rating}</b>", body_style),
                Paragraph(f"<i>{it.verification_status}</i>", body_style)
            ])

        if len(intel_rows) > 1:
            intel_table = Table(intel_rows, colWidths=[130, 80, 150, 75, 105])
            intel_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), c_navy),
                ('BOX', (0, 0), (-1, -1), 0.5, c_border),
                ('INNERGRID', (0, 0), (-1, -1), 0.5, c_border),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))
            story.append(intel_table)
            story.append(Spacer(1, 10))

        # 7. Statutory Limitations & Chain of Custody Note
        story.append(Spacer(1, 5))
        story.append(HRFlowable(width="100%", thickness=0.5, color=c_border, spaceBefore=4, spaceAfter=8))
        disclaimer_text = (
            "<b>STATUTORY DISCLAIMER & INVESTIGATIVE INTEGRITY NOTICE:</b><br/>"
            "This report is generated by TRACEGRID (Team CyboShield) for the Rajasthan Police Hackathon 2026 (PS05). "
            "All findings, anomaly scores, and risk tags represent algorithmic intelligence leads synthesized from provided transaction logs. "
            "No determination in this document constitutes autonomous proof of guilt or criminal liability. "
            "Human verification, sworn witness testimony, and formal Section 91 CrPC requisitions are mandatory prior to judicial proceedings. "
            "All demonstration data is purely synthetic and bears no intentional resemblance to actual commercial entities."
        )
        story.append(Paragraph(disclaimer_text, disclaimer_style))

        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        return pdf_bytes

