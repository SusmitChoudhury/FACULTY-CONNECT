import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
os.makedirs(ASSETS_DIR, exist_ok=True)

# Colors
C_DARK_GREEN = (21, 55, 13)
C_CREAM = (252, 249, 234)
C_ORANGE = (242, 132, 47)
C_BLACK = (0, 0, 0)
C_SLATE = (30, 41, 59)
C_MUTED = (100, 116, 139)
C_WHITE = (255, 255, 255)
C_LIGHT_GREEN = (235, 245, 235)
C_LIGHT_ORANGE = (255, 245, 237)
C_BORDER = (203, 213, 225)
C_RED = (220, 38, 38)
C_GREEN = (22, 101, 52)

def get_font(size=14, bold=False):
    font_paths = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_empathy_map(title, role_text, quadrants, filename):
    """
    Renders a 4-quadrant Empathy Map (Says, Thinks, Does, Feels).
    """
    w, h = 900, 520
    img = Image.new('RGB', (w, h), C_CREAM)
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([10, 10, w - 10, h - 10], outline=C_DARK_GREEN, width=3)

    # Header Bar
    draw.rectangle([10, 10, w - 10, 60], fill=C_DARK_GREEN)
    draw.text((25, 20), title.upper(), fill=C_WHITE, font=get_font(20, bold=True))
    draw.text((w - 320, 24), role_text, fill=C_ORANGE, font=get_font(13, bold=True))

    # Center intersection lines
    mid_x, mid_y = w // 2, (h + 60) // 2
    draw.line([(mid_x, 60), (mid_x, h - 10)], fill=C_BORDER, width=2)
    draw.line([(10, mid_y), (w - 10, mid_y)], fill=C_BORDER, width=2)

    # 4 Quadrants configuration: (x0, y0, x1, y1, title, items, fill_bg)
    boxes = [
        (15, 65, mid_x - 5, mid_y - 5, "💬 SAYS (Verbatim Quotes)", quadrants.get('says', []), C_WHITE),
        (mid_x + 5, 65, w - 15, mid_y - 5, "💭 THINKS (Internal Beliefs)", quadrants.get('thinks', []), C_WHITE),
        (15, mid_y + 5, mid_x - 5, h - 15, "🏃 DOES (Observable Behaviors)", quadrants.get('does', []), C_WHITE),
        (mid_x + 5, mid_y + 5, w - 15, h - 15, "❤️ FEELS (Emotions & Anxiety)", quadrants.get('feels', []), C_LIGHT_ORANGE)
    ]

    for (bx0, by0, bx1, by1, q_title, items, bg) in boxes:
        draw.rectangle([bx0, by0, bx1, by1], fill=bg, outline=C_BORDER, width=1)
        # Header banner inside quadrant
        draw.rectangle([bx0, by0, bx1, by0 + 32], fill=C_LIGHT_GREEN if bg != C_LIGHT_ORANGE else (254, 226, 200))
        draw.text((bx0 + 12, by0 + 8), q_title, fill=C_DARK_GREEN, font=get_font(13, bold=True))

        curr_y = by0 + 44
        for item in items[:4]:
            draw.text((bx0 + 16, curr_y), "•", fill=C_ORANGE, font=get_font(13, bold=True))
            # Wrap text manually
            words = item.split()
            lines = []
            cur_line = []
            for word in words:
                cur_line.append(word)
                if len(" ".join(cur_line)) > 42:
                    lines.append(" ".join(cur_line[:-1]))
                    cur_line = [word]
            if cur_line:
                lines.append(" ".join(cur_line))

            for l in lines:
                draw.text((bx0 + 32, curr_y), l, fill=C_SLATE, font=get_font(11, bold=False))
                curr_y += 16
            curr_y += 6

    # Center circle badge
    r = 38
    draw.ellipse([mid_x - r, mid_y - r, mid_x + r, mid_y + r], fill=C_DARK_GREEN, outline=C_ORANGE, width=3)
    draw.text((mid_x - 24, mid_y - 12), "USER", fill=C_WHITE, font=get_font(14, bold=True))
    draw.text((mid_x - 22, mid_y + 4), "CORE", fill=C_ORANGE, font=get_font(10, bold=True))

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path


