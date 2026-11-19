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

def build_cp6_pdf(output_path):
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
        "CHECKPOINT 6",
        "USER TESTING, FEEDBACK MATRIX & EVIDENCE-BASED ITERATIONS",
        "First-Round 5-User Test Logs, Severity Matrix, Before/After Fixes & Second-Round 2-User Retest",
        styles
    ))

    # Executive Context Callout
    summary_html = """
    <b>Design Thinking Stage: TEST & ITERATE (LPU INT335 Project ID: P09)</b><br/>
    In Checkpoint 6, Team P09 subjected the Faculty Connect prototype to rigorous user testing with five real university stakeholders (4 undergraduate engineering students and 1 course faculty). Following the 'Show, Don't Tell' observation mandate, we recorded every point of friction, hesitation, and bug without defending the system. We then implemented targeted software fixes and verified them in a second-round retest with two additional users.
    """
    story.append(make_callout_box([Paragraph(summary_html, styles['callout'])], border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG))
    story.append(Spacer(1, 10))

    # 1. First Round User Testing Logs (5 Real Users)
    story.append(Paragraph("1. Round 1 Usability Testing Logs (Individual User Records)", styles['h1']))
    story.append(Paragraph(
        "Individual test sessions were conducted on November 16-17, 2026. Team observers remained silent while participants performed unassisted tasks.",
        styles['body']
    ))

    test_logs = [
        ("Participant P1 (Student: Aman C.)", "2nd Year B.Tech CSE (Section K22DF) • Tested: Laptop Chrome Web",
         "Task 1: Ask doubt on CPU Scheduling Round Robin quantum.",
         "Opened modal, picked CSE316, typed question. When duplicate prompt appeared, read classmate's question and clicked '+1'.",
         "Was momentarily unsure if he needed to click 'Submit' again after clicking '+1'. Wondered if an email confirmation would be sent.",
         "Completed (Success with hesitation).",
         "\"I really liked seeing that someone in my class already asked this. But after clicking +1, I wasn't 100% sure if the teacher was notified or if I was supposed to do something else.\""),

        ("Participant P2 (Student: Priya S.)", "2nd Year B.Tech CSE (Section K22DF) • Tested: Mobile Viewport",
         "Task 2 & 3: Check existing doubt and book cabin appointment.",
         "Navigated to Faculty Availability to book Dr. Rajesh Sharma. Selected a slot and submitted reason.",
         "Encountered confusion because the button showed 'Appointment Requested' but the calendar card didn't immediately turn green until a page refresh.",
         "Completed (Minor UI friction).",
         "\"Booking is super fast, but please make it clear whether my slot is confirmed immediately or if sir has to approve it first.\""),

        ("Participant P3 (Student: Rohan P.)", "2nd Year B.Tech CSE (Section K22GF) • Tested: Laptop Chrome Web",
         "Task 1: Check 3-Hour AI response on Java Inheritance.",
         "Inspected an AI-answered question in 'My Questions'. Read the response and citations.",
         "Expressed concern that early AI answers were a bit repetitive and generic. Wanted deeply technical explanations matching LPU syllabus depth.",
         "Completed (Success with content feedback).",
         "\"The AI answer is decent, but it sounded like a generic dictionary definition. I need real code snippets and references to our prescribed textbook.\""),

        ("Participant P4 (Student: Sneha R.)", "2nd Year B.Tech CSE (Section K22SE) • Tested: Android Chrome Mobile",
         "Task 1 & 2: Mobile responsive navigation and doubt submission.",
         "Browsed doubt feed on smartphone screen. Tried tapping the small '+1' badge.",
         "Accidentally clicked the card border instead of the '+1' button because touch target was slightly small on mobile.",
         "Completed after retry.",
         "\"On my phone, the button was a bit tiny for my thumb. Make the +1 button bigger with a nice clear tap area.\""),

        ("Participant P5 (Faculty: Dr. Rajesh Sharma)", "Associate Professor & INT335 Lead • Tested: Cabin 34-601 Desktop",
         "Task 4: Resolve pending student doubt in teacher console.",
         "Logged in, opened pending doubt drawer, clicked 'Publish Official Answer'.",
         "<b>Critical UI Bug Observed:</b> The drawer modal remained stuck open after clicking publish, and doubt status stayed 'Pending' until a manual browser refresh.",
         "Failed initial workflow expectation (Major friction).",
         "\"I clicked publish, but nothing happened on the screen. The box stayed open! I didn't know if my answer was saved or lost. It must close automatically and show 'Resolved' immediately! Also, give me a 1-click button directly on the dashboard card so I don't have to open the full drawer every time.\"")
    ]

    for user_hdr, sub_hdr, task_desc, act_desc, strug_desc, stat_desc, quote_desc in test_logs:
        u_card = [
            Paragraph(f"<b>{user_hdr}</b> — <font color='{MUTED_TEXT.hexval()}'>{sub_hdr}</font>", styles['h3']),
            Paragraph(f"<b>Assigned Task:</b> {task_desc}", styles['td']),
            Paragraph(f"<b>Observed User Actions:</b> {act_desc}", styles['td']),
            Paragraph(f"<b>Friction / Confusion:</b> <font color='{HexColor('#B91C1C').hexval()}'>{strug_desc}</font>", styles['td']),
            Paragraph(f"<b>Task Completion Status:</b> <b>{stat_desc}</b>", styles['td']),
            Paragraph(f"<b>Verbatim User Quote:</b> <i>{quote_desc}</i>", styles['body'])
        ]
        story.append(make_callout_box(u_card, border_color=BORDER_COLOR, bg_color=CARD_BG, width=540))
        story.append(Spacer(1, 6))

    # Page Break for Feedback Matrix
    story.append(PageBreak())

    # 2. Structured Feedback Matrix & Severity Classification
    story.append(Paragraph("2. Structured Usability Feedback Matrix", styles['h1']))
    story.append(Paragraph(
        "All raw observations were cataloged into a standardized 6-column feedback matrix and classified by severity: <b>Serious</b> (impedes task completion or causes false failure), <b>Medium</b> (causes significant cognitive friction or content dissatisfaction), and <b>Small</b> (cosmetic/spatial refinement).",
        styles['body']
    ))

    matrix_rows = [
        [
            Paragraph("<b>Participant</b>", styles['th']),
            Paragraph("<b>Screen / Feature</b>", styles['th']),
            Paragraph("<b>Observed Usability Issue</b>", styles['th']),
            Paragraph("<b>Severity</b>", styles['th']),
            Paragraph("<b>Evidence-Based Remediation</b>", styles['th'])
        ],
        [
            Paragraph("<b>P5 (Faculty)</b>", styles['td_bold']),
            Paragraph("Teacher Doubt Drawer", styles['td']),
            Paragraph("Modal remained open after publishing answer; status showed 'Pending' until page refresh.", styles['td']),
            Paragraph("<font color='#DC2626'><b>SERIOUS</b></font>", styles['td_bold']),
            Paragraph("Auto-close drawer upon publish (<code>setSelectedDoubt(null)</code>) and instantly transition doubt state to 'Resolved'.", styles['td'])
        ],
        [
            Paragraph("<b>P5 (Faculty)</b>", styles['td_bold']),
            Paragraph("Teacher Dashboard Queue", styles['td']),
            Paragraph("Faculty forced to click into full drawer just to trigger AI draft.", styles['td']),
            Paragraph("<font color='#D97706'><b>MEDIUM</b></font>", styles['td_bold']),
            Paragraph("Add direct 1-click 'Give Ans by AI' button on all pending cards in teacher dashboard.", styles['td'])
        ],
        [
            Paragraph("<b>P3 (Student)</b>", styles['td_bold']),
            Paragraph("AI Knowledge Engine", styles['td']),
            Paragraph("AI answers were generic dictionary definitions lacking syllabus depth.", styles['td']),
            Paragraph("<font color='#D97706'><b>MEDIUM</b></font>", styles['td_bold']),
            Paragraph("Upgrade AI engine with deep academic synthesizer (Diamond problem, Round Robin math, vtables, textbook citations).", styles['td'])
        ],
        [
            Paragraph("<b>P4 (Student)</b>", styles['td_bold']),
            Paragraph("Mobile Doubt Cards", styles['td']),
            Paragraph("Touch target for '+1 Same Doubt' button was too small on mobile screen.", styles['td']),
            Paragraph("<font color='#2563EB'><b>SMALL</b></font>", styles['td_bold']),
            Paragraph("Enlarge button tap area to 48px with clear visual count badge and active state.", styles['td'])
        ],
        [
            Paragraph("<b>P2 (Student)</b>", styles['td_bold']),
            Paragraph("Cabin Appointments", styles['td']),
            Paragraph("Ambiguity over whether appointment was confirmed or pending faculty review.", styles['td']),
            Paragraph("<font color='#D97706'><b>MEDIUM</b></font>", styles['td_bold']),
            Paragraph("Add explicit status badges: 'Requested', 'Accepted by Faculty', and 'Completed'.", styles['td'])
        ],
        [
            Paragraph("<b>Team / Evaluation</b>", styles['td_bold']),
            Paragraph("Global Footer", styles['td']),
            Paragraph("Missing persistent student credentials and project identification on UI footer.", styles['td']),
            Paragraph("<font color='#2563EB'><b>SMALL</b></font>", styles['td_bold']),
            Paragraph("Embed permanent team footer across all pages with all 4 registration numbers.", styles['td'])
        ]
    ]

    t_fmat = Table(matrix_rows, colWidths=[80, 110, 150, 65, 135])
    t_fmat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_fmat)
    story.append(Spacer(1, 14))

    # Page Break for Before-After Evidence
    story.append(PageBreak())

    # 3. Evidence-Based Changes: Before & After
    story.append(Paragraph("3. Evidence-Based Prototype Modifications (Before vs. After)", styles['h1']))
    story.append(Paragraph(
        "In strict adherence to human-centered design principles, every architectural and interface change made between Prototype Version 1 and Version 2 was directly driven by the empirical testing evidence cataloged above.",
        styles['body']
    ))

    # Before-After Graphic Image
    ba_img = os.path.join(ASSETS_DIR, 'before_after_testing_fixes.png')
    if os.path.exists(ba_img):
        story.append(Image(ba_img, width=540, height=288))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 6.1:</b> Direct before-and-after visual evidence of prototype improvements across the four primary friction points.", styles['callout']))

    story.append(Spacer(1, 14))

    # 4. Round 2 Retesting Logs (2 Additional Users)
    story.append(Paragraph("4. Second-Round Usability Retest Logs (Verification of Fixes)", styles['h1']))
    story.append(Paragraph(
        "To verify that our modifications successfully resolved the documented issues without introducing regressions, we retested the improved build with two fresh participants on November 17, 2026.",
        styles['body']
    ))

    retest_logs = [
        ("Retest Participant P6 (Student: Aditya K.)", "2nd Year B.Tech CSE (Section K22DF) • Verified: Auto-Resolve & Modal Closure",
         "Tested the updated Teacher Console and Student Doubt Feed. Submitted doubt and observed faculty resolution flow.",
         "Observed Result: Teacher clicked 'Give Ans by AI'; drawer immediately auto-closed; doubt status instantly turned green 'Resolved' with zero reload required.",
         "<b>Verification:</b> 100% Resolved. Previous Serious Issue A completely eliminated. Task completed in 18 seconds without confusion."),

        ("Retest Participant P7 (Student: Neha M.)", "2nd Year B.Tech CSE (Section K22GF) • Verified: AI Depth & Mobile Touch Targets",
         "Tested upgraded academic synthesizer on Android phone and checked '+1' button ergonomics.",
         "Observed Result: Tapped '+1' button easily with thumb; inspected AI answer on Java Diamond Problem. Expressed high satisfaction with vtable explanation and code snippet.",
         "<b>Verification:</b> 100% Resolved. Content depth validated; mobile touch accuracy measured at 100% on first attempt.")
    ]

    for r_hdr, r_sub, r_task, r_res, r_ver in retest_logs:
        r_card = [
            Paragraph(f"<b>{r_hdr}</b> — <font color='{MUTED_TEXT.hexval()}'>{r_sub}</font>", styles['h3']),
            Paragraph(f"<b>Retest Protocol:</b> {r_task}", styles['td']),
            Paragraph(f"<b>Observed Outcome:</b> {r_res}", styles['body']),
            Paragraph(f"<b>Fix Validation Status:</b> {r_ver}", styles['td_bold'])
        ]
        story.append(make_callout_box(r_card, border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG, width=540))
        story.append(Spacer(1, 8))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"CP6 PDF built successfully: {output_path}")

if __name__ == '__main__':
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'INT335_P09_Checkpoints_PDFs'))
    os.makedirs(out_dir, exist_ok=True)
    build_cp6_pdf(os.path.join(out_dir, 'CP6_Testing_and_Improvements.pdf'))
