import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# Initialize 16:9 Presentation
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

blank_layout = prs.slide_layouts[6]

# Palette
DARK_BG = RGBColor(11, 23, 44)          # Deep Slate/Navy #0B172C
DARK_CARD = RGBColor(22, 36, 64)        # Navy Card #162440
LIGHT_BG = RGBColor(248, 250, 252)      # Slate 50
CARD_BG = RGBColor(255, 255, 255)       # White
EMERALD = RGBColor(22, 163, 74)         # Emerald 600
EMERALD_LIGHT = RGBColor(240, 253, 244) # Emerald 50
EMERALD_DARK = RGBColor(20, 83, 45)     # Emerald 900
AMBER = RGBColor(217, 119, 6)           # Amber 600
AMBER_LIGHT = RGBColor(254, 243, 199)   # Amber 100
BLUE = RGBColor(37, 99, 235)            # Blue 600
TEXT_DARK = RGBColor(15, 23, 42)        # Slate 900
TEXT_MUTED = RGBColor(100, 116, 139)    # Slate 500
TEXT_LIGHT = RGBColor(241, 245, 249)    # Slate 100
BORDER_COLOR = RGBColor(226, 232, 240)  # Slate 200

def set_slide_bg(slide, color):
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = color
    bg.line.fill.background()
    return bg

def add_header(slide, title, subtitle=None, is_dark=False):
    tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = TEXT_LIGHT if is_dark else TEXT_DARK
    
    if subtitle:
        p2 = tf.add_paragraph()
        p2.text = subtitle
        p2.font.size = Pt(13)
        p2.font.color.rgb = RGBColor(148, 163, 184) if is_dark else TEXT_MUTED
        p2.space_before = Pt(4)

def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=BORDER_COLOR):
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(1)
    else:
        card.line.fill.background()
    return card

# =============================================================================
# SLIDE 1: TITLE SLIDE (Clean & Professional Dark Theme)
# =============================================================================
s1 = prs.slides.add_slide(blank_layout)
set_slide_bg(s1, DARK_BG)

# Tagline Badge
badge = add_card(s1, Inches(0.8), Inches(1.2), Inches(4.5), Inches(0.45), bg_color=DARK_CARD, border_color=EMERALD)
tf_b = badge.text_frame
tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
p_b = tf_b.paragraphs[0]
p_b.text = "🌱 HACKATHON & IDEATHON PROJECT"
p_b.font.size = Pt(11)
p_b.font.bold = True
p_b.font.color.rgb = EMERALD
p_b.alignment = PP_ALIGN.CENTER

# Main Title & Subtitle
tb = s1.shapes.add_textbox(Inches(0.8), Inches(1.85), Inches(11.7), Inches(2.2))
tf = tb.text_frame
tf.word_wrap = True
tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0

p = tf.paragraphs[0]
p.text = "CropCare AI"
p.font.size = Pt(54)
p.font.bold = True
p.font.color.rgb = RGBColor(255, 255, 255)

p2 = tf.add_paragraph()
p2.text = "AI-Driven Crop Disease Diagnosis & Farmer Advisory System"
p2.font.size = Pt(20)
p2.font.color.rgb = RGBColor(203, 213, 225)
p2.space_before = Pt(6)

p3 = tf.add_paragraph()
p3.text = '"Detect Early. Protect Crops. Empower Farmers."'
p3.font.size = Pt(14)
p3.font.italic = True
p3.font.color.rgb = EMERALD
p3.space_before = Pt(4)

# Team Card at Bottom
team_card = add_card(s1, Inches(0.8), Inches(4.5), Inches(11.733), Inches(2.3), bg_color=DARK_CARD, border_color=BORDER_COLOR)
tb_t = s1.shapes.add_textbox(Inches(1.1), Inches(4.7), Inches(11.1), Inches(1.9))
tf_t = tb_t.text_frame
tf_t.word_wrap = True

p_th = tf_t.paragraphs[0]
p_th.text = "PROJECT TEAM & LEADERSHIP"
p_th.font.size = Pt(12)
p_th.font.bold = True
p_th.font.color.rgb = AMBER

# 3 Columns for Team Members
p_tl = tf_t.add_paragraph()
p_tl.text = "👑 Team Leader: Ram raghuvir Roy  (AI Architecture & Full Stack Development)"
p_tl.font.size = Pt(14)
p_tl.font.bold = True
p_tl.font.color.rgb = RGBColor(255, 255, 255)
p_tl.space_before = Pt(6)

