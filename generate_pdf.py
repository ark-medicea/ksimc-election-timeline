#!/usr/bin/env python3
"""Generate KSIMC Election & AGM Timeline 2026 PDF — v3 polished letterhead."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ── Colours ──────────────────────────────────────────────────────────
NAVY = HexColor("#0B1F3A")
NAVY_LIGHT = HexColor("#1A3A5C")
GREY_TEXT = HexColor("#6B7280")
GREY_LIGHT = HexColor("#F3F4F6")
GREY_LINE = HexColor("#D1D5DB")
WHITE = white
ELECTION_BG = HexColor("#EFF6FF")
AGM_BG = HexColor("#F0FDF4")
ACCENT_GOLD = HexColor("#C5975B")

# ── Paths ────────────────────────────────────────────────────────────
DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(DIR, "hujjat-logo.png")
OUTPUT_PATH = os.path.join(DIR, "KSIMC-Election-Timeline-2026.pdf")

# ── Page setup ───────────────────────────────────────────────────────
PAGE_W, PAGE_H = A4
MARGIN_L = 20 * mm
MARGIN_R = 20 * mm
MARGIN_T = 20 * mm
MARGIN_B = 18 * mm

# ── Styles ───────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

style_org_name = ParagraphStyle(
    "OrgName", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=11, textColor=NAVY,
    alignment=TA_RIGHT, leading=14, spaceAfter=1,
)
style_org_detail = ParagraphStyle(
    "OrgDetail", parent=styles["Normal"],
    fontName="Helvetica", fontSize=8.5, textColor=GREY_TEXT,
    alignment=TA_RIGHT, leading=11, spaceAfter=0,
)
style_title = ParagraphStyle(
    "Title", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=18, textColor=WHITE,
    alignment=TA_CENTER, leading=24, spaceBefore=0, spaceAfter=0,
)
style_date_col = ParagraphStyle(
    "DateCol", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=9, textColor=NAVY,
    alignment=TA_LEFT, leading=12,
)
style_event_col = ParagraphStyle(
    "EventCol", parent=styles["Normal"],
    fontName="Helvetica-Bold", fontSize=9, textColor=HexColor("#1F2937"),
    alignment=TA_LEFT, leading=12,
)
style_detail_col = ParagraphStyle(
    "DetailCol", parent=styles["Normal"],
    fontName="Helvetica", fontSize=7.8, textColor=GREY_TEXT,
    alignment=TA_LEFT, leading=10.5,
)
style_clause_col = ParagraphStyle(
    "ClauseCol", parent=styles["Normal"],
    fontName="Helvetica", fontSize=7, textColor=HexColor("#9CA3AF"),
    alignment=TA_RIGHT, leading=10,
)
style_footer = ParagraphStyle(
    "Footer", parent=styles["Normal"],
    fontName="Helvetica", fontSize=7.5, textColor=GREY_TEXT,
    alignment=TA_CENTER, leading=10,
)
style_section = ParagraphStyle(
    "Section", parent=styles["Normal"],
    fontName="Helvetica", fontSize=7.5, textColor=GREY_TEXT,
    alignment=TA_LEFT, leading=10,
)


def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH, pagesize=A4,
        leftMargin=MARGIN_L, rightMargin=MARGIN_R,
        topMargin=MARGIN_T, bottomMargin=MARGIN_B,
    )

    elements = []
    usable_w = PAGE_W - MARGIN_L - MARGIN_R

    # ── LETTERHEAD ───────────────────────────────────────────────────
    logo = Image(LOGO_PATH, width=55, height=55)

    right_block = [
        Paragraph("The KSIMC of London", style_org_name),
        Paragraph("Hujjat Islamic Centre", style_org_detail),
        Paragraph("Stanmore, London", style_org_detail),
        Spacer(1, 2),
        Paragraph("Registered Charity No. 288356", ParagraphStyle(
            "CharityNo", parent=style_org_detail,
            fontSize=7.5, textColor=HexColor("#9CA3AF"),
        )),
    ]

    from reportlab.platypus import KeepTogether
    # Use a table for logo-left, details-right
    header_table = Table(
        [[logo, right_block]],
        colWidths=[65, usable_w - 65],
    )
    header_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (0, 0), (0, 0), "LEFT"),
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    elements.append(header_table)
    elements.append(Spacer(1, 8))

    # Navy line under letterhead
    elements.append(HRFlowable(
        width="100%", thickness=1.5, color=NAVY,
        spaceBefore=0, spaceAfter=14,
    ))

    # ── TITLE BANNER ─────────────────────────────────────────────────
    title_table = Table(
        [[Paragraph("Election &amp; AGM Timeline 2026", style_title)]],
        colWidths=[usable_w],
        rowHeights=[38],
    )
    title_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
    ]))
    elements.append(title_table)
    elements.append(Spacer(1, 14))

    # ── TIMELINE DATA ────────────────────────────────────────────────
    # (date, event, detail, clause, special_style)
    rows = [
        (
            "Mon 30 Mar",
            "EGM notice issued to members",
            "Formal notice of EGM to elect Electoral Commissioners, sent by email with 21 clear days\u2019 notice",
            "Cl. 6.1, 8.1",
            None,
        ),
        (
            "Sun 26 Apr",
            "EGM held \u2014 Electoral Commissioners elected",
            "Five commissioners elected by secret ballot to oversee the election process",
            "R. 7.6, 7.9",
            None,
        ),
        (
            "Sun 3 May",
            "Constitutional amendments submission deadline",
            "Last day for members to submit proposed amendments to the Hon Secretary (6 weeks before AGM)",
            "Cl. 18.1",
            None,
        ),
        (
            "Mon 4 May",
            "Nominations open",
            "Electoral Commission invites nominations for all Executive Committee positions",
            "R. 7.2",
            None,
        ),
        (
            "Fri 15 May",
            "Nominations close",
            "Completed nomination papers must be returned at least 14 clear days before the Election",
            "R. 7.2",
            None,
        ),
        (
            "~Thu 22 May",
            "AGM notice issued to members",
            "Formal notice of AGM including agenda, audited accounts, and any proposed constitutional amendments",
            "Cl. 6.1, 12.9",
            None,
        ),
        (
            "Fri 22 May",
            "Candidate details circulated",
            "Names, CVs and manifestos of all verified candidates sent to members (7+ clear days before Election)",
            "R. 7.4.1",
            None,
        ),
        (
            "Fri 29 May",
            "Hustings (if President contested)",
            "Mandatory public meeting if more than one candidate stands for President",
            "R. 7.4.3",
            None,
        ),
        (
            "Sun 31 May",
            "\U0001f5f3\ufe0f  ELECTION DAY",
            "Polling 10:30\u201319:30 at the Centre. Secret ballot. Results declared same day.",
            "Cl. 10.1, R. 7.16",
            "election",
        ),
        (
            "Sun 14 Jun",
            "\U0001f4cb  AGM",
            "New Executive Committee takes office. Accounts adopted, budget approved, auditor appointed.",
            "Cl. 6.8, 6.9",
            "agm",
        ),
    ]

    # Build table
    col_date_w = 68
    col_clause_w = 72
    col_event_w = usable_w - col_date_w - col_clause_w

    table_data = []
    # Header row
    table_data.append([
        Paragraph("<b>Date</b>", ParagraphStyle("TH", parent=style_date_col, textColor=WHITE, fontSize=8)),
        Paragraph("<b>Event</b>", ParagraphStyle("TH", parent=style_event_col, textColor=WHITE, fontSize=8)),
        Paragraph("<b>Reference</b>", ParagraphStyle("TH", parent=style_clause_col, textColor=WHITE, fontSize=8)),
    ])

    row_styles = []  # (row_index, bg_color)
    for i, (date, event, detail, clause, special) in enumerate(rows):
        row_idx = i + 1  # +1 for header

        # Combine event + detail in one cell
        event_para = Paragraph(
            f"<b>{event}</b><br/><font size='7.5' color='#6B7280'>{detail}</font>",
            ParagraphStyle("EventDetail", parent=style_event_col, leading=11.5, spaceAfter=1),
        )
        date_para = Paragraph(date, style_date_col)
        clause_para = Paragraph(clause, style_clause_col)

        table_data.append([date_para, event_para, clause_para])

        if special == "election":
            row_styles.append((row_idx, ELECTION_BG))
        elif special == "agm":
            row_styles.append((row_idx, AGM_BG))

    timeline_table = Table(
        table_data,
        colWidths=[col_date_w, col_event_w, col_clause_w],
        repeatRows=1,
    )

    ts = [
        # Header
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

        # Grid
        ("LINEBELOW", (0, 0), (-1, -1), 0.5, GREY_LINE),
        ("LINEABOVE", (0, 0), (-1, 0), 1, NAVY),
        ("LINEBELOW", (0, -1), (-1, -1), 1, NAVY),

        # Padding
        ("TOPPADDING", (0, 0), (-1, 0), 6),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("TOPPADDING", (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 7),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),

        # Alignment
        ("VALIGN", (0, 0), (-1, -1), "TOP"),

        # Alternating rows (light)
        *[("BACKGROUND", (0, r), (-1, r), GREY_LIGHT) for r in range(2, len(table_data), 2)],
    ]

    # Override with special row colours
    for row_idx, bg in row_styles:
        ts.append(("BACKGROUND", (0, row_idx), (-1, row_idx), bg))

    timeline_table.setStyle(TableStyle(ts))
    elements.append(timeline_table)

    # ── FOOTER ───────────────────────────────────────────────────────
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(
        width="100%", thickness=0.5, color=GREY_LINE,
        spaceBefore=0, spaceAfter=8,
    ))
    elements.append(Paragraph("hujjat.org  ·  March 2026", style_footer))

    # ── Build ────────────────────────────────────────────────────────
    doc.build(elements)
    print(f"✅ PDF written to {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
