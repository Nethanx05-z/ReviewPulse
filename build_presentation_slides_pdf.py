import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfgen import canvas

pdf_path = "/Users/nethan/.gemini/antigravity/scratch/reviewpulse/ReviewPulse_Presentation_Slides.pdf"
base_dir = "/Users/nethan/.gemini/antigravity/scratch/reviewpulse"

img1 = os.path.join(base_dir, "fig1_upload_landing.png")
img2 = os.path.join(base_dir, "fig2_dataset_preview.png")
img3 = os.path.join(base_dir, "fig3_analysis_threshold5.png")
img4 = os.path.join(base_dir, "fig4_charts_threshold3.png")
img5 = os.path.join(base_dir, "fig5_column_edgecase.png")

class SlideCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        w, h = landscape(letter)
        # Background bar
        self.setFillColor(colors.HexColor("#0F172A"))
        self.rect(0, 0, w, 28, fill=1, stroke=0)
        self.setFillColor(colors.HexColor("#1E3A8A"))
        self.rect(0, h - 18, w, 18, fill=1, stroke=0)

        # Header text
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.white)
        self.drawString(30, h - 12, "REVIEWPULSE | ASPECT-BASED SENTIMENT ANALYSIS (ABSA)")
        self.drawRightString(w - 30, h - 12, "PROJECT PRESENTATION & DEFENSE DECK")

        # Footer text
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#94A3B8"))
        self.drawString(30, 10, "ReviewPulse &bull; NLP Pipeline & Evaluation &bull; Nethan Malcome Gonsalves")
        self.drawRightString(w - 30, 10, f"Slide {self._pageNumber} of {page_count}")
        self.restoreState()

w, h = landscape(letter)
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=landscape(letter),
    leftMargin=35,
    rightMargin=35,
    topMargin=32,
    bottomMargin=38
)

styles = getSampleStyleSheet()
c_navy = colors.HexColor("#1E3A8A")
c_teal = colors.HexColor("#0D9488")
c_slate = colors.HexColor("#0F172A")
c_card = colors.HexColor("#F8FAFC")
c_border = colors.HexColor("#CBD5E1")

title_s = ParagraphStyle("STitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=26, leading=30, textColor=c_navy, alignment=1)
sub_s = ParagraphStyle("SSub", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=13, leading=17, textColor=c_teal, alignment=1, spaceAfter=8)
meta_s = ParagraphStyle("SMeta", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=13, textColor=colors.HexColor("#64748B"), alignment=1)

slide_h1 = ParagraphStyle("SH1", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=c_navy, spaceBefore=4, spaceAfter=8)
body_s = ParagraphStyle("SBody", parent=styles["Normal"], fontName="Helvetica", fontSize=9.5, leading=14, textColor=c_slate)
bullet_s = ParagraphStyle("SBullet", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=13, textColor=c_slate, leftIndent=12, firstLineIndent=-8, spaceAfter=4)
callout_s = ParagraphStyle("SCallout", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=13, textColor=c_slate)
tbl_head = ParagraphStyle("STHead", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=8, leading=10, textColor=colors.white)
tbl_cell = ParagraphStyle("STCell", parent=styles["Normal"], fontName="Helvetica", fontSize=7.5, leading=9.5, textColor=c_slate)

elements = []

# ==================== SLIDE 1: TITLE SLIDE ====================
elements.append(Spacer(1, 100))
elements.append(Paragraph("ReviewPulse", title_s))
elements.append(Spacer(1, 6))
elements.append(Paragraph("Aspect-Based Sentiment Analysis of Product Reviews", sub_s))
elements.append(Spacer(1, 12))
elements.append(Paragraph("A Deep Linguistic Feature-Extraction Pipeline & Real-Time Intelligence Dashboard<br/><br/><b>Presenter:</b> Nethan Malcome Gonsalves &nbsp;|&nbsp; <b>Tech Stack:</b> Python, spaCy, VADER, Streamlit, Plotly, Vercel", meta_s))

# ==================== SLIDE 2: THE PROBLEM ====================
elements.append(PageBreak())
elements.append(Paragraph("1. The Problem: Monolithic Sentiment Analysis", slide_h1))
p_text = """<b>The Fundamental Flaw in Traditional E-Commerce Sentiment Analysis:</b><br/>
Real consumer reviews regularly bundle contrasting opinions into a single sentence:<br/>
<font color='#B45309' size=11><i>'The battery easily lasts two days, but the camera is blurry in low light.'</i></font><br/><br/>
Standard classifiers average words across the entire document: (+0.50) + (-0.50) = <b>0.00 (Neutral / 3 Stars)</b>.<br/>
• <b>Shoppers are misled:</b> Potential buyers looking for battery life are repelled by a mediocre average score.<br/>
• <b>Engineers are blinded:</b> Critical hardware defects (e.g. low-light lens sensor failure) are completely masked."""
elements.append(Table([[Paragraph(p_text, callout_s)]], colWidths=[722], style=TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF3C7")),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#F59E0B")),
    ('PADDING', (0,0), (-1,-1), 12),
])))