p_tm1 = tf_t.add_paragraph()
p_tm1.text = "👥 Team Mate: Anurag kumar Ray  (Cloud Infrastructure, Database & Backend API)"
p_tm1.font.size = Pt(13)
p_tm1.font.color.rgb = RGBColor(226, 232, 240)
p_tm1.space_before = Pt(4)

p_tm2 = tf_t.add_paragraph()
p_tm2.text = "👥 Team Mate: Keshav kumar jha  (Agronomy Dataset, Disease Research & UI/UX)"
p_tm2.font.size = Pt(13)
p_tm2.font.color.rgb = RGBColor(226, 232, 240)
p_tm2.space_before = Pt(4)

p_live = tf_t.add_paragraph()
p_live.text = "🌐 Live Application: https://royanurag959-tech.github.io/CropCareAI/  |  GitHub: github.com/royanurag959-tech/CropCareAI"
p_live.font.size = Pt(11)
p_live.font.color.rgb = EMERALD
p_live.space_before = Pt(8)

# =============================================================================
# SLIDE 2: THE PROBLEM (Clear, Human, Realistic)
# =============================================================================
s2 = prs.slides.add_slide(blank_layout)
set_slide_bg(s2, LIGHT_BG)
add_header(s2, "The Problem: The Agricultural Disease Crisis in India", "Smallholder farmers suffer catastrophic crop losses due to lack of timely, accessible diagnostic expertise.")

prob_cards = [
    ("Severe Crop Losses", "30-35% Annual Losses", "Indian farmers lose ~₹2 Lakh Crore ($29B) annually to preventable crop fungal, bacterial, and pest diseases.", AMBER),
    ("Expertise Gap", "1 Expert : 1,200 Farmers", "Critical shortage of agricultural extension officers in rural blocks, causing 5-10 day delays before diagnosis.", BLUE),
    ("Poor Rural Connectivity", "No Signal in Remote Fields", "Most modern agritech apps fail because they require high-speed 4G/5G, which is absent on actual farmland.", TEXT_DARK),
    ("Wrong Treatment Usage", "Misuse of Chemicals", "Without accurate identification, farmers overuse expensive chemical pesticides, degrading soil and wasting money.", EMERALD_DARK)
]