def create_persona_card(name, subtitle, quote, traits, goals, frustrations, filename):
    """
    Renders an official Design Thinking User Persona Infographic card.
    """
    w, h = 900, 500
    img = Image.new('RGB', (w, h), C_WHITE)
    draw = ImageDraw.Draw(img)

    # Frame border
    draw.rectangle([10, 10, w - 10, h - 10], outline=C_DARK_GREEN, width=2)

    # Top Header
    draw.rectangle([10, 10, w - 10, 70], fill=C_DARK_GREEN)
    draw.text((30, 22), name.upper(), fill=C_WHITE, font=get_font(22, bold=True))
    draw.text((30, 48), subtitle, fill=C_ORANGE, font=get_font(12, bold=True))

    # Left Column: Avatar & Profile Details
    col1_w = 280
    draw.rectangle([20, 80, col1_w, h - 20], fill=C_CREAM, outline=C_BORDER)

    # Avatar Circle
    cx, cy, cr = 150, 150, 50
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=C_DARK_GREEN, outline=C_ORANGE, width=3)
    initials = "".join([part[0] for part in name.split()[:2]])
    draw.text((cx - 18, cy - 14), initials, fill=C_WHITE, font=get_font(24, bold=True))

    # Quote box
    draw.rectangle([35, 215, col1_w - 15, 275], fill=C_LIGHT_ORANGE, outline=C_ORANGE, width=1)
    draw.text((45, 222), f'"{quote}"', fill=C_SLATE, font=get_font(10, bold=True))

    # Profile Stats
    sy = 290
    for label, val in traits:
        draw.text((35, sy), label + ":", fill=C_DARK_GREEN, font=get_font(11, bold=True))
        draw.text((120, sy), str(val), fill=C_SLATE, font=get_font(11))
        sy += 24

    # Right Column: Goals vs Frustrations
    rx0 = col1_w + 15
    rx1 = w - 20

    # Section 1: Goals & Motivations
    draw.rectangle([rx0, 80, rx1, 275], fill=C_WHITE, outline=C_BORDER)
    draw.rectangle([rx0, 80, rx1, 112], fill=C_LIGHT_GREEN)
    draw.text((rx0 + 15, 88), "🎯 KEY GOALS & MOTIVATIONS", fill=C_DARK_GREEN, font=get_font(13, bold=True))

    gy = 125
    for g in goals:
        draw.text((rx0 + 20, gy), "✔", fill=C_GREEN, font=get_font(12, bold=True))
        draw.text((rx0 + 40, gy), g, fill=C_SLATE, font=get_font(11))
        gy += 30

    # Section 2: Frustrations & Pain Points
    draw.rectangle([rx0, 290, rx1, h - 20], fill=C_WHITE, outline=C_BORDER)
    draw.rectangle([rx0, 290, rx1, 322], fill=C_LIGHT_ORANGE)
    draw.text((rx0 + 15, 298), "⚠️ FRUSTRATIONS & PAIN POINTS", fill=C_RED, font=get_font(13, bold=True))

    fy = 335
    for f in frustrations:
        draw.text((rx0 + 20, fy), "✖", fill=C_RED, font=get_font(12, bold=True))
        draw.text((rx0 + 40, fy), f, fill=C_SLATE, font=get_font(11))
        fy += 30

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path


