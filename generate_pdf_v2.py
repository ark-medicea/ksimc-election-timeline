#!/usr/bin/env python3
"""Generate KSIMC Election & AGM Timeline 2026 — member-facing PDF."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOGO_PATH = os.path.join(SCRIPT_DIR, "hujjat-logo.png")
OUTPUT_PATH = os.path.join(SCRIPT_DIR, "KSIMC-Election-Timeline-2026.pdf")

# Colours
NAVY = HexColor("#0B1F3A")
LIGHT_GREY = HexColor("#F2F4F6")
MEDIUM_GREY = HexColor("#E0E4E8")
HIGHLIGHT_BLUE = HexColor("#E8F0FE")
HIGHLIGHT_GREEN = HexColor("#E6F4EA")
WHITE = white
DARK_TEXT = HexColor("#1A1A1A")
SUBTLE_TEXT = HexColor("#5A6270")

PAGE_W, PAGE_H = A4
MARGIN_LEFT = 25 * mm
MARGIN_RIGHT = 25 * mm
CONTENT_W = PAGE_W - MARGIN_LEFT - MARGIN_RIGHT

# Timeline data: (date, event, explanation, highlight)
TIMELINE = [
    ("Mon 30 Mar", "EGM notice issued",
     "An EGM is required to elect Electoral Commissioners who were not elected at the 2025 AGM. "
     "Formal notice will be sent to all members at least 21 days before the EGM (Clause 14).",
     None),
    ("Sun 5 Apr", "Reminder: constitutional amendment proposals due in 4 weeks",
     "If you wish to propose changes to the Constitution, prepare your proposals now — "
     "they must be submitted in writing to the Hon Secretary by 3 May (Clause 25).",
     None),
    ("Sun 26 Apr", "EGM — Electoral Commissioners elected by secret ballot",
     "Members will elect Electoral Commissioners at this Extraordinary General Meeting. "
     "The EC must consist of members who are not standing for election (Clause 17).",
     None),
    ("Sun 3 May", "Deadline: constitutional amendment proposals",
     "Last day to submit proposed constitutional amendments in writing to the Hon Secretary. "
     "Proposals received after this date cannot be considered at the AGM (Clause 25).",
     None),
    ("Mon 4 May", "Nominations open for Executive Committee",
     "Nomination papers available from the Electoral Commission. Each candidate needs a proposer "
     "and seconder. Presidential candidates require 5 seconders (Clause 18).",
     None),
    ("Fri 15 May", "Nominations close",
     "All completed nomination forms must be received by the Electoral Commission by this date. "
     "Late nominations will not be accepted.",
     None),
    ("Fri 22 May", "Candidate details circulated to members",
     "The Electoral Commission will circulate details of all valid candidates to the membership, "
     "at least 7 days before Election Day (Clause 18).",
     None),
    ("Fri 29 May", "Hustings (if President position is contested)",
     "If more than one candidate is standing for President, a hustings event will be held "
     "to allow candidates to address the membership.",
     None),
    ("Sun 31 May", "ELECTION DAY — 10:30 to 19:30",
     "Voting at Hujjat Islamic Centre, Imambara Building. All members are entitled to vote. "
     "Please bring your membership details. Secret ballot (Clause 18).",
     "election"),
    ("Sun 14 Jun", "AGM — new Executive Committee takes office",
     "Audited accounts, budget, motions, and constitutional amendments will be considered. "
     "The newly elected Executive Committee formally takes office (Clause 13).",
     "agm"),
]


def draw_header(c):
    """Draw the letterhead: logo, title, address, divider line."""
    y = PAGE_H - 20 * mm

    # Logo — centered, good size
    logo = ImageReader(LOGO_PATH)
    logo_h = 22 * mm
    logo_w = 22 * mm
    logo_x = (PAGE_W - logo_w) / 2
    c.drawImage(logo, logo_x, y - logo_h, logo_w, logo_h, mask="auto")
    y -= logo_h + 4 * mm

    # Organisation name
    c.setFont("Helvetica-Bold", 18)
    c.setFillColor(NAVY)
    c.drawCentredString(PAGE_W / 2, y, "The KSIMC of London")
    y -= 6 * mm

    # Address line
    c.setFont("Helvetica", 9)
    c.setFillColor(SUBTLE_TEXT)
    c.drawCentredString(PAGE_W / 2, y, "Hujjat Islamic Centre  ·  Thegam House  ·  Wood Lane  ·  Stanmore  ·  HA7 4LQ")
    y -= 5 * mm

    # Thin navy divider
    c.setStrokeColor(NAVY)
    c.setLineWidth(0.8)
    c.line(MARGIN_LEFT, y, PAGE_W - MARGIN_RIGHT, y)
    y -= 10 * mm

    return y


def draw_title(c, y):
    """Draw document title."""
    c.setFont("Helvetica-Bold", 20)
    c.setFillColor(NAVY)
    c.drawCentredString(PAGE_W / 2, y, "Election & AGM Timeline 2026")
    y -= 7 * mm

    # Subtitle
    c.setFont("Helvetica", 10)
    c.setFillColor(SUBTLE_TEXT)
    c.drawCentredString(PAGE_W / 2, y, "Key dates and deadlines for members")
    y -= 12 * mm

    return y


def draw_timeline(c, y):
    """Draw the timeline entries."""
    date_col_w = 28 * mm
    event_col_x = MARGIN_LEFT + date_col_w + 4 * mm
    event_col_w = CONTENT_W - date_col_w - 4 * mm

    for i, (date, event, explanation, highlight) in enumerate(TIMELINE):
        # Calculate row height needed
        # Wrap explanation text
        from reportlab.lib.utils import simpleSplit
        exp_lines = simpleSplit(explanation, "Helvetica", 8.5, event_col_w - 2 * mm)
        row_h = 7 * mm + len(exp_lines) * 3.2 * mm + 3 * mm

        # Check if we need a new page
        if y - row_h < 25 * mm:
            c.showPage()
            y = PAGE_H - 20 * mm
            # Re-draw a minimal header on continuation
            c.setFont("Helvetica-Bold", 10)
            c.setFillColor(NAVY)
            c.drawString(MARGIN_LEFT, y, "Election & AGM Timeline 2026 (continued)")
            y -= 8 * mm

        # Row background
        if highlight == "election":
            bg = HIGHLIGHT_GREEN
        elif highlight == "agm":
            bg = HIGHLIGHT_BLUE
        elif i % 2 == 0:
            bg = LIGHT_GREY
        else:
            bg = WHITE

        c.setFillColor(bg)
        c.roundRect(MARGIN_LEFT - 2 * mm, y - row_h + 2 * mm,
                     CONTENT_W + 4 * mm, row_h, 2 * mm, fill=1, stroke=0)

        # Left accent bar for highlighted rows
        if highlight:
            accent = HexColor("#2E7D32") if highlight == "election" else HexColor("#1565C0")
            c.setFillColor(accent)
            c.roundRect(MARGIN_LEFT - 2 * mm, y - row_h + 2 * mm, 1.2 * mm, row_h, 0.6 * mm, fill=1, stroke=0)

        # Date
        c.setFont("Helvetica-Bold", 9.5)
        c.setFillColor(NAVY)
        c.drawString(MARGIN_LEFT + 1 * mm, y - 1 * mm, date)

        # Event title
        if highlight == "election":
            c.setFont("Helvetica-Bold", 11)
        else:
            c.setFont("Helvetica-Bold", 10)
        c.setFillColor(DARK_TEXT)
        c.drawString(event_col_x, y - 1 * mm, event)

        # Explanation
        c.setFont("Helvetica", 8.5)
        c.setFillColor(SUBTLE_TEXT)
        text_y = y - 5.5 * mm
        for line in exp_lines:
            c.drawString(event_col_x + 0.5 * mm, text_y, line)
            text_y -= 3.2 * mm

        y -= row_h + 1.5 * mm

    return y


def draw_footer(c):
    """Draw footer with date of issue."""
    footer_y = 12 * mm

    # Thin line
    c.setStrokeColor(MEDIUM_GREY)
    c.setLineWidth(0.5)
    c.line(MARGIN_LEFT, footer_y + 4 * mm, PAGE_W - MARGIN_RIGHT, footer_y + 4 * mm)

    c.setFont("Helvetica", 7.5)
    c.setFillColor(SUBTLE_TEXT)
    c.drawString(MARGIN_LEFT, footer_y, "Issued: 28 March 2026  ·  The KSIMC of London  ·  Registered Charity")
    c.drawRightString(PAGE_W - MARGIN_RIGHT, footer_y, "www.ksimc.com")


def draw_watermark(c):
    """Subtle watermark in the background."""
    c.saveState()
    c.setFillColor(Color(0.04, 0.12, 0.23, alpha=0.03))  # Very faint navy
    c.setFont("Helvetica-Bold", 72)
    c.translate(PAGE_W / 2, PAGE_H / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, "KSIMC")
    c.restoreState()


def main():
    c = Canvas(OUTPUT_PATH, pagesize=A4)
    c.setTitle("KSIMC Election & AGM Timeline 2026")
    c.setAuthor("The KSIMC of London")

    # Watermark first (behind everything)
    draw_watermark(c)

    y = draw_header(c)
    y = draw_title(c, y)
    y = draw_timeline(c, y)
    draw_footer(c)

    c.save()
    print(f"PDF generated: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
