import os
from PIL import Image, ImageDraw, ImageFont

ASSETS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets'))
os.makedirs(ASSETS_DIR, exist_ok=True)

# Colors
C_DARK_BG = (35, 39, 42)
C_DARK_CONTAINER = (45, 52, 58)
C_DARK_HEADER = (25, 30, 34)
C_GREEN_BORDER = (21, 55, 13)
C_ORANGE_BORDER = (242, 132, 47)
C_PURPLE_BORDER = (150, 115, 166)
C_SUCCESS_BORDER = (130, 179, 102)
C_DIAMOND_BORDER = (214, 182, 86)

C_CREAM_FILL = (252, 249, 234)
C_WHITE_FILL = (255, 255, 255)
C_YELLOW_FILL = (255, 242, 204)
C_PURPLE_FILL = (225, 213, 231)
C_SUCCESS_FILL = (213, 232, 212)
C_ORANGE_LIGHT = (255, 245, 237)

C_BLACK_TEXT = (0, 0, 0)
C_WHITE_TEXT = (255, 255, 255)
C_GRAY_TEXT = (200, 205, 210)
C_ARROW_GRAY = (180, 185, 190)

def get_font(size=14, bold=False):
    font_paths = [
        "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
        "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
        "C:\\Windows\\Fonts\\calibrib.ttf" if bold else "C:\\Windows\\Fonts\\calibri.ttf"
    ]
    for p in font_paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

def draw_rounded_rect(draw, bbox, fill, outline, width=2, radius=6):
    draw.rounded_rectangle(bbox, radius=radius, fill=fill, outline=outline, width=width)

def draw_diamond(draw, center, rx, ry, fill, outline, width=2):
    cx, cy = center
    pts = [(cx, cy - ry), (cx + rx, cy), (cx, cy + ry), (cx - rx, cy)]
    draw.polygon(pts, fill=fill, outline=outline)
    if width > 1:
        draw.line([pts[0], pts[1], pts[2], pts[3], pts[0]], fill=outline, width=width)

def draw_arrow(draw, start, end, color=C_ARROW_GRAY, width=2):
    draw.line([start, end], fill=color, width=width)
    # Arrowhead
    x1, y1 = start
    x2, y2 = end
    if x1 == x2: # Vertical
        if y2 > y1: # Down
            draw.polygon([(x2, y2), (x2 - 4, y2 - 7), (x2 + 4, y2 - 7)], fill=color)
        else: # Up
            draw.polygon([(x2, y2), (x2 - 4, y2 + 7), (x2 + 4, y2 + 7)], fill=color)
    elif y1 == y2: # Horizontal
        if x2 > x1: # Right
            draw.polygon([(x2, y2), (x2 - 7, y2 - 4), (x2 - 7, y2 + 4)], fill=color)
        else: # Left
            draw.polygon([(x2, y2), (x2 + 7, y2 - 4), (x2 + 7, y2 + 4)], fill=color)


