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

def build_cp4_pdf(output_path):
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
        "CHECKPOINT 4",
        "IDEATION, AFFINITY CLUSTERING & CONCEPT SELECTION",
        "36 Distinct Concepts, Brainwriting, Crazy 8s, SCAMPER, Weighted Screening Matrix & Selection Analysis",
        styles
    ))

    # Executive Context Callout
    summary_html = """
    <b>Design Thinking Stage: IDEATE (LPU INT335 Project ID: P09)</b><br/>
    In Checkpoint 4, Team P09 engaged in expansive divergent thinking to generate a wide spectrum of potential interventions addressing our core HMW challenge. By strictly separating idea generation from evaluation, we explored physical kiosks, peer-led networks, WhatsApp bot automation, and hybrid platforms before applying a pre-weighted screening matrix to select the most defensible concept.
    """
    story.append(make_callout_box([Paragraph(summary_html, styles['callout'])], border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG))
    story.append(Spacer(1, 10))

    # 1. Ideation Methodologies
    story.append(Paragraph("1. Multi-Method Divergent Ideation Process", styles['h1']))
    story.append(Paragraph(
        "To break functional fixedness and prevent premature convergence, Team P09 employed three established ideation techniques across two intensive group sessions.",
        styles['body']
    ))

    # Ideation Graphic Image
    ideation_img = os.path.join(ASSETS_DIR, 'ideation_methods_crazy8s.png')
    if os.path.exists(ideation_img):
        story.append(Image(ideation_img, width=540, height=276))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 4.1:</b> Overview of the three divergent ideation methodologies deployed during team brainstorming.", styles['callout']))

    story.append(Spacer(1, 12))

    # 2. 30+ Ideas Log (36 Genuinely Distinct Ideas)
    story.append(Paragraph("2. Comprehensive 30+ Ideas Log (36 Genuinely Distinct Concepts)", styles['h1']))
    story.append(Paragraph(
        "Every concept was recorded with author attribution and initial inspiration method. Contributors: Aryan Singh (AS), Kaya Hamir Reddy (KH), Aditya Tiwari (AT), Susmit Choudhury (SC).",
        styles['body']
    ))

    # Table of 36 Ideas (split across 2 pages)
    ideas_part1 = [
        [Paragraph("<b>#</b>", styles['th']), Paragraph("<b>Concept Title</b>", styles['th']), Paragraph("<b>Description & Mechanism</b>", styles['th']), Paragraph("<b>Method</b>", styles['th']), Paragraph("<b>Author</b>", styles['th'])],
        [Paragraph("1", styles['td']), Paragraph("Physical LED Cabin Presence Board", styles['td_bold']), Paragraph("Hardware display outside cabin door indicating Real-Time status (Free, Busy, In Meeting).", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("AS", styles['td'])],
        [Paragraph("2", styles['td']), Paragraph("Paper Token Consultation Dispenser", styles['td_bold']), Paragraph("Physical numbered ticket dispenser outside cabin allowing 10-minute queue pacing.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("AT", styles['td'])],
        [Paragraph("3", styles['td']), Paragraph("WhatsApp Bot Auto-Responder", styles['td_bold']), Paragraph("Twilio/WhatsApp automation answering syllabus queries via keyword regex matching.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("4", styles['td']), Paragraph("Weekly Physical Doubt Hour in Hall", styles['td_bold']), Paragraph("Designated 1-hour common tutorial room block reserved solely for walk-in doubts.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("KH", styles['td'])],
        [Paragraph("5", styles['td']), Paragraph("Class Representative (CR) Filter Hub", styles['td_bold']), Paragraph("Students submit all questions to section CR who compiles a single daily summary sheet.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("AS", styles['td'])],
        [Paragraph("6", styles['td']), Paragraph("Anonymous Corridor Doubt Drop-Box", styles['td_bold']), Paragraph("Physical wooden box where students drop written question slips; faculty answers next class.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("KH", styles['td'])],
        [Paragraph("7", styles['td']), Paragraph("Static PDF Syllabus FAQ Bulletin", styles['td_bold']), Paragraph("Faculty creates a static shared Google Doc with 50 common questions ahead of each unit.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("AT", styles['td'])],
        [Paragraph("8", styles['td']), Paragraph("Shared Google Calendar Cabin Slots", styles['td_bold']), Paragraph("Faculty publishes open 15-minute consultation slots on a shared university calendar link.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("9", styles['td']), Paragraph("Senior Peer-Tutor Relay Network", styles['td_bold']), Paragraph("4th year topper students assigned to solve 2nd year doubts during evening hostel hours.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("AS", styles['td'])],
        [Paragraph("10", styles['td']), Paragraph("Voice-Note Micro-Podcast Answers", styles['td_bold']), Paragraph("Faculty records 2-minute daily audio clips addressing top doubts broadcast via Telegram.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("11", styles['td']), Paragraph("Classroom Live Upvote Whiteboard", styles['td_bold']), Paragraph("Sticky-note board inside classroom where students upvote confusing topics before lecture.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("KH", styles['td'])],
        [Paragraph("12", styles['td']), Paragraph("Telegram Discussion Channel with Polls", styles['td_bold']), Paragraph("Section Telegram group with topic threading and student anonymous voting.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("AT", styles['td'])],
        [Paragraph("13", styles['td']), Paragraph("Office Hour QR Code Door Scanner", styles['td_bold']), Paragraph("QR code on cabin door routing students to a live Google Sheet showing daily availability.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("14", styles['td']), Paragraph("Lecture Exit-Ticket Slip Review", styles['td_bold']), Paragraph("Students hand in 1 index card with their top confusion before leaving lecture hall.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("AS", styles['td'])],
        [Paragraph("15", styles['td']), Paragraph("Departmental Centralized FAQ Kiosk", styles['td_bold']), Paragraph("Touchscreen terminal installed in Block 34 lobby for searching common syllabus answers.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("AT", styles['td'])],
        [Paragraph("16", styles['td']), Paragraph("StackOverflow-Style Section Forum", styles['td_bold']), Paragraph("Internal university forum with voting, tags, and bounty points for peer explanations.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("KH", styles['td'])],
        [Paragraph("17", styles['td']), Paragraph("LPU Touch Mobile UMS Plugin", styles['td_bold']), Paragraph("Official mobile application extension embedding a formal consultation booking tab.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("18", styles['td']), Paragraph("Hostel Study-Circle Evening Helpdesk", styles['td_bold']), Paragraph("Physical helpdesk in hostel common room staffed by postgraduate teaching assistants.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("AS", styles['td'])]
    ]

    t_ideas1 = Table(ideas_part1, colWidths=[20, 140, 260, 75, 45])
    t_ideas1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ideas1)

    story.append(PageBreak())

    # Ideas Part 2
    story.append(Paragraph("2. Comprehensive 30+ Ideas Log (Continued: Ideas 19 to 36)", styles['h1']))
    ideas_part2 = [
        [Paragraph("<b>#</b>", styles['th']), Paragraph("<b>Concept Title</b>", styles['th']), Paragraph("<b>Description & Mechanism</b>", styles['th']), Paragraph("<b>Method</b>", styles['th']), Paragraph("<b>Author</b>", styles['th'])],
        [Paragraph("19", styles['td']), Paragraph("Discord Academic Server with Voice Rooms", styles['td_bold']), Paragraph("Discord community categorized by subject codes with designated faculty office hours.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("20", styles['td']), Paragraph("Automated SMS Broadcast for Presence", styles['td_bold']), Paragraph("SMS alert triggered to section when faculty scans punch-card entering cabin.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("AT", styles['td'])],
        [Paragraph("21", styles['td']), Paragraph("RFID Door Sensor Presence Beacon", styles['td_bold']), Paragraph("Hardware door sensor detecting faculty badge to toggle digital 'In Cabin' badge.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("AS", styles['td'])],
        [Paragraph("22", styles['td']), Paragraph("Flashcard Question Pre-Screening", styles['td_bold']), Paragraph("Students must solve a basic diagnostic flashcard before booking a cabin slot.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("KH", styles['td'])],
        [Paragraph("23", styles['td']), Paragraph("Email Ticket Queue (ZenDesk-style)", styles['td_bold']), Paragraph("Formal email ticketing assigning ticket numbers and SLA deadlines to student queries.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("AT", styles['td'])],
        [Paragraph("24", styles['td']), Paragraph("Crowdsourced Section Lecture Wiki", styles['td_bold']), Paragraph("Notion/Wiki maintained jointly by students with faculty official annotations.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("25", styles['td']), Paragraph("Google Form Weekly Doubt Form", styles['td_bold']), Paragraph("Standard Google form opened every Friday morning and compiled for Monday lecture.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("AS", styles['td'])],
        [Paragraph("26", styles['td']), Paragraph("AI Chatbot on University Intranet", styles['td_bold']), Paragraph("Generic AI bot answering general engineering questions without course grounding.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("KH", styles['td'])],
        [Paragraph("27", styles['td']), Paragraph("Peer-to-Peer Bounty Exchange", styles['td_bold']), Paragraph("Gamified student token reward system for helping classmates resolve coding errors.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("28", styles['td']), Paragraph("Video Micro-Clips Library by Faculty", styles['td_bold']), Paragraph("Faculty records 3-minute Loom video clips for the 10 most failed exam questions.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("AT", styles['td'])],
        [Paragraph("29", styles['td']), Paragraph("Cabin Door Digital Tablet Scheduler", styles['td_bold']), Paragraph("Mounted 8-inch iPad outside cabin where students tap to reserve 10-minute slots.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("AS", styles['td'])],
        [Paragraph("30", styles['td']), Paragraph("Virtual Cabin Walk-In via Zoom", styles['td_bold']), Paragraph("Open 30-minute Zoom call on weekday evenings with a digital waiting room.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("KH", styles['td'])],
        [Paragraph("31", styles['td']), Paragraph("Semantic Question Deduplicator (+1)", styles['td_bold']), Paragraph("Asynchronous engine detecting similar doubts and allowing '+1 Same Doubt' pooling.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("32", styles['td']), Paragraph("3-Hour SLA Automated Fallback Engine", styles['td_bold']), Paragraph("Syllabus-grounded knowledge generator answering doubts if faculty is delayed >3h.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("AT", styles['td'])],
        [Paragraph("33", styles['td']), Paragraph("Section-Wise Confusion Analytics Heatmap", styles['td_bold']), Paragraph("Curriculum analytics highlighting unit-level doubt density to adjust lecture pace.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("AS", styles['td'])],
        [Paragraph("34", styles['td']), Paragraph("Integrated Cabin Appointment Ledger", styles['td_bold']), Paragraph("Mutual 2-way consultation slot booking with student reason and faculty notes.", styles['td']), Paragraph("Crazy 8s", styles['td']), Paragraph("KH", styles['td'])],
        [Paragraph("35", styles['td']), Paragraph("Installable Chrome Desktop/Mobile PWA", styles['td_bold']), Paragraph("Zero-install web application working across laptop and phone with offline caching.", styles['td']), Paragraph("SCAMPER", styles['td']), Paragraph("SC", styles['td'])],
        [Paragraph("36", styles['td']), Paragraph("Official Faculty Answer Broadcast Banner", styles['td_bold']), Paragraph("1-click publication of authoritative answer pushed instantly to all supporters.", styles['td']), Paragraph("Brainwriting", styles['td']), Paragraph("AT", styles['td'])]
    ]

    t_ideas2 = Table(ideas_part2, colWidths=[20, 140, 260, 75, 45])
    t_ideas2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_ideas2)

    story.append(PageBreak())

    # 3. Affinity Grouping & Clustering
    story.append(Paragraph("3. Affinity Grouping & Thematic Clustering", styles['h1']))
    story.append(Paragraph(
        "Following raw ideation, the team clustered all 36 ideas into six operational solution archetypes to identify recurring strategic patterns.",
        styles['body']
    ))

    clusters = [
        ("Cluster 1: Physical & Hardware Interventions (Ideas 1, 2, 6, 11, 13, 21, 29)",
         "Focuses on retrofitting cabin doors with LED indicators, token dispensers, or mounted tablets. Strength: Immediate physical clarity. Limitation: High hardware cost, prone to vandalism, fails after 5 PM campus exit."),

        ("Cluster 2: Informal & Chat-Based Bots (Ideas 3, 10, 12, 19, 20)",
         "Leverages WhatsApp/Telegram/Discord channels. Strength: High student familiarity. Limitation: Unstructured data, privacy invasion, high maintenance, and inability to link directly to university syllabus records."),

        ("Cluster 3: Peer-Assisted Student Relays (Ideas 5, 9, 16, 18, 24, 27)",
         "Delegates doubts to seniors, TAs, or student forums. Strength: Distributes workload away from faculty. Limitation: Risk of inaccurate peer explanations, lack of student trust for exam grading benchmarks."),

        ("Cluster 4: Static Archives & Video Repositories (Ideas 7, 14, 15, 25, 28)",
         "Pre-compiled FAQs, video clips, and exit tickets. Strength: Asynchronous access. Limitation: Passive; students ignore static FAQs when stressed, and faculty lack time to record dozens of videos."),

        ("Cluster 5: Standalone Appointment Schedulers (Ideas 8, 17, 23, 30)",
         "Calendly or Google Calendar clones for booking cabin visits. Strength: Solves transit friction. Limitation: Does nothing to reduce the 68% repetitive questions that could have been resolved digitally."),

        ("Cluster 6: Intelligent Academic Assistance Platform (Ideas 31, 32, 33, 34, 35, 36)",
         "Unified digital platform combining semantic question deduplication (+1), bookable cabin slots, section analytics, and a 3-hour SLA fallback bridge. Strength: Solves both student transit and faculty overload simultaneously.")
    ]

    for c_title, c_desc in clusters:
        story.append(Paragraph(f"<b>{c_title}</b>", styles['h3']))
        story.append(Paragraph(c_desc, styles['body']))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 8))

    # 4. Weighted Screening Matrix
    story.append(Paragraph("4. Weighted Concept Screening Matrix", styles['h1']))
    story.append(Paragraph(
        "Evaluation criteria and weights were established <b>before</b> scoring candidate concepts to guarantee objective, defensible selection aligned with our research evidence.",
        styles['body']
    ))

    # Screening Table
    matrix_data = [
        [
            Paragraph("<b>Candidate Concept</b>", styles['th']),
            Paragraph("<b>User Value<br/>(25%)</b>", styles['th']),
            Paragraph("<b>Faculty Low Friction<br/>(20%)</b>", styles['th']),
            Paragraph("<b>Technical Feasibility<br/>(20%)</b>", styles['th']),
            Paragraph("<b>Implementation Effort<br/>(15%)</b>", styles['th']),
            Paragraph("<b>Scalability<br/>(10%)</b>", styles['th']),
            Paragraph("<b>Research Fit<br/>(10%)</b>", styles['th']),
            Paragraph("<b>Weighted Total</b>", styles['th']),
            Paragraph("<b>Rank</b>", styles['th'])
        ],
        [
            Paragraph("<b>A. Hardware LED Cabin Display + Token Dispenser</b>", styles['td_bold']),
            Paragraph("3.0 / 5", styles['td']), Paragraph("2.5 / 5", styles['td']), Paragraph("3.0 / 5", styles['td']), Paragraph("1.5 / 5", styles['td']), Paragraph("2.0 / 5", styles['td']), Paragraph("3.0 / 5", styles['td']),
            Paragraph("<b>2.58</b>", styles['td_bold']), Paragraph("5th", styles['td'])
        ],
        [
            Paragraph("<b>B. Automated WhatsApp Keyword Bot</b>", styles['td_bold']),
            Paragraph("3.5 / 5", styles['td']), Paragraph("2.0 / 5", styles['td']), Paragraph("3.5 / 5", styles['td']), Paragraph("3.5 / 5", styles['td']), Paragraph("3.0 / 5", styles['td']), Paragraph("2.5 / 5", styles['td']),
            Paragraph("<b>3.05</b>", styles['td_bold']), Paragraph("4th", styles['td'])
        ],
        [
            Paragraph("<b>C. Static Google Doc / Notion Course FAQ</b>", styles['td_bold']),
            Paragraph("2.5 / 5", styles['td']), Paragraph("3.5 / 5", styles['td']), Paragraph("5.0 / 5", styles['td']), Paragraph("4.5 / 5", styles['td']), Paragraph("2.5 / 5", styles['td']), Paragraph("2.0 / 5", styles['td']),
            Paragraph("<b>3.48</b>", styles['td_bold']), Paragraph("3rd", styles['td'])
        ],
        [
            Paragraph("<b>D. Peer-Assisted Senior Student Doubt Forum</b>", styles['td_bold']),
            Paragraph("3.5 / 5", styles['td']), Paragraph("4.0 / 5", styles['td']), Paragraph("4.0 / 5", styles['td']), Paragraph("3.5 / 5", styles['td']), Paragraph("3.5 / 5", styles['td']), Paragraph("3.0 / 5", styles['td']),
            Paragraph("<b>3.65</b>", styles['td_bold']), Paragraph("2nd", styles['td'])
        ],
        [
            Paragraph("<b>E. Standalone Office Hours Scheduler (Calendly Clone)</b>", styles['td_bold']),
            Paragraph("3.0 / 5", styles['td']), Paragraph("3.0 / 5", styles['td']), Paragraph("4.5 / 5", styles['td']), Paragraph("4.0 / 5", styles['td']), Paragraph("3.5 / 5", styles['td']), Paragraph("3.0 / 5", styles['td']),
            Paragraph("<b>3.50</b>", styles['td_bold']), Paragraph("3rd (Tie)", styles['td'])
        ],
        [
            Paragraph("<b>F. FACULTY CONNECT (Unified Deduplication, +1 & SLA)</b>", styles['td_bold']),
            Paragraph("4.8 / 5", styles['td']), Paragraph("4.5 / 5", styles['td']), Paragraph("4.5 / 5", styles['td']), Paragraph("4.0 / 5", styles['td']), Paragraph("4.8 / 5", styles['td']), Paragraph("4.8 / 5", styles['td']),
            Paragraph("<b>4.56</b>", styles['td_bold']), Paragraph("<b>1st (WIN)</b>", styles['td_bold'])
        ]
    ]

    t_matrix = Table(matrix_data, colWidths=[120, 48, 52, 52, 52, 48, 48, 70, 50])
    t_matrix.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BACKGROUND', (0,6), (-1,6), LIGHT_GREEN_BG),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_matrix)
    story.append(Spacer(1, 14))

    # Page Break for Concept Justification
    story.append(PageBreak())

    # 5. Selected Concept Justification & Post-Mortem of Rejected Ideas
    story.append(Paragraph("5. Final Concept Selection & Traceability to Research", styles['h1']))
    sel_html = """
    <b>SELECTED CONCEPT: Faculty Connect (Concept F)</b><br/>
    <b>Why Concept F Emerged as the Clear Winner:</b><br/>
    Concept F directly targets the twin root causes identified in CP2 and CP3: (1) <i>Redundant student questions</i> and (2) <i>Unpredictable faculty physical availability</i>.<br/>
    • <b>Semantic Duplicate Detection & '+1' Pooling:</b> When a student types a query, semantic similarity detects matching doubts in the same course/unit. Instead of posting a duplicate, the student clicks '+1 - I Have the Same Doubt'. Faculty answers once; all supporters receive notifications instantly.<br/>
    • <b>3-Hour SLA Academic Fallback:</b> If a professor is in an extended conference, examination, or meeting, a syllabus-grounded academic synthesizer provides a preliminary explanation so student momentum is never blocked.<br/>
    • <b>Cabin Consultation Booking:</b> Replaces chaotic corridor wandering with transparent 1-click consultation slot requests that professors accept with specific preparation instructions.
    """
    story.append(make_callout_box([Paragraph(sel_html, styles['body'])], border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG))
    story.append(Spacer(1, 12))

    story.append(Paragraph("6. Honest Post-Mortem of Rejected Alternative Concepts", styles['h1']))
    story.append(Paragraph(
        "Design Thinking mandates documenting why compelling alternative concepts were rejected. Below are our empirical rationales:",
        styles['body']
    ))

    rejected_notes = [
        ("Why Concept A (Hardware LED Board + Token Dispenser) Was Rejected:",
         "High physical infrastructure and maintenance overhead across 400+ LPU cabins. Moreover, hardware physical boards fail completely for commuter students and evening hostel self-study after 5:00 PM when campus buildings close."),
        ("Why Concept B (Automated WhatsApp Bot) Was Rejected:",
         "WhatsApp API imposes ongoing per-message costs and strict template constraints. Furthermore, students strongly disliked mixing casual personal messaging with official university assessment benchmarks, and WhatsApp lacks syllabus scoping (Course/Unit/Topic hierarchy)."),
        ("Why Concept C (Static Google Doc / Notion FAQ) Was Rejected:",
         "Our empathy research revealed that students rarely read static 50-page FAQ documents when stressed. Static repositories lack interactive search and provide no mechanism for genuine, novel doubts."),
        ("Why Concept D (Peer-Assisted Senior Student Forum) Was Rejected:",
         "While scalable, student interviewees explicitly stated they do not trust peer explanations for graded Continuous Assessments and end-term exam preparation. They require authoritative faculty verification.")
    ]

    for title, reason in rejected_notes:
        story.append(Paragraph(f"• <b>{title}</b> {reason}", styles['bullet']))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 10))

    # Page Break for Figma System Architecture
    story.append(PageBreak())

    # 7. Production UI/UX & Figma Architectural Parity Specifications
    story.append(Paragraph("7. Production UI/UX Architecture & Figma System Specifications", styles['h1']))
    story.append(Paragraph(
        "To ensure seamless fidelity between design thinking ideation and the production codebase, Team P09 established strict component parity matching the live deployed application across all structural dimensions.",
        styles['body']
    ))

    # Embed Figma Design System Image
    figma_img = os.path.join(ASSETS_DIR, 'figma_design_system_preview.png')
    if os.path.exists(figma_img):
        story.append(Image(figma_img, width=540, height=315))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 4.2:</b> Comprehensive Figma Design System Architecture & Component Inventory matching the production application.", styles['callout']))

    story.append(Spacer(1, 10))

    figma_specs_data = [
        [Paragraph("<b>UI/UX Design Dimension</b>", styles['th']), Paragraph("<b>Figma Design Specification & Component Architecture</b>", styles['th'])],
        [
            Paragraph("<b>Layout Architecture</b>", styles['td_bold']),
            Paragraph("Desktop SaaS dashboard layout with sticky top navigation header, 240px contextual left sidebar, multi-column card grid, and full-width modal drawers. Fully responsive mobile-first PWA viewport.", styles['td'])
        ],
        [
            Paragraph("<b>Global Navigation</b>", styles['td_bold']),
            Paragraph("Persistent header navbar in Dark Green (<code>#15370D</code>) featuring Faculty Connect branding, Project P09 badge, 1-click Student/Faculty role switcher, notification badge, and native Chrome PWA 'Install App' trigger.", styles['td'])
        ],
        [
            Paragraph("<b>Typography Hierarchy</b>", styles['td_bold']),
            Paragraph("Clean Inter font family. Title: 22px/26px Bold; H1 Section: 14px/18px Bold; Card Headers: 12px/16px Bold; Body Typography: 9px/13px in crisp, high-contrast black (<code>#000000</code>).", styles['td'])
        ],
        [
            Paragraph("<b>Colour Tokens</b>", styles['td_bold']),
            Paragraph("Strict official palette: Primary Green (<code>#15370D</code>), Surface Cream (<code>#FCF9EA</code>), Accent Orange (<code>#F2842F</code>), High-Contrast Text (<code>#000000</code>), and Neutral Border (<code>#CBD5E1</code>). Zero unauthorized neons or gradients.", styles['td'])
        ],
        [
            Paragraph("<b>Spacing System</b>", styles['td_bold']),
            Paragraph("Strict 8px spatial baseline grid. Card padding: 16px (p-4) to 24px (p-6); Gap spacing: 12px to 16px; Modal margins: 24px; Touch targets: minimum 44px height for mobile accessibility.", styles['td'])
        ],
        [
            Paragraph("<b>Buttons & States</b>", styles['td_bold']),
            Paragraph("Primary Action Button (Dark Green solid with white text), Secondary Action (Cream background with green border), Accent '+1' Support Button (Orange badge with active state), Ghost Cancel (text only), and Disabled states.", styles['td'])
        ],
        [
            Paragraph("<b>Forms & Inputs</b>", styles['td_bold']),
            Paragraph("Dynamic 3-tier cascading dropdowns (Subject -> Unit -> Topic), calendar date pickers, auto-expanding question textarea with character counters, search input with clear icon.", styles['td'])
        ],
        [
            Paragraph("<b>Cards & Surfaces</b>", styles['td_bold']),
            Paragraph("Doubt Summary Cards with urgency badges, Course Progress Cards, Consultation Slot Badges, and Teacher Queue Cards with supporter count indicators.", styles['td'])
        ],
        [
            Paragraph("<b>Dashboard Structure</b>", styles['td_bold']),
            Paragraph("Student Portal: Overview, Ask a Doubt, My Questions, Faculty Availability, Cabin Consultation Bookings.<br/>Teacher Portal: Urgent Doubt Queue, Resolved Doubts, Consultation Management, Section-Wise Analytics.", styles['td'])
        ],
        [
            Paragraph("<b>Interaction Patterns</b>", styles['td_bold']),
            Paragraph("Instant semantic typing similarity check; 1-click 'Give Ans by AI' draft generation; direct status update to 'Resolved'; automatic modal drawer closing (<code>setSelectedDoubt(null)</code>); real-time supporter counter increments.", styles['td'])
        ]
    ]

    t_fspecs = Table(figma_specs_data, colWidths=[140, 400])
    t_fspecs.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_fspecs)
    story.append(Spacer(1, 14))

    # Page Break for Step-by-Step User Flow
    story.append(PageBreak())

    # 8. Step-by-Step Formal User Flow Diagram
    story.append(Paragraph("8. Formal Step-by-Step User Flow Architecture", styles['h1']))
    story.append(Paragraph(
        "Below is the complete, numbered step-by-step user flow diagram mapping the operational sequence of the selected concept, detailing decision diamonds, duplicate resolution branches, and the 3-hour SLA safety net.",
        styles['body']
    ))

    # Embed User Flow Diagram
    uf_img = os.path.join(ASSETS_DIR, 'user_flow_step_by_step_academic.png')
    if os.path.exists(uf_img):
        story.append(Image(uf_img, width=540, height=350))
        story.append(Spacer(1, 6))
        story.append(Paragraph("<b>Figure 4.3:</b> Formal Step-by-Step User Flow Architecture illustrating Student Inquiry, Semantic Deduplication, SLA Fallback, and Faculty Direct Resolution.", styles['callout']))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"CP4 PDF built successfully: {output_path}")

if __name__ == '__main__':
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'INT335_P09_Checkpoints_PDFs'))
    os.makedirs(out_dir, exist_ok=True)
    build_cp4_pdf(os.path.join(out_dir, 'CP4_Ideation_and_Selection.pdf'))
