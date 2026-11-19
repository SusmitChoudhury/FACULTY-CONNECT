import os
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image, HRFlowable
from reportlab.pdfgen import canvas

# Official Palette
PRIMARY_GREEN = HexColor('#15370D')
ACCENT_ORANGE = HexColor('#F2842F')
BG_CREAM = HexColor('#FCF9EA')
DARK_TEXT = HexColor('#000000')
SLATE_TEXT = HexColor('#1E293B')
MUTED_TEXT = HexColor('#475569')
BORDER_COLOR = HexColor('#CBD5E1')
LIGHT_GREEN_BG = HexColor('#EBF5EB')
LIGHT_ORANGE_BG = HexColor('#FFF5ED')
CARD_BG = HexColor('#F8FAFC')
SUCCESS_GREEN = HexColor('#166534')
WARNING_ORANGE = HexColor('#C2410C')

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to dynamically compute total page count and draw
    consistent, professional headers and footers across all checkpoints.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        width, height = letter

        # Running Top Accent Bar
        self.setFillColor(PRIMARY_GREEN)
        self.rect(36, height - 20, width - 72, 3, fill=1, stroke=0)
        self.setFillColor(ACCENT_ORANGE)
        self.rect(36, height - 20, 90, 3, fill=1, stroke=0)

        # Header Text (Skip on cover if desired, but we show subtle header)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(PRIMARY_GREEN)
            self.drawString(36, height - 32, "FACULTY CONNECT (P09) • INT335 DESIGN THINKING")
            self.setFont("Helvetica", 8)
            self.setFillColor(MUTED_TEXT)
            self.drawRightString(width - 36, height - 32, "LOVELY PROFESSIONAL UNIVERSITY (LPU)")

            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(36, height - 36, width - 36, height - 36)

        # Running Bottom Accent Bar & Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(36, 40, width - 36, 40)

        self.setFont("Helvetica", 7.5)
        self.setFillColor(MUTED_TEXT)
        self.drawString(36, 28, "Team: Aryan Singh (12516621) | Kaya H. Reddy (12516680) | Aditya Tiwari (12516873) | Susmit Choudhury (12517025)")

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(width - 36, 28, page_str)

        self.restoreState()


def get_dt_styles():
    """Generates a comprehensive paragraph style hierarchy."""
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=PRIMARY_GREEN,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=ACCENT_ORANGE,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=16,
        leading=20,
        textColor=PRIMARY_GREEN,
        spaceBefore=12,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=DARK_TEXT,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )

    h3_style = ParagraphStyle(
        'H3',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=PRIMARY_GREEN,
        spaceBefore=6,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=SLATE_TEXT,
        spaceAfter=6
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=14,
        firstLineIndent=-10,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=body_style,
        fontSize=8.5,
        leading=12,
        textColor=PRIMARY_GREEN
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=HexColor('#FFFFFF'),
        alignment=0
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=SLATE_TEXT
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=table_cell_style,
        fontName='Helvetica-Bold',
        textColor=DARK_TEXT
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=PRIMARY_GREEN,
        alignment=1
    )

    return {
        'title': title_style,
        'subtitle': subtitle_style,
        'h1': h1_style,
        'h2': h2_style,
        'h3': h3_style,
        'body': body_style,
        'body_bold': body_bold,
        'bullet': bullet_style,
        'callout': callout_style,
        'th': table_header_style,
        'td': table_cell_style,
        'td_bold': table_cell_bold,
        'badge': badge_style
    }


def make_callout_box(content_flowables, border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG, width=540):
    """Wraps flowables in a styled rounded card."""
    tbl_data = [[content_flowables]]
    tbl = Table(tbl_data, colWidths=[width])
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_color),
        ('BOX', (0,0), (-1,-1), 1.2, border_color),
        ('ROUNDEDCORNERS', [4, 4, 4, 4]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    return tbl


def make_cover_header(checkpoint_code, checkpoint_title, subtitle, styles):
    """Generates standard top section with official metadata box."""
    elements = []
    elements.append(Paragraph(f"<b>{checkpoint_code}</b>: {checkpoint_title}", styles['title']))
    elements.append(Paragraph(subtitle, styles['subtitle']))

    meta_data = [
        [
            Paragraph("<b>Course:</b> INT335 Design Thinking", styles['td']),
            Paragraph("<b>Project ID:</b> P09 — Faculty Connect", styles['td']),
            Paragraph("<b>Session:</b> 2026–2027", styles['td'])
        ],
        [
            Paragraph("<b>Domain:</b> Academic Communication", styles['td']),
            Paragraph("<b>Institution:</b> Lovely Professional Univ.", styles['td']),
            Paragraph("<b>Evaluation:</b> Official Submission", styles['td'])
        ]
    ]
    meta_tbl = Table(meta_data, colWidths=[180, 180, 180])
    meta_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_CREAM),
        ('BOX', (0,0), (-1,-1), 1, PRIMARY_GREEN),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    elements.append(meta_tbl)
    elements.append(Spacer(1, 12))
    return elements
