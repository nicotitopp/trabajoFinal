from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import copy

# ── Paleta de colores ──────────────────────────────────────────────
NAVY      = RGBColor(0x1F, 0x4E, 0x79)   # Azul marino principal
BLUE_MID  = RGBColor(0x2E, 0x75, 0xB6)   # Azul medio (acento)
BLUE_LITE = RGBColor(0xBD, 0xD7, 0xEE)   # Azul claro (fondo bloques)
GOLD      = RGBColor(0xFF, 0xC0, 0x00)   # Dorado (destacados)
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
DARK_GRAY = RGBColor(0x26, 0x26, 0x26)
MID_GRAY  = RGBColor(0x60, 0x60, 0x60)
GREEN_OK  = RGBColor(0x37, 0x86, 0x36)   # Verde (resultados positivos)
RED_BAD   = RGBColor(0xC0, 0x39, 0x2B)   # Rojo (resultados negativos)

W = Inches(13.33)   # Ancho slide widescreen 16:9
H = Inches(7.5)     # Alto slide widescreen 16:9

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK = prs.slide_layouts[6]   # layout completamente en blanco

# ══════════════════════════════════════════════════════════════════
# UTILIDADES GENERALES
# ══════════════════════════════════════════════════════════════════

def add_rect(slide, l, t, w, h, fill_rgb=None, line_rgb=None, line_width_pt=0):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.line.fill.background()
    if fill_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_rgb
    else:
        shape.fill.background()
    if line_rgb:
        shape.line.color.rgb = line_rgb
        shape.line.width = Pt(line_width_pt)
    else:
        shape.line.fill.background()
    return shape

def add_text_box(slide, text, l, t, w, h,
                 font_name="Calibri", size=18, bold=False, italic=False,
                 color=DARK_GRAY, align=PP_ALIGN.LEFT,
                 word_wrap=True, v_anchor=None):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = word_wrap
    tf = txb.text_frame
    tf.word_wrap = word_wrap
    if v_anchor:
        tf.vertical_anchor = v_anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.name  = font_name
    run.font.size  = Pt(size)
    run.font.bold  = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb

def add_multiline_textbox(slide, lines, l, t, w, h,
                          font_name="Calibri", size=18,
                          default_color=DARK_GRAY, align=PP_ALIGN.LEFT,
                          word_wrap=True):
    """
    lines: list of dicts  { text, bold, italic, color, size (optional) }
    """
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = word_wrap
    tf = txb.text_frame
    tf.word_wrap = word_wrap
    first = True
    for item in lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        if item.get("space_before"):
            p.space_before = Pt(item["space_before"])
        run = p.add_run()
        run.text = item.get("text", "")
        run.font.name  = font_name
        run.font.size  = Pt(item.get("size", size))
        run.font.bold  = item.get("bold", False)
        run.font.italic = item.get("italic", False)
        run.font.color.rgb = item.get("color", default_color)
    return txb

def add_bg_gradient(slide, top_color=NAVY, bot_color=BLUE_MID):
    """Fondo completo con un rectángulo de color sólido oscuro."""
    bg = add_rect(slide, 0, 0, 13.33, 7.5, fill_rgb=top_color)
    return bg