# =============================================================================
# 1. GITHUB MERMAID USER FLOW (EXACT REPLICA OF USER SCREENSHOTS)
# =============================================================================
def generate_github_mermaid_user_flow(filename="github_mermaid_user_flow.png"):
    """
    Builds the exact visual flowchart matching the GitHub screenshots uploaded by the user:
    - 4 clear subgraphs
    - Distinct node colors (cream, orange, yellow diamond, purple AI, green success)
    - Full vertical layout with clear branching paths
    """
    w, h = 1100, 1500
    img = Image.new('RGB', (w, h), (26, 29, 33)) # Dark GitHub-style canvas
    draw = ImageDraw.Draw(img)

    # Main Title
    draw.text((35, 25), "FACULTY CONNECT — OFFICIAL SYSTEM USER FLOW ARCHITECTURE", fill=C_WHITE_TEXT, font=get_font(20, bold=True))
    draw.text((35, 55), "INT335 Design Thinking (P09) • Lovely Professional University", fill=(160, 170, 180), font=get_font(12))

    # -------------------------------------------------------------------------
    # SUBGRAPH 4 (LEFT): CABIN CONSULTATION BOOKING
    # -------------------------------------------------------------------------
    c4_box = [35, 100, 310, 680]
    draw.rounded_rectangle(c4_box, radius=8, fill=(38, 44, 50), outline=(70, 80, 90), width=1)
    draw.text((50, 115), "📅 4. CABIN CONSULTATION BOOKING", fill=C_WHITE_TEXT, font=get_font(12, bold=True))

    # C1
    draw_rounded_rect(draw, [55, 160, 290, 240], fill=C_CREAM_FILL, outline=C_GREEN_BORDER, width=2)
    draw.text((75, 180), "Student Views Live\nFaculty Cabin\nConsultation Hours", fill=C_BLACK_TEXT, font=get_font(11, bold=True))

    draw_arrow(draw, (172, 240), (172, 275))

    # C2
    draw_rounded_rect(draw, [55, 275, 290, 355], fill=C_CREAM_FILL, outline=C_GREEN_BORDER, width=2)
    draw.text((80, 295), "Select Date,\nTime Slot &\nState Academic Reason", fill=C_BLACK_TEXT, font=get_font(11, bold=True))

    draw_arrow(draw, (172, 355), (172, 390))

    # C3
    draw_rounded_rect(draw, [55, 390, 290, 470], fill=C_WHITE_FILL, outline=C_ORANGE_BORDER, width=2)
    draw.text((75, 410), "Faculty Reviews\nRequest in\nAppointments Tab", fill=C_BLACK_TEXT, font=get_font(11, bold=True))

    draw_arrow(draw, (172, 470), (172, 505))

    # C4
    draw_rounded_rect(draw, [55, 505, 290, 585], fill=C_WHITE_FILL, outline=C_ORANGE_BORDER, width=2)
    draw.text((75, 520), "Accept Slot +\nAttach Preparation\nGuidance", fill=C_BLACK_TEXT, font=get_font(11, bold=True))

    draw_arrow(draw, (172, 585), (172, 620))

    # C5
    draw_rounded_rect(draw, [55, 620, 290, 660], fill=C_SUCCESS_FILL, outline=C_SUCCESS_BORDER, width=2)
    draw.text((70, 628), "In-Person Cabin Session\nConfirmed with Calendar", fill=C_BLACK_TEXT, font=get_font(10, bold=True))

    # -------------------------------------------------------------------------
    # SUBGRAPH 1 (TOP RIGHT): STUDENT ACADEMIC JOURNEY
    # -------------------------------------------------------------------------
    s1_box = [335, 100, 1060, 680]
    draw.rounded_rectangle(s1_box, radius=8, fill=(38, 44, 50), outline=(70, 80, 90), width=1)
    draw.text((350, 115), "🎓 1. STUDENT ACADEMIC JOURNEY", fill=C_WHITE_TEXT, font=get_font(12, bold=True))

    # Node S1
    draw_rounded_rect(draw, [620, 140, 830, 205], fill=C_CREAM_FILL, outline=C_GREEN_BORDER, width=2)
    draw.text((645, 158), "Student Logs In\nvia LPU Registration ID", fill=C_BLACK_TEXT, font=get_font(11, bold=True))

    draw_arrow(draw, (725, 205), (725, 230))

    # Node S2
    draw_rounded_rect(draw, [620, 230, 830, 295], fill=C_CREAM_FILL, outline=C_GREEN_BORDER, width=2)
    draw.text((635, 248), "Select Course, Unit,\nTopic & Lecture Date", fill=C_BLACK_TEXT, font=get_font(11, bold=True))

    draw_arrow(draw, (725, 295), (725, 320))

    # Node S3
    draw_rounded_rect(draw, [620, 320, 830, 385], fill=C_CREAM_FILL, outline=C_GREEN_BORDER, width=2)
    draw.text((645, 342), "Enter Academic\nQuestion", fill=C_BLACK_TEXT, font=get_font(11, bold=True))

    draw_arrow(draw, (725, 385), (725, 415))

    # Diamond S4: Semantic Similarity Check
    draw_diamond(draw, (725, 475), 95, 55, fill=C_YELLOW_FILL, outline=C_DIAMOND_BORDER, width=2)
    draw.text((665, 465), "Smart Semantic\nSimilarity Check", fill=C_BLACK_TEXT, font=get_font(10.5, bold=True))

    # Path A: Duplicate (Downwards Left)
    draw_arrow(draw, (670, 520), (580, 560))
    draw.text((550, 532), "Similarity >= 60%", fill=(180, 190, 200), font=get_font(10, bold=True))

    # Duplicate Box
    draw_rounded_rect(draw, [500, 560, 660, 615], fill=C_YELLOW_FILL, outline=C_DIAMOND_BORDER, width=2)
    draw.text((520, 575), "Duplicate Question\nDetected!", fill=C_BLACK_TEXT, font=get_font(11, bold=True))

    # Path to Option A (+1) & Option B (Distinct)
    draw_arrow(draw, (550, 615), (460, 650))
    draw_arrow(draw, (610, 615), (690, 650))

    # Option A (+1)
    draw_rounded_rect(draw, [360, 650, 530, 715], fill=C_WHITE_FILL, outline=C_GREEN_BORDER, width=2)
    draw.text((375, 668), "Option A: Click\n'+1 - I Have the\nSame Doubt'", fill=C_BLACK_TEXT, font=get_font(10, bold=True))

    # Option B (Distinct)
    draw_rounded_rect(draw, [600, 650, 770, 715], fill=C_WHITE_FILL, outline=C_GREEN_BORDER, width=2)
    draw.text((620, 668), "Option B:\nSubmit as Distinct\nQuestion", fill=C_BLACK_TEXT, font=get_font(10, bold=True))

    # Success Box (+1 linked)
    draw_rounded_rect(draw, [360, 745, 530, 810], fill=C_SUCCESS_FILL, outline=C_SUCCESS_BORDER, width=2)
    draw.text((375, 758), "Classmate Linked to\nQuestion (Zero\nFaculty Clutter)", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))
    draw_arrow(draw, (445, 715), (445, 745))

    # Unique Query Path (from Diamond right down to Queue)
    draw.line([(820, 475), (930, 475), (930, 740)], fill=C_ARROW_GRAY, width=2)
    draw.text((840, 455), "Unique Query", fill=(180, 190, 200), font=get_font(10, bold=True))

    # Distinct query joins into Queue
    draw.line([(685, 715), (685, 740), (840, 740)], fill=C_ARROW_GRAY, width=2)

    # Queue Box
    draw_rounded_rect(draw, [760, 745, 960, 810], fill=C_CREAM_FILL, outline=C_GREEN_BORDER, width=2)
    draw.text((785, 760), "Doubt Published to\nFaculty Section\nQueue", fill=C_BLACK_TEXT, font=get_font(10.5, bold=True))
    draw_arrow(draw, (930, 740), (930, 745))

    # -------------------------------------------------------------------------
    # SUBGRAPH 2: 3-HOUR AUTOMATIC AI SAFETY NET
    # -------------------------------------------------------------------------
    s2_box = [335, 835, 1060, 1140]
    draw.rounded_rectangle(s2_box, radius=8, fill=(38, 44, 50), outline=(70, 80, 90), width=1)
    draw.text((350, 848), "⏱️ 2. 3-HOUR AUTOMATIC AI SAFETY NET", fill=C_WHITE_TEXT, font=get_font(12, bold=True))

    # Connect from Queue to 3-hour diamond
    draw_arrow(draw, (860, 810), (860, 875))

    # Diamond: Faculty Responds Within 3 Hours?
    draw_diamond(draw, (860, 930), 105, 52, fill=C_YELLOW_FILL, outline=C_DIAMOND_BORDER, width=2)
    draw.text((790, 920), "Faculty Responds\nWithin 3 Hours?", fill=C_BLACK_TEXT, font=get_font(10.5, bold=True))

    # Path NO (SLA Exceeded) -> Downward to AI engine
    draw_arrow(draw, (860, 982), (860, 1015))
    draw.text((870, 990), "No (3-Hour SLA Exceeded)", fill=(210, 180, 230), font=get_font(9.5, bold=True))

    # Purple Box 1: Timer triggers
    draw_rounded_rect(draw, [740, 1015, 980, 1060], fill=C_PURPLE_FILL, outline=C_PURPLE_BORDER, width=2)
    draw.text((760, 1028), "Server Daemon Timer Service Triggers", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))

    draw_arrow(draw, (860, 1060), (860, 1080))

    # Purple Box 2: Synthesize Answer
    draw_rounded_rect(draw, [740, 1080, 980, 1125], fill=C_PURPLE_FILL, outline=C_PURPLE_BORDER, width=2)
    draw.text((750, 1092), "Generate Syllabus-Grounded Answer", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))

    # -------------------------------------------------------------------------
    # SUBGRAPH 3: FACULTY EVALUATION & RESOLUTION
    # -------------------------------------------------------------------------
    s3_box = [335, 1160, 1060, 1470]
    draw.rounded_rectangle(s3_box, radius=8, fill=(38, 44, 50), outline=(70, 80, 90), width=1)
    draw.text((350, 1172), "👨‍🏫 3. FACULTY EVALUATION & RESOLUTION", fill=C_WHITE_TEXT, font=get_font(12, bold=True))

    # Path YES (Within 3 Hours) from Diamond down to Teacher Console
    draw.line([(755, 930), (520, 930), (520, 1195)], fill=C_ARROW_GRAY, width=2)
    draw.text((530, 915), "Yes (Within 3 Hours)", fill=(160, 220, 160), font=get_font(10, bold=True))
    draw_arrow(draw, (520, 1195), (520, 1205))

    # Also connection from AI review queue to Teacher Console
    draw.line([(860, 1125), (860, 1150), (620, 1150), (620, 1205)], fill=C_ARROW_GRAY, width=2)

    # Teacher Opens Console
    draw_rounded_rect(draw, [470, 1205, 680, 1255], fill=C_WHITE_FILL, outline=C_ORANGE_BORDER, width=2)
    draw.text((495, 1222), "Teacher Opens Faculty Console", fill=C_BLACK_TEXT, font=get_font(10.5, bold=True))

    draw_arrow(draw, (575, 1255), (575, 1275))

    # Diamond: Choose Resolution Method
    draw_diamond(draw, (575, 1315), 85, 40, fill=C_YELLOW_FILL, outline=C_DIAMOND_BORDER, width=2)
    draw.text((520, 1308), "Choose Resolution\nMethod", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))

    # Method 1 (AI) Left
    draw_arrow(draw, (490, 1315), (420, 1345))
    draw_rounded_rect(draw, [350, 1345, 520, 1395], fill=C_WHITE_FILL, outline=C_ORANGE_BORDER, width=2)
    draw.text((365, 1358), "Method 1: 1-Click\n'Give Ans by AI'", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))

    # Method 2 (Manual) Right
    draw_arrow(draw, (660, 1315), (730, 1345))
    draw_rounded_rect(draw, [640, 1345, 830, 1395], fill=C_WHITE_FILL, outline=C_ORANGE_BORDER, width=2)
    draw.text((655, 1358), "Method 2: Authoritative\nManual Answer Draft", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))

    # Convergence to RESOLVED
    draw.line([(435, 1395), (435, 1415), (575, 1415)], fill=C_ARROW_GRAY, width=2)
    draw.line([(735, 1395), (735, 1415), (575, 1415)], fill=C_ARROW_GRAY, width=2)
    draw_arrow(draw, (575, 1415), (575, 1425))

    # Final Success Box: Status Instantly Set to 'Resolved'
    draw_rounded_rect(draw, [470, 1425, 680, 1460], fill=C_SUCCESS_FILL, outline=C_SUCCESS_BORDER, width=2)
    draw.text((490, 1436), "Status Instantly Set to 'Resolved' • Drawer Auto-Closes", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"Created: {out_path}")
    return out_path