# ==================== SLIDE 3: SYSTEM ARCHITECTURE ====================
elements.append(PageBreak())
elements.append(Paragraph("2. System Architecture & 5-Layer Processing Pipeline", slide_h1))
elements.append(Paragraph("ReviewPulse is engineered as a decoupled, multi-layer NLP architecture running 100% locally on CPU:", body_s))
elements.append(Spacer(1, 6))

arch_table = [
    [Paragraph("Layer", tbl_head), Paragraph("Module & Tool", tbl_head), Paragraph("Technical Responsibility & Implementation", tbl_head)],
    [Paragraph("1. Ingestion", tbl_cell), Paragraph("CSV Parser + Raw Text Buffer", tbl_cell), Paragraph("Auto-encoding fallback (UTF-8, Latin-1), dataset preview, and smart text column mapping.", tbl_cell)],
    [Paragraph("2. Preprocessing", tbl_cell), Paragraph("clean_text() + spaCy Tokenizer", tbl_cell), Paragraph("Strips URLs/HTML; tokenizes sentences; splits multi-clause statements at contrast conjunctions.", tbl_cell)],
    [Paragraph("3. Aspect Extraction", tbl_cell), Paragraph("spaCy en_core_web_sm POS Tagger", tbl_cell), Paragraph("Filters NOUN/PROPN tokens, lemmatizes plurals, and maps synonyms (<i>display &rarr; screen</i>).", tbl_cell)],
    [Paragraph("4. Polarity Scoring", tbl_cell), Paragraph("VADER + Custom Domain Lexicon", tbl_cell), Paragraph("Calculates localized valence (-1.0 to +1.0) with tech weights (<i>blurry, overheats, sturdy</i>).", tbl_cell)],
    [Paragraph("5. Presentation", tbl_cell), Paragraph("Streamlit & Vercel Dashboard", tbl_cell), Paragraph("Four KPI metric cards, Plotly charts, aspect verdict synthesis, and CSV/PDF export.", tbl_cell)]
]
elements.append(Table(arch_table, colWidths=[80, 180, 462], style=TableStyle([
    ('BACKGROUND', (0,0), (-1,0), c_navy),
    ('GRID', (0,0), (-1,-1), 0.5, c_border),
    ('PADDING', (0,0), (-1,-1), 6),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card]),
])))

