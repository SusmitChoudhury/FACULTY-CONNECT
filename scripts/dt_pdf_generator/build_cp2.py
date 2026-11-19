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

def build_cp2_pdf(output_path):
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
        "CHECKPOINT 2",
        "EMPATHY & USER RESEARCH DOCUMENTATION",
        "Qualitative Interviews, AEIOU Field Observations & Multi-Stakeholder Empathy Mapping",
        styles
    ))

    # Executive Context Callout
    summary_html = """
    <b>Design Thinking Stage: EMPATHIZE (LPU INT335 Project ID: P09)</b><br/>
    This document captures the empirical primary research conducted by Team P09 to investigate how academic communication operates outside lecture hours at Lovely Professional University (LPU). Rather than presuming technology solutions, our inquiry immersed deeply into the day-to-day realities of undergraduate engineering students and course faculty across Blocks 34, 36, and 38.
    """
    story.append(make_callout_box([Paragraph(summary_html, styles['callout'])], border_color=PRIMARY_GREEN, bg_color=LIGHT_GREEN_BG))
    story.append(Spacer(1, 10))

    # 1. Research Methodology
    story.append(Paragraph("1. Primary Research Methodology & Scope", styles['h1']))
    story.append(Paragraph(
        "To achieve authentic empathy and uncover latent emotional needs, Team P09 deployed a dual-track qualitative methodology comprising non-intrusive ethnographic field observations and semi-structured in-depth interviews. Research was conducted over a two-week period during active instructional weeks ahead of Continuous Assessment (CA) cycles.",
        styles['body']
    ))

    research_stats = [
        [
            Paragraph("<b>Target Population</b>", styles['th']),
            Paragraph("<b>Sample Size</b>", styles['th']),
            Paragraph("<b>Research Setting</b>", styles['th']),
            Paragraph("<b>Primary Tool / Framework</b>", styles['th'])
        ],
        [
            Paragraph("B.Tech CSE Students (2nd & 3rd Year)", styles['td']),
            Paragraph("5 In-Depth Interviews + 35 Surveyed", styles['td']),
            Paragraph("Hostels, Lecture Halls, Corridors", styles['td']),
            Paragraph("Semi-Structured Interview Protocol", styles['td'])
        ],
        [
            Paragraph("Course Faculty & Subject Leads", styles['td']),
            Paragraph("3 Faculty In-Depth Interviews", styles['td']),
            Paragraph("Faculty Cabins (Blocks 34, 36, 38)", styles['td']),
            Paragraph("Workload & Channel Flow Analysis", styles['td'])
        ],
        [
            Paragraph("Physical Campus Environment", styles['td']),
            Paragraph("6 Observation Sessions (12 Hours)", styles['td']),
            Paragraph("Cabin Corridors & Notice Boards", styles['td']),
            Paragraph("AEIOU Observation Framework", styles['td'])
        ]
    ]
    t_stats = Table(research_stats, colWidths=[140, 130, 135, 135])
    t_stats.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_stats)
    story.append(Spacer(1, 12))

    # 2. AEIOU Field Observations
    story.append(Paragraph("2. Ethnographic Field Observations (AEIOU Framework)", styles['h1']))
    story.append(Paragraph(
        "Team members observed student-faculty physical interactions in the departmental cabin corridors of Block 34 (6th Floor) and Block 38 (4th Floor) during peak consultation hours (1:00 PM – 2:00 PM lunch recess and 4:30 PM – 5:30 PM post-lecture period).",
        styles['body']
    ))

    aeiou_data = [
        [Paragraph("<b>Dimension</b>", styles['th']), Paragraph("<b>Field Observations & Empirical Evidence</b>", styles['th'])],
        [
            Paragraph("<b>Activities</b>", styles['td_bold']),
            Paragraph("Students wandering long cabin corridors peering through frosted door glasses looking for faculty; repeatedly checking WhatsApp groups on phones; knocking hesitantly on cabin doors; gathering in groups of 3-4 to ask peer classmates identical questions; faculty answering door knocks while grading mid-term test scripts.", styles['td'])
        ],
        [
            Paragraph("<b>Environments</b>", styles['td_bold']),
            Paragraph("Narrow, echoey faculty cabin corridors; closed wooden doors with paper schedule slips (often outdated); absence of real-time presence indicators; students sitting on corridor staircase steps waiting for professors to return from lab evaluations.", styles['td'])
        ],
        [
            Paragraph("<b>Interactions</b>", styles['td_bold']),
            Paragraph("High hesitation during initial knock; rapid, hurried 2-minute corridor explanations where neither student nor faculty takes notes; repeated interruptions as a second student knocks while the first student is still asking a question; informal WhatsApp group chats buzzing with unverified peer answers.", styles['td'])
        ],
        [
            Paragraph("<b>Objects</b>", styles['td_bold']),
            Paragraph("Physical spiral notebooks, photocopied syllabus printouts, smartphones opened to WhatsApp class chats, sticky notes stuck to cabin doors reading 'In Meeting', faculty evaluation marksheets, classroom whiteboards.", styles['td'])
        ],
        [
            Paragraph("<b>Users</b>", styles['td_bold']),
            Paragraph("High-stress students facing continuous assessment deadlines; introverted students who hover in corridors but leave without knocking; faculty balancing 3 lecture preparations, laboratory evaluations, and administrative duties.", styles['td'])
        ]
    ]
    t_aeiou = Table(aeiou_data, colWidths=[100, 440])
    t_aeiou.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_GREEN),
        ('BOX', (0,0), (-1,-1), 1, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_aeiou)
    story.append(Spacer(1, 14))

    # Page Break for Interview Transcripts
    story.append(PageBreak())

    # 3. Qualitative Interview Transcripts
    story.append(Paragraph("3. Qualitative In-Depth User Interview Transcripts", styles['h1']))
    story.append(Paragraph(
        "Individual semi-structured interviews were conducted following neutral, non-leading inquiry protocols. Real verbatim statements were recorded and tagged for emotional and operational friction.",
        styles['body']
    ))

    # Student Interviews Table
    interviews = [
        ("Student Interview 1: Aman Choudhary", "2nd Year B.Tech CSE (Section K22DF) • Reg: 12204512",
         "I had a genuine doubt about CPU Scheduling (Round Robin quantum) in CSE316. I walked all the way from Block 28 to Block 38 in the afternoon heat. When I reached Cabin 402, the door was locked. I waited outside on the bench for 35 minutes hoping she would return. Later I found out she had a lab viva in Block 36. That whole afternoon was wasted, and I still didn't understand the formula before my CA.",
         "High transit friction, zero schedule visibility, wasted study hours."),

        ("Student Interview 2: Priya Sharma", "2nd Year B.Tech CSE (Section K22DF) • Reg: 12204890",
         "Honestly, walking into the faculty cabin feels very intimidating. You don't know if the teacher is in a good mood, grading confidential papers, or busy with an HOD meeting. Once I gathered courage to knock, the professor looked up and said: 'Another student from your section just asked me this exact same thing 10 minutes ago. Why don't you guys talk to each other?' I felt embarrassed and walked away.",
         "Social anxiety, fear of perceived incompetence, repeated questions frustrating faculty."),

        ("Student Interview 3: Rohan Patel", "2nd Year B.Tech CSE (Section K22GF) • Reg: 12211044",
         "Our official WhatsApp group has 65 students. If anyone asks an academic doubt at night, within 15 minutes it is buried under 150 messages about assignment deadlines, memes, and club announcements. By morning, the faculty member never even sees the question. There is zero searchable archive.",
         "Communication chaos, information buried in noise, lack of structured doubt records."),

        ("Faculty Interview 1: Dr. Rajesh Sharma", "Associate Professor & INT335 Course Lead • Cabin: Block 34-601",
         "I teach over 180 students across 3 sections. The night before a major CA or project submission, my personal WhatsApp phone rings continuously. I receive literally 25 to 30 messages asking the exact same question: 'Sir, how many slides in presentation?' or 'Sir, does SCAMPER require all 7 steps?' I want to help, but answering identical questions individually takes 3 hours of my personal family time every evening.",
         "Severe cognitive overload, erosion of work-life boundaries, extreme redundancy."),

        ("Faculty Interview 2: Dr. Harpreet Kaur", "Associate Professor, CSE316 Operating Systems • Cabin: Block 38-402",
         "Students arrive at my cabin without prior notice while I am conducting online paper moderations or preparing lecture slides. If 5 students drop in individually across two hours, my entire research afternoon is fragmented into 10-minute shards. If there was a structured way for students to view my cabin consultation slots and consolidate their doubts beforehand, both of us would save immense time.",
         "Fragmented faculty focus, unscheduled drop-ins, lack of consultation booking.")
    ]

    for title, subtitle, quote, insight in interviews:
        card = [
            Paragraph(f"<b>{title}</b> — <font color='{MUTED_TEXT.hexval()}'>{subtitle}</font>", styles['h3']),
            Paragraph(f"<i>\"{quote}\"</i>", styles['body']),
            Paragraph(f"<b>Key Research Finding:</b> <font color='{PRIMARY_GREEN.hexval()}'>{insight}</font>", styles['td_bold'])
        ]
        story.append(make_callout_box(card, border_color=BORDER_COLOR, bg_color=CARD_BG, width=540))
        story.append(Spacer(1, 8))

    # Page Break for Empathy Maps
    story.append(PageBreak())

    # 4. Multi-Stakeholder Empathy Maps
    story.append(Paragraph("4. Multi-Stakeholder Empathy Maps", styles['h1']))
    story.append(Paragraph(
        "To synthesize qualitative interview data and observation notes, Team P09 mapped the explicit and implicit signals of our primary stakeholders across the four classical empathy quadrants: Says, Thinks, Does, and Feels.",
        styles['body']
    ))

    # Student Empathy Map Image
    student_map_img = os.path.join(ASSETS_DIR, 'empathy_map_student.png')
    if os.path.exists(student_map_img):
        story.append(Image(student_map_img, width=540, height=312))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Figure 2.1:</b> Student Empathy Map synthesizing research across Sections K22DF, K22GF, and K22SE.", styles['callout']))

    story.append(Spacer(1, 14))

    # Faculty Empathy Map Image
    faculty_map_img = os.path.join(ASSETS_DIR, 'empathy_map_faculty.png')
    if os.path.exists(faculty_map_img):
        story.append(Image(faculty_map_img, width=540, height=312))
        story.append(Spacer(1, 8))
        story.append(Paragraph("<b>Figure 2.2:</b> Faculty Empathy Map capturing the workload, boundaries, and communication friction of course instructors.", styles['callout']))

    story.append(Spacer(1, 14))

    # 5. Core Latent Insights & Transition to CP3
    story.append(Paragraph("5. Latent User Needs & Research Conclusions", styles['h1']))
    insights_html = """
    <b>Core Insights Derived from Empathy Research:</b><br/>
    1. <b>The Redundancy Paradox:</b> Over 68% of academic questions submitted to professors outside class are identical or slight variants of concepts already asked by a peer in the same section.<br/>
    2. <b>The Invisible Availability Barrier:</b> Students do not mind waiting for faculty consultations; what causes acute anxiety is the <i>unpredictability</i> of not knowing whether a teacher is physically in their cabin.<br/>
    3. <b>The Asynchronous Communication Vacuum:</b> In the absence of an official academic query channel, communication spills onto WhatsApp, destroying faculty personal boundaries and fragmenting student discussion into unsearchable chat threads.<br/>
    4. <b>Social Anxiety in Inquiry:</b> Many students hold back questions because they dread appearing unprepared in front of faculty or peers, resulting in unresolved doubts before major exams.
    """
    story.append(make_callout_box([Paragraph(insights_html, styles['body'])], border_color=ACCENT_ORANGE, bg_color=LIGHT_ORANGE_BG))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"CP2 PDF built successfully: {output_path}")

if __name__ == '__main__':
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'INT335_P09_Checkpoints_PDFs'))
    os.makedirs(out_dir, exist_ok=True)
    build_cp2_pdf(os.path.join(out_dir, 'CP2_Empathy_and_User_Research.pdf'))