def create_journey_map(title, stages, filename):
    """
    Renders a 5-stage User Journey Map with Emotional Valence Line.
    """
    w, h = 900, 480
    img = Image.new('RGB', (w, h), C_WHITE)
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([10, 10, w - 10, h - 10], outline=C_DARK_GREEN, width=2)

    # Header Bar
    draw.rectangle([10, 10, w - 10, 55], fill=C_DARK_GREEN)
    draw.text((25, 18), title.upper(), fill=C_WHITE, font=get_font(18, bold=True))
    draw.text((w - 280, 22), "CURRENT AS-IS USER EXPERIENCE", fill=C_ORANGE, font=get_font(11, bold=True))

    n = len(stages)
    col_w = (w - 40) // n
    x_starts = [20 + i * col_w for i in range(n)]

    # Draw columns
    for i, stg in enumerate(stages):
        x0 = x_starts[i]
        x1 = x0 + col_w - 6

        # Column header
        draw.rectangle([x0, 65, x1, 100], fill=C_LIGHT_GREEN, outline=C_BORDER)
        draw.text((x0 + 8, 70), f"STAGE {i+1}", fill=C_ORANGE, font=get_font(9, bold=True))
        draw.text((x0 + 8, 83), stg['name'][:22], fill=C_DARK_GREEN, font=get_font(11, bold=True))

        # Actions Box
        draw.rectangle([x0, 105, x1, 180], fill=C_CREAM, outline=C_BORDER)
        draw.text((x0 + 6, 110), "USER ACTIONS:", fill=C_DARK_GREEN, font=get_font(9, bold=True))
        draw.text((x0 + 6, 126), stg['actions'], fill=C_SLATE, font=get_font(8.5))

        # Thoughts Box
        draw.rectangle([x0, 185, x1, 260], fill=C_WHITE, outline=C_BORDER)
        draw.text((x0 + 6, 190), "THOUGHTS:", fill=C_MUTED, font=get_font(9, bold=True))
        draw.text((x0 + 6, 206), f'"{stg["thoughts"]}"', fill=C_SLATE, font=get_font(8.5))

        # Pain Points Box
        draw.rectangle([x0, 360, x1, 465], fill=C_LIGHT_ORANGE, outline=C_BORDER)
        draw.text((x0 + 6, 365), "PAIN POINT / OPPORTUNITY:", fill=C_RED, font=get_font(8.5, bold=True))
        draw.text((x0 + 6, 382), stg['pain_point'], fill=C_SLATE, font=get_font(8))

    # Emotion Curve Area (between y=270 and y=350)
    draw.rectangle([20, 270, w - 20, 350], fill=(248, 250, 252), outline=C_BORDER)
    draw.text((25, 274), "EMOTIONAL VALENCE CURVE", fill=C_DARK_GREEN, font=get_font(8.5, bold=True))
    draw.line([(30, 310), (w - 30, 310)], fill=C_BORDER, width=1) # Neutral line

    # Plot emotion points
    pts = []
    for i, stg in enumerate(stages):
        cx = x_starts[i] + (col_w // 2)
        # score -2 (deep negative) to +2 (positive)
        val = stg.get('valence', 0)
        cy = 310 - (val * 16)
        pts.append((cx, cy))

    # Draw spline / polyline
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i+1]], fill=C_ORANGE, width=3)

    for i, (cx, cy) in enumerate(pts):
        draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=C_DARK_GREEN, outline=C_ORANGE, width=2)
        score_txt = stages[i].get('valence_label', 'Neutral')
        draw.text((cx - 16, cy + 8), score_txt, fill=C_SLATE, font=get_font(8, bold=True))

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path