# =============================================================================
# 2. REAL FIGMA UI SCREEN MOCKUPS (VISUAL DESIGN SYSTEM)
# =============================================================================
def generate_figma_screen_mockups(filename="figma_screen_mockups_combined.png"):
    """
    Renders actual, visible visual Figma mockup frames matching the live application:
    1. Student Portal: Ask Doubt + Cascading Subject/Unit/Topic Picker
    2. Smart Duplicate Alert Modal with Classmate Question & '+1' Action
    3. Teacher Dashboard Queue with Urgent Countdown & 1-Click AI Button
    4. Official Faculty Answer Drawer with Markdown Preview & Publish
    """
    w, h = 1100, 850
    img = Image.new('RGB', (w, h), (245, 247, 250)) # Clean light canvas
    draw = ImageDraw.Draw(img)

    # Header Bar
    draw.rectangle([0, 0, w, 50], fill=(21, 55, 13)) # Primary Green #15370D
    draw.text((25, 14), "FACULTY CONNECT — FIGMA PRODUCTION SCREEN SYSTEM", fill=C_WHITE_TEXT, font=get_font(15, bold=True))
    draw.text((w - 380, 18), "UI/UX FIDELITY: LIVE APP PARITY", fill=(242, 132, 47), font=get_font(11, bold=True))

    # 4 Mockup Frames arranged in 2x2 grid
    # Frame 1: Top Left - Student Ask Doubt Modal
    f1 = [25, 70, 535, 435]
    draw.rectangle(f1, fill=C_WHITE_FILL, outline=(200, 210, 220), width=1)
    # Header of Mockup
    draw.rectangle([f1[0], f1[1], f1[2], f1[1] + 35], fill=(21, 55, 13))
    draw.text((f1[0] + 15, f1[1] + 10), "FRAME 01: STUDENT PORTAL — ASK ACADEMIC DOUBT", fill=C_WHITE_TEXT, font=get_font(10.5, bold=True))

    # Form Fields
    fy = f1[1] + 45
    draw.text((f1[0] + 20, fy), "Select Registered Course:", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))
    draw.rectangle([f1[0] + 20, fy + 16, f1[2] - 20, fy + 44], fill=(250, 250, 250), outline=(180, 180, 180))
    draw.text((f1[0] + 28, fy + 24), "CSE316: Operating Systems (3 Credits)", fill=(30, 30, 30), font=get_font(9))

    fy += 55
    draw.text((f1[0] + 20, fy), "Syllabus Unit & Lecture Date:", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))
    draw.rectangle([f1[0] + 20, fy + 16, f1[2] - 20, fy + 44], fill=(250, 250, 250), outline=(180, 180, 180))
    draw.text((f1[0] + 28, fy + 24), "Unit II: CPU Scheduling Principles & Algorithms", fill=(30, 30, 30), font=get_font(9))

    fy += 55
    draw.text((f1[0] + 20, fy), "Describe Academic Doubt:", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))
    draw.rectangle([f1[0] + 20, fy + 16, f1[2] - 20, fy + 110], fill=(252, 249, 234), outline=(21, 55, 13))
    draw.text((f1[0] + 28, fy + 24), "What is the purpose of time quantum in Round Robin\nscheduling, and how does it prevent starvation?", fill=(20, 20, 20), font=get_font(9.5))

    fy += 120
    # Submit Button
    draw.rectangle([f1[0] + 20, fy, f1[2] - 20, fy + 35], fill=(21, 55, 13))
    draw.text((f1[0] + 160, fy + 10), "Next: Check & Submit Doubt", fill=C_WHITE_TEXT, font=get_font(10, bold=True))

    # Frame 2: Top Right - Duplicate Detection Alert Modal
    f2 = [565, 70, 1075, 435]
    draw.rectangle(f2, fill=C_WHITE_FILL, outline=(200, 210, 220), width=1)
    draw.rectangle([f2[0], f2[1], f2[2], f2[1] + 35], fill=(242, 132, 47)) # Accent Orange
    draw.text((f2[0] + 15, f2[1] + 10), "FRAME 02: SMART SEMANTIC DUPLICATE DETECTION MODAL", fill=C_WHITE_TEXT, font=get_font(10.5, bold=True))

    fy = f2[1] + 45
    draw.rectangle([f2[0] + 15, fy, f2[2] - 15, fy + 35], fill=(255, 245, 237), outline=(242, 132, 47))
    draw.text((f2[0] + 25, fy + 10), "⚠️ 84% Match Found: A similar question already exists!", fill=(180, 60, 0), font=get_font(10, bold=True))

    fy += 45
    draw.rectangle([f2[0] + 15, fy, f2[2] - 15, fy + 120], fill=(252, 249, 234), outline=(200, 200, 200))
    draw.text((f2[0] + 25, fy + 12), "Existing Doubt from Classmate:", fill=C_BLACK_TEXT, font=get_font(9, bold=True))
    draw.text((f2[0] + 25, fy + 30), "\"Why does Round Robin scheduling divide CPU bursts\ninto time quanta rather than running FCFS?\"", fill=(40, 40, 40), font=get_font(9.5))
    draw.text((f2[0] + 25, fy + 75), "Status: Faculty Answer Published • 1 Supporter", fill=(21, 55, 13), font=get_font(8.5, bold=True))

    fy += 135
    # Option 1 Button: +1
    draw.rectangle([f2[0] + 15, fy, f2[0] + 240, fy + 40], fill=(21, 55, 13))
    draw.text((f2[0] + 30, fy + 12), "👍 +1 — I Have the Same Doubt", fill=C_WHITE_TEXT, font=get_font(9.5, bold=True))

    # Option 2 Button: Post anyway
    draw.rectangle([f2[0] + 255, fy, f2[2] - 15, fy + 40], fill=C_WHITE_FILL, outline=(150, 150, 150))
    draw.text((f2[0] + 280, fy + 12), "Post as Distinct Question", fill=C_BLACK_TEXT, font=get_font(9.5))

    # Frame 3: Bottom Left - Teacher Console Dashboard
    f3 = [25, 460, 535, 825]
    draw.rectangle(f3, fill=C_WHITE_FILL, outline=(200, 210, 220), width=1)
    draw.rectangle([f3[0], f3[1], f3[2], f3[1] + 35], fill=(21, 55, 13))
    draw.text((f3[0] + 15, f3[1] + 10), "FRAME 03: TEACHER CONSOLE — QUEUE & 1-CLICK AI", fill=C_WHITE_TEXT, font=get_font(10.5, bold=True))

    fy = f3[1] + 45
    # Metrics Bar
    draw.rectangle([f3[0] + 15, fy, f3[0] + 165, fy + 45], fill=(245, 245, 245), outline=(200, 200, 200))
    draw.text((f3[0] + 25, fy + 8), "Pending Doubts", fill=(80, 80, 80), font=get_font(8))
    draw.text((f3[0] + 25, fy + 22), "3 Urgent", fill=(220, 38, 38), font=get_font(12, bold=True))

    draw.rectangle([f3[0] + 180, fy, f3[0] + 330, fy + 45], fill=(245, 245, 245), outline=(200, 200, 200))
    draw.text((f3[0] + 190, fy + 8), "Resolved Today", fill=(80, 80, 80), font=get_font(8))
    draw.text((f3[0] + 190, fy + 22), "14 Doubts", fill=(21, 55, 13), font=get_font(12, bold=True))

    draw.rectangle([f3[0] + 345, fy, f3[2] - 15, fy + 45], fill=(245, 245, 245), outline=(200, 200, 200))
    draw.text((f3[0] + 355, fy + 8), "3-Hour SLA Status", fill=(80, 80, 80), font=get_font(8))
    draw.text((f3[0] + 355, fy + 22), "Active Guard", fill=(242, 132, 47), font=get_font(11, bold=True))

    fy += 60
    # Pending Question Card
    draw.rectangle([f3[0] + 15, fy, f3[2] - 15, fy + 140], fill=(252, 249, 234), outline=(21, 55, 13))
    draw.text((f3[0] + 25, fy + 10), "CSM229: Java • Unit IV: Inheritance", fill=(21, 55, 13), font=get_font(8.5, bold=True))
    draw.text((f3[0] + 25, fy + 26), "\"Why does Java prohibit multiple inheritance with classes\nbut allow it with interfaces?\"", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))
    draw.text((f3[0] + 25, fy + 65), "Supporters: 2 Students (+1) • Time in Queue: 1h 12m", fill=(100, 100, 100), font=get_font(8))

    # 1-Click AI Answer Button
    draw.rectangle([f3[0] + 25, fy + 90, f3[0] + 195, fy + 125], fill=(21, 55, 13))
    draw.text((f3[0] + 45, fy + 100), "✨ Give Ans by AI", fill=C_WHITE_TEXT, font=get_font(9.5, bold=True))

    # Review button
    draw.rectangle([f3[0] + 210, fy + 90, f3[2] - 25, fy + 125], fill=C_WHITE_FILL, outline=(150, 150, 150))
    draw.text((f3[0] + 250, fy + 100), "Open Answer Drawer", fill=C_BLACK_TEXT, font=get_font(9.5))

    # Frame 4: Bottom Right - Answer Drawer Modal & Direct Resolution
    f4 = [565, 460, 1075, 825]
    draw.rectangle(f4, fill=C_WHITE_FILL, outline=(200, 210, 220), width=1)
    draw.rectangle([f4[0], f4[1], f4[2], f4[1] + 35], fill=(21, 55, 13))
    draw.text((f4[0] + 15, f4[1] + 10), "FRAME 04: OFFICIAL FACULTY ANSWER DRAWER & PUBLISH", fill=C_WHITE_TEXT, font=get_font(10.5, bold=True))

    fy = f4[1] + 45
    draw.text((f4[0] + 20, fy), "Official Explanation (Supports Markdown & Code):", fill=C_BLACK_TEXT, font=get_font(9.5, bold=True))
    draw.rectangle([f4[0] + 20, fy + 16, f4[2] - 20, fy + 140], fill=(255, 255, 255), outline=(180, 180, 180))
    draw.text((f4[0] + 28, fy + 24), "1. Diamond Problem: In Java, class-based multiple\ninheritance causes ambiguity in method dispatch (vtable).\n2. Interfaces eliminate state collision because variables are\npublic static final.\nTextbook Reference: Core Java Volume I, Chapter 5.", fill=(30, 30, 30), font=get_font(8.5))

    fy += 170
    # Quick Status Badges
    draw.text((f4[0] + 20, fy + 8), "Direct Status:", fill=(80, 80, 80), font=get_font(9, bold=True))
    draw.rectangle([f4[0] + 100, fy + 2, f4[0] + 180, fy + 26], fill=(213, 232, 212), outline=(130, 179, 102))
    draw.text((f4[0] + 110, fy + 8), "✔ Resolved", fill=(21, 55, 13), font=get_font(8.5, bold=True))

    # Publish Button
    draw.rectangle([f4[0] + 200, fy - 5, f4[2] - 20, fy + 35], fill=(21, 55, 13))
    draw.text((f4[0] + 240, fy + 8), "🚀 Publish Official Answer", fill=C_WHITE_TEXT, font=get_font(10, bold=True))

    out_path = os.path.join(ASSETS_DIR, filename)
    img.save(out_path, quality=95)
    print(f"Created: {out_path}")
    return out_path

if __name__ == '__main__':
    generate_github_mermaid_user_flow()
    generate_figma_screen_mockups()
