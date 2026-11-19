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

def build_cp5_pdf(output_path):
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
        "CHECKPOINT 5",
        "PROTOTYPE READINESS & USER TESTING PROTOCOL",
        "Low-Fi Wireframes, Visual User Flows, Narrative Storyboards, Live Figma System & Neutral Test Plan",
        styles
    ))

    # Executive Context Callout
    summary_html = """
    <b>Design Thinking Stage: PROTOTYPE (LPU INT335 Project ID: P09)</b><br/>
    Checkpoint 5 prepares a testable prototype representing our selected concept and establishes an ethical, neutral test protocol. The prototype is not merely a visual artifact; it is an experimental instrument designed to test whether a complete stranger can navigate the core academic tasks—asking a doubt, detecting duplicate questions, booking office hours, and answering as faculty—without any verbal instruction from our team.
    """
    story.append(make_callout_box([Paragraph(summary_html, styles['callout'])], border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG))
    story.append(Spacer(1, 10))

    # 1. Prototyping Philosophy & What is Tested
    story.append(Paragraph("1. Prototyping Evolution & Core Hypotheses", styles['h1']))
    story.append(Paragraph(
        "In accordance with INT335 Unit IV guidelines, our project spans two distinct prototyping fidelities: an early low-fidelity paper wireframe (Version 1) designed to test conceptual navigation, and an interactive high-fidelity web/PWA application (Version 2) deployed on cloud infrastructure to test real behavioral adoption.",
        styles['body']
    ))

    proto_comp = [
        [
            Paragraph("<b>Prototype Version</b>", styles['th']),
            Paragraph("<b>Medium & Tooling</b>", styles['th']),
            Paragraph("<b>Core Usability Questions Tested</b>", styles['th']),
            Paragraph("<b>Primary Evaluation Metric</b>", styles['th'])
        ],
        [
            Paragraph("<b>Version 1 (Initial Rough Prototype)</b>", styles['td_bold']),
            Paragraph("Paper wireframe cards & clickable Balsamiq sketches", styles['td']),
            Paragraph("Do students understand the course/unit selection flow? Does the '+1 Same Doubt' metaphor make intuitive sense?", styles['td']),
            Paragraph("Cognitive clarity & concept comprehension rate", styles['td'])
        ],
        [
            Paragraph("<b>Version 2 (High-Fi Interactive Prototype)</b>", styles['td_bold']),
            Paragraph("React 19 + TypeScript + Vite + Flask PWA", styles['td']),
            Paragraph("Can faculty publish answers in < 60s? Does duplicate detection prevent new query creation? Can students book cabin slots?", styles['td']),
            Paragraph("Task completion time, error count, subjective satisfaction", styles['td'])
        ]
    ]
    t_proto = Table(proto_comp, colWidths=[130, 130, 160, 120])
    t_proto.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_proto)
    story.append(Spacer(1, 12))

    # 2. Visual User Flow Architecture
    story.append(Paragraph("2. Comprehensive System User Flow Architecture", styles['h1']))
    story.append(Paragraph(
        "The complete user flow diagram below maps the operational tracks for student inquiry and faculty resolution, matching the institutional GitHub flowchart architecture with 4 integrated modules: Student Academic Journey, 3-Hour SLA Fallback Safety Net, Faculty Multi-Method Resolution, and Cabin Consultation Booking.",
        styles['body']
    ))
    story.append(Spacer(1, 6))

    # User Flow Image (Exact match with GitHub README Mermaid)
    flow_img = os.path.join(ASSETS_DIR, 'github_mermaid_user_flow.png')
    if os.path.exists(flow_img):
        story.append(Image(flow_img, width=480, height=655))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 5.1:</b> Dual-track User Flow showing student doubt submission with duplicate detection, 3-hour SLA AI fallback, and faculty direct resolution.", styles['callout']))

    story.append(Spacer(1, 14))

    # Page Break for Storyboard
    story.append(PageBreak())

    # 3. Narrative Storyboard
    story.append(Paragraph("3. Human-Centered Narrative Storyboard", styles['h1']))
    story.append(Paragraph(
        "Grounding our software architecture in our CP2/CP3 empathy findings, the narrative storyboard contrasts the current broken experience against the transformed experience provided by Faculty Connect.",
        styles['body']
    ))

    storyboard_data = [
        [
            Paragraph("<b>Panel # & Context</b>", styles['th']),
            Paragraph("<b>As-Is Experience (Current Problem)</b>", styles['th']),
            Paragraph("<b>To-Be Experience with Faculty Connect</b>", styles['th'])
        ],
        [
            Paragraph("<b>Panel 1:<br/>Doubt Emergence</b>", styles['td_bold']),
            Paragraph("A student is studying course concepts at 8:30 PM in their room. They are completely stuck on key formula derivations ahead of continuous evaluation.", styles['td']),
            Paragraph("The student opens Faculty Connect on their phone, selects the registered course, and navigates to the relevant unit topic.", styles['td'])
        ],
        [
            Paragraph("<b>Panel 2:<br/>Doubt Submission</b>", styles['td_bold']),
            Paragraph("The student considers asking in a large unstructured chat group, but knows it will be quickly buried under unrelated messages.", styles['td']),
            Paragraph("As the student begins typing their question, the Smart Doubt Engine instantly alerts them: <i>'Similar doubt found from a classmate in your course!'</i>", styles['td'])
        ],
        [
            Paragraph("<b>Panel 3:<br/>Deduplication (+1)</b>", styles['td_bold']),
            Paragraph("The student considers walking across campus to faculty cabins tomorrow, dreading the 40-minute wait and possible locked cabin doors.", styles['td']),
            Paragraph("The student reads the classmate's existing doubt. It matches their exact confusion. They click <b>'+1 - I Have the Same Doubt'</b>. Supporter count increments.", styles['td'])
        ],
        [
            Paragraph("<b>Panel 4:<br/>Faculty Queue</b>", styles['td_bold']),
            Paragraph("A faculty member wakes up to dozens of individual messages asking the same formula question, feeling overwhelmed before morning lectures.", styles['td']),
            Paragraph("The faculty member opens the Faculty Console. A single consolidated card appears showing: <i>'Multiple Students Support This Doubt'</i>.", styles['td'])
        ],
        [
            Paragraph("<b>Panel 5:<br/>1-Click Resolution</b>", styles['td_bold']),
            Paragraph("The faculty member attempts to type individual replies, spending 45 minutes on repetitive manual messaging.", styles['td']),
            Paragraph("The faculty member reviews the context, clicks <b>'Give Ans by AI'</b> to synthesize a syllabus-grounded explanation, verifies it, and publishes. One authoritative answer resolves all supporters at once.", styles['td'])
        ],
        [
            Paragraph("<b>Panel 6:<br/>Office Hour Booking</b>", styles['td_bold']),
            Paragraph("The student still has an in-depth conceptual question requiring face-to-face guidance. They wander departmental corridors searching for availability.", styles['td']),
            Paragraph("The student opens the <b>'Faculty Availability'</b> tab, views verified consultation hours, and books a dedicated 10-minute slot with 1 click.", styles['td'])
        ]
    ]

    t_sb = Table(storyboard_data, colWidths=[100, 220, 220])
    t_sb.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_sb)
    story.append(Spacer(1, 14))

    # Page Break for Figma and Testing
    story.append(PageBreak())

    # 4. Live Figma System & Component Architecture
    story.append(Paragraph("4. Production UI Screen System & Figma Component Architecture", styles['h1']))
    story.append(Paragraph(
        "A complete, production-parity UI design system was constructed to mirror the exact components, spatial grid, typography, and color tokens of the deployed application. Below are the visual Figma screen mockups showcasing the key interactive states of the system.",
        styles['body']
    ))

    # Embed Visual Figma Mockups
    figma_mockups_img = os.path.join(ASSETS_DIR, 'figma_screen_mockups_combined.png')
    if os.path.exists(figma_mockups_img):
        story.append(Image(figma_mockups_img, width=540, height=415))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 5.2:</b> Production Figma Screen System — Frame 01: Student Doubt Modal, Frame 02: Duplicate Alert with '+1', Frame 03: Teacher Console Queue, and Frame 04: Official Answer Drawer.", styles['callout']))

    story.append(Spacer(1, 10))

    figma_meta_html = """
    <b>Official Project Design System Tokens & Deploy Parity:</b><br/>
    • <b>Primary Navigation Green:</b> <code>#15370D</code> (Navbar, primary action buttons, active tabs)<br/>
    • <b>Background Cream:</b> <code>#FCF9EA</code> (Card surface backgrounds, modal backdrops)<br/>
    • <b>Orange Accent:</b> <code>#F2842F</code> (Notification counters, duplicate warning badges, +1 highlights)<br/>
    • <b>Primary Text:</b> <code>#000000</code> (High contrast headings, crisp black typography)<br/>
    • <b>Typography Hierarchy:</b> Inter & Outfit (Web Font family, 12pt body, 16pt cards, 24pt headers)<br/>
    • <b>Live Application Reference:</b> <font color='#15370D'><b>https://faculty-connect-production.up.railway.app/</b></font>
    """
    story.append(make_callout_box([Paragraph(figma_meta_html, styles['body'])], border_color=PRIMARY_GREEN, bg_color=BG_CREAM))
    story.append(Spacer(1, 10))

    # Frames Catalog Table
    story.append(Paragraph("Figma Frames & Screen Inventory Catalog:", styles['h2']))
    frames_data = [
        [Paragraph("<b>Frame #</b>", styles['th']), Paragraph("<b>Screen Title</b>", styles['th']), Paragraph("<b>Role / Panel</b>", styles['th']), Paragraph("<b>Key Interactive Elements Tested</b>", styles['th'])],
        [Paragraph("F01", styles['td_bold']), Paragraph("Welcome & Role Selection", styles['td']), Paragraph("Universal Entry", styles['td']), Paragraph("1-click student section picker, hashed faculty login credentials.", styles['td'])],
        [Paragraph("F02", styles['td_bold']), Paragraph("Student Academic Dashboard", styles['td']), Paragraph("Student Portal", styles['td']), Paragraph("Course cards, pending doubt trackers, notifications counter.", styles['td'])],
        [Paragraph("F03", styles['td_bold']), Paragraph("Ask a Doubt Modal Flow", styles['td']), Paragraph("Student Portal", styles['td']), Paragraph("Dynamic Course -> Unit -> Topic drilldown and date picker.", styles['td'])],
        [Paragraph("F04", styles['td_bold']), Paragraph("Semantic Duplicate Warning", styles['td']), Paragraph("Student Portal", styles['td']), Paragraph("Classmate question comparison, '+1 I Have the Same Doubt' button.", styles['td'])],
        [Paragraph("F05", styles['td_bold']), Paragraph("Doubt Detail & Answer View", styles['td']), Paragraph("Student Portal", styles['td']), Paragraph("Official faculty badge, 3-hour AI preliminary notice, textbook citations.", styles['td'])],
        [Paragraph("F06", styles['td_bold']), Paragraph("Faculty Availability Calendar", styles['td']), Paragraph("Student Portal", styles['td']), Paragraph("Cabin block badges, bookable time slots, consultation reason input.", styles['td'])],
        [Paragraph("F07", styles['td_bold']), Paragraph("Faculty Console Dashboard", styles['td']), Paragraph("Teacher Portal", styles['td']), Paragraph("Urgent pending queue, '+1' impact counters, 3-hour SLA clock.", styles['td'])],
        [Paragraph("F08", styles['td_bold']), Paragraph("Faculty Answer Drawer", styles['td']), Paragraph("Teacher Portal", styles['td']), Paragraph("1-click 'Give Ans by AI', manual answer Markdown editor, instant resolution.", styles['td'])],
        [Paragraph("F09", styles['td_bold']), Paragraph("Appointments Management", styles['td']), Paragraph("Teacher Portal", styles['td']), Paragraph("Accept/Decline student cabin slot requests, add preparation notes.", styles['td'])],
        [Paragraph("F10", styles['td_bold']), Paragraph("Section Confusion Analytics", styles['td']), Paragraph("Teacher Portal", styles['td']), Paragraph("Empirical confusion heatmaps by course/unit, 1-click CSV export.", styles['td'])]
    ]
    t_frames = Table(frames_data, colWidths=[35, 145, 100, 260])
    t_frames.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_frames)
    story.append(Spacer(1, 14))

    # Page Break for Test Plan
    story.append(PageBreak())

    # 5. Neutral Prototype Usability Test Plan
    story.append(Paragraph("5. Neutral Usability Test Plan & Testing Protocol", styles['h1']))
    story.append(Paragraph(
        "To satisfy the core Design Thinking mandate ('Show, Don't Tell'), the testing protocol enforces strict neutrality: team observers remain silent, giving no verbal assistance or hints while the participant interacts with the interface.",
        styles['body']
    ))

    test_plan_html = """
    <b>Usability Testing Protocol & Constraints:</b><br/>
    • <b>Testing Objective:</b> Evaluate task completion speed, cognitive friction points, and user comprehension of duplicate detection and cabin appointment features.<br/>
    • <b>Participant Cohort:</b> 5 Users in Round 1 (4 Students + 1 Faculty Member).<br/>
    • <b>Observation Methodology:</b> Think-Aloud Protocol. Observers remain silent and record hesitations, erroneous clicks, and verbal comments.<br/>
    • <b>Success Threshold:</b> 80% unassisted task completion across all core flows without team intervention.
    """
    story.append(make_callout_box([Paragraph(test_plan_html, styles['body'])], border_color=ACCENT_ORANGE, bg_color=LIGHT_ORANGE_BG))
    story.append(Spacer(1, 10))

    # 4 Neutral Test Tasks Table
    story.append(Paragraph("Neutral Test Scenarios (Given to Participants):", styles['h2']))
    tasks_data = [
        [Paragraph("<b>Task #</b>", styles['th']), Paragraph("<b>Scenario Prompt Given to User</b>", styles['th']), Paragraph("<b>Expected User Action</b>", styles['th']), Paragraph("<b>Pass Criteria</b>", styles['th'])],
        [
            Paragraph("<b>Task 1</b>", styles['td_bold']),
            Paragraph("You missed the explanation on CPU Scheduling Round Robin quantum in CSE316. Submit this doubt to your faculty.", styles['td']),
            Paragraph("Enters student portal, selects CSE316 -> Unit II -> CPU Scheduling, types query.", styles['td']),
            Paragraph("Submits or encounters duplicate detection without asking for help.", styles['td'])
        ],
        [
            Paragraph("<b>Task 2</b>", styles['td_bold']),
            Paragraph("The system alerts you that a classmate already asked a very similar question. Decide what to do next.", styles['td']),
            Paragraph("Inspects the displayed classmate doubt and clicks '+1 - I Have the Same Doubt'.", styles['td']),
            Paragraph("Correctly understands that +1 links them to answer notifications.", styles['td'])
        ],
        [
            Paragraph("<b>Task 3</b>", styles['td_bold']),
            Paragraph("You need a 10-minute in-person meeting with your course faculty to show your wireframe sketches. Book a consultation.", styles['td']),
            Paragraph("Navigates to Faculty Availability, locates course faculty member, picks upcoming slot, inputs reason.", styles['td']),
            Paragraph("Successfully receives 'Appointment Requested' confirmation.", styles['td'])
        ],
        [
            Paragraph("<b>Task 4 (Faculty)</b>", styles['td_bold']),
            Paragraph("You are the course faculty member. Open your dashboard and resolve a pending student doubt using the most efficient method available.", styles['td']),
            Paragraph("Logs in as faculty, opens pending doubt, uses 'Give Ans by AI' or types answer, clicks publish.", styles['td']),
            Paragraph("Doubt moves to Resolved state in under 60 seconds.", styles['td'])
        ]
    ]

    t_tasks = Table(tasks_data, colWidths=[50, 190, 170, 130])
    t_tasks.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_tasks)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"CP5 PDF built successfully: {output_path}")

if __name__ == '__main__':
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'INT335_P09_Checkpoints_PDFs'))
    os.makedirs(out_dir, exist_ok=True)
    build_cp5_pdf(os.path.join(out_dir, 'CP5_Prototype_Readiness.pdf'))