def create_ideation_graphic(filename):
    """
    Renders an infographic summarizing Brainwriting, Crazy 8s, and SCAMPER.
    """
    w, h = 900, 460
    img = Image.new('RGB', (w, h), C_CREAM)
    draw = ImageDraw.Draw(img)

    draw.rectangle([10, 10, w - 10, h - 10], outline=C_DARK_GREEN, width=2)
    draw.rectangle([10, 10, w - 10, 55], fill=C_DARK_GREEN)
    draw.text((25, 18), "DIVERGENT IDEATION METHODOLOGIES (INT335 CP4)", fill=C_WHITE, font=get_font(18, bold=True))

    # 3 Columns for the 3 Methods
    col_w = (w - 40) // 3
    methods = [
        ("METHOD 1: BRAINWRITING 6-3-5", "Adapted for 4 team members: 4 rounds of silent idea expansion building on peer cards without premature judgment.", [
            "Round 1: 3 core communication concepts per member",
            "Round 2: Pass card to peer; add asynchronous layer",
            "Round 3: Integrate deduplication mechanisms",
            "Round 4: Synthesize 12 hybrid structural concepts"
        ], C_LIGHT_GREEN),
        ("METHOD 2: CRAZY 8s RAPID SKETCHES", "Fast visual ideation: 8 distinct solution sketches per member in 8 minutes, forcing divergent thinking.", [
            "Physical cabin electronic LED availability badge",
            "Centralized WhatsApp broadcast token bot",
            "Peer-to-peer student doubt upvote forum",
            "3-hour SLA academic fallback knowledge engine"
        ], C_WHITE),
        ("METHOD 3: SCAMPER FRAMEWORK", "Targeted morphological idea manipulation across 7 creative dimensions.", [
            "Substitute: Replace phone calls with structured tags",
            "Combine: Merge consultation booking with doubt logs",
            "Adapt: Adapt StackOverflow upvotes to university",
            "Eliminate: Kill duplicate questions via similarity"
        ], C_LIGHT_ORANGE)
    ]

    for i, (m_title, m_desc, m_bullets, m_bg) in enumerate(methods):
        x0 = 20 + i * col_w
        x1 = x0 + col_w - 8
        draw.rectangle([x0, 65, x1, h - 20], fill=m_bg, outline=C_BORDER)
        draw.rectangle([x0, 65, x1, 105], fill=C_DARK_GREEN)
        draw.text((x0 + 10, 78), m_title, fill=C_WHITE, font=get_font(11, bold=True))

        # Desc
        draw.text((x0 + 12, 115), m_desc[:120], fill=C_SLATE, font=get_font(9))

        # Bullets
        by = 175
        draw.text((x0 + 12, by), "Session Artifacts Generated:", fill=C_DARK_GREEN, font=get_font(10, bold=True))
        by += 22
        for b in m_bullets:
            draw.text((x0 + 12, by), "•", fill=C_ORANGE, font=get_font(11, bold=True))
            draw.text((x0 + 24, by), b[:38], fill=C_SLATE, font=get_font(9))
            by += 26

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path


