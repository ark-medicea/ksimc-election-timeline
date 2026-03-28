#!/usr/bin/env python3
"""Generate Route A PDF for KSIMC Election Timeline."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

# Brand colours
NAVY = HexColor('#0B1F3A')
GREEN = HexColor('#1b4332')
GREEN_LIGHT = HexColor('#e8f5e9')
GREEN_ACCENT = HexColor('#2d6a4f')
GREY_LIGHT = HexColor('#f1f3f5')
GREY_TEXT = HexColor('#555555')
GREY_RULE = HexColor('#cccccc')
WHITE = white

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(BASE_DIR, 'hujjat-logo.png')
OUTPUT_PATH = os.path.join(BASE_DIR, 'KSIMC-Election-Timeline-Route-A.pdf')

# Page setup
PAGE_W, PAGE_H = A4
MARGIN = 18 * mm

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PATH,
        pagesize=A4,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=15 * mm,
        bottomMargin=18 * mm,
    )

    styles = getSampleStyleSheet()

    # Custom styles
    s_org = ParagraphStyle('OrgName', parent=styles['Normal'],
                           fontName='Helvetica', fontSize=11, textColor=NAVY,
                           alignment=TA_CENTER, spaceAfter=2)
    s_title = ParagraphStyle('Title2', parent=styles['Normal'],
                             fontName='Helvetica-Bold', fontSize=16, textColor=NAVY,
                             alignment=TA_CENTER, spaceAfter=4)
    s_subtitle = ParagraphStyle('Subtitle2', parent=styles['Normal'],
                                fontName='Helvetica', fontSize=10.5, textColor=GREEN_ACCENT,
                                alignment=TA_CENTER, spaceAfter=2)
    s_rec = ParagraphStyle('Rec', parent=styles['Normal'],
                           fontName='Helvetica-Oblique', fontSize=8.5, textColor=GREY_TEXT,
                           alignment=TA_CENTER, spaceAfter=6)
    s_section = ParagraphStyle('Section', parent=styles['Normal'],
                               fontName='Helvetica-Bold', fontSize=11, textColor=WHITE,
                               spaceAfter=0, spaceBefore=0)
    s_normal = ParagraphStyle('Norm', parent=styles['Normal'],
                              fontName='Helvetica', fontSize=8.5, textColor=black,
                              leading=11)
    s_detail = ParagraphStyle('Detail', parent=styles['Normal'],
                              fontName='Helvetica', fontSize=7.2, textColor=GREY_TEXT,
                              leading=9.5, spaceBefore=1)
    s_bold = ParagraphStyle('Bold', parent=s_normal,
                            fontName='Helvetica-Bold')
    s_note_head = ParagraphStyle('NoteHead', parent=styles['Normal'],
                                 fontName='Helvetica-Bold', fontSize=10, textColor=NAVY,
                                 spaceBefore=6, spaceAfter=4)
    s_note = ParagraphStyle('Note', parent=styles['Normal'],
                            fontName='Helvetica', fontSize=8, textColor=GREY_TEXT,
                            leading=10.5, bulletIndent=0, leftIndent=10)
    s_check_head = ParagraphStyle('CheckHead', parent=styles['Normal'],
                                  fontName='Helvetica-Bold', fontSize=9, textColor=GREEN,
                                  spaceBefore=6, spaceAfter=2)
    s_check = ParagraphStyle('Check', parent=styles['Normal'],
                             fontName='Helvetica', fontSize=8, textColor=black,
                             leading=11, leftIndent=12)
    s_footer = ParagraphStyle('Footer', parent=styles['Normal'],
                              fontName='Helvetica', fontSize=7.5, textColor=GREY_TEXT,
                              alignment=TA_CENTER, spaceBefore=10)

    elements = []

    # --- Header with logo ---
    if os.path.exists(LOGO_PATH):
        logo = Image(LOGO_PATH, width=28*mm, height=28*mm)
        logo.hAlign = 'CENTER'
        elements.append(logo)
        elements.append(Spacer(1, 3*mm))

    elements.append(Paragraph("The KSIMC of London", s_org))
    elements.append(Spacer(1, 3*mm))
    elements.append(Paragraph("Election Cycle Timeline — AGM 2026", s_title))
    elements.append(Paragraph("Route A: EGM → AGM Sunday 14 June 2026", s_subtitle))
    elements.append(Paragraph("★ Recommended — Standard EGM with full 21 clear days' notice. Most comfortable timeline.", s_rec))
    elements.append(Spacer(1, 2*mm))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=GREEN, spaceAfter=4*mm))

    # --- Timeline data ---
    sections = [
        {
            'title': '1 · Commissioner Election (Mar–Apr)',
            'rows': [
                ('Mon 30 Mar', '76 days', 'EGM notice SENT by email',
                 'Cl. 6.1, 8.1, 17.3.1',
                 '21 clear days\' notice required. Email deemed received 24h later (Tue 31 Mar). Clear days exclude day of receipt and day of event. 21 clear days: Wed 1 Apr – Tue 21 Apr.'),
                ('Tue 31 Mar –\nTue 21 Apr', '', '21 clear days\' notice period', '', ''),
                ('Sun 5 Apr', '70 days', 'Remind members: constitutional amendments deadline in 4 weeks',
                 '—',
                 'Members wishing to propose amendments must submit to Hon Secretary by Sun 3 May (6 weeks before AGM).'),
                ('Sun 26 Apr', '49 days', 'EGM held — Electoral Commissioners elected',
                 'R. 7.6, 7.9',
                 '5 commissioners elected by secret ballot (at least 1 woman, at least 1 man). First available Sunday after notice period expires.'),
                ('Mon 27 Apr –\nSun 3 May', '', 'Commission organises: elects Chairperson, establishes processes', '', ''),
            ]
        },
        {
            'title': '2 · Pre-Election (May)',
            'rows': [
                ('Sun 3 May', '42 days', 'Constitutional amendments deadline',
                 'Cl. 18.1',
                 'Members must submit proposed amendments to Hon Secretary at least 6 weeks before AGM.'),
                ('Mon 4 May', '41 days', 'Nominations open',
                 'R. 7.2',
                 'Electoral Commission announces nominations are open and makes nomination papers available.'),
                ('Sun 10 May', '35 days', 'Member register snapshot date',
                 'R. 7.15',
                 'Register must be correct as at 20 clear days before Election (Sun 31 May).'),
                ('Thu 14 May', '31 days', 'Hon Sec provides member register to Electoral Commission',
                 'R. 7.15, Cl. 17.3.1',
                 'Register must be provided 15 clear days before Election. With 24h email receipt rule: send by Thu 14 May.'),
                ('Fri 15 May', '30 days', 'Nominations close',
                 'R. 7.2, Cl. 17.3.1',
                 'Nomination papers must be returned at least 14 clear days before Election. Deadline: Fri 15 May.'),
                ('Sat 16 May –\nThu 21 May', '', 'Electoral Commission verifies nominations, checks eligibility', '', ''),
            ]
        },
        {
            'title': '3 · EC Preparation & AGM Notices (May)',
            'rows': [
                ('By Fri 22 May', '—', 'EC Preparation — must be completed before AGM notice',
                 'Cl. 3.5.5, 6.9, 12.9',
                 'Audit completed · Annual report prepared · Budget approved · Subscription levels recommended · Previous AGM & EGM/SGM minutes prepared · Auditor appointment on agenda.'),
                ('Fri 22 May', '23 days', 'AGM notice + audited accounts SENT by email',
                 'Cl. 6.1, 12.9, 17.3.1',
                 '21 clear days\' notice. Sent Fri 22 May, received Sat 23 May. Clear days: Sun 24 May – Sat 13 Jun = 21 days. ✓'),
                ('Fri 22 May', '23 days', 'Constitutional amendments circulated',
                 'Cl. 18.3, 17.3.1',
                 'Members must receive 21 clear days\' notice of proposed amendments. Sent with AGM notice.'),
                ('Fri 22 May', '23 days', 'Candidate details circulated',
                 'R. 7.4.1, Cl. 17.3.1',
                 'Names, CVs, and manifestos circulated at least 7 clear days before Election. ✓'),
            ]
        },
        {
            'title': '4 · Motions, Election & AGM (May–Jun)',
            'rows': [
                ('Fri 29 May', '16 days', 'Motions deadline — members must send by this date',
                 'Cl. 7.3, 17.3.1',
                 '14 clear days\' written notice to Hon Secretary. Received Sat 30 May; clear days Sun 31 May – Sat 13 Jun = 14 days. ✓'),
                ('Fri 29 May', '16 days', 'Hustings (if President contested)',
                 'R. 7.4.3',
                 'Mandatory if more than one candidate for President. Must be held at least 1 day before Election.'),
                ('Sun 31 May', '14 days', '🗳  ELECTION DAY',
                 'Cl. 10.1, R. 7.16, 7.20, 7.22',
                 'Polling 10:30–19:30 at Imambara Building. Secret ballot. All 5 commissioners present. Results declared same day.'),
                ('Tue 2 Jun', '12 days', 'Motions circulated to members',
                 'Cl. 7.3, 17.3.1',
                 'All motions circulated at least 10 clear days before AGM. ✓'),
                ('Mon 1 Jun –\nSat 13 Jun', '', 'Handover period — Incoming EC liaises with outgoing EC',
                 'Cl. 11.4', ''),
                ('Sun 14 Jun', 'Day 0', '📋  AGM — New EC takes office',
                 'Cl. 6.8, 6.9, 11.4, R. 7.23',
                 'Accounts adopted, budget approved, subscriptions set, motions heard, constitutional amendments voted, auditor appointed.'),
            ]
        },
    ]

    # Column widths for the table
    col_widths = [28*mm, 15*mm, 58*mm, 30*mm, None]  # last col auto
    # Actually let's use a simpler layout: Date | Days | Event+Detail | Clause
    col_w = [30*mm, 16*mm, 82*mm, 32*mm]

    for sec in sections:
        # Section header as a coloured bar
        sec_header_data = [[Paragraph(sec['title'], s_section)]]
        sec_header_table = Table(sec_header_data, colWidths=[sum(col_w)])
        sec_header_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), NAVY),
            ('TEXTCOLOR', (0, 0), (-1, -1), WHITE),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('LEFTPADDING', (0, 0), (-1, -1), 6),
            ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(sec_header_table)

        # Build table rows
        table_data = []
        row_styles = []  # (row_index, bg_color) for special rows

        for i, (date, days, event, clause, detail) in enumerate(sec['rows']):
            is_period = (days == '' and detail == '')
            is_election = ('ELECTION DAY' in event)
            is_agm = ('AGM' in event and 'Day 0' in days)

            if is_period:
                # Period row - italic, span across
                row = [
                    Paragraph(f'<i><font color="#555555" size="7.5">{date} · {event}</font></i>', s_normal),
                    '', '', ''
                ]
                table_data.append(row)
                row_styles.append((len(table_data) - 1, 'period'))
            else:
                # Build event cell with detail underneath
                event_text = f'<b>{event}</b>'
                if is_election:
                    event_text = f'<b><font color="#1b4332">{event}</font></b>'
                if is_agm:
                    event_text = f'<b><font color="#1b4332">{event}</font></b>'

                event_parts = [Paragraph(event_text, s_normal)]
                if detail:
                    event_parts.append(Paragraph(detail, s_detail))

                # Stack event + detail
                from reportlab.platypus import ListFlowable
                event_cell = event_parts

                days_text = f'<font size="7" color="#6c757d">{days}</font>' if days else ''
                clause_text = f'<font size="7" color="#888888">{clause}</font>' if clause else ''

                row = [
                    Paragraph(f'<b>{date}</b>', s_normal),
                    Paragraph(days_text, s_normal),
                    event_cell,
                    Paragraph(clause_text, s_normal),
                ]
                table_data.append(row)

                if is_election:
                    row_styles.append((len(table_data) - 1, 'election'))
                elif is_agm:
                    row_styles.append((len(table_data) - 1, 'agm'))
                else:
                    row_styles.append((len(table_data) - 1, 'normal'))

        t = Table(table_data, colWidths=col_w, repeatRows=0)
        style_cmds = [
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('LINEBELOW', (0, 0), (-1, -2), 0.5, GREY_RULE),
            ('LINEBELOW', (0, -1), (-1, -1), 0.5, GREY_RULE),
        ]

        for row_idx, row_type in row_styles:
            if row_type == 'period':
                style_cmds.append(('SPAN', (0, row_idx), (-1, row_idx)))
                style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), GREY_LIGHT))
            elif row_type == 'election':
                style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), GREEN_LIGHT))
                style_cmds.append(('LINEBELOW', (0, row_idx), (-1, row_idx), 1, GREEN_ACCENT))
            elif row_type == 'agm':
                style_cmds.append(('BACKGROUND', (0, row_idx), (-1, row_idx), GREEN_LIGHT))
                style_cmds.append(('LINEBELOW', (0, row_idx), (-1, row_idx), 1.5, GREEN))

        t.setStyle(TableStyle(style_cmds))
        elements.append(t)
        elements.append(Spacer(1, 4*mm))

    # --- AGM Preparation Checklist ---
    elements.append(Spacer(1, 2*mm))
    elements.append(HRFlowable(width="100%", thickness=1, color=GREEN, spaceAfter=3*mm))
    elements.append(Paragraph("AGM Preparation Checklist", s_title.clone('CheckTitle', fontSize=12, spaceAfter=2)))

    checklist_sections = [
        ('Electoral Commission', [
            'Electoral Commissioners elected at EGM (R. 7.9)',
            'Member register snapshot taken — 20+ clear days before Election (R. 7.15)',
            'Member register provided to Electoral Commission — 15+ clear days before Election (R. 7.15)',
            'Nomination papers distributed and collected (R. 7.2)',
            'Candidate details circulated — 7+ clear days before Election (R. 7.4.1)',
            'Hustings arranged if President contested (R. 7.4.3)',
        ]),
        ('Audit & Accounts', [
            'Audit completed (Cl. 12.9, R. 5.2)',
            'Audited accounts sent to members — 21+ clear days before AGM (Cl. 12.9)',
            'Auditor appointment placed on AGM agenda (Cl. 6.9.8)',
        ]),
        ('Reports & Minutes', [
            'Annual report prepared by Hon Sec and approved by EC (Cl. 3.5.5)',
            'Budget for forthcoming year prepared and approved by EC (Cl. 6.9.5)',
            'Subscription level recommendations prepared (R. 6.3)',
            'Previous AGM minutes prepared (Cl. 6.9.1)',
            'All EGM/SGM minutes since last AGM prepared (Cl. 6.9.2)',
        ]),
        ('Notices & Circulation', [
            'AGM notice issued — 21+ clear days before (23 cal days by email) (Cl. 6.1)',
            'Constitutional amendment notices received — 6+ weeks before AGM (Cl. 18.1)',
            'Constitutional amendments circulated — 21+ clear days before AGM (Cl. 18.3)',
            'Motions received — 14+ clear days before AGM (Cl. 7.3)',
            'Motions circulated — 10+ clear days before AGM (Cl. 7.3)',
        ]),
    ]

    for heading, items in checklist_sections:
        elements.append(Paragraph(heading, s_check_head))
        for item in items:
            elements.append(Paragraph(f'☐  {item}', s_check))

    # --- Notes ---
    elements.append(Spacer(1, 4*mm))
    elements.append(HRFlowable(width="100%", thickness=1, color=GREEN, spaceAfter=3*mm))
    elements.append(Paragraph("Notes", s_note_head))

    notes = [
        '<b>24-Hour Email Receipt Rule</b> — Notice sent by email is deemed received 24 hours after sending (Cl. 17.3.1).',
        '<b>"Clear days"</b> exclude both the day of receipt and the day of the event (Cl. 20.1). For X clear days\' notice by email, send X+2 calendar days before the event.',
        '<b>Quick reference:</b> 21 clear days → send 23 cal days before · 15 clear days → 17 cal days · 14 clear days → 16 cal days · 10 clear days → 12 cal days · 7 clear days → 9 cal days.',
        '<b>AGM window</b> — Must be held between 1 June and 31 July (Cl. 6.8). Must not fall on a UK public holiday or auspicious Shia Ithna-Asheri date.',
        '<b>Election must be on a Sunday</b> (Cl. 10.1) — Polling hours 10:30–19:30, at least 2 weeks before the AGM.',
        '<b>Uncontested positions</b> are declared elected without a vote (R. 7.4.2).',
    ]
    for note in notes:
        elements.append(Paragraph(f'•  {note}', s_note))
        elements.append(Spacer(1, 1.5*mm))

    # --- Footer ---
    elements.append(Spacer(1, 6*mm))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=GREY_RULE, spaceAfter=3*mm))
    elements.append(Paragraph(
        "Prepared by the Electoral Commission · March 2026<br/>"
        "Based on the KSIMC London Constitution &amp; Election Rules<br/>"
        "All dates incorporate the 24-hour email receipt rule (Cl. 17.3.1) and clear days calculation (Cl. 20.1)",
        s_footer
    ))

    doc.build(elements)
    print(f"PDF generated: {OUTPUT_PATH}")

if __name__ == '__main__':
    build_pdf()
