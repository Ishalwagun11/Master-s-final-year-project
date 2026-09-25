"""
Generate a clean, simple 13-slide PowerPoint for the COMP7037 presentation.
Slide content mirrors PRESENTATION_PLAN.md (updated 15-minute plan).
Output: docs/Political_News_Credibility_Presentation_13slides.pptx
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE

# ── Constants ──
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x1A, 0x1A, 0x1A)
DARK_GRAY = RGBColor(0x33, 0x33, 0x33)
MID_GRAY = RGBColor(0x66, 0x66, 0x66)
LIGHT_GRAY = RGBColor(0x99, 0x99, 0x99)
ACCENT = RGBColor(0x2C, 0x5F, 0x8A)
ACCENT_LIGHT = RGBColor(0xE8, 0xEE, 0xF4)
GREEN = RGBColor(0x27, 0xAE, 0x60)
RED = RGBColor(0xC0, 0x39, 0x2B)

SLIDE_W = Inches(13.333)
SLIDE_H = Inches(7.5)
MARGIN_L = Inches(0.65)
MARGIN_R = Inches(0.65)
CONTENT_W = SLIDE_W - MARGIN_L - MARGIN_R

prs = Presentation()
prs.slide_width = SLIDE_W
prs.slide_height = SLIDE_H

# ── Helpers ──

def add_blank_slide():
    return prs.slides.add_slide(prs.slide_layouts[6])

def add_textbox(slide, left, top, width, height):
    return slide.shapes.add_textbox(left, top, width, height)

def set_text(tf, text, size=18, color=BLACK, bold=False, italic=False,
             alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    tf.clear()
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.italic = italic
    p.font.name = font_name
    p.alignment = alignment
    return p

def add_bullet(tf, text, size=16, color=BLACK, bold=False, space_before=Pt(8)):
    tf.word_wrap = True
    tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.LEFT
    p.space_before = space_before
    p.level = 0
    return p

def add_accent_bar(slide):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, MARGIN_L, Inches(0.3),
                                   CONTENT_W, Inches(0.06))
    shape.fill.solid()
    shape.fill.fore_color.rgb = ACCENT
    shape.line.fill.background()

def add_slide_number(slide, num):
    tb = add_textbox(slide, Inches(12.0), Inches(7.05), Inches(0.7), Inches(0.35))
    set_text(tb.text_frame, str(num), size=10, color=LIGHT_GRAY,
             alignment=PP_ALIGN.RIGHT)

def add_title(slide, text):
    tb = add_textbox(slide, MARGIN_L, Inches(0.55), CONTENT_W, Inches(0.95))
    set_text(tb.text_frame, text, size=32, color=ACCENT, bold=True)

def add_subtitle_line(slide, text, top):
    tb = add_textbox(slide, MARGIN_L, top, CONTENT_W, Inches(0.45))
    set_text(tb.text_frame, text, size=13, color=MID_GRAY)

def add_table(slide, left, top, col_widths, row_height, headers, rows,
              font_size=12, header_color=ACCENT, header_text_color=WHITE,
              row_colors=None, align_center_cols=None):
    """Draw a table using individual shapes for maximum compatibility."""
    if align_center_cols is None:
        align_center_cols = list(range(1, len(headers)))
    total_width = sum(col_widths)
    total_height = row_height * (len(rows) + 1)

    # Outer border
    outer = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top,
                                   total_width, total_height)
    outer.fill.background()
    outer.line.color.rgb = LIGHT_GRAY
    outer.line.width = Pt(1)

    # Header
    x = left
    for i, header in enumerate(headers):
        cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, top,
                                      col_widths[i], row_height)
        cell.fill.solid()
        cell.fill.fore_color.rgb = header_color
        cell.line.color.rgb = LIGHT_GRAY
        cell.line.width = Pt(0.5)
        tf = cell.text_frame
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        tf.margin_left = Inches(0.06)
        tf.margin_right = Inches(0.06)
        tf.margin_top = Inches(0.04)
        tf.margin_bottom = Inches(0.04)
        p = tf.paragraphs[0]
        p.text = header
        p.font.size = Pt(font_size)
        p.font.bold = True
        p.font.color.rgb = header_text_color
        p.font.name = "Calibri"
        p.alignment = PP_ALIGN.CENTER
        x += col_widths[i]

    if row_colors is None:
        row_colors = [WHITE, ACCENT_LIGHT] * (len(rows) // 2 + 1)
        row_colors = row_colors[:len(rows)]

    y = top + row_height
    for row_idx, row in enumerate(rows):
        x = left
        for col_idx, cell_text in enumerate(row):
            cell = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y,
                                          col_widths[col_idx], row_height)
            cell.fill.solid()
            cell.fill.fore_color.rgb = row_colors[row_idx]
            cell.line.color.rgb = LIGHT_GRAY
            cell.line.width = Pt(0.5)
            tf = cell.text_frame
            tf.word_wrap = True
            tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
            tf.margin_left = Inches(0.06)
            tf.margin_right = Inches(0.06)
            tf.margin_top = Inches(0.04)
            tf.margin_bottom = Inches(0.04)
            p = tf.paragraphs[0]
            p.text = str(cell_text)
            p.font.size = Pt(font_size)
            p.font.color.rgb = BLACK
            p.font.name = "Calibri"
            p.alignment = PP_ALIGN.CENTER if col_idx in align_center_cols else PP_ALIGN.LEFT
            x += col_widths[col_idx]
        y += row_height


# ═══════════════════════════════════════════════════════════════
# SLIDE 1 — Title & Project Overview
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)

# Title block
tb = add_textbox(slide, MARGIN_L, Inches(1.3), CONTENT_W, Inches(1.3))
set_text(tb.text_frame, "Measuring Framing Disagreement Between UK Political News Sources",
         size=38, color=ACCENT, bold=True)

# Subtitle
tb = add_textbox(slide, MARGIN_L, Inches(2.7), CONTENT_W, Inches(0.6))
set_text(tb.text_frame, "An experimental study — not a product", size=22, color=DARK_GRAY)

# Stats bar
tb = add_textbox(slide, MARGIN_L, Inches(3.6), CONTENT_W, Inches(0.8))
set_text(tb.text_frame, "44 events  ·  264 articles  ·  6 sources  ·  2015–2024",
         size=20, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

# Meta
tb = add_textbox(slide, MARGIN_L, Inches(5.8), CONTENT_W, Inches(1.0))
set_text(tb.text_frame, "Isha Lwagun  ·  MSc Dissertation  ·  Oxford Brookes University\nSupervisor: Alexander Rast  ·  September 2026",
         size=14, color=MID_GRAY, alignment=PP_ALIGN.CENTER)

add_slide_number(slide, 1)

# ═══════════════════════════════════════════════════════════════
# SLIDE 2 — The Problem: Why This Matters
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "The Problem: Why This Matters")

# Left example
tb = add_textbox(slide, MARGIN_L, Inches(1.7), Inches(5.8), Inches(2.2))
set_text(tb.text_frame, "When a political story breaks:", size=17, color=DARK_GRAY, bold=True)
add_bullet(tb.text_frame, "The Guardian: \"This is a fatal blow, they're finished.\"", size=15)
add_bullet(tb.text_frame, "The BBC: \"Pressure is mounting, situation unclear.\"", size=15)
add_bullet(tb.text_frame, "The Times: \"Sources say he'll resign by tonight.\"", size=15)

# Right gap
tb = add_textbox(slide, Inches(7.0), Inches(1.7), Inches(5.7), Inches(2.4))
set_text(tb.text_frame, "The gap this project fills:", size=17, color=DARK_GRAY, bold=True)
add_bullet(tb.text_frame, "Same event, completely different framing.", size=15)
add_bullet(tb.text_frame, "Readers cannot tell how contested the story is.", size=15)
add_bullet(tb.text_frame, "No existing tool measures disagreement between sources on one event.", size=15)

# Bottom key point
tb = add_textbox(slide, MARGIN_L, Inches(4.6), CONTENT_W, Inches(1.4))
set_text(tb.text_frame, "Core question: Can we measure how much UK news outlets disagree on the same political event?",
         size=20, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

add_slide_number(slide, 2)

# ═══════════════════════════════════════════════════════════════
# SLIDE 3 — Experiment One: The Prediction Idea
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "Experiment One: The Prediction Idea")

# Hypothesis
tb = add_textbox(slide, MARGIN_L, Inches(1.65), CONTENT_W, Inches(1.0))
set_text(tb.text_frame, "Original hypothesis", size=18, color=DARK_GRAY, bold=True)
add_bullet(tb.text_frame, "If sources disagree, the outlier is probably wrong.", size=15)
add_bullet(tb.text_frame, "Match a new event to similar past events to predict who will be right.", size=15)

# Pipeline diagram
tb = add_textbox(slide, MARGIN_L, Inches(3.0), CONTENT_W, Inches(1.0))
set_text(tb.text_frame, "Planned pipeline:", size=18, color=DARK_GRAY, bold=True)

tb = add_textbox(slide, MARGIN_L, Inches(3.55), CONTENT_W, Inches(0.8))
set_text(tb.text_frame,
         "RSS feeds  →  read articles  →  group by event  →  measure disagreement  →  match history  →  predict  →  check after 72h",
         size=14, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

# Claim box
tb = add_textbox(slide, MARGIN_L, Inches(4.7), CONTENT_W, Inches(1.3))
set_text(tb.text_frame,
         "Testable claim: Event-specific matching should beat always trusting the historically most reliable source.",
         size=18, color=DARK_GRAY, bold=True, alignment=PP_ALIGN.CENTER)

add_slide_number(slide, 3)

# ═══════════════════════════════════════════════════════════════
# SLIDE 4 — What Went Wrong (Issues Encountered)
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "What Went Wrong: Issues Encountered")
add_subtitle_line(slide, "Three pieces of evidence redirected the project", Inches(1.45))

add_table(
    slide, MARGIN_L, Inches(1.95),
    col_widths=[Inches(2.8), Inches(3.5), Inches(2.2), Inches(2.2), Inches(1.5)],
    row_height=Inches(0.7),
    headers=["Issue", "What happened", "My method", "Baseline", "Random"],
    rows=[
        ["Prediction failed", "k-NN lost to simple baseline", "56.8%", "61.4%", "37.5%"],
        ["Tone is fragile", "VADER vs RoBERTa disagree", "5 flagged", "0 flagged", "r = 0.33"],
        ["Tone misses meaning", "May Brexit event: tone quiet, meaning far apart", "0.017", "0.473", "semantic distance"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT, WHITE],
    align_center_cols=[2, 3, 4],
    font_size=13
)

# Takeaway
tb = add_textbox(slide, MARGIN_L, Inches(5.4), CONTENT_W, Inches(1.1))
set_text(tb.text_frame,
         "Takeaway: The data rejected the prediction claim. That negative result is what made the project pivot to measuring disagreement instead.",
         size=17, color=ACCENT, bold=True, alignment=PP_ALIGN.CENTER)

add_slide_number(slide, 4)

# ═══════════════════════════════════════════════════════════════
# SLIDE 5 — Experiment Two: 3 Dimensions of Disagreement
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "Experiment Two: Three Dimensions of Disagreement")

add_table(
    slide, MARGIN_L, Inches(1.75),
    col_widths=[Inches(2.0), Inches(3.4), Inches(3.6), Inches(3.0)],
    row_height=Inches(0.72),
    headers=["Dimension", "Measures", "Tool", "Output"],
    rows=[
        ["D1 — Tone", "Do headlines sound different?", "VADER compound → variance", "0.15 threshold flags 5/44 events"],
        ["D2 — Meaning", "Do articles say different things?", "MiniLM embeddings → cosine distance", "Catches events tone misses"],
        ["D3 — Structure", "Which outlets disagree with which?", "Pairwise tone difference", "BBC↔Times widest gap (0.408)"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT, WHITE],
    align_center_cols=[],
    font_size=12
)

# Why three
tb = add_textbox(slide, MARGIN_L, Inches(5.15), CONTENT_W, Inches(1.2))
set_text(tb.text_frame, "Why three dimensions?", size=18, color=DARK_GRAY, bold=True)
add_bullet(tb.text_frame, "Tone and meaning measure different things.", size=15)
add_bullet(tb.text_frame, "Using only one dimension misses real disagreement.", size=15)

add_slide_number(slide, 5)

# ═══════════════════════════════════════════════════════════════
# SLIDE 6 — How We Measure Tone: VADER vs RoBERTa
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "How We Measure Tone: VADER vs RoBERTa")

add_table(
    slide, MARGIN_L, Inches(1.75),
    col_widths=[Inches(3.2), Inches(4.2), Inches(4.2)],
    row_height=Inches(0.55),
    headers=["", "VADER", "RoBERTa"],
    rows=[
        ["Type", "Lexicon (word dictionary)", "Transformer AI model"],
        ["Score range", "−1 to +1 compound", "P(positive) − P(negative)"],
        ["Training", "None needed", "Pre-trained on Twitter data"],
        ["Speed", "Instant, runs on laptop", "Slower, model download"],
        ["Events flagged ≥ 0.15", "5", "0"],
        ["Variance correlation", "r = 0.33 (weak) — across all 44 events"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT, WHITE, ACCENT_LIGHT, WHITE, ACCENT_LIGHT],
    align_center_cols=[],
    font_size=12
)

# Decision
tb = add_textbox(slide, MARGIN_L, Inches(5.4), CONTENT_W, Inches(1.2))
set_text(tb.text_frame, "Decision: Use VADER for Dimension 1.", size=18, color=GREEN, bold=True)
add_bullet(tb.text_frame, "RoBERTa was the robustness check that proved tone alone is fragile.", size=15)
add_bullet(tb.text_frame, "VADER's scores are transparent: you can see which words drove each result.", size=15)

add_slide_number(slide, 6)

# ═══════════════════════════════════════════════════════════════
# SLIDE 7 — Dimension 1 Results: The 0.15 Threshold
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "Dimension 1 Results: The 0.15 Threshold")
add_subtitle_line(slide, "High-disagreement events (variance ≥ 0.15)", Inches(1.45))

add_table(
    slide, MARGIN_L, Inches(1.9),
    col_widths=[Inches(4.6), Inches(2.4), Inches(1.8), Inches(2.2)],
    row_height=Inches(0.42),
    headers=["Event", "Category", "Variance", "Tone range"],
    rows=[
        ["Theresa May confidence vote", "Confidence vote", "0.276", "−0.62 → +0.44"],
        ["North Shropshire by-election", "Election", "0.204", "−0.38 → +0.51"],
        ["Owen Paterson resignation", "Resignation", "0.186", "−0.55 → +0.29"],
        ["Cressida Dick resignation", "Resignation", "0.162", "−0.41 → +0.33"],
        ["Sunak net-zero retreat", "Economic policy", "0.154", "−0.29 → +0.36"],
    ],
    row_colors=[WHITE] * 5,
    font_size=12
)

tb = add_textbox(slide, Inches(7.2), Inches(4.5), Inches(5.0), Inches(0.3))
set_text(tb.text_frame, "Pattern by event type", size=13, color=DARK_GRAY, bold=True)

# Bottom right: variance by category
add_table(
    slide, Inches(7.2), Inches(4.82),
    col_widths=[Inches(3.4), Inches(1.8)],
    row_height=Inches(0.38),
    headers=["Event type", "Avg variance"],
    rows=[
        ["Confidence votes", "0.117"],
        ["Elections / leadership", "0.094"],
        ["Resignations", "0.077"],
        ["Economic policy", "0.052"],
    ],
    row_colors=[WHITE] * 4,
    font_size=11
)

# Bottom left note
tb = add_textbox(slide, MARGIN_L, Inches(4.5), Inches(6.3), Inches(1.6))
set_text(tb.text_frame, "Validation:", size=16, color=DARK_GRAY, bold=True)
add_bullet(tb.text_frame, "0.15 = 90th percentile; 5 flagged events.", size=14)
add_bullet(tb.text_frame, "Flagged: genuinely uncertain outcomes.", size=14)
add_bullet(tb.text_frame, "Lowest: HS2 (0.011), Kwarteng U-turn (0.014) — settled facts.", size=14)

add_slide_number(slide, 7)

# ═══════════════════════════════════════════════════════════════
# SLIDE 8 — Dimensions 2 & 3: Meaning and Structure
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "Dimensions 2 & 3: Meaning and Structure")

add_subtitle_line(slide, "Dimension 2 — semantic distance catches what tone misses", Inches(1.45))
add_table(
    slide, MARGIN_L, Inches(1.9),
    col_widths=[Inches(4.0), Inches(2.2), Inches(2.2), Inches(3.2)],
    row_height=Inches(0.48),
    headers=["Event", "Tone variance", "Semantic distance", "Interpretation"],
    rows=[
        ["May Brexit-defeat event", "0.017", "0.473", "Tone blind; meaning catches it"],
        ["Theresa May confidence vote", "0.276", "0.381", "Both dimensions fire"],
        ["HS2 rail cancellation", "0.011", "0.092", "Both quiet — settled fact"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT, WHITE],
    font_size=11
)

add_subtitle_line(slide, "Dimension 3 — source-pair disagreement (15 pairs)", Inches(4.05))
add_table(
    slide, MARGIN_L, Inches(4.5),
    col_widths=[Inches(2.6), Inches(1.5), Inches(2.6), Inches(1.5)],
    row_height=Inches(0.42),
    headers=["Most disagreeing", "Gap", "Least disagreeing", "Gap"],
    rows=[
        ["BBC ↔ Times", "0.408", "Guardian ↔ Times", "0.261"],
        ["Guardian ↔ Telegraph", "0.403", "Reuters ↔ Sky News", "0.285"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT],
    font_size=11
)

tb = add_textbox(slide, Inches(7.2), Inches(4.5), Inches(5.5), Inches(1.8))
set_text(tb.text_frame, "Topic-dependent gaps:", size=14, color=DARK_GRAY, bold=True)
add_bullet(tb.text_frame, "Confidence votes: Telegraph↔Times 0.699", size=12)
add_bullet(tb.text_frame, "Legal rulings: Sky↔Telegraph 0.597", size=12)
add_bullet(tb.text_frame, "Elections: Guardian↔Sky 0.518", size=12)
add_bullet(tb.text_frame, "Scandals: BBC↔Times 0.444", size=12)

add_slide_number(slide, 8)

# ═══════════════════════════════════════════════════════════════
# SLIDE 9 — Risks & Mitigation
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "Risks & Mitigation")

add_table(
    slide, MARGIN_L, Inches(1.75),
    col_widths=[Inches(3.6), Inches(1.3), Inches(6.0)],
    row_height=Inches(0.58),
    headers=["Risk", "Status", "Mitigation"],
    rows=[
        ["Small dataset (44 events)", "✅ Resolved", "Hand-curated corpus; tested 5 threshold methods"],
        ["Prediction doesn't beat baseline", "✅ Resolved", "Reported negative result; pivoted to measurement"],
        ["Tone measurement fragile", "✅ Resolved", "Added meaning + structure dimensions"],
        ["Clustering fails on high disagreement", "⚠️ Acknowledged", "Documented as limitation"],
        ["User-study ethics approval", "✅ Approved", "RQ4 study not conducted within the available project timeframe"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT, WHITE, ACCENT_LIGHT, WHITE],
    align_center_cols=[1],
    font_size=12
)

add_slide_number(slide, 9)

# ═══════════════════════════════════════════════════════════════
# SLIDE 10 — Legal, Social, Ethical & Professional Issues
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "Legal, Social, Ethical & Professional Issues")

add_table(
    slide, MARGIN_L, Inches(1.75),
    col_widths=[Inches(2.4), Inches(9.5)],
    row_height=Inches(0.78),
    headers=["Area", "How it is addressed"],
    rows=[
        ["Legal", "RSS metadata only (titles + summaries); no paywall bypass; no full-text scraping"],
        ["Ethical", "Hand-labelled by researcher; no personal data collected; ethics approval obtained for the proposed RQ4 study"],
        ["Social", "Media literacy tool — measures disagreement, does not label outlets as 'misleading'"],
        ["Professional", "Honest reporting of negative results; reproducible code; version control; documented limitations"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT, WHITE, ACCENT_LIGHT],
    align_center_cols=[],
    font_size=13
)

add_slide_number(slide, 10)

# ═══════════════════════════════════════════════════════════════
# SLIDE 11 — Demo of Current Implementation
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "Demo of Current Implementation")
add_subtitle_line(slide, "Everything is reproducible from the repository", Inches(1.45))

add_table(
    slide, MARGIN_L, Inches(1.9),
    col_widths=[Inches(3.6), Inches(6.4), Inches(2.0)],
    row_height=Inches(0.54),
    headers=["Script to run", "Evidence it produces", "For slide"],
    rows=[
        ["scripts/divergence_table.py", "Ranked per-event tone variance; 5 flagged ≥ 0.15", "7"],
        ["scripts/multi_dimensional_sentiment.py", "VADER vs RoBERTa: r = 0.33; 5 vs 0 flagged", "6"],
        ["scripts/extended_disagreement_analysis.py", "Semantic distance + source-pair CSVs", "8"],
        ["scripts/nearest_neighbour_demo.py", "Worked example: May confidence vote", "4"],
        ["scripts/compare_predictions.py", "56.8% vs 61.4% vs 37.5%", "4"],
        ["scripts/cluster_events_demo.py", "ARI = 0.617 vs hand labels", "(RQ1)"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT] * 3,
    font_size=11
)

tb = add_textbox(slide, MARGIN_L, Inches(5.5), CONTENT_W, Inches(0.9))
set_text(tb.text_frame,
         "Tip: Pre-run the RoBERTa script once — the model download takes a few minutes. Keep screenshots as backup slides.",
         size=14, color=MID_GRAY, alignment=PP_ALIGN.CENTER)

add_slide_number(slide, 11)

# ═══════════════════════════════════════════════════════════════
# SLIDE 12 — What's Deferred to Future Work
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "What's Deferred to Future Work")

add_table(
    slide, MARGIN_L, Inches(1.75),
    col_widths=[Inches(4.2), Inches(6.0)],
    row_height=Inches(0.56),
    headers=["Deferred component", "Why not now"],
    rows=[
        ["Live RSS ingestion pipeline", "Needs weeks of runtime to collect new events"],
        ["72-hour resolution tracking", "Requires live events to play out"],
        ["Credibility prediction", "Not proven — 56.8% vs 61.4% baseline on 44 events"],
        ["Dashboard + API", "Delivery layer, not the research contribution"],
        ["User study (RQ4)", "Approved but not conducted within the available project timeframe; retained as future empirical validation"],
    ],
    row_colors=[WHITE, ACCENT_LIGHT] * 3,
    align_center_cols=[],
    font_size=12
)

add_slide_number(slide, 12)

# ═══════════════════════════════════════════════════════════════
# SLIDE 13 — Conclusion + Limitation
# ═══════════════════════════════════════════════════════════════
slide = add_blank_slide()
add_accent_bar(slide)
add_title(slide, "Conclusion + Limitation")

# Results block
tb = add_textbox(slide, MARGIN_L, Inches(1.7), CONTENT_W, Inches(1.0))
set_text(tb.text_frame, "What the experiment shows:", size=18, color=DARK_GRAY, bold=True)

results = [
    ("Disagreement is measurable", "5 of 44 events flagged by VADER variance"),
    ("Disagreement is structured", "BBC↔Times is the widest source gap"),
    ("Disagreement is topic-dependent", "Confidence votes are most contested"),
    ("Some disagreement is invisible to tone", "Semantic distance catches what VADER misses"),
]

y = Inches(2.45)
for title, desc in results:
    tb = add_textbox(slide, MARGIN_L, y, Inches(4.5), Inches(0.45))
    set_text(tb.text_frame, f"• {title}", size=15, color=ACCENT, bold=True)
    tb = add_textbox(slide, Inches(5.3), y, Inches(7.4), Inches(0.45))
    set_text(tb.text_frame, desc, size=15, color=BLACK)
    y += Inches(0.5)

# Limitation box
tb = add_textbox(slide, MARGIN_L, Inches(5.0), CONTENT_W, Inches(1.1))
set_text(tb.text_frame,
         "Limitation: 44 events is enough to measure disagreement, not enough to predict outcomes. The live pipeline is the natural next step.",
         size=17, color=RED, bold=True, alignment=PP_ALIGN.CENTER)

tb = add_textbox(slide, MARGIN_L, Inches(6.2), CONTENT_W, Inches(0.6))
set_text(tb.text_frame, "Thank you — questions welcome.", size=20, color=ACCENT, bold=True,
         alignment=PP_ALIGN.CENTER)

add_slide_number(slide, 13)

# ═══════════════════════════════════════════════════════════════
# Save
# ═══════════════════════════════════════════════════════════════
output_path = r"c:\Users\ishal\OneDrive\MyFolder\Dissertation\docs\Political_News_Credibility_Presentation_13slides_2015-2024.pptx"
prs.save(output_path)
print(f"Presentation saved to: {output_path}")
print(f"Total slides: {len(prs.slides)}")
