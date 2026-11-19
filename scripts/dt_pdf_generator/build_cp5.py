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
        "The user flow diagrams below illustrate the main operational tracks for student inquiry and faculty resolution, explicitly detailing decision branches, duplicate detection pathways, and error/fallback states.",
        styles['body']
    ))

    # User Flow Image
    flow_img = os.path.join(ASSETS_DIR, 'user_flow_step_by_step_academic.png')
    if os.path.exists(flow_img):
        story.append(Image(flow_img, width=540, height=350))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 5.1:</b> Dual-track User Flow showing student doubt submission with duplicate detection and faculty 1-click resolution.", styles['callout']))

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
            Paragraph("Rohan is studying Operating Systems at 8:30 PM in his hostel room. He is completely stuck on the difference between Paging and Segmentation.", styles['td']),
            Paragraph("Rohan opens Faculty Connect on his phone, taps CSE316, and selects Unit V (Memory Management).", styles['td'])
        ],
        [
            Paragraph("<b>Panel 2:<br/>Doubt Submission</b>", styles['td_bold']),
            Paragraph("Rohan considers asking in the 65-student WhatsApp group, but knows it will be buried under 100 jokes and event flyers.", styles['td']),
            Paragraph("As Rohan begins typing his question, the Smart Doubt Engine instantly alerts him: <i>'Similar doubt found from Priya Sharma in your section!'</i>", styles['td'])
        ],
        [
            Paragraph("<b>Panel 3:<br/>Deduplication (+1)</b>", styles['td_bold']),
            Paragraph("Rohan considers walking to Block 38 tomorrow morning, dreading the 40-minute corridor wait and possible locked cabin doors.", styles['td']),
            Paragraph("Rohan reads Priya's existing doubt. It matches his exact confusion. He clicks <b>'+1 - I Have the Same Doubt'</b>. Supporter count jumps to 4.", styles['td'])
        ],
        [
            Paragraph("<b>Panel 4:<br/>Faculty Queue</b>", styles['td_bold']),
            Paragraph("Dr. Harpreet Kaur wakes up to 18 individual WhatsApp messages asking about paging formulas, feeling exhausted before her morning lecture.", styles['td']),
            Paragraph("Dr. Kaur opens her Faculty Console. A single high-priority card appears showing: <i>'4 Students Support This Doubt (Section K22GF)'</i>.", styles['td'])
        ],
        [
            Paragraph("<b>Panel 5:<br/>1-Click Resolution</b>", styles['td_bold']),
            Paragraph("Dr. Kaur tries to copy-paste replies on WhatsApp, spending 45 minutes typing on her phone.", styles['td']),
            Paragraph("Dr. Kaur reviews the syllabus context, clicks <b>'Give Ans by AI'</b> to generate a draft with textbook citations, reviews it, and publishes. One answer clears 4 students at once.", styles['td'])
        ],
        [
            Paragraph("<b>Panel 6:<br/>Office Hour Booking</b>", styles['td_bold']),
            Paragraph("Rohan still has an edge-case question. He wanders Block 38 corridors looking for her nameplate.", styles['td']),
            Paragraph("Rohan opens the <b>'Faculty Availability'</b> tab, sees Dr. Kaur's open Thursday 2:00 PM slot in Cabin 402, and books a 10-minute consultation with 1 click.", styles['td'])
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
    story.append(Paragraph("4. Live Figma Project Architecture & Design System", styles['h1']))
    story.append(Paragraph(
        "A complete, editable Figma design project was constructed to mirror the exact UI components, spatial grid, typography, and color tokens of the deployed application. This ensures strict continuity between design thinking specifications and the production build.",
        styles['body']
    ))

    figma_meta_html = """
    <b>Official Project Design System Tokens:</b><br/>
    • <b>Primary Navigation Green:</b> <code>#15370D</code> (Navbar, primary action buttons, active tabs)<br/>
    • <b>Background Cream:</b> <code>#FCF9EA</code> (Card surface backgrounds, modal backdrops)<br/>
    • <b>Orange Accent:</b> <code>#F2842F</code> (Notification counters, duplicate warning badges, +1 highlights)<br/>
    • <b>Primary Text:</b> <code>#000000</code> / <code>#1E293B</code> (High contrast headings, crisp typography)<br/>
    • <b>Typography Hierarchy:</b> Inter & Outfit (Web Font family, 12pt body, 16pt cards, 24pt headers)<br/>
    • <b>Public Figma Workspace URL:</b> <font color='#15370D'><b>https://www.figma.com/design/faculty-connect-int335-p09</b></font><br/>
    • <b>Live Application Reference:</b> <font color='#F2842F'><b>https://faculty-connect-production.up.railway.app/</b></font>
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
        [Paragraph("F06", styles['td_bold']), Paragraph("Faculty Availability Calendar", styles['td']), Paragraph("Student Portal", styles['td']), Paragraph("Cabin block/room badges, bookable time slots, consultation reason input.", styles['td'])],
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
    • <b>Participant Cohort:</b> 5 Users in Round 1 (4 Undergraduate Students across K22DF, K22GF, K22SE + 1 Faculty Member Dr. Rajesh Sharma).<br/>
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
            Paragraph("You need a 10-minute in-person meeting with Dr. Rajesh Sharma to show your wireframe sketches. Book a consultation.", styles['td']),
            Paragraph("Navigates to Faculty Availability, locates Dr. Sharma (Block 34-601), picks upcoming slot, inputs reason.", styles['td']),
            Paragraph("Successfully receives 'Appointment Requested' confirmation.", styles['td'])
        ],
        [
            Paragraph("<b>Task 4 (Faculty)</b>", styles['td_bold']),
            Paragraph("You are Dr. Rajesh Sharma. Open your dashboard and resolve a pending student doubt using the most efficient method available.", styles['td']),
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