def create_user_flow_graphic(filename):
    """
    Renders visual flowchart diagram of student and faculty journeys.
    """
    w, h = 900, 480
    img = Image.new('RGB', (w, h), C_WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([10, 10, w - 10, h - 10], outline=C_DARK_GREEN, width=2)
    draw.rectangle([10, 10, w - 10, 55], fill=C_DARK_GREEN)
    draw.text((25, 18), "END-TO-END SYSTEM USER FLOW ARCHITECTURE", fill=C_WHITE, font=get_font(18, bold=True))

    # Top Half: Student Flow
    draw.rectangle([20, 65, w - 20, 255], fill=C_CREAM, outline=C_BORDER)
    draw.rectangle([20, 65, w - 20, 95], fill=C_DARK_GREEN)
    draw.text((30, 72), "🎓 STUDENT ACADEMIC WORKFLOW", fill=C_WHITE, font=get_font(13, bold=True))

    # Steps for Student
    s_steps = [
        ("1. Login", "Enters LPU Reg ID"),
        ("2. Ask Doubt", "Selects Subject & Unit"),
        ("3. AI Deduplication", "Checks 60% Similarity"),
        ("4. Decision", "+1 Same Doubt OR Post New"),
        ("5. Resolution", "Notified via Official Answer")
    ]
    sw = 150
    for i, (title, sub) in enumerate(s_steps):
        sx0 = 35 + i * 170
        sy0 = 115
        draw.rectangle([sx0, sy0, sx0 + sw, sy0 + 65], fill=C_WHITE, outline=C_DARK_GREEN, width=2)
        draw.text((sx0 + 10, sy0 + 12), title, fill=C_DARK_GREEN, font=get_font(11, bold=True))
        draw.text((sx0 + 10, sy0 + 34), sub, fill=C_SLATE, font=get_font(8.5))
        if i < len(s_steps) - 1:
            draw.line([(sx0 + sw, sy0 + 32), (sx0 + sw + 20, sy0 + 32)], fill=C_ORANGE, width=3)

    # Bottom Half: Faculty Flow
    draw.rectangle([20, 270, w - 20, 460], fill=C_WHITE, outline=C_BORDER)
    draw.rectangle([20, 270, w - 20, 300], fill=C_DARK_GREEN)
    draw.text((30, 278), "👨‍🏫 FACULTY RESOLUTION WORKFLOW", fill=C_WHITE, font=get_font(13, bold=True))

    f_steps = [
        ("1. Teacher Console", "Hashed Credentials Login"),
        ("2. Review Queue", "Urgent Pending Doubts"),
        ("3. AI / Manual Mode", "1-Click AI OR Type Ans"),
        ("4. Direct Resolve", "Marks 'Resolved' Instantly"),
        ("5. Office Hours", "Approves Cabin Bookings")
    ]
    for i, (title, sub) in enumerate(f_steps):
        sx0 = 35 + i * 170
        sy0 = 325
        draw.rectangle([sx0, sy0, sx0 + sw, sy0 + 65], fill=C_CREAM, outline=C_ORANGE, width=2)
        draw.text((sx0 + 10, sy0 + 12), title, fill=C_DARK_GREEN, font=get_font(11, bold=True))
        draw.text((sx0 + 10, sy0 + 34), sub, fill=C_SLATE, font=get_font(8.5))
        if i < len(f_steps) - 1:
            draw.line([(sx0 + sw, sy0 + 32), (sx0 + sw + 20, sy0 + 32)], fill=C_DARK_GREEN, width=3)

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path


def create_testing_before_after(filename):
    """
    Renders visual before-and-after comparison of the 5 key evidence-based improvements.
    """
    w, h = 900, 480
    img = Image.new('RGB', (w, h), C_WHITE)
    draw = ImageDraw.Draw(img)

    draw.rectangle([10, 10, w - 10, h - 10], outline=C_DARK_GREEN, width=2)
    draw.rectangle([10, 10, w - 10, 55], fill=C_DARK_GREEN)
    draw.text((25, 18), "EVIDENCE-BASED BEFORE & AFTER PROTOTYPE IMPROVEMENTS (CP6)", fill=C_WHITE, font=get_font(16, bold=True))

    items = [
        ("1. Teacher Answer Drawer", "Drawer remained open after publishing; faculty confused if answer saved.", "Drawer closes automatically; doubt status updates directly to 'Resolved'.", C_LIGHT_GREEN),
        ("2. AI Answer Depth", "Rigid 1-paragraph generic response for all subjects.", "Deep academic synthesizer grounded in LPU syllabus with code and textbook citations.", C_WHITE),
        ("3. 1-Click AI Answering", "Faculty forced to click into doubt drawer to generate answer.", "Added direct 1-click 'Give Ans by AI' button on dashboard card queue.", C_LIGHT_GREEN),
        ("4. Mobile Touch Targets", "Small '+1' support button caused mis-clicks on mobile.", "Enlarged button target to 48px with clear supporter count badge.", C_WHITE)
    ]

    rw = (w - 40) // 2
    for idx, (title, before_txt, after_txt, bg) in enumerate(items):
        r_col = idx % 2
        r_row = idx // 2
        bx0 = 20 + r_col * rw
        by0 = 65 + r_row * 195
        bx1 = bx0 + rw - 8
        by1 = by0 + 185

        draw.rectangle([bx0, by0, bx1, by1], fill=bg, outline=C_BORDER)
        draw.rectangle([bx0, by0, bx1, by0 + 30], fill=C_DARK_GREEN)
        draw.text((bx0 + 10, by0 + 8), title, fill=C_WHITE, font=get_font(11, bold=True))

        # Before
        draw.rectangle([bx0 + 8, by0 + 38, bx1 - 8, by0 + 100], fill=(254, 242, 242), outline=C_RED)
        draw.text((bx0 + 14, by0 + 44), "❌ BEFORE (Observed Failure):", fill=C_RED, font=get_font(9, bold=True))
        draw.text((bx0 + 14, by0 + 60), before_txt[:110], fill=C_SLATE, font=get_font(8.5))

        # After
        draw.rectangle([bx0 + 8, by0 + 106, bx1 - 8, by1 - 8], fill=C_LIGHT_GREEN, outline=C_GREEN)
        draw.text((bx0 + 14, by0 + 112), "✅ AFTER (Implemented Fix):", fill=C_GREEN, font=get_font(9, bold=True))
        draw.text((bx0 + 14, by0 + 128), after_txt[:110], fill=C_SLATE, font=get_font(8.5))

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path


def generate_all_diagrams():
    """Generates all diagram image assets needed across checkpoints."""
    print("Generating Empathy Map: Student...")
    create_empathy_map(
        "Student Empathy Map",
        "Target: Undergraduate Engineering Students (LPU)",
        {
            'says': [
                '"Sir, are you free for 5 minutes?"',
                '"Did anyone ask about question 3 on WhatsApp?"',
                '"I waited outside his cabin for 40 minutes."',
                '"I was too embarrassed to knock on the door."'
            ],
            'thinks': [
                '"Will the professor think my doubt is stupid?"',
                '"What if he is busy grading or in a meeting?"',
                '"I really need this clarified before tomorrow\'s CA."',
                '"WhatsApp is completely flooded with irrelevant spam."'
            ],
            'does': [
                'Wanders Block 34/38 corridors searching cabins',
                'Repeatedly checks WhatsApp class groups',
                'Asks classmates before approaching faculty',
                'Gives up and resorts to unreliable YouTube tutorials'
            ],
            'feels': [
                'High anxiety before exams and continuous evaluations',
                'Hesitation and intimidation knocking on cabin doors',
                'Frustration over wasted walking and waiting transit',
                'Overwhelmed by scattered, unorganized communications'
            ]
        },
        "empathy_map_student.png"
    )

    print("Generating Empathy Map: Faculty...")
    create_empathy_map(
        "Faculty Empathy Map",
        "Target: Engineering Faculty & Course Coordinators (LPU)",
        {
            'says': [
                '"Please do not message me on WhatsApp after 8 PM."',
                '"I already explained this exact concept in Unit II."',
                '"Come during my free consultation hour on Thursday."',
                '"Email me your question with proper subject code."'
            ],
            'thinks': [
                '"I wish students checked if someone else asked this."',
                '"I have 3 lecture preps, research papers, and lab grading."',
                '"My personal phone number has become a 24/7 helpdesk."',
                '"I want to help sincere students, but I am exhausted."'
            ],
            'does': [
                'Answers identical questions repeatedly across sections',
                'Locks cabin door during research or continuous grading',
                'Receives unscheduled cabin knocks mid-thought',
                'Feels guilty when student doubts remain unaddressed'
            ],
            'feels': [
                'Overwhelmed by fragmented communication channels',
                'Fatigued by repetitive low-level syllabus queries',
                'Anxious about boundary invasion on personal messaging',
                'Frustrated by lack of structured consultation slots'
            ]
        },
        "empathy_map_faculty.png"
    )

    print("Generating Personas...")
    create_persona_card(
        "Rohan Patel",
        "2nd Year B.Tech CSE (Section K22GF) • Age: 20 • Commuter Student",
        "I just want clear, textbook-grounded answers without wasting an hour in cabin corridors.",
        [
            ("Section", "K22GF"),
            ("Attendance", "88%"),
            ("Tech Comfort", "High (Mobile/Web)"),
            ("Major Focus", "Data Structures & Java")
        ],
        [
            "Get fast, authoritative clarification on lecture doubts ahead of CAs.",
            "Know exactly when professors are physically free in cabins.",
            "Avoid asking redundant questions already answered for classmates."
        ],
        [
            "Cabin hunting between Block 34 and 38 only to find locked doors.",
            "WhatsApp groups buried under hundreds of unrelated messages.",
            "Intimidation when asking questions in front of 60 peers in lecture hall."
        ],
        "persona_student_rohan.png"
    )

    create_persona_card(
        "Dr. Rajesh Sharma",
        "Associate Professor & INT335 Course Lead • Cabin: Block 34-601",
        "I love teaching, but answering the same doubt 30 times on WhatsApp drains my research energy.",
        [
            ("Teaching Load", "3 Courses (180+ Students)"),
            ("Cabin", "Block 34, Cabin 601"),
            ("Experience", "12 Years Academic"),
            ("Key Focus", "Design Thinking & Algorithms")
        ],
        [
            "Protect deep-work hours for research, curriculum development, and grading.",
            "Answer student academic queries efficiently without redundant repetition.",
            "Maintain organized, scheduled face-to-face consultation hours in cabin."
        ],
        [
            "Receiving 20-30 identical questions about SCAMPER before assignment deadlines.",
            "Unscheduled door knocks during confidential evaluation grading.",
            "Blurry boundaries between personal WhatsApp life and academic consultations."
        ],
        "persona_faculty_dr_sharma.png"
    )

    print("Generating Journey Maps...")
    create_journey_map(
        "Current Student Experience: Journey Map",
        [
            {
                'name': 'Doubt Emerges',
                'actions': 'Studies lecture notes at hostel; gets stuck on concept.',
                'thoughts': 'This wasn\'t clear in lecture today.',
                'pain_point': 'No immediate way to verify textbook accuracy.',
                'valence': 0,
                'valence_label': 'Confused'
            },
            {
                'name': 'Search for Info',
                'actions': 'Checks WhatsApp group; asks roommates.',
                'thoughts': 'Group has 200 unread memes and spam.',
                'pain_point': 'Scattered, unsearchable chat messages.',
                'valence': -1,
                'valence_label': 'Frustrated'
            },
            {
                'name': 'Cabin Transit',
                'actions': 'Walks from Block 28 to Block 34 in 35°C heat.',
                'thoughts': 'Hope sir is in his cabin today.',
                'pain_point': 'Zero visibility of professor\'s physical schedule.',
                'valence': -1,
                'valence_label': 'Anxious'
            },
            {
                'name': 'Corridor Wait',
                'actions': 'Finds cabin closed; waits on staircase 30 mins.',
                'thoughts': 'Did he go for lunch or a departmental meeting?',
                'pain_point': 'Wasted time; missed next lecture preparation.',
                'valence': -2,
                'valence_label': 'Defeated'
            },
            {
                'name': 'Resolution / Loss',
                'actions': 'Gives up; turns to random YouTube video or skips.',
                'thoughts': 'I guess I\'ll just wing this in the CA.',
                'pain_point': 'Academic concept remains fundamentally unmastered.',
                'valence': -2,
                'valence_label': 'Hopeless'
            }
        ],
        "journey_map_student.png"
    )

    create_journey_map(
        "Current Faculty Experience: Journey Map",
        [
            {
                'name': 'Lecture Delivery',
                'actions': 'Delivers 50-minute lecture to 65 students in hall.',
                'thoughts': 'Covered syllabus, but some students seemed hesitant.',
                'pain_point': 'Limited time for 1-on-1 questions during lecture.',
                'valence': 1,
                'valence_label': 'Engaged'
            },
            {
                'name': 'Cabin Return',
                'actions': 'Returns to cabin to grade mid-term evaluation papers.',
                'thoughts': 'Need 2 uninterrupted hours for university grading.',
                'pain_point': 'Knocks at door begin within 10 minutes.',
                'valence': 0,
                'valence_label': 'Guarded'
            },
            {
                'name': 'Unscheduled Knocks',
                'actions': 'Answers door; 3 students ask same question consecutively.',
                'thoughts': 'I literally just answered this 5 minutes ago.',
                'pain_point': 'Extreme cognitive fragmentation and frustration.',
                'valence': -1,
                'valence_label': 'Interrupted'
            },
            {
                'name': 'WhatsApp Flood',
                'actions': 'Opens phone at 9 PM; 45 unread doubt messages.',
                'thoughts': 'My personal evening is completely gone.',
                'pain_point': 'No boundary between work and personal life.',
                'valence': -2,
                'valence_label': 'Overwhelmed'
            },
            {
                'name': 'Backlog Fatigue',
                'actions': 'Types copy-paste replies; leaves half unread.',
                'thoughts': 'I feel guilty, but this system is unsustainable.',
                'pain_point': 'Faculty burnout; delayed support for sincere doubts.',
                'valence': -1,
                'valence_label': 'Burnout'
            }
        ],
        "journey_map_faculty.png"
    )

    print("Generating Ideation & System Graphics...")
    create_ideation_graphic("ideation_methods_crazy8s.png")
    create_user_flow_graphic("user_flow_student_faculty.png")
    create_testing_before_after("before_after_testing_fixes.png")

    print("All diagram assets successfully created in:", ASSETS_DIR)

if __name__ == '__main__':
    generate_all_diagrams()