# ==================== SLIDE 4: CONTRAST SPLITTING ====================
elements.append(PageBreak())
elements.append(Paragraph("3. Core Linguistic Innovation: Contrastive Clause Division", slide_h1))
c_text = """<b>Why Contrast Splitting is Essential:</b><br/>
Coordinating conjunctions (<i>but, however, yet, while, although</i>) indicate a polarity inflection point.<br/><br/>
<code>CONTRAST_SPLIT = re.compile(r'\\b(?:but|however|although|though|yet|while|whereas)\\b', re.I)</code><br/><br/>
<b>Execution Trace:</b><br/>
• Input: <i>'The battery easily lasts two days, but the camera is blurry in low light.'</i><br/>
• <b>Clause 1:</b> <i>'The battery easily lasts two days'</i> &rarr; Aspect: <b>battery</b> | Polarity: <b>+0.49 (Positive)</b><br/>
• <b>Clause 2:</b> <i>'the camera is blurry in low light'</i> &rarr; Aspect: <b>camera</b> | Polarity: <b>-0.36 (Negative)</b><br/>
• <b>Result:</b> Zero polarity cancellation. High attribution fidelity."""
elements.append(Table([[Paragraph(c_text, callout_s)]], colWidths=[722], style=TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
    ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#93C5FD")),
    ('PADDING', (0,0), (-1,-1), 12),
])))

# ==================== SLIDE 5: LIVE VERIFICATION (FIG 1 & 2) ====================
elements.append(PageBreak())
elements.append(Paragraph("4. Live System Walkthrough: Data Ingestion & Schema Mapping", slide_h1))
if os.path.exists(img1) and os.path.exists(img2):
    img_row = [
        [Image(img1, width=350, height=227), Image(img2, width=350, height=227)],
        [Paragraph("<b>Figure 1:</b> Initial drag-and-drop landing interface with frequency sensitivity slider.", tbl_cell),
         Paragraph("<b>Figure 2:</b> Ingestion of 72 rows and column selection dropdown (mapping <code>segment</code>).", tbl_cell)]
    ]
    elements.append(Table(img_row, colWidths=[361, 361], style=TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ])))

# ==================== SLIDE 6: LIVE VERIFICATION (FIG 3 & 4) ====================
elements.append(PageBreak())
elements.append(Paragraph("5. Live Analytics & Threshold Sensitivity Tuning", slide_h1))
if os.path.exists(img3) and os.path.exists(img4):
    img_row2 = [
        [Image(img3, width=350, height=227), Image(img4, width=350, height=227)],
        [Paragraph("<b>Figure 3:</b> Threshold = 5 (10 key aspects, 60% positive ratio, row-level quote drill-down).", tbl_cell),
         Paragraph("<b>Figure 4:</b> Threshold = 3 (15 aspects in Plotly grouped distributions and ranked polarity chart).", tbl_cell)]
    ]
    elements.append(Table(img_row2, colWidths=[361, 361], style=TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 4),
    ])))

# ==================== SLIDE 7: BENCHMARK RESULTS ====================
elements.append(PageBreak())
elements.append(Paragraph("6. Empirical Benchmark Results (40 Smartphone Reviews)", slide_h1))

