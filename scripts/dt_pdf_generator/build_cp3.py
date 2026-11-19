import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether, HRFlowable
from reportlab.lib.colors import HexColor
from styles_and_utils import (
    NumberedCanvas, get_dt_styles, make_callout_box, make_cover_header,
    PRIMARY_GREEN, ACCENT_ORANGE, BG_CREAM, DARK_TEXT, SLATE_TEXT, MUTED_TEXT,
    BORDER_COLOR, LIGHT_GREEN_BG, LIGHT_ORANGE_BG, CARD_BG
)

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))

def build_cp3_pdf(output_path):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=46,
        bottomMargin=46
    )

    styles = get_dt_styles()
    story = []

    # Cover / Header
    story.extend(make_cover_header(
        "CHECKPOINT 3",
        "PROBLEM DEFINITION & USER SYNTHESIS",
        "Thematic Grouping, User Personas, As-Is Journey Maps, POV Statements & Main HMW Question",
        styles
    ))

    # Executive Context Callout
    summary_html = """
    <b>Design Thinking Stage: DEFINE (LPU INT335 Project ID: P09)</b><br/>
    In Checkpoint 3, Team P09 converts the empirical qualitative and observational findings gathered during the Empathize stage into an authoritative, actionable problem framework. In strict accordance with Design Thinking principles, this document focuses entirely on defining the human and systemic problem rather than prematurely prescribing a digital solution.
    """
    story.append(make_callout_box([Paragraph(summary_html, styles['callout'])], border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG))
    story.append(Spacer(1, 10))

    # 1. Organized Research Findings by Theme
    story.append(Paragraph("1. Thematic Organization of User Research Findings", styles['h1']))
    story.append(Paragraph(
        "Analysis of our 8 in-depth interviews and 6 field observation sessions revealed seven recurring friction themes that degrade the academic experience of students and faculty outside formal lecture hours.",
        styles['body']
    ))

    themes_data = [
        [
            Paragraph("<b>Core Problem Theme</b>", styles['th']),
            Paragraph("<b>Underlying Human Breakdown</b>", styles['th']),
            Paragraph("<b>Empirical Evidence from Fieldwork</b>", styles['th'])
        ],
        [
            Paragraph("<b>1. Faculty Availability Unpredictability</b>", styles['td_bold']),
            Paragraph("Students cannot determine whether a professor is physically present, in a meeting, or invigilating a laboratory examination.", styles['td']),
            Paragraph("68% of student corridor trips in Block 34 & 38 ended at locked doors with outdated paper schedule notices.", styles['td'])
        ],
        [
            Paragraph("<b>2. Excessive Waiting & Transit Friction</b>", styles['td_bold']),
            Paragraph("Students expend 30-45 minutes trekking across campus and waiting on corridor stairs during short breaks between lectures.", styles['td']),
            Paragraph("Interviewee Aman C. reported wasting 40 minutes sitting outside Cabin 402 only to miss preparation for his next class.", styles['td'])
        ],
        [
            Paragraph("<b>3. Repetitive Academic Inquiries</b>", styles['td_bold']),
            Paragraph("Faculty members spend hours answering the exact same conceptual question asked separately by individual students across sections.", styles['td']),
            Paragraph("Dr. Rajesh Sharma recorded 28 nearly identical WhatsApp messages regarding SCAMPER steps within a 48-hour deadline.", styles['td'])
        ],
        [
            Paragraph("<b>4. Chaotic, Unstructured Channels</b>", styles['td_bold']),
            Paragraph("Academic questions compete with informal chatter, memes, and club announcements on WhatsApp class groups.", styles['td']),
            Paragraph("Student Rohan P. highlighted that legitimate doubts get buried beneath 150+ messages in less than 30 minutes.", styles['td'])
        ],
        [
            Paragraph("<b>5. Absence of Bookable Office Hours</b>", styles['td_bold']),
            Paragraph("No structured mechanism exists to request or confirm a 10-minute 1-on-1 cabin consultation in advance.", styles['td']),
            Paragraph("Dr. Harpreet Kaur reported her research afternoons are constantly disrupted by unscheduled student knocks.", styles['td'])
        ],
        [
            Paragraph("<b>6. Social Anxiety in Inquiry</b>", styles['td_bold']),
            Paragraph("Students experience cognitive intimidation when knocking on closed doors or asking questions publicly in class.", styles['td']),
            Paragraph("Student Priya S. abandoned an important OOP question after a professor noted another classmate had just asked it.", styles['td'])
        ],
        [
            Paragraph("<b>7. Faculty Cognitive Burnout</b>", styles['td_bold']),
            Paragraph("Constant asynchronous messaging erodes work-life boundaries, causing faculty fatigue and guilt over unread queries.", styles['td']),
            Paragraph("Faculty work weeks showed an average of 9.5 uncompensated hours spent answering late-night messages.", styles['td'])
        ]
    ]
    t_themes = Table(themes_data, colWidths=[130, 205, 205])
    t_themes.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_themes)
    story.append(Spacer(1, 14))

    # Page Break for Personas
    story.append(PageBreak())

    # 2. Research-Based User Personas
    story.append(Paragraph("2. Research-Based User Personas", styles['h1']))
    story.append(Paragraph(
        "To ground all subsequent design decisions in concrete human behaviors rather than abstract stereotypes, we synthesized two detailed personas directly from our qualitative interview findings.",
        styles['body']
    ))

    # Persona 1: Student
    p_student_img = os.path.join(ASSETS_DIR, 'persona_student_rohan.png')
    if os.path.exists(p_student_img):
        story.append(Image(p_student_img, width=540, height=300))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 3.1:</b> Student Archetype Persona — Rohan Patel (B.Tech CSE 2nd Year, Section K22GF).", styles['callout']))

    story.append(Spacer(1, 14))

    # Persona 2: Faculty
    p_faculty_img = os.path.join(ASSETS_DIR, 'persona_faculty_dr_sharma.png')
    if os.path.exists(p_faculty_img):
        story.append(Image(p_faculty_img, width=540, height=300))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 3.2:</b> Faculty Archetype Persona — Dr. Rajesh Sharma (Associate Professor & INT335 Lead, Cabin 34-601).", styles['callout']))

    story.append(Spacer(1, 14))

    # Page Break for Journey Maps
    story.append(PageBreak())

    # 3. Current State User Journey Maps
    story.append(Paragraph("3. Current State User Journey Maps (As-Is Experience)", styles['h1']))
    story.append(Paragraph(
        "Journey mapping illustrates the operational hurdles and emotional valleys experienced by both actors under the current ad-hoc communication paradigm.",
        styles['body']
    ))

    # Student Journey Map Image
    j_student_img = os.path.join(ASSETS_DIR, 'journey_map_student.png')
    if os.path.exists(j_student_img):
        story.append(Image(j_student_img, width=540, height=288))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 3.3:</b> Current Student Journey Map illustrating the steep drop in emotional valence during cabin corridor transit and waiting.", styles['callout']))

    story.append(Spacer(1, 12))

    # Faculty Journey Map Image
    j_faculty_img = os.path.join(ASSETS_DIR, 'journey_map_faculty.png')
    if os.path.exists(j_faculty_img):
        story.append(Image(j_faculty_img, width=540, height=288))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 3.4:</b> Current Faculty Journey Map showing cognitive fragmentation from repetitive WhatsApp doubts and unscheduled drop-ins.", styles['callout']))

    story.append(Spacer(1, 14))

    # Page Break for POV and HMW
    story.append(PageBreak())

    # 4. Point of View (POV) Statements
    story.append(Paragraph("4. Point of View (POV) Statements", styles['h1']))
    story.append(Paragraph(
        "Following Stanford d.school guidelines, each Point of View statement synthesizes a specific user group, their critical human need, and an unexpected qualitative insight uncovered during field research. Notice that each statement strictly articulates the problem space without prescribing technology solutions.",
        styles['body']
    ))

    povs = [
        ("Student POV Statement",
         "A conscientious 2nd-year engineering student preparing for continuous assessments",
         "A predictable, timely, and non-intimidating way to verify complex academic concepts outside scheduled lecture hours",
         "They are frequently paralyzed not by difficult subject matter, but by the social anxiety of knocking on cabin doors and the uncertainty of faculty presence, causing them to abandon doubts rather than risk embarrassment.",
         PRIMARY_GREEN, LIGHT_GREEN_BG),

        ("Faculty POV Statement",
         "A committed engineering professor teaching multiple sections while managing continuous evaluations and academic research",
         "A structured, boundary-respecting method to address genuine student conceptual difficulties without being overwhelmed by repetitive identical questions",
         "Every unorganized notification and unscheduled cabin knock shatters deep intellectual focus, transforming their evening personal hours into an unpaid, chaotic helpdesk.",
         ACCENT_ORANGE, LIGHT_ORANGE_BG)
    ]

    for title, user, need, insight, b_color, bg_color in povs:
        p_card = [
            Paragraph(f"<b>{title}</b>", styles['h3']),
            Paragraph(f"<b>User:</b> {user}", styles['body']),
            Paragraph(f"<b>Needs:</b> {need}", styles['body']),
            Paragraph(f"<b>Because (Insight):</b> {insight}", styles['body'])
        ]
        story.append(make_callout_box(p_card, border_color=b_color, bg_color=bg_color, width=540))
        story.append(Spacer(1, 10))

    # 5. How Might We (HMW) Questions
    story.append(Paragraph("5. How Might We (HMW) Exploration & Main Selection", styles['h1']))
    story.append(Paragraph(
        "Translating our POV insights into generative springboards for ideation, Team P09 formulated exploratory How Might We questions across multiple dimensions.",
        styles['body']
    ))

    hmws = [
        ("HMW 1 (Availability)", "How might we make faculty consultation hours and physical presence transparently visible to students in real-time?"),
        ("HMW 2 (Efficiency)", "How might we prevent students from wasting 30+ minutes in cabin transit only to find professors engaged in other academic duties?"),
        ("HMW 3 (Deduplication)", "How might we enable students with identical academic questions to pool their doubts together rather than asking faculty individually?"),
        ("HMW 4 (Workload)", "How might we protect faculty personal boundaries and research focus while ensuring sincere student questions receive authoritative answers?"),
        ("HMW 5 (Psychological)", "How might we eliminate the social hesitation and anxiety that prevents introverted students from seeking help outside class?"),
        ("HMW 6 (Asynchronous)", "How might we provide students with immediate, reliable academic guidance when faculty are legitimately unavailable for several hours?")
    ]

    for code, text in hmws:
        story.append(Paragraph(f"• <b>{code}:</b> {text}", styles['bullet']))

    story.append(Spacer(1, 10))

    # Selected Main HMW
    selected_hmw_html = """
    <b>SELECTED MAIN HOW MIGHT WE (HMW) QUESTION:</b><br/>
    <i>\"How might we make academic consultation and doubt resolution outside lectures predictable, timely, and organized for students without increasing faculty workload through repeated queries?\"</i><br/><br/>
    <b>Selection Justification & Alignment with User Needs:</b><br/>
    1. <b>Dual-Stakeholder Harmony:</b> It balances student demand for timely resolution against faculty capacity and cognitive bandwidth.<br/>
    2. <b>Sufficient Breadth:</b> It does not mandate a software app; solutions could range from physical token kiosks to peer relays to digital aggregators.<br/>
    3. <b>Targeted Root Cause:</b> It zeroes in on the single greatest friction uncovered in research: <i>redundant, unorganized repetition</i> that exhausts faculty and delays student learning.
    """
    story.append(make_callout_box([Paragraph(selected_hmw_html, styles['body'])], border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG))
    story.append(Spacer(1, 12))

    # 6. Final Problem Definition Statement
    story.append(Paragraph("6. Final Problem Definition Statement", styles['h1']))
    def_html = """
    <b>Official Problem Statement (P09 — Faculty Connect):</b><br/>
    Undergraduate engineering students at Lovely Professional University encounter severe delays, social anxiety, and wasted transit time when attempting to resolve academic questions outside scheduled lectures, while course faculty suffer from cognitive overload and personal boundary erosion caused by dozens of unorganized, repetitive inquiries arriving across fragmented informal channels. The academic institution lacks an organized, predictable mechanism to deduplicate identical doubts, schedule consultation appointments, and ensure timely, authoritative academic assistance.
    """
    story.append(make_callout_box([Paragraph(def_html, styles['body'])], border_color=ACCENT_ORANGE, bg_color=LIGHT_ORANGE_BG))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"CP3 PDF built successfully: {output_path}")

if __name__ == '__main__':
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'INT335_P09_Checkpoints_PDFs'))
    os.makedirs(out_dir, exist_ok=True)
    build_cp3_pdf(os.path.join(out_dir, 'CP3_Problem_Definition.pdf'))
