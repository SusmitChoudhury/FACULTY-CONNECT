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


def create_step_by_step_user_flow(filename):
    """
    Renders a clean academic, step-by-step user flow diagram in black and white
    matching the GitHub flowchart with numbered stages, decision diamonds, and paths.
    """
    w, h = 920, 600
    img = Image.new('RGB', (w, h), C_WHITE)
    draw = ImageDraw.Draw(img)

    # Frame border
    draw.rectangle([10, 10, w - 10, h - 10], outline=C_BLACK, width=2)

    # Header Bar
    draw.rectangle([10, 10, w - 10, 50], fill=(245, 245, 245), outline=C_BLACK, width=1)
    draw.text((25, 16), "FACULTY CONNECT: END-TO-END STEP-BY-STEP USER FLOW", fill=C_BLACK, font=get_font(16, bold=True))
    draw.text((w - 280, 20), "FORMAL ACADEMIC ARCHITECTURE", fill=C_BLACK, font=get_font(10, bold=True))

    # SECTION 1: STUDENT FLOW (y: 60 to 220)
    draw.rectangle([20, 60, w - 20, 230], fill=(255, 255, 255), outline=C_BLACK, width=1)
    draw.rectangle([20, 60, w - 20, 85], fill=(240, 240, 240), outline=C_BLACK, width=1)
    draw.text((30, 66), "STAGE 1: STUDENT ACADEMIC INQUIRY & DEDUPLICATION FLOW", fill=C_BLACK, font=get_font(11, bold=True))

    # Boxes for Student Flow
    # Box 1: Login
    draw.rectangle([35, 100, 165, 155], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((45, 108), "Step 1: Auth", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((45, 124), "Student Login via", fill=C_BLACK, font=get_font(8.5))
    draw.text((45, 136), "LPU Registration ID", fill=C_BLACK, font=get_font(8.5))

    # Arrow 1->2
    draw.line([(165, 127), (195, 127)], fill=C_BLACK, width=2)
    draw.polygon([(195, 127), (188, 123), (188, 131)], fill=C_BLACK)

    # Box 2: Scope
    draw.rectangle([195, 100, 335, 155], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((205, 108), "Step 2: Scoping", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((205, 124), "Selects Course, Unit,", fill=C_BLACK, font=get_font(8.5))
    draw.text((205, 136), "Topic & Lecture Date", fill=C_BLACK, font=get_font(8.5))

    # Arrow 2->3
    draw.line([(335, 127), (365, 127)], fill=C_BLACK, width=2)
    draw.polygon([(365, 127), (358, 123), (358, 131)], fill=C_BLACK)

    # Box 3: Query
    draw.rectangle([365, 100, 495, 155], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((375, 108), "Step 3: Input", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((375, 124), "Types Academic Doubt", fill=C_BLACK, font=get_font(8.5))
    draw.text((375, 136), "Text & Math Formulas", fill=C_BLACK, font=get_font(8.5))

    # Arrow 3->Diamond
    draw.line([(495, 127), (530, 127)], fill=C_BLACK, width=2)
    draw.polygon([(530, 127), (523, 123), (523, 131)], fill=C_BLACK)

    # Decision Diamond (center 585, 127; radius 55, 32)
    cx, cy, rx, ry = 585, 127, 55, 32
    draw.polygon([(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)], fill=(245, 245, 245), outline=C_BLACK)
    draw.text((cx - 42, cy - 14), "Semantic Check", fill=C_BLACK, font=get_font(8.5, bold=True))
    draw.text((cx - 44, cy + 2), "(Similarity >= 60%)", fill=C_BLACK, font=get_font(8))

    # Branch A: YES (Match found) -> Upward to 5A
    draw.line([(cx, cy - ry), (cx, cy - ry - 20), (690, cy - ry - 20)], fill=C_BLACK, width=2)
    draw.polygon([(690, cy - ry - 20), (683, cy - ry - 24), (683, cy - ry - 16)], fill=C_BLACK)
    draw.text((cx + 5, cy - ry - 15), "YES (Duplicate)", fill=C_BLACK, font=get_font(8, bold=True))

    draw.rectangle([690, 70, 890, 120], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((700, 76), "Step 4A: Duplicate Modal", fill=C_BLACK, font=get_font(9.5, bold=True))
    draw.text((700, 92), "Inspects classmate's doubt.", fill=C_BLACK, font=get_font(8))
    draw.text((700, 104), "Clicks '+1 - I Have Same Doubt'", fill=C_BLACK, font=get_font(8, bold=True))

    # Branch B: NO (Unique query) -> Straight to 5B
    draw.line([(cx + rx, cy), (690, cy)], fill=C_BLACK, width=2)
    draw.polygon([(690, cy), (683, cy - 4), (683, cy + 4)], fill=C_BLACK)
    draw.text((cx + rx + 5, cy - 12), "NO (Unique)", fill=C_BLACK, font=get_font(8, bold=True))

    draw.rectangle([690, 140, 890, 195], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((700, 146), "Step 4B: Enters Queue", fill=C_BLACK, font=get_font(9.5, bold=True))
    draw.text((700, 162), "Query published directly to", fill=C_BLACK, font=get_font(8))
    draw.text((700, 174), "Teacher's Section Queue", fill=C_BLACK, font=get_font(8, bold=True))

    # SECTION 2: 3-HOUR SLA AI SAFETY NET (y: 240 to 350)
    draw.rectangle([20, 240, w - 20, 360], fill=(255, 255, 255), outline=C_BLACK, width=1)
    draw.rectangle([20, 240, w - 20, 265], fill=(240, 240, 240), outline=C_BLACK, width=1)
    draw.text((30, 246), "STAGE 2: ASYNCHRONOUS 3-HOUR SLA TIMER & AI FALLBACK ENGINE", fill=C_BLACK, font=get_font(11, bold=True))

    # Steps for SLA
    draw.rectangle([35, 280, 260, 340], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((45, 288), "Daemon Background Timer", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((45, 306), "Monitors all pending doubts.", fill=C_BLACK, font=get_font(8.5))
    draw.text((45, 320), "Tracks 3-hour SLA window.", fill=C_BLACK, font=get_font(8.5))

    draw.line([(260, 310), (330, 310)], fill=C_BLACK, width=2)
    draw.polygon([(330, 310), (323, 306), (323, 314)], fill=C_BLACK)

    # SLA Diamond (center 400, 310)
    cx, cy, rx, ry = 400, 310, 70, 32
    draw.polygon([(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)], fill=(245, 245, 245), outline=C_BLACK)
    draw.text((cx - 56, cy - 12), "Faculty Resolved", fill=C_BLACK, font=get_font(8.5, bold=True))
    draw.text((cx - 60, cy + 4), "Within 3 Hours?", fill=C_BLACK, font=get_font(8.5, bold=True))

    # SLA YES -> Goes to Faculty Workflow
    draw.line([(cx, cy + ry), (cx, 380)], fill=C_BLACK, width=2)
    draw.polygon([(cx, 380), (cx - 4, 373), (cx + 4, 373)], fill=C_BLACK)
    draw.text((cx + 6, cy + ry + 10), "YES: Normal Review", fill=C_BLACK, font=get_font(8, bold=True))

    # SLA NO -> Triggers AI
    draw.line([(cx + rx, cy), (570, cy)], fill=C_BLACK, width=2)
    draw.polygon([(570, cy), (563, cy - 4), (563, cy + 4)], fill=C_BLACK)
    draw.text((cx + rx + 10, cy - 12), "NO (Overdue)", fill=C_BLACK, font=get_font(8, bold=True))

    draw.rectangle([570, 280, 890, 340], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((580, 288), "Automated Academic AI Synthesizer", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((580, 306), "Generates syllabus-grounded explanation with code & textbook references.", fill=C_BLACK, font=get_font(8.5))
    draw.text((580, 320), "Status marked 'AI Answered' • Student unblocked • Remains in queue for teacher.", fill=C_BLACK, font=get_font(8.5, bold=True))

    # SECTION 3: FACULTY RESOLUTION & APPOINTMENTS (y: 370 to 585)
    draw.rectangle([20, 370, w - 20, 585], fill=(255, 255, 255), outline=C_BLACK, width=1)
    draw.rectangle([20, 370, w - 20, 395], fill=(240, 240, 240), outline=C_BLACK, width=1)
    draw.text((30, 376), "STAGE 3: FACULTY CONSOLE RESOLUTION & CABIN CONSULTATION BOOKING", fill=C_BLACK, font=get_font(11, bold=True))

    # Steps for Faculty
    draw.rectangle([35, 410, 220, 475], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((45, 418), "Faculty Review Queue", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((45, 436), "Views urgent pending doubts.", fill=C_BLACK, font=get_font(8.5))
    draw.text((45, 452), "Cards show '+1' impact count.", fill=C_BLACK, font=get_font(8.5))

    draw.line([(220, 442), (260, 442)], fill=C_BLACK, width=2)
    draw.polygon([(260, 442), (253, 438), (253, 446)], fill=C_BLACK)

    # Resolution Choice Box
    draw.rectangle([260, 410, 480, 475], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((270, 418), "Choose Resolution Mode", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((270, 436), "Mode A: 1-Click 'Give Ans by AI'", fill=C_BLACK, font=get_font(8.5, bold=True))
    draw.text((270, 452), "Mode B: Draft Official Solution", fill=C_BLACK, font=get_font(8.5, bold=True))

    draw.line([(480, 442), (520, 442)], fill=C_BLACK, width=2)
    draw.polygon([(520, 442), (513, 438), (513, 446)], fill=C_BLACK)

    # Direct Resolve Box
    draw.rectangle([520, 410, 710, 475], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((530, 418), "Instant 'Resolved' State", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((530, 436), "Status updates directly.", fill=C_BLACK, font=get_font(8.5))
    draw.text((530, 452), "Drawer auto-closes.", fill=C_BLACK, font=get_font(8.5, bold=True))

    draw.line([(710, 442), (745, 442)], fill=C_BLACK, width=2)
    draw.polygon([(745, 442), (738, 438), (738, 446)], fill=C_BLACK)

    # Broadcast Box
    draw.rectangle([745, 410, 890, 475], fill=(255, 255, 255), outline=C_BLACK, width=2)
    draw.text((755, 418), "Instant Notification", fill=C_BLACK, font=get_font(10, bold=True))
    draw.text((755, 436), "Pushed to author & all", fill=C_BLACK, font=get_font(8.5))
    draw.text((755, 452), "'+1' supporters at once.", fill=C_BLACK, font=get_font(8.5, bold=True))

    # Row 2 in Section 3: Office Hours Booking
    draw.rectangle([35, 495, 890, 565], fill=(255, 255, 255), outline=C_BLACK, width=1)
    draw.text((45, 502), "PARALLEL WORKFLOW: CABIN CONSULTATION APPOINTMENT LEDGER", fill=C_BLACK, font=get_font(9.5, bold=True))
    draw.text((45, 520), "1. Student checks real-time cabin consultation slots -> 2. Selects date/time & submits reason ->", fill=C_BLACK, font=get_font(8.5))
    draw.text((45, 536), "3. Faculty reviews in Appointments tab -> 4. Accepts with preparation notes -> 5. Both parties confirmed without corridor wait.", fill=C_BLACK, font=get_font(8.5))

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    return out_path


def create_figma_system_architecture(filename):
    """
    Renders detailed Figma-like UI screen architecture matching live application
    (Layout, Navigation, Typography, Colors, Spacing, Buttons, Forms, Cards, Tables, Icons).
    """
    w, h = 920, 560
    img = Image.new('RGB', (w, h), C_WHITE)
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([10, 10, w - 10, h - 10], outline=C_BLACK, width=2)

    # Header Bar
    draw.rectangle([10, 10, w - 10, 50], fill=(245, 245, 245), outline=C_BLACK, width=1)
    draw.text((25, 16), "FIGMA UI/UX DESIGN SYSTEM SPECIFICATIONS (P09 — FACULTY CONNECT)", fill=C_BLACK, font=get_font(16, bold=True))
    draw.text((w - 280, 20), "LIVE APP CODE-CONNECT PARITY", fill=C_BLACK, font=get_font(10, bold=True))

    # 4 Design System Columns
    col_w = (w - 40) // 4
    cols = [
        ("1. BRAND TOKENS", [
            ("Primary Nav Green", "#15370D"),
            ("Background Cream", "#FCF9EA"),
            ("Orange Accent", "#F2842F"),
            ("Primary Text", "#000000"),
            ("Border Line", "#CBD5E1"),
            ("Typography", "Inter / Outfit"),
            ("Grid System", "8px Spatial Baseline"),
            ("Border Radius", "8px Cards / 6px Inputs")
        ]),
        ("2. CORE COMPONENTS", [
            ("Navbar Header", "Global Dark Green Bar"),
            ("Role Switcher", "Student / Faculty toggle"),
            ("Doubt Card", "Course, Topic, Author, +1"),
            ("Duplicate Modal", "Classmate doubt preview"),
            ("Answer Drawer", "Markdown & Math support"),
            ("Availability Card", "Cabin slot reservation"),
            ("Analytics Table", "Section-wise confusion"),
            ("Permanent Footer", "Team registration info")
        ]),
        ("3. INTERACTION PATTERNS", [
            ("Semantic Typing", "Auto-checks 60% similarity"),
            ("'+1' Action", "Single-click support link"),
            ("1-Click AI Answer", "Synthesizes syllabus draft"),
            ("Publish Action", "Sets doubt to 'Resolved'"),
            ("Auto-Drawer Close", "setSelectedDoubt(null)"),
            ("Status Badges", "Pending / AI / Resolved"),
            ("Conflict Check", "Prevents double-booking"),
            ("CSV Export", "Downloads empirical report")
        ]),
        ("4. PRODUCTION FRAMES", [
            ("F01: Welcome Entry", "Role picker & credentials"),
            ("F02: Student Home", "Subject cards & notifications"),
            ("F03: Ask a Doubt", "Dynamic unit/topic cascade"),
            ("F04: Deduplication", "+1 Same Doubt modal"),
            ("F05: Answer View", "Verified textbook solution"),
            ("F06: Cabin Booking", "Time slot reservation"),
            ("F07: Teacher Console", "Urgent cards with 1-click AI"),
            ("F08: Confusion Stats", "Course confusion heatmaps")
        ])
    ]

    for i, (col_title, items) in enumerate(cols):
        cx0 = 20 + i * col_w
        cx1 = cx0 + col_w - 6
        draw.rectangle([cx0, 60, cx1, h - 20], fill=(255, 255, 255), outline=C_BLACK, width=1)
        draw.rectangle([cx0, 60, cx1, 95], fill=(240, 240, 240), outline=C_BLACK, width=1)
        draw.text((cx0 + 10, 72), col_title, fill=C_BLACK, font=get_font(11, bold=True))

        cy = 110
        for label, val in items:
            draw.text((cx0 + 10, cy), "• " + label + ":", fill=C_BLACK, font=get_font(9.5, bold=True))
            draw.text((cx0 + 20, cy + 14), val[:32], fill=(60, 60, 60), font=get_font(8.5))
            cy += 36

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
        "Anonymous Student",
        "Role: Student",
        "I just want clear, textbook-grounded answers without wasting an hour waiting outside faculty cabins.",
        [
            ("Role", "Student"),
            ("Attendance", "Regular"),
            ("Tech Comfort", "High (Mobile/Web)"),
            ("Primary Goal", "Clear Academic Doubts")
        ],
        [
            "Get fast, authoritative clarification on lecture doubts ahead of examinations.",
            "Know exactly when professors are physically free in cabins.",
            "Avoid asking redundant questions already answered for classmates."
        ],
        [
            "Cabin hunting across campus corridors only to find locked doors.",
            "WhatsApp groups buried under hundreds of unrelated messages.",
            "Intimidation when asking questions in front of peers in lecture hall."
        ],
        "persona_student_rohan.png"
    )

    create_persona_card(
        "Anonymous Faculty",
        "Role: Faculty",
        "I want to support sincere students, but answering identical questions repeatedly drains my academic energy.",
        [
            ("Role", "Faculty"),
            ("Responsibilities", "Course Instruction & Evaluation"),
            ("Mode", "In-Person & Digital Guidance"),
            ("Primary Goal", "Pedagogical Clarity")
        ],
        [
            "Protect deep-work hours for research, curriculum development, and grading.",
            "Answer student academic queries efficiently without redundant repetition.",
            "Maintain organized, scheduled face-to-face consultation hours in cabin."
        ],
        [
            "Receiving repetitive identical questions before assignment deadlines.",
            "Unscheduled door knocks during confidential evaluation grading.",
            "Blurry boundaries between personal life and academic consultations."
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
    create_step_by_step_user_flow("user_flow_step_by_step_academic.png")
    create_figma_system_architecture("figma_design_system_preview.png")

    print("All diagram assets successfully created in:", ASSETS_DIR)

if __name__ == '__main__':
    generate_all_diagrams()