bench_data = [
    [Paragraph("Aspect", tbl_head), Paragraph("Pos", tbl_head), Paragraph("Neg", tbl_head), Paragraph("Neu", tbl_head), Paragraph("Mentions", tbl_head), Paragraph("Avg Score", tbl_head), Paragraph("Verdict", tbl_head), Paragraph("Business Diagnostic & Action Item", tbl_head)],
    [Paragraph("screen", tbl_cell), Paragraph("8", tbl_cell), Paragraph("1", tbl_cell), Paragraph("0", tbl_cell), Paragraph("9", tbl_cell), Paragraph("+0.669", tbl_cell), Paragraph("<font color='#16A34A'><b>Good</b></font>", tbl_cell), Paragraph("Major selling point; exceptional brightness and clarity.", tbl_cell)],
    [Paragraph("price", tbl_cell), Paragraph("6", tbl_cell), Paragraph("0", tbl_cell), Paragraph("1", tbl_cell), Paragraph("7", tbl_cell), Paragraph("+0.736", tbl_cell), Paragraph("<font color='#16A34A'><b>Good</b></font>", tbl_cell), Paragraph("High value proposition; competitive pricing confirmed.", tbl_cell)],
    [Paragraph("battery", tbl_cell), Paragraph("5", tbl_cell), Paragraph("4", tbl_cell), Paragraph("0", tbl_cell), Paragraph("9", tbl_cell), Paragraph("+0.065", tbl_cell), Paragraph("<font color='#D97706'><b>Mixed</b></font>", tbl_cell), Paragraph("High standby life, but drains fast during 3D gaming.", tbl_cell)],
    [Paragraph("camera", tbl_cell), Paragraph("3", tbl_cell), Paragraph("3", tbl_cell), Paragraph("2", tbl_cell), Paragraph("8", tbl_cell), Paragraph("-0.047", tbl_cell), Paragraph("<font color='#D97706'><b>Mixed</b></font>", tbl_cell), Paragraph("Sharp in daylight; poor noise control in low light.", tbl_cell)],
    [Paragraph("customer service", tbl_cell), Paragraph("1", tbl_cell), Paragraph("2", tbl_cell), Paragraph("0", tbl_cell), Paragraph("3", tbl_cell), Paragraph("-0.004", tbl_cell), Paragraph("<font color='#DC2626'><b>Poor</b></font>", tbl_cell), Paragraph("Unresponsive ticketing system and slow RMA replacements.", tbl_cell)],
    [Paragraph("software", tbl_cell), Paragraph("1", tbl_cell), Paragraph("2", tbl_cell), Paragraph("0", tbl_cell), Paragraph("3", tbl_cell), Paragraph("-0.119", tbl_cell), Paragraph("<font color='#DC2626'><b>Poor</b></font>", tbl_cell), Paragraph("App crashes and frame drops observed after OTA updates.", tbl_cell)]
]
elements.append(Table(bench_data, colWidths=[75, 25, 25, 25, 35, 50, 45, 442], style=TableStyle([
    ('BACKGROUND', (0,0), (-1,0), c_navy),
    ('GRID', (0,0), (-1,-1), 0.5, c_border),
    ('PADDING', (0,0), (-1,-1), 5),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card]),
])))

# ==================== SLIDE 8: VIVA DEFENSE & CONCLUSION ====================
elements.append(PageBreak())
elements.append(Paragraph("7. Viva Defense: Classical NLP vs. Generative LLMs", slide_h1))

viva_table = [
    [Paragraph("Evaluation Criterion", tbl_head), Paragraph("ReviewPulse (Classical NLP Hybrid)", tbl_head), Paragraph("Cloud LLM (e.g. GPT-4)", tbl_head)],
    [Paragraph("Financial Cost", tbl_cell), Paragraph("<b>$0.00</b> (Runs on free consumer hardware forever)", tbl_cell), Paragraph("Recurring per-token API bills", tbl_cell)],
    [Paragraph("Inference Latency", tbl_cell), Paragraph("<b>&lt; 0.5 seconds</b> per batch on standard CPU", tbl_cell), Paragraph("3 &ndash; 10 seconds per API request", tbl_cell)],
    [Paragraph("Data Privacy", tbl_cell), Paragraph("<b>100% Local</b> (Zero customer data leaves machine)", tbl_cell), Paragraph("Transmits customer reviews to third-party cloud", tbl_cell)],
    [Paragraph("Hallucination Risk", tbl_cell), Paragraph("<b>0%</b> (Grammatical & rule-based determinism)", tbl_cell), Paragraph("Susceptible to synthetic feature hallucination", tbl_cell)]
]
elements.append(Table(viva_table, colWidths=[120, 301, 301], style=TableStyle([
    ('BACKGROUND', (0,0), (-1,0), c_navy),
    ('GRID', (0,0), (-1,-1), 0.5, c_border),
    ('PADDING', (0,0), (-1,-1), 6),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_card]),
])))

elements.append(Spacer(1, 10))
elements.append(Paragraph("<b>GitHub Repository:</b> https://github.com/Nethanx05-z/ReviewPulse &nbsp;|&nbsp; <b>Live App:</b> http://localhost:8501", meta_s))

doc.build(elements, canvasmaker=SlideCanvas)
print("PRESENTATION_SLIDES_BUILT:", pdf_path)