for idx, (title, stat, desc, color) in enumerate(prob_cards):
    left = Inches(0.8 + idx * 3.0)
    card = add_card(s2, left, Inches(1.9), Inches(2.8), Inches(4.8), bg_color=CARD_BG, border_color=BORDER_COLOR)
    
    tb = s2.shapes.add_textbox(left + Inches(0.2), Inches(2.1), Inches(2.4), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = stat
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(8)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.size = Pt(12)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(10)

# =============================================================================
# SLIDE 3: THE SOLUTION (Detect -> Explain -> Solve -> Prevent)
# =============================================================================
s3 = prs.slides.add_slide(blank_layout)
set_slide_bg(s3, LIGHT_BG)
add_header(s3, "Our Solution: The 4-Step CropCare AI Lifecycle", "A complete, practical agricultural care system engineered specifically for real-world farming conditions.")

steps = [
    ("1. DETECT", "Instant Visual AI Scan", "Farmer snaps leaf photo. Deep learning model identifies disease with 94%+ accuracy in under 1 second.", EMERALD),
    ("2. EXPLAIN", "Root-Cause Analysis", "Answers 'Why did this happen?' based on weather, excess moisture, soil humidity, and leaf wetness.", BLUE),
    ("3. SOLVE", "Dual Treatment Steps", "Immediate organic remedies (Neem oil, biocontrol) alongside regulated chemical fungicide dosages.", AMBER),
    ("4. PREVENT", "Long-Term Protection", "Crop rotation guidelines, resistant seed varieties, and soil care to stop recurrence next season.", DARK_BG)
]

for idx, (step_num, title, desc, color) in enumerate(steps):
    left = Inches(0.8 + idx * 3.0)
    card = add_card(s3, left, Inches(1.9), Inches(2.8), Inches(4.8), bg_color=CARD_BG, border_color=BORDER_COLOR)
    
    tb = s3.shapes.add_textbox(left + Inches(0.2), Inches(2.1), Inches(2.4), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = step_num
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = color
    
    p2 = tf.add_paragraph()
    p2.text = title
    p2.font.size = Pt(14)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(6)
    
    p3 = tf.add_paragraph()
    p3.text = desc
    p3.font.size = Pt(12)
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(12)

# =============================================================================
# SLIDE 4: TECHNICAL ARCHITECTURE & INNOVATIONS
# =============================================================================
s4 = prs.slides.add_slide(blank_layout)
set_slide_bg(s4, DARK_BG)
add_header(s4, "Technical Architecture & Rural Inclusivity", "Robust offline-first architecture designed to operate seamlessly across all digital divides.", is_dark=True)

arch_items = [
    ("Multi-Tier AI Inference", [
        "Edge Model: Lightweight MobileNet quantized for real-time in-browser inference (TensorFlow.js).",
        "Cloud Ensemble: High-resolution Vision Transformer backup when online connectivity is detected.",
        "Latency: Sub-second analysis on mid-range smartphones."
    ], EMERALD),
    ("100% Offline Capability", [
        "PWA Architecture: Pre-cached service workers and offline asset bundles.",
        "IndexedDB: Stores farmer scan history, photos, and prescriptions on-device.",
        "Auto-Sync: Silently uploads stored records when phone reconnects to network."
    ], BLUE),
    ("Universal Access & Telecom", [
        "Hindi + English vernacular interface with high-contrast buttons for sunlight visibility.",
        "IVR Voice & SMS Helpline (51969) simulator for farmers with basic button keypad phones.",
        "Krishi Mitra batch portal for village extension workers."
    ], AMBER)
]

for idx, (title, points, color) in enumerate(arch_items):
    left = Inches(0.8 + idx * 4.0)
    card = add_card(s4, left, Inches(1.9), Inches(3.8), Inches(4.8), bg_color=DARK_CARD, border_color=color)
    
    tb = s4.shapes.add_textbox(left + Inches(0.25), Inches(2.1), Inches(3.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = color
    
    for pt in points:
        p_pt = tf.add_paragraph()
        p_pt.text = "• " + pt
        p_pt.font.size = Pt(12)
        p_pt.font.color.rgb = RGBColor(226, 232, 240)
        p_pt.space_before = Pt(10)

# =============================================================================
# SLIDE 5: LIVE WORKING DEMONSTRATION
# =============================================================================
s5 = prs.slides.add_slide(blank_layout)
set_slide_bg(s5, LIGHT_BG)
add_header(s5, "Live Platform Demonstration & Verification", "Tested and validated across real crop leaves, mobile browsers, and desktop environments.")

# Left Card: Evaluation Flow
left_card = add_card(s5, Inches(0.8), Inches(1.8), Inches(6.8), Inches(5.0), bg_color=CARD_BG, border_color=BORDER_COLOR)
tb_demo = s5.shapes.add_textbox(Inches(1.1), Inches(2.0), Inches(6.2), Inches(4.6))
tf_d = tb_demo.text_frame
tf_d.word_wrap = True

p_dh = tf_d.paragraphs[0]
p_dh.text = "Verified End-to-End User Flow"
p_dh.font.size = Pt(17)
p_dh.font.bold = True
p_dh.font.color.rgb = TEXT_DARK

demo_steps = [
    ("Step 1: Crop Selection", "Farmer picks crop (Tomato, Potato, Rice, Corn, Apple, Wheat, Cotton)."),
    ("Step 2: Instant Leaf Scan", "Camera captures leaf photo or uploads from device gallery."),
    ("Step 3: AI Diagnosis Result", "Outputs disease name, 94% confidence score, and severity indicator."),
    ("Step 4: Root Cause Breakdown", "Explains correlation between recent rain, humidity, and pathogen growth."),
    ("Step 5: Actionable Solutions", "Provides chemical dosages (Mancozeb/Copper) and organic alternatives.")
]

for s_title, s_sub in demo_steps:
    p_st = tf_d.add_paragraph()
    p_st.text = f"✔ {s_title}"
    p_st.font.size = Pt(12)
    p_st.font.bold = True
    p_st.font.color.rgb = EMERALD_DARK
    p_st.space_before = Pt(8)
    
    p_ss = tf_d.add_paragraph()
    p_ss.text = f"    {s_sub}"
    p_ss.font.size = Pt(11)
    p_ss.font.color.rgb = TEXT_MUTED

# Right: Screenshot placement
user_shot1 = r"C:\Users\royan\.gemini\antigravity\brain\a72522be-4325-4840-904d-8d60e58daac9\.user_uploaded\media_1789491310118.jpg"
user_shot2 = r"C:\Users\royan\.gemini\antigravity\brain\a72522be-4325-4840-904d-8d60e58daac9\.user_uploaded\media_1789491327757.jpg"

if os.path.exists(user_shot1):
    s5.shapes.add_picture(user_shot1, Inches(8.0), Inches(1.8), Inches(2.35), Inches(5.0))
if os.path.exists(user_shot2):
    s5.shapes.add_picture(user_shot2, Inches(10.55), Inches(1.8), Inches(2.35), Inches(5.0))

# =============================================================================
# SLIDE 6: BUSINESS & DEPLOYMENT MODEL
# =============================================================================
s6 = prs.slides.add_slide(blank_layout)
set_slide_bg(s6, LIGHT_BG)
add_header(s6, "Business Model & Rural Deployment Strategy", "Free baseline service for farmers paired with enterprise data monetization.")

biz_tiers = [
    ("Free Farmer Tier", "₹0 / Month", [
        "Free unlimited offline basic scans",
        "Dual treatment (organic + chemical)",
        "Builds farmer grassroots adoption"
    ], TEXT_MUTED),
    ("CropCare Plus / Voice", "₹49 / Month", [
        "Voice audio readout in Hindi",
        "SMS weather & disease alert push",
        "Priority agronomy review routing"
    ], BLUE),
    ("Krishi Mitra / FPO", "₹199 / Month", [
        "Batch scan tools for field workers",
        "Offline village register sync",
        "Exportable PDF prescriptions"
    ], EMERALD),
    ("B2B Outbreak Heatmap", "Enterprise License", [
        "District-level disease spread API",
        "Crop yield forecast data for NGOs",
        "Agrochemical supply chain planning"
    ], DARK_BG)
]

for idx, (b_title, b_price, b_perks, b_col) in enumerate(biz_tiers):
    left = Inches(0.8 + idx * 3.0)
    card = add_card(s6, left, Inches(1.9), Inches(2.8), Inches(4.8), bg_color=CARD_BG, border_color=BORDER_COLOR)
    
    tb = s6.shapes.add_textbox(left + Inches(0.2), Inches(2.1), Inches(2.4), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = b_title
    p.font.size = Pt(15)
    p.font.bold = True
    p.font.color.rgb = b_col
    
    p2 = tf.add_paragraph()
    p2.text = b_price
    p2.font.size = Pt(18)
    p2.font.bold = True
    p2.font.color.rgb = TEXT_DARK
    p2.space_before = Pt(6)
    
    for perk in b_perks:
        p_p = tf.add_paragraph()
        p_p.text = "• " + perk
        p_p.font.size = Pt(11)
        p_p.font.color.rgb = TEXT_MUTED
        p_p.space_before = Pt(8)

# =============================================================================
# SLIDE 7: PROJECT TEAM & RESPONSIBILITIES (Clean, Realistic, Human)
# =============================================================================
s7 = prs.slides.add_slide(blank_layout)
set_slide_bg(s7, LIGHT_BG)
add_header(s7, "Meet the Project Team", "A dedicated 3-member team combining AI engineering, cloud deployment, and agricultural domain research.")

team_members_data = [
    ("Ram raghuvir Roy", "👑 Team Leader & AI Architect", [
        "Project lead and overall system architecture.",
        "Trained and optimized the vision model for crop disease classification.",
        "Implemented frontend React application and multi-tier diagnosis pipeline.",
        "Engineered the offline PWA service worker and indexed database."
    ], EMERALD, True),
    ("Anurag kumar Ray", "👥 Co-Lead & Cloud/Backend", [
        "Designed backend API architecture and cloud database schema.",
        "Configured continuous deployment pipelines (GitHub Actions & Vercel).",
        "Implemented data synchronization protocols for offline-to-cloud transfers.",
        "Integrated the telecom IVR & SMS communication simulator."
    ], BLUE, False),
    ("Keshav kumar jha", "👥 Agronomy & UX Design", [
        "Curated and validated agricultural plant pathology datasets across 14 crops.",
        "Formulated localized organic and chemical treatment recommendations.",
        "Designed bilingual Hindi-English user interface tailored for rural farmers.",
        "Conducted farmer usability and accessibility testing."
    ], AMBER, False)
]

for idx, (m_name, m_role, m_tasks, m_col, is_lead) in enumerate(team_members_data):
    left = Inches(0.8 + idx * 4.0)
    card = add_card(s7, left, Inches(1.9), Inches(3.8), Inches(4.8), bg_color=CARD_BG, border_color=m_col if is_lead else BORDER_COLOR)
    
    tb = s7.shapes.add_textbox(left + Inches(0.25), Inches(2.1), Inches(3.3), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = m_name
    p.font.size = Pt(17)
    p.font.bold = True
    p.font.color.rgb = TEXT_DARK
    
    p2 = tf.add_paragraph()
    p2.text = m_role
    p2.font.size = Pt(12)
    p2.font.bold = True
    p2.font.color.rgb = m_col
    p2.space_before = Pt(4)
    
    p_th = tf.add_paragraph()
    p_th.text = "Key Contributions:"
    p_th.font.size = Pt(11)
    p_th.font.bold = True
    p_th.font.color.rgb = TEXT_DARK
    p_th.space_before = Pt(10)
    
    for task in m_tasks:
        p_t = tf.add_paragraph()
        p_t.text = "✔ " + task
        p_t.font.size = Pt(11)
        p_t.font.color.rgb = TEXT_MUTED
        p_t.space_before = Pt(6)

# =============================================================================
# SLIDE 8: ROADMAP & IMPACT (Closing Slide - High Impact)
# =============================================================================
s8 = prs.slides.add_slide(blank_layout)
set_slide_bg(s8, DARK_BG)
add_header(s8, "Roadmap & Nationwide Agritech Vision", "Scaling from a hackathon prototype to an impactful agricultural public lifeline.", is_dark=True)

roadmap_milestones = [
    ("Phase 1: Present (Live)", "Deployed live web PWA with 7 crops, offline inference, bilingual Hindi UI, and IVR simulator.", EMERALD),
    ("Phase 2: Telecom Integration", "Partner with rural telecom providers (BSNL/Kisan Call Centers) for toll-free voice diagnosis.", BLUE),
    ("Phase 3: Drone & Satellite", "Satellite vegetation index (NDVI) overlay and drone survey kits for village FPO cooperatives.", AMBER),
    ("Phase 4: Ecosystem Scale", "Direct tie-up with Ministry of Agriculture & fertilizer subsidy verification channels.", RGBColor(168, 85, 247))
]

for idx, (rm_phase, rm_desc, rm_col) in enumerate(roadmap_milestones):
    left = Inches(0.8 + idx * 3.0)
    card = add_card(s8, left, Inches(1.9), Inches(2.8), Inches(2.6), bg_color=DARK_CARD, border_color=rm_col)
    
    tb = s8.shapes.add_textbox(left + Inches(0.2), Inches(2.1), Inches(2.4), Inches(2.2))
    tf = tb.text_frame
    tf.word_wrap = True
    
    p = tf.paragraphs[0]
    p.text = rm_phase
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = rm_col
    
    p2 = tf.add_paragraph()
    p2.text = rm_desc
    p2.font.size = Pt(11)
    p2.font.color.rgb = RGBColor(203, 213, 225)
    p2.space_before = Pt(8)

# Final Callout Card
bot_card = add_card(s8, Inches(0.8), Inches(4.8), Inches(11.733), Inches(2.0), bg_color=DARK_CARD, border_color=EMERALD)
tb_b = s8.shapes.add_textbox(Inches(1.1), Inches(5.0), Inches(11.1), Inches(1.6))
tf_b = tb_b.text_frame
tf_b.word_wrap = True

p_b1 = tf_b.paragraphs[0]
p_b1.text = '"Our mission is simple: zero crop loss from preventable plant diseases for 140 Million Indian farmers."'
p_b1.font.size = Pt(16)
p_b1.font.bold = True
p_b1.font.color.rgb = RGBColor(255, 255, 255)
p_b1.alignment = PP_ALIGN.CENTER

p_b2 = tf_b.add_paragraph()
p_b2.text = "Team: Ram raghuvir Roy (Lead) | Anurag kumar Ray | Keshav kumar jha"
p_b2.font.size = Pt(13)
p_b2.font.color.rgb = AMBER
p_b2.space_before = Pt(6)
p_b2.alignment = PP_ALIGN.CENTER

p_b3 = tf_b.add_paragraph()
p_b3.text = "Live Demo: https://royanurag959-tech.github.io/CropCareAI/  |  Repository: github.com/royanurag959-tech/CropCareAI"
p_b3.font.size = Pt(11)
p_b3.font.color.rgb = EMERALD
p_b3.space_before = Pt(4)
p_b3.alignment = PP_ALIGN.CENTER

# Save presentation to all relevant destinations
out_paths = [
    r"C:\Users\royan\.gemini\antigravity\scratch\cropcare-ai\CropCare_AI_Hackathon_PitchDeck.pptx",
    r"C:\Users\royan\.gemini\antigravity\scratch\cropcare-ai\frontend\public\CropCare_AI_Hackathon_PitchDeck.pptx",
    r"C:\Users\royan\.gemini\antigravity\scratch\cropcare-ai\frontend\dist\CropCare_AI_Hackathon_PitchDeck.pptx",
    r"C:\Users\royan\Desktop\CropCare_AI_Hackathon_PitchDeck.pptx"
]

for path in out_paths:
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        prs.save(path)
        print(f"Saved to: {path}")
    except Exception as e:
        print(f"Could not save to {path}: {e}")

print("Successfully generated 8-Slide Pitch Deck!")