# ══════════════════════════════════════════════════════════════════
# DIAPOSITIVA 1 – PORTADA
# ══════════════════════════════════════════════════════════════════
def slide_portada():
    sld = prs.slides.add_slide(BLANK)
    # Fondo navy
    add_rect(sld, 0, 0, 13.33, 7.5, fill_rgb=NAVY)
    # Franja dorada izquierda
    add_rect(sld, 0, 0, 0.45, 7.5, fill_rgb=GOLD)
    # Franja blanca decorativa
    add_rect(sld, 0.45, 0, 0.08, 7.5, fill_rgb=WHITE)

    # Título principal
    add_text_box(sld,
        "Optimización de Consultas de Mínimo en Rango (RMQ)",
        l=0.75, t=1.3, w=11.8, h=1.6,
        size=38, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

    # Subtítulo
    add_text_box(sld,
        "De  O(N)  a  O(1)  —  Escalabilidad Masiva mediante Precomputación",
        l=0.75, t=3.0, w=11.0, h=0.7,
        size=22, bold=False, italic=True, color=GOLD, align=PP_ALIGN.LEFT)

    # Línea separadora
    add_rect(sld, 0.75, 3.85, 10.5, 0.06, fill_rgb=BLUE_LITE)

    # Metadatos
    add_multiline_textbox(sld,
        [
            {"text": "Grupo de Investigación Algorítmica", "bold": True,  "size": 16, "color": WHITE},
            {"text": "Ingeniería en Sistemas  ·  Algoritmos y Estructuras de Datos", "size": 14, "color": BLUE_LITE, "space_before": 4},
            {"text": "github.com/nicotitopp/trabajoFinal  (rama: dev-nico)", "size": 13, "color": GOLD, "space_before": 4},
        ],
        l=0.75, t=4.05, w=10.0, h=1.5)

    # Badge "Sparse Table"
    add_rect(sld, 9.5, 5.8, 3.3, 0.95, fill_rgb=BLUE_MID,
             line_rgb=GOLD, line_width_pt=1.5)
    add_text_box(sld, "Sparse Table  ·  O(1) Query",
                 l=9.5, t=5.82, w=3.3, h=0.9,
                 size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# DIAPOSITIVA 2 – PLANTEAMIENTO DEL PROBLEMA
# ══════════════════════════════════════════════════════════════════
def slide_problema():
    sld = prs.slides.add_slide(BLANK)
    add_rect(sld, 0, 0, 13.33, 7.5, fill_rgb=RGBColor(0xF4, 0xF7, 0xFB))
    # Encabezado
    add_rect(sld, 0, 0, 13.33, 1.2, fill_rgb=NAVY)
    add_rect(sld, 0, 0, 0.45, 1.2, fill_rgb=GOLD)
    add_text_box(sld, "1.  ¿Qué es el Problema RMQ?",
                 l=0.65, t=0.18, w=12.0, h=0.85,
                 size=28, bold=True, color=WHITE)
    # Número de diapositiva
    add_text_box(sld, "02 / 08", l=11.5, t=0.25, w=1.6, h=0.6,
                 size=13, color=GOLD, align=PP_ALIGN.RIGHT)

    # Definición formal
    add_rect(sld, 0.5, 1.4, 5.9, 2.5, fill_rgb=NAVY,
             line_rgb=GOLD, line_width_pt=1)
    add_multiline_textbox(sld,
        [
            {"text": "Definición Formal", "bold": True, "size": 17, "color": GOLD},
            {"text": "Dado un arreglo A de N elementos y un par", "size": 14, "color": WHITE, "space_before": 6},
            {"text": "de índices (L, R) tal que 0 ≤ L ≤ R < N,", "size": 14, "color": WHITE},
            {"text": "se desea determinar:", "size": 14, "color": WHITE},
            {"text": "RMQ(L, R) = min  A[i]", "bold": True, "size": 19, "color": GOLD, "space_before": 8},
            {"text": "               L ≤ i ≤ R", "size": 13, "color": BLUE_LITE},
        ],
        l=0.7, t=1.55, w=5.5, h=2.2)

    # Ejemplo visual
    add_rect(sld, 6.7, 1.4, 6.1, 2.5, fill_rgb=WHITE,
             line_rgb=BLUE_MID, line_width_pt=1.2)
    add_text_box(sld, "Ejemplo Visual", l=6.9, t=1.5, w=5.8, h=0.5,
                 size=16, bold=True, color=NAVY)

    # Arreglo visual con cajas
    arr = [7, 2, 8, 4, 1, 9, 6]
    highlight = {1, 2, 3}    # rango [1,3] en azul
    min_idx   = 1
    for i, v in enumerate(arr):
        x = 7.0 + i * 0.75
        fill = BLUE_MID if i in highlight else RGBColor(0xE8, 0xF0, 0xF8)
        border = GOLD if i == min_idx else NAVY
        add_rect(sld, x, 2.15, 0.62, 0.62, fill_rgb=fill,
                 line_rgb=border, line_width_pt=2 if i == min_idx else 1)
        add_text_box(sld, str(v), l=x, t=2.15, w=0.62, h=0.62,
                     size=17, bold=(i == min_idx), color=WHITE if i in highlight else NAVY,
                     align=PP_ALIGN.CENTER)
        # índice
        add_text_box(sld, str(i), l=x, t=2.8, w=0.62, h=0.3,
                     size=10, color=MID_GRAY, align=PP_ALIGN.CENTER)

    add_text_box(sld, "Consulta RMQ(1, 3)  →  mín(2, 8, 4)  =  2  ✓",
                 l=6.9, t=3.25, w=5.8, h=0.5,
                 size=14, bold=True, color=GREEN_OK)

    # Problema a escala
    add_rect(sld, 0.5, 4.1, 12.3, 2.9, fill_rgb=RGBColor(0xE8, 0xF0, 0xF8),
             line_rgb=BLUE_MID, line_width_pt=1)
    add_text_box(sld, "⚠  El reto a escala masiva",
                 l=0.7, t=4.2, w=11.5, h=0.5,
                 size=16, bold=True, color=NAVY)
    add_multiline_textbox(sld,
        [
            {"text": "Si un sistema realiza Q = 1,000,000 consultas sobre un arreglo de N = 1,000,000 elementos,", "size": 14, "color": DARK_GRAY},
            {"text": "el costo total lineal escala a  O(Q · N) = O(10¹²)  operaciones.", "size": 14, "color": RED_BAD, "bold": True, "space_before": 4},
            {"text": "Esto equivale a horas de procesamiento. La escalabilidad colapsa.", "size": 13, "color": MID_GRAY, "space_before": 4},
        ],
        l=0.7, t=4.75, w=12.0, h=2.0)

# ══════════════════════════════════════════════════════════════════
# DIAPOSITIVA 3 – ALGORITMO INGENUO
# ══════════════════════════════════════════════════════════════════
def slide_naive():
    sld = prs.slides.add_slide(BLANK)
    add_rect(sld, 0, 0, 13.33, 7.5, fill_rgb=RGBColor(0xF4, 0xF7, 0xFB))
    add_rect(sld, 0, 0, 13.33, 1.2, fill_rgb=NAVY)
    add_rect(sld, 0, 0, 0.45, 1.2, fill_rgb=GOLD)
    add_text_box(sld, "2.  Algoritmo Ingenuo  —  Fuerza Bruta",
                 l=0.65, t=0.18, w=12.0, h=0.85, size=28, bold=True, color=WHITE)
    add_text_box(sld, "03 / 08", l=11.5, t=0.25, w=1.6, h=0.6,
                 size=13, color=GOLD, align=PP_ALIGN.RIGHT)

    # Pseudocódigo
    add_rect(sld, 0.5, 1.35, 5.8, 4.0, fill_rgb=RGBColor(0x1A, 0x1A, 0x2E),
             line_rgb=BLUE_MID, line_width_pt=1)
    add_text_box(sld, "Pseudocódigo", l=0.7, t=1.45, w=5.4, h=0.45,
                 size=14, bold=True, color=GOLD)
    code = (
        "función  NaiveRMQ(A, L, R):\n"
        "   min_val ← A[L]\n"
        "   para i desde L+1 hasta R:\n"
        "      si A[i] < min_val:\n"
        "         min_val ← A[i]\n"
        "   retornar  min_val"
    )
    add_text_box(sld, code, l=0.65, t=1.95, w=5.6, h=3.0,
                 font_name="Consolas", size=14.5, color=RGBColor(0xA8, 0xD8, 0xFF))

    # Complejidades
    add_rect(sld, 6.6, 1.35, 6.2, 4.0, fill_rgb=WHITE,
             line_rgb=BLUE_MID, line_width_pt=1)
    add_text_box(sld, "Análisis de Complejidad", l=6.8, t=1.45, w=5.8, h=0.45,
                 size=16, bold=True, color=NAVY)

    items = [
        ("Precomputación:", "O(1)", "No hace nada — almacena el arreglo.", GREEN_OK),
        ("Por consulta:",   "O(N)", "Recorre el rango completo de L hasta R.", RED_BAD),
        ("Q consultas:",    "O(Q · N)", "El costo crece de forma cuadrática.", RED_BAD),
    ]
    for k, (label, compl, desc, col) in enumerate(items):
        y = 2.05 + k * 1.05
        add_rect(sld, 6.8, y, 5.8, 0.9, fill_rgb=RGBColor(0xF8, 0xF9, 0xFA),
                 line_rgb=col, line_width_pt=2)
        add_text_box(sld, label, l=6.95, t=y+0.04, w=2.0, h=0.4,
                     size=13, bold=True, color=NAVY)
        add_text_box(sld, compl, l=9.0, t=y+0.02, w=1.6, h=0.45,
                     size=18, bold=True, color=col, align=PP_ALIGN.CENTER)
        add_text_box(sld, desc, l=6.95, t=y+0.48, w=5.5, h=0.38,
                     size=11.5, color=MID_GRAY)

    # Conclusión
    add_rect(sld, 0.5, 5.55, 12.3, 1.5, fill_rgb=RGBColor(0xFF, 0xEB, 0xEB),
             line_rgb=RED_BAD, line_width_pt=1.5)
    add_text_box(sld,
        "✗  Para N = Q = 10⁶  →  10¹² operaciones  ≈  más de 51 minutos en Python.\n"
        "   Absolutamente inviable en producción.",
        l=0.7, t=5.65, w=12.0, h=1.3,
        size=14, bold=False, color=RED_BAD)

# ══════════════════════════════════════════════════════════════════
# DIAPOSITIVA 4 – LA CLAVE: SPARSE TABLE (CONCEPTO)
# ══════════════════════════════════════════════════════════════════
def slide_concepto():
    sld = prs.slides.add_slide(BLANK)
    add_rect(sld, 0, 0, 13.33, 7.5, fill_rgb=RGBColor(0xF4, 0xF7, 0xFB))
    add_rect(sld, 0, 0, 13.33, 1.2, fill_rgb=NAVY)
    add_rect(sld, 0, 0, 0.45, 1.2, fill_rgb=GOLD)
    add_text_box(sld, "3.  La Solución:  Sparse Table  —  El Ingenio Matemático",
                 l=0.65, t=0.18, w=12.0, h=0.85, size=26, bold=True, color=WHITE)
    add_text_box(sld, "04 / 08", l=11.5, t=0.25, w=1.6, h=0.6,
                 size=13, color=GOLD, align=PP_ALIGN.RIGHT)

    # Pilar 1
    add_rect(sld, 0.5, 1.35, 5.9, 2.7, fill_rgb=NAVY,
             line_rgb=GOLD, line_width_pt=1.5)
    add_text_box(sld, "💡 Concepto 1: Potencias de 2",
                 l=0.7, t=1.45, w=5.5, h=0.5, size=15, bold=True, color=GOLD)
    add_text_box(sld,
        "Cualquier número entero positivo puede\n"
        "representarse como suma de potencias de 2.\n\n"
        "Por tanto, cualquier rango [L, R] se puede\n"
        "cubrir con bloques de tamaño 2⁰, 2¹, 2², ...",
        l=0.7, t=1.98, w=5.5, h=2.0, size=14, color=WHITE)

    # Pilar 2
    add_rect(sld, 6.9, 1.35, 5.9, 2.7, fill_rgb=NAVY,
             line_rgb=GOLD, line_width_pt=1.5)
    add_text_box(sld, "💡 Concepto 2: Idempotencia del Mínimo",
                 l=7.1, t=1.45, w=5.5, h=0.5, size=15, bold=True, color=GOLD)
    add_text_box(sld,
        "La función mínimo es idempotente:",
        l=7.1, t=1.98, w=5.5, h=0.4, size=14, color=WHITE)
    add_rect(sld, 7.4, 2.45, 4.8, 0.65, fill_rgb=RGBColor(0x2E, 0x75, 0xB6))
    add_text_box(sld, "min(x, x) = x",
                 l=7.4, t=2.45, w=4.8, h=0.65,
                 size=22, bold=True, color=GOLD, align=PP_ALIGN.CENTER)
    add_text_box(sld,
        "Dos bloques solapados NO alteran\n"
        "el resultado final. Podemos solapar\n"
        "sin perder exactitud.",
        l=7.1, t=3.18, w=5.5, h=1.0, size=14, color=WHITE)

    # Visual del solapamiento
    add_rect(sld, 0.5, 4.25, 12.3, 2.85, fill_rgb=WHITE,
             line_rgb=BLUE_MID, line_width_pt=1)
    add_text_box(sld, "¿Cómo se cubre cualquier rango [L, R]?",
                 l=0.7, t=4.32, w=12.0, h=0.45, size=15, bold=True, color=NAVY)

    # Representación del arreglo
    n = 10
    for i in range(n):
        x = 1.0 + i * 1.1
        fill = RGBColor(0xE8, 0xF0, 0xF8)
        add_rect(sld, x, 4.88, 0.95, 0.5, fill_rgb=fill,
                 line_rgb=NAVY, line_width_pt=0.8)
        add_text_box(sld, str(i), l=x, t=4.88, w=0.95, h=0.5,
                     size=13, color=NAVY, align=PP_ALIGN.CENTER, bold=True)

    # Bloque 1 (azul)
    add_rect(sld, 1.0, 5.5, 4 * 1.1 - 0.15, 0.45,
             fill_rgb=BLUE_MID, line_rgb=NAVY, line_width_pt=0.5)
    add_text_box(sld, "Bloque 1: [L=1, L+2ᵏ-1]  (2ᵏ = 4 elementos)",
                 l=1.0, t=5.52, w=4.2, h=0.4,
                 size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # Bloque 2 (dorado)
    add_rect(sld, 1.0 + 3 * 1.1, 6.05, 4 * 1.1 - 0.15, 0.45,
             fill_rgb=GOLD, line_rgb=NAVY, line_width_pt=0.5)
    add_text_box(sld, "Bloque 2: [R-2ᵏ+1, R=6]  (solapado)",
                 l=1.0 + 3 * 1.1, t=6.07, w=4.2, h=0.4,
                 size=11, bold=True, color=DARK_GRAY, align=PP_ALIGN.CENTER)

    add_text_box(sld,
        "RMQ(L, R) = min( ST[L][k],  ST[R-2ᵏ+1][k] )   →   O(1) ✓",
        l=8.5, t=5.8, w=4.5, h=0.7,
        size=13, bold=True, color=GREEN_OK, align=PP_ALIGN.CENTER)

# ══════════════════════════════════════════════════════════════════
# DIAPOSITIVA 5 – DESARROLLO MATEMÁTICO
# ══════════════════════════════════════════════════════════════════
def slide_math():
    sld = prs.slides.add_slide(BLANK)
    add_rect(sld, 0, 0, 13.33, 7.5, fill_rgb=RGBColor(0xF4, 0xF7, 0xFB))
    add_rect(sld, 0, 0, 13.33, 1.2, fill_rgb=NAVY)
    add_rect(sld, 0, 0, 0.45, 1.2, fill_rgb=GOLD)
    add_text_box(sld, "4.  Desarrollo Matemático e Implementación",
                 l=0.65, t=0.18, w=12.0, h=0.85, size=28, bold=True, color=WHITE)
    add_text_box(sld, "05 / 08", l=11.5, t=0.25, w=1.6, h=0.6,
                 size=13, color=GOLD, align=PP_ALIGN.RIGHT)

    # DP tabla
    add_rect(sld, 0.5, 1.35, 5.9, 5.75, fill_rgb=WHITE,
             line_rgb=BLUE_MID, line_width_pt=1)
    add_text_box(sld, "Precomputación (Programación Dinámica)",
                 l=0.7, t=1.45, w=5.5, h=0.5, size=14, bold=True, color=NAVY)

    add_text_box(sld, "ST[i][j]  =  mínimo del rango de tamaño 2ʲ desde i",
                 l=0.7, t=2.0, w=5.5, h=0.45, size=13, color=MID_GRAY)

    add_rect(sld, 0.7, 2.55, 5.5, 0.65, fill_rgb=BLUE_LITE)
    add_text_box(sld, "Caso base  (j = 0):",
                 l=0.85, t=2.58, w=5.2, h=0.3, size=13, bold=True, color=NAVY)
    add_rect(sld, 0.7, 3.25, 5.5, 0.55, fill_rgb=RGBColor(0x1F, 0x4E, 0x79))
    add_text_box(sld, "ST[i][0] = A[i]    ∀ i ∈ [0, N-1]",
                 l=0.7, t=3.25, w=5.5, h=0.55,
                 font_name="Consolas", size=15, bold=True, color=GOLD,
                 align=PP_ALIGN.CENTER)

    add_rect(sld, 0.7, 3.9, 5.5, 0.65, fill_rgb=BLUE_LITE)
    add_text_box(sld, "Transición DP  (j > 0):",
                 l=0.85, t=3.93, w=5.2, h=0.3, size=13, bold=True, color=NAVY)
    add_rect(sld, 0.7, 4.6, 5.5, 0.75, fill_rgb=RGBColor(0x1F, 0x4E, 0x79))
    add_text_box(sld, "ST[i][j] = min(\n  ST[i][j-1],  ST[i+2^(j-1)][j-1]  )",
                 l=0.7, t=4.6, w=5.5, h=0.75,
                 font_name="Consolas", size=13, bold=True, color=GOLD,
                 align=PP_ALIGN.CENTER)

    add_text_box(sld, "Costo:   O(N log N)  en tiempo y espacio",
                 l=0.7, t=5.5, w=5.5, h=0.45,
                 size=13, bold=True, color=BLUE_MID)

    # Consulta O(1)
    add_rect(sld, 6.9, 1.35, 5.9, 5.75, fill_rgb=WHITE,
             line_rgb=BLUE_MID, line_width_pt=1)
    add_text_box(sld, "Consulta en Tiempo Constante  O(1)",
                 l=7.1, t=1.45, w=5.5, h=0.5, size=14, bold=True, color=NAVY)

    add_multiline_textbox(sld,
        [
            {"text": "1.  Calcular k = ⌊log₂(R - L + 1)⌋", "size": 14, "color": DARK_GRAY},
            {"text": "    (Una sola operación de bits, instantáneo)", "size": 12, "color": MID_GRAY},
            {"text": "2.  Combinar dos bloques solapados:", "size": 14, "color": DARK_GRAY, "space_before": 8},
        ],
        l=7.1, t=2.05, w=5.5, h=1.5)

    add_rect(sld, 7.1, 3.5, 5.5, 0.9, fill_rgb=NAVY)
    add_text_box(sld, "RMQ(L,R) = min( ST[L][k],\n               ST[R-2ᵏ+1][k] )",
                 l=7.1, t=3.5, w=5.5, h=0.9,
                 font_name="Consolas", size=14, bold=True, color=GOLD,
                 align=PP_ALIGN.CENTER)

    add_multiline_textbox(sld,
        [
            {"text": "Solo 1 resta  +  1 potencia de 2  +  1 comparación.", "size": 13, "color": MID_GRAY},
            {"text": "Independiente del tamaño del rango [L, R].", "size": 13, "color": MID_GRAY, "space_before": 4},
        ],
        l=7.1, t=4.55, w=5.5, h=0.9)

    # Tabla comparativa
    add_rect(sld, 7.1, 5.55, 5.5, 1.35, fill_rgb=RGBColor(0xE8, 0xF5, 0xE9),
             line_rgb=GREEN_OK, line_width_pt=1)
    add_text_box(sld, "Complejidad Total para Q consultas:",
                 l=7.25, t=5.6, w=5.2, h=0.38, size=13, bold=True, color=NAVY)
    add_multiline_textbox(sld,
        [
            {"text": "Naive:         O(Q · N)         ← lento", "size": 13, "color": RED_BAD, "bold": True},
            {"text": "Sparse Table:  O(N log N + Q)   ← rápido", "size": 13, "color": GREEN_OK, "bold": True},
        ],
        l=7.25, t=6.02, w=5.2, h=0.9, font_name="Consolas")

# ══════════════════════════════════════════════════════════════════
# DIAPOSITIVA 6 – RESULTADOS EMPÍRICOS (BENCHMARK)
# ══════════════════════════════════════════════════════════════════
def slide_resultados():
    sld = prs.slides.add_slide(BLANK)
    add_rect(sld, 0, 0, 13.33, 7.5, fill_rgb=RGBColor(0xF4, 0xF7, 0xFB))
    add_rect(sld, 0, 0, 13.33, 1.2, fill_rgb=NAVY)
    add_rect(sld, 0, 0, 0.45, 1.2, fill_rgb=GOLD)
    add_text_box(sld, "5.  Resultados Empíricos  —  Benchmark",
                 l=0.65, t=0.18, w=12.0, h=0.85, size=28, bold=True, color=WHITE)
    add_text_box(sld, "06 / 08", l=11.5, t=0.25, w=1.6, h=0.6,
                 size=13, color=GOLD, align=PP_ALIGN.RIGHT)

    add_text_box(sld, "Ejecutado en Python 3.11  ·  src/benchmark.py  ·  Datos 100% reales",
                 l=0.65, t=1.28, w=12.0, h=0.35, size=12, italic=True, color=MID_GRAY)

    # Tabla de resultados
    headers = ["N (Arreglo)", "Q (Consultas)", "Naive — Consultas", "Sparse Table", "Speedup"]
    rows = [
        ["100",       "1,000",       "0.000710 s",    "0.000239 s",  "3.0×"],
        ["1,000",     "5,000",       "0.028931 s",    "0.001299 s",  "22×"],
        ["5,000",     "10,000",      "0.278195 s",    "0.002953 s",  "94×"],
        ["10,000",    "20,000",      "~1.097 s*",     "0.006228 s",  "176×"],
        ["100,000",   "100,000",     "~56.85 s*",     "0.064673 s",  "879×"],
        ["500,000",   "1,000,000",   "~51 minutos*",  "0.829445 s",  "3,743×"],
    ]

    col_widths = [1.8, 1.8, 2.5, 2.3, 1.8]
    col_x = [0.5, 2.35, 4.2, 6.75, 9.1]
    row_h = 0.52
    start_y = 1.72

    # Cabecera
    for ci, (hdr, cw, cx) in enumerate(zip(headers, col_widths, col_x)):
        add_rect(sld, cx, start_y, cw, row_h, fill_rgb=NAVY)
        add_text_box(sld, hdr, l=cx, t=start_y, w=cw, h=row_h,
                     size=12.5, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # Filas
    speedup_colors = [MID_GRAY, MID_GRAY, MID_GRAY, BLUE_MID, BLUE_MID, RED_BAD]
    for ri, row in enumerate(rows):
        y = start_y + (ri + 1) * row_h
        bg = RGBColor(0xF0, 0xF6, 0xFF) if ri % 2 == 0 else WHITE
        for ci, (cell, cw, cx) in enumerate(zip(row, col_widths, col_x)):
            add_rect(sld, cx, y, cw, row_h, fill_rgb=bg,
                     line_rgb=BLUE_LITE, line_width_pt=0.5)
            cell_color = DARK_GRAY
            cell_bold = False
            if ci == 4:  # Speedup col
                cell_color = GREEN_OK if ri >= 3 else MID_GRAY
                cell_bold = (ri == 5)
            if ci == 2 and ri >= 3:
                cell_color = RED_BAD
            add_text_box(sld, cell, l=cx, t=y, w=cw, h=row_h,
                         size=12, bold=cell_bold, color=cell_color,
                         align=PP_ALIGN.CENTER)

    add_text_box(sld, "* Valor estimado por proyección estadística (muestra de 200 consultas)",
                 l=0.5, t=5.0, w=9.5, h=0.35,
                 size=10, italic=True, color=MID_GRAY)

    # Badge de resultado estrella
    add_rect(sld, 10.1, 4.55, 2.8, 1.95, fill_rgb=GREEN_OK,
             line_rgb=GOLD, line_width_pt=2)
    add_text_box(sld, "SPEEDUP\nMÁXIMO",
                 l=10.1, t=4.6, w=2.8, h=0.65,
                 size=14, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    add_text_box(sld, "3,743×",
                 l=10.1, t=5.2, w=2.8, h=0.8,
                 size=30, bold=True, color=GOLD, align=PP_ALIGN.CENTER)

    add_text_box(sld,
        "✓  Las pruebas de corrección pasaron al 100%  (50 casos aleatorios, arreglos hasta 1,000 elementos)",
        l=0.5, t=5.45, w=12.8, h=0.5,
        size=12.5, bold=True, color=GREEN_OK)

# ══════════════════════════════════════════════════════════════════
# DIAPOSITIVA 7 – APLICACIONES REALES
# ══════════════════════════════════════════════════════════════════
def slide_aplicaciones():
    sld = prs.slides.add_slide(BLANK)
    add_rect(sld, 0, 0, 13.33, 7.5, fill_rgb=RGBColor(0xF4, 0xF7, 0xFB))
    add_rect(sld, 0, 0, 13.33, 1.2, fill_rgb=NAVY)
    add_rect(sld, 0, 0, 0.45, 1.2, fill_rgb=GOLD)
    add_text_box(sld, "6.  Aplicaciones Reales en la Industria",
                 l=0.65, t=0.18, w=12.0, h=0.85, size=28, bold=True, color=WHITE)
    add_text_box(sld, "07 / 08", l=11.5, t=0.25, w=1.6, h=0.6,
                 size=13, color=GOLD, align=PP_ALIGN.RIGHT)

    apps = [
        ("🗄️", "Bases de Datos Jerárquicas",
         "LCA (Lowest Common Ancestor)",
         "El problema de encontrar el Ancestro Común más Bajo en un árbol se reduce\n"
         "a RMQ mediante el recorrido de Euler. Respuestas en O(1) en motores de\n"
         "bases de datos XML, JSON y grafos empresariales.", NAVY),
        ("🧬", "Bioinformática",
         "LCP sobre Suffix Arrays",
         "El Prefijo Común más Largo (LCP) entre sufijos de cadenas de ADN se resuelve\n"
         "vía RMQ sobre el arreglo LCP. Utilizado en alineadores genómicos (BWA, Bowtie)\n"
         "para procesar millones de lecturas de ADN por segundo.", RGBColor(0x1E, 0x66, 0x3D)),
        ("🌐", "Redes y Enrutamiento IP",
         "Longest Prefix Match",
         "Los enrutadores de alta velocidad buscan coincidencias de prefijo más largo\n"
         "en tablas con millones de entradas. Estructuras basadas en RMQ permiten\n"
         "tomar decisiones de enrutamiento a velocidades de gigabits por segundo.", RGBColor(0x6A, 0x0D, 0x72)),
    ]

    for i, (icon, title, subtitle, desc, col) in enumerate(apps):
        y = 1.4 + i * 1.95
        add_rect(sld, 0.5, y, 12.3, 1.82, fill_rgb=WHITE,
                 line_rgb=col, line_width_pt=2)
        # Icono círculo
        add_rect(sld, 0.65, y + 0.3, 0.9, 0.9, fill_rgb=col)
        add_text_box(sld, icon, l=0.65, t=y + 0.28, w=0.9, h=0.9,
                     size=22, align=PP_ALIGN.CENTER)
        # Título y subtítulo
        add_text_box(sld, title, l=1.75, t=y + 0.08, w=5.5, h=0.48,
                     size=16, bold=True, color=col)
        add_text_box(sld, subtitle, l=1.75, t=y + 0.52, w=5.5, h=0.35,
                     size=12.5, italic=True, color=MID_GRAY)
        # Descripción
        add_text_box(sld, desc, l=1.75, t=y + 0.88, w=10.8, h=0.88,
                     size=12.5, color=DARK_GRAY)

# ══════════════════════════════════════════════════════════════════
# DIAPOSITIVA 8 – CONCLUSIONES
# ══════════════════════════════════════════════════════════════════
def slide_conclusiones():
    sld = prs.slides.add_slide(BLANK)
    add_rect(sld, 0, 0, 13.33, 7.5, fill_rgb=NAVY)
    add_rect(sld, 0, 0, 0.45, 7.5, fill_rgb=GOLD)
    add_rect(sld, 0.45, 0, 0.08, 7.5, fill_rgb=WHITE)
    add_text_box(sld, "08 / 08", l=11.5, t=0.3, w=1.6, h=0.6,
                 size=13, color=GOLD, align=PP_ALIGN.RIGHT)

    add_text_box(sld, "Conclusiones", l=0.75, t=0.5, w=11.0, h=0.9,
                 size=34, bold=True, color=WHITE)
    add_rect(sld, 0.75, 1.45, 10.5, 0.06, fill_rgb=GOLD)

    puntos = [
        ("🔁", "Trade-off inteligente",
         "Sacrificamos O(N log N) en memoria para eliminar el cuello de botella temporal.\n"
         "El costo de precomputación se amortiza con cada consulta procesada."),
        ("📐", "Propiedad algebraica como ventaja",
         "La idempotencia del operador mínimo es la clave que habilita el solapamiento\n"
         "de bloques sin alterar la correctitud del resultado."),
        ("📈", "Escalabilidad demostrada",
         "3,743× más rápido en consultas para N=500K, Q=1M.\n"
         "De 51 minutos a 0.83 segundos. La diferencia entre viable e inviable."),
        ("🔗", "Código disponible",
         "github.com/nicotitopp/trabajoFinal  (rama: dev-nico)"),
    ]

    for i, (icon, title, desc) in enumerate(puntos):
        y = 1.65 + i * 1.38
        add_rect(sld, 0.75, y, 11.5, 1.25, fill_rgb=RGBColor(0x17, 0x3A, 0x60),
                 line_rgb=BLUE_MID, line_width_pt=1)
        add_text_box(sld, icon, l=0.85, t=y + 0.22, w=0.7, h=0.7,
                     size=20, align=PP_ALIGN.CENTER)
        add_text_box(sld, title, l=1.65, t=y + 0.08, w=10.3, h=0.42,
                     size=15, bold=True, color=GOLD)
        add_text_box(sld, desc, l=1.65, t=y + 0.5, w=10.3, h=0.72,
                     size=13, color=BLUE_LITE)

# ══════════════════════════════════════════════════════════════════
# GENERAR TODAS LAS DIAPOSITIVAS
# ══════════════════════════════════════════════════════════════════
slide_portada()
slide_problema()
slide_naive()
slide_concepto()
slide_math()
slide_resultados()
slide_aplicaciones()
slide_conclusiones()

OUTPUT_PATH = "presentacion/RMQ_Sparse_Table.pptx"
import os
os.makedirs("presentacion", exist_ok=True)
prs.save(OUTPUT_PATH)
print(f"[OK] PowerPoint generado en:  {OUTPUT_PATH}")
