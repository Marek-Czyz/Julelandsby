"""Generates the assembly instruction HTML and exports it to A4 PDF via headless Edge."""
import math, subprocess, pathlib
import texts

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = "../Assembly/"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SIZES = {
    "Hus_1": (1026, 978), "Hus_2": (1030, 936), "Hus_3": (1026, 1043), "Hus_4": (949, 1042),
    "Hus_5": (896, 1092), "Hus_6": (949, 1033), "Hus_7": (1054, 1106), "Hus_8": (1030, 1076),
    "Hus_komplett_off": (1070, 1129), "Hus_komplett_on": (1107, 1087),
    "Corner": (760, 1016), "Tak_1": (947, 619), "Tak_2": (990, 605), "Tak_3": (1017, 605), "Tak_lys": (974, 611),
}

ORANGE = "#F76707"
BLUE = "#1C7ED6"
RED = "#E03131"
INK = "#1F2A37"

# ---------------------------------------------------------------- SVG helpers

def arrow(x1, y1, x2, y2, w=12, color=ORANGE, curve=0):
    """Thick arrow with white halo. curve bends the shaft sideways (px)."""
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    hl, hw = w * 2.6, w * 2.1           # head length / half-width
    bx, by = x2 - ux * hl, y2 - uy * hl  # head base
    if curve:
        cx, cy = (x1 + bx) / 2 + nx * curve, (y1 + by) / 2 + ny * curve
        shaft = f"M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {bx + ux*2:.1f},{by + uy*2:.1f}"
    else:
        shaft = f"M{x1:.1f},{y1:.1f} L{bx + ux*2:.1f},{by + uy*2:.1f}"
    head = (f"{x2:.1f},{y2:.1f} {bx + nx*hw:.1f},{by + ny*hw:.1f} "
            f"{bx - nx*hw:.1f},{by - ny*hw:.1f}")
    halo = w * 0.55
    return (f'<path d="{shaft}" stroke="#fff" stroke-width="{w + 2*halo}" fill="none" stroke-linecap="round"/>'
            f'<polygon points="{head}" fill="#fff" stroke="#fff" stroke-width="{2*halo}" stroke-linejoin="round"/>'
            f'<path d="{shaft}" stroke="{color}" stroke-width="{w}" fill="none" stroke-linecap="round"/>'
            f'<polygon points="{head}" fill="{color}" stroke="{color}" stroke-width="{w*0.3}" stroke-linejoin="round"/>')


def glue_icon(x, y, s=1.0, crossed=False):
    """Glue drop marker centred at (x, y); s scales a ~60 px icon."""
    col = RED if crossed else BLUE
    g = (f'<g transform="translate({x},{y}) scale({s})">'
         f'<circle r="30" fill="#fff" stroke="{col}" stroke-width="5"/>'
         f'<path d="M0,-19 C9,-6 14,1 14,8 A14,14 0 0 1 -14,8 C-14,1 -9,-6 0,-19Z" fill="{col}"/>'
         f'<path d="M-6,6 A7,7 0 0 0 -1,14" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round"/>')
    if crossed:
        g += f'<line x1="-21" y1="-21" x2="21" y2="21" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>'
    return g + '</g>'


def leader(px, py, lx, ly, text, side="r", fs=30, dot=True, sub=""):
    """Callout: line from a point on the part to a shoulder, label sitting on the shoulder.
    If the line would climb through the label (point above, shoulder extending towards it),
    the label is placed under the shoulder instead."""
    pad = fs * 0.2
    tw = 0.53 * fs * max(len(text), len(sub) * 0.8) + pad
    sx2 = lx + tw if side == "r" else lx - tw
    tx = lx + pad if side == "r" else sx2
    toward = (px > lx) == (side == "r")
    below = py < ly and toward
    s = (f'<polyline points="{px},{py} {lx},{ly} {sx2},{ly}" fill="none" stroke="{INK}" stroke-width="{fs*0.09:.1f}"/>')
    if dot:
        s += f'<circle cx="{px}" cy="{py}" r="{fs*0.25:.1f}" fill="{ORANGE}" stroke="#fff" stroke-width="{fs*0.1:.1f}"/>'
    ty = ly + fs * 0.95 if below else ly - fs * 0.25
    s += (f'<text x="{tx}" y="{ty:.1f}" font-size="{fs}" font-weight="700" fill="{INK}" '
          f'font-family="Segoe UI, Arial">{text}</text>')
    if sub:
        sy = ty + fs * 0.95 if below else ly + fs * 0.95
        s += (f'<text x="{tx}" y="{sy:.1f}" font-size="{fs*0.78:.1f}" fill="#5B6573" '
              f'font-family="Segoe UI, Arial">{sub}</text>')
    return s


def badge(x, y, text, s=1.0):
    return (f'<g transform="translate({x},{y}) scale({s})"><rect x="-46" y="-22" width="92" height="44" rx="22" '
            f'fill="{ORANGE}"/><text y="10" text-anchor="middle" font-size="27" font-weight="700" fill="#fff" '
            f'font-family="Segoe UI, Arial">{text}</text></g>')


_FIG = 0


def fig(name, crop, overlay="", height=None, details=(), extra_defs=""):
    """Image as SVG cropped by viewBox; overlay is drawn in original pixel coords.
    details: list of (src_crop(x,y,w,h), dest(cx,cy,r), label) magnified circle insets."""
    global _FIG
    _FIG += 1
    W, H = SIZES[name]
    x, y, w, h = crop
    style = f'height:{height}' if height else 'width:100%'
    defs, det = extra_defs, ""
    for i, (sc, dc, label) in enumerate(details):
        sx, sy, sw, sh = sc
        cx, cy, r = dc
        cid = f"c{_FIG}_{i}"
        defs += f'<clipPath id="{cid}"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath>'
        # leader from source to inset
        det += (f'<circle cx="{sx + sw/2}" cy="{sy + sh/2}" r="{max(sw, sh)/2}" fill="none" '
                f'stroke="{INK}" stroke-width="3" stroke-dasharray="8 6"/>')
        scx, scy = sx + sw / 2, sy + sh / 2
        d = math.hypot(cx - scx, cy - scy)
        k1, k2 = max(sw, sh) / 2 / d, r / d
        det += (f'<line x1="{scx + (cx-scx)*k1}" y1="{scy + (cy-scy)*k1}" x2="{cx - (cx-scx)*k2}" '
                f'y2="{cy - (cy-scy)*k2}" stroke="{INK}" stroke-width="3" stroke-dasharray="8 6"/>')
        det += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#fff"/>'
        det += (f'<g clip-path="url(#{cid})"><svg x="{cx-r}" y="{cy-r}" width="{2*r}" height="{2*r}" '
                f'viewBox="{sx} {sy} {sw} {sh}" preserveAspectRatio="xMidYMid slice">'
                f'<image href="{IMG}{name}.png" width="{W}" height="{H}"/></svg></g>')
        det += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{INK}" stroke-width="5"/>'
        if label:
            det += (f'<rect x="{cx - 34}" y="{cy - r - 22}" width="68" height="44" rx="8" fill="{INK}"/>'
                    f'<text x="{cx}" y="{cy - r + 11}" text-anchor="middle" font-size="28" font-weight="700" '
                    f'fill="#fff" font-family="Segoe UI, Arial">{label}</text>')
    return (f'<svg class="fig" viewBox="{x} {y} {w} {h}" style="{style}" '
            f'preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">'
            f'<defs><clipPath id="k{_FIG}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>{defs}</defs>'
            f'<image href="{IMG}{name}.png" width="{W}" height="{H}" clip-path="url(#k{_FIG})"/>{overlay}{det}</svg>')

# ---------------------------------------------------------------- HTML helpers

ICON_GLUE = ('<svg viewBox="-32 -32 64 64" class="ico">' + glue_icon(0, 0) + '</svg>')
ICON_NOGLUE = ('<svg viewBox="-32 -32 64 64" class="ico">' + glue_icon(0, 0, crossed=True) + '</svg>')
ICON_ARROW = ('<svg viewBox="0 0 64 64" class="ico">' + arrow(8, 32, 58, 32, w=8) + '</svg>')
ICON_CHECK = ('<svg viewBox="-32 -32 64 64" class="ico"><circle r="30" fill="#2F9E44"/>'
              '<path d="M-14,1 L-4,11 L15,-10" stroke="#fff" stroke-width="7" fill="none" '
              'stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_DETAIL = ('<svg viewBox="-32 -32 64 64" class="ico"><circle r="27" fill="#fff" stroke="#1F2A37" '
               'stroke-width="5"/><circle r="11" fill="none" stroke="#1F2A37" stroke-width="4" '
               'stroke-dasharray="5 4"/></svg>')
ICON_INFO = ('<svg viewBox="-32 -32 64 64" class="ico"><circle r="30" fill="#1C7ED6"/>'
             '<rect x="-4" y="-4" width="8" height="20" rx="3" fill="#fff"/><circle cy="-14" r="5" fill="#fff"/></svg>')
ICON_WARN = ('<svg viewBox="-32 -32 64 64" class="ico"><path d="M0,-28 L29,24 L-29,24Z" fill="#E03131" '
             'stroke="#E03131" stroke-width="5" stroke-linejoin="round"/><rect x="-4" y="-12" width="8" height="21" '
             'rx="3" fill="#fff"/><circle cy="16" r="4.5" fill="#fff"/></svg>')

def progress(T, cur):
    items = ""
    for i, s in enumerate(T["steps"], 1):
        cls = "cur" if i == cur else ("done" if i < cur else "")
        items += f'<div class="pg {cls}"><span>{i}</span>{s}</div>'
    return f'<div class="progress">{items}</div>'


def step_header(T, n, title, sub, tag_html):
    return (f'<div class="sh"><div class="snum">{n}</div><div class="stitle"><div class="kicker">'
            f'{T["step_of"].format(n=n)}</div><h1>{title}</h1><p>{sub}</p></div><div class="stag">{tag_html}</div></div>'
            f'{progress(T, n)}')


def card(num, body_fig, text, cls=""):
    return (f'<div class="card {cls}"><div class="ctop"><span class="cnum">{num}</span>'
            f'<div class="ctext">{text}</div></div><div class="cfig">{body_fig}</div></div>')


FLOW_R = '<div class="flow r"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#FFF4E6"/><path d="M15,10 L26,20 L15,30" stroke="#F76707" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
FLOW_D = '<div class="flow d"><svg viewBox="0 0 40 40"><circle cx="20" cy="20" r="19" fill="#FFF4E6"/><path d="M10,15 L20,26 L30,15" stroke="#F76707" stroke-width="5" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg></div>'
ICON_LED = ('<svg viewBox="-32 -32 64 64" class="ico"><circle r="30" fill="#FAB005"/>'
            '<path d="M-9,8 A14,14 0 1 1 9,8 L6,16 L-6,16Z" fill="#fff"/><rect x="-6" y="18" width="12" height="5" rx="2" fill="#fff"/></svg>')


def build_pages(T):
    def footer(p):
        return f'<div class="foot"><span>{T["doc"]}</span><span>{p} / 7</span></div>'

    def page(content, p, cls=""):
        return f'<section class="page {cls}">{content}{footer(p) if p else ""}</section>'

    def note(kind, icon, html):
        return f'<div class="note {kind}">{icon}<div>{html}</div></div>'

    tag_glue = f'<div class="tag glue">{ICON_GLUE}<span>{T["glue"]}</span></div>'
    tag_noglue = f'<div class="tag noglue">{ICON_NOGLUE}<span>{T["noglue"]}</span></div>'
    pages = []

    # ---- Cover
    overview = ""
    thumbs = [("Hus_4", (80, 295, 730, 690)), ("Hus_6", (100, 170, 690, 800)), ("Tak_3", (60, 30, 870, 520)),
              ("Tak_lys", (115, 50, 680, 400)), ("Hus_8", (80, 185, 810, 830))]
    for i, (n, c) in enumerate(thumbs, 1):
        overview += (f'<div class="ov"><div class="ovimg">{fig(n, c)}</div>'
                     f'<div class="ovlab"><span>{i}</span>{T["steps"][i-1]}</div></div>')
        if i < 5:
            overview += '<div class="ovarr">&#8250;</div>'
    pages.append(page(f'''
<div class="cover">
  <div class="cv-top"><div class="brandbar"></div><div class="kicker">{T["cv_kicker"]}</div>
  <h1 class="cv-title">{T["cv_title"]}</h1>
  <p class="cv-sub">{T["cv_sub"]}</p></div>
  <div class="cv-hero">{fig("Hus_komplett_on", (60, 170, 860, 860))}</div>
  <div class="cv-meta">
     <div><b>5</b><span>{T["cv_steps"]}</span></div>
     <div><b>14</b><span>{T["cv_parts"]}</span></div>
     <div>{ICON_GLUE}<span>{T["cv_glue"]}</span></div>
  </div>
  <div class="cv-ov">{overview}</div>
</div>''', 0, "coverpage"))

    # ---- Parts & legend
    ov = (leader(640, 200, 1060, 92, T["lab_roof"], side="l", fs=36)
          + leader(175, 388, 0, 150, T["lab_eave"], fs=36)
          + leader(360, 930, 300, 1100, T["lab_gable"], side="l", fs=36)
          + leader(800, 780, 1062, 945, T["lab_long"], side="l", fs=36)
          + leader(573, 900, 690, 1100, T["lab_corner"], fs=36))
    thumbs = [fig("Hus_1", (170, 285, 380, 530)), fig("Hus_2", (538, 248, 284, 606)),
              fig("Hus_5", (185, 400, 340, 620)), fig("Corner", (262, 73, 206, 832)),
              fig("Tak_3", (60, 30, 870, 520)), fig("Tak_1", (235, 62, 400, 150)),
              fig("Tak_1", (125, 230, 365, 180)), fig("Tak_lys", (230, 50, 400, 160))]
    qty = [1, 1, 2, 4, 2, 1, 2, 1]
    rows = "".join(f'<tr><td class="pl"><span>{l}</span></td><td class="pimg">{f}</td><td>{d}</td>'
                   f'<td class="pq">{q}×</td></tr>' for l, d, q, f in zip("ABCDEFGH", T["parts"], qty, thumbs))
    need = "".join(f"<li>{x}</li>" for x in T["need"])
    icons = [ICON_ARROW, ICON_GLUE, ICON_NOGLUE, ICON_DETAIL, ICON_CHECK]
    legend = "".join(f"<div>{i}<span>{t}</span></div>" for i, t in zip(icons, T["sym"]))
    pages.append(page(f"""
<div class="ph"><div class="kicker">{T["p_kicker"]}</div><h1>{T["p_title"]}</h1>
<p class="lead">{T["p_lead"]}</p></div>
<div class="parts-grid">
  <div class="pbox ovbox"><h2>{T["p_ov"]}</h2><div class="ovfig">{fig("Hus_komplett_off", (0, 40, 1070, 1089), ov)}</div></div>
  <div class="pbox"><h2>{T["p_list"]}</h2><table class="parts">{rows}</table></div>
</div>
<div class="two">
  <div class="pbox"><h2>{T["need_t"]}</h2><ul class="need">{need}</ul></div>
  <div class="pbox"><h2>{T["sym_t"]}</h2><div class="legend">{legend}</div></div>
</div>
""", 2))

    # ---- Step 1
    s1b = (arrow(104, 380, 129, 505) + arrow(490, 180, 503, 300) + arrow(556, 450, 566, 588)
           + arrow(834, 215, 838, 340)
           + glue_icon(85, 700, 1.1) + glue_icon(585, 430, 1.1) + glue_icon(500, 850, 1.1) + glue_icon(900, 520, 1.1))
    s = step_header(T, 1, T["s1_t"], T["s1_s"], tag_glue)
    s += f"""
<div class="grid g-12">
  {card("1.1", fig("Hus_2", (120, 190, 720, 680)), T["s1_1"])}
  {FLOW_R}
  {card("1.2", fig("Hus_3", (40, 160, 900, 850), s1b), T["s1_2"])}
</div>
{FLOW_D}
<div class="grid g-wide">
  {card("1.3", fig("Hus_4", (60, 240, 840, 740), details=[((465, 545, 110, 110), (700, 335, 92), "A")]), T["s1_3"], "result")}
  <div class="side">{note("info", ICON_INFO, T["s1_n1"])}{note("ok", ICON_CHECK, T["s1_n2"])}</div>
</div>"""
    pages.append(page(s, 3))

    # ---- Step 2
    s2a = arrow(265, 255, 265, 392, w=14) + arrow(595, 95, 595, 225, w=14)
    s = step_header(T, 2, T["s2_t"], T["s2_s"], tag_noglue)
    s += f"""
<div class="stack">
  {card("2.1", fig("Hus_5", (60, 80, 780, 970), s2a), T["s2_1"], "h")}
  {FLOW_D}
  {card("2.2", fig("Hus_6", (90, 160, 720, 820), details=[((440, 555, 110, 110), (230, 300, 105), "B")]), T["s2_2"], "h result")}
</div>
<div class="note warn big">{ICON_WARN}<div>{T["s2_w"]}</div></div>"""
    pages.append(page(s, 4))

    # ---- Step 3
    t1 = (leader(430, 138, 560, 52, T["lab_ridge"], fs=34)
          + leader(200, 372, 230, 482, T["lab_eave2"], fs=34)
          + leader(720, 305, 740, 500, T["lab_eave2"], fs=30))
    t2 = (glue_icon(470, 98, 1.0) + glue_icon(560, 205, 1.0) + glue_icon(860, 330, 1.0)
          + leader(400, 152, 330, 78, T["lab_ridge"], side="l", fs=32)
          + leader(300, 348, 330, 462, T["lab_eave2"], fs=32)
          + leader(680, 352, 700, 465, T["lab_eave2"], fs=30, sub=T["lab_2nd"]))
    t3 = glue_icon(255, 100, 1.1) + glue_icon(300, 300, 1.0) + leader(600, 300, 720, 130, T["lab_roof"], fs=30)
    s = step_header(T, 3, T["s3_t"], T["s3_s"], tag_glue)
    s += f"""
<div class="grid g-11">
  {card("3.1", fig("Tak_1", (60, 0, 887, 540), t1), T["s3_1"])}
  {FLOW_R}
  {card("3.2", fig("Tak_2", (60, 20, 910, 490), t2), T["s3_2"])}
</div>
{FLOW_D}
<div class="grid g-wide">
  {card("3.3", fig("Tak_3", (40, 20, 900, 545), t3), T["s3_3"], "result")}
  <div class="side">{note("info", ICON_INFO, T["s3_n1"])}{note("ok", ICON_CHECK, T["s3_n2"])}</div>
</div>"""
    pages.append(page(s, 5))

    # ---- Step 4
    l1 = (arrow(570, 235, 476, 168, w=7)
          + leader(570, 235, 600, 205, T["lab_led"], fs=30, dot=False, sub=T["lab_led_sub"]))
    s = step_header(T, 4, T["s4_t"], T["s4_s"], f'<div class="tag led">{ICON_LED}<span>{T["light"]}</span></div>')
    s += f"""
<div class="stack">
  {card("4.1", fig("Tak_lys", (110, 30, 860, 420), l1), T["s4_1"], "h")}
  {FLOW_D}
  {card("4.2", fig("Tak_2", (60, 30, 760, 450), details=[((300, 150, 170, 80), (600, 330, 115), "C")]), T["s4_2"], "h result")}
</div>
<div class="two notes">{note("info", ICON_INFO, T["s4_n1"])}{note("ok", ICON_CHECK, T["s4_n2"])}</div>"""
    pages.append(page(s, 6))

    # ---- Step 5
    h7 = arrow(58, 485, 96, 650, w=18) + arrow(918, 322, 912, 500, w=18) + arrow(590, 560, 607, 680, w=15)
    s = step_header(T, 5, T["s5_t"], T["s5_s"], tag_noglue)
    s += f"""
<div class="stack">
  {card("5.1", fig("Hus_7", (30, 30, 1010, 1040), h7), T["s5_1"], "h")}
  {FLOW_D}
  {card("5.2", fig("Hus_komplett_on", (70, 180, 840, 850)), T["s5_2"], "h result")}
</div>
<div class="note ok big">{ICON_CHECK}<div>{T["s5_n"]}</div></div>"""
    pages.append(page(s, 7))
    return pages


# ---------------------------------------------------------------- CSS

CSS = f"""
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; font-family: 'Segoe UI', Arial, sans-serif; color: {INK}; }}
.page {{ width: 210mm; height: 297mm; padding: 14mm 14mm 16mm; position: relative; overflow: hidden;
        page-break-after: always; break-after: page; display: flex; flex-direction: column; }}
.page:last-child {{ page-break-after: auto; }}
b {{ font-weight: 700; }}
.kicker {{ text-transform: uppercase; letter-spacing: .14em; font-size: 8.5pt; font-weight: 700; color: {ORANGE}; }}
h1 {{ margin: 1mm 0 0; font-size: 21pt; line-height: 1.1; font-weight: 700; }}
h2 {{ margin: 0 0 3mm; font-size: 11pt; font-weight: 700; }}
.ico {{ width: 9mm; height: 9mm; flex: none; }}
svg.fig {{ display: block; }}

/* footer */
.foot {{ position: absolute; left: 14mm; right: 14mm; bottom: 7mm; display: flex; justify-content: space-between;
        font-size: 8pt; color: #8A94A3; border-top: 0.3mm solid #E3E7EC; padding-top: 2mm; }}

/* cover */
.coverpage {{ padding: 0; }}
.cover {{ height: 100%; display: flex; flex-direction: column; }}
.cv-top {{ padding: 18mm 16mm 0; }}
.brandbar {{ width: 22mm; height: 2.2mm; background: {ORANGE}; border-radius: 1mm; margin-bottom: 6mm; }}
.cv-title {{ font-size: 40pt; margin-top: 2mm; letter-spacing: -.01em; }}
.cv-sub {{ font-size: 13pt; color: #5B6573; margin: 2mm 0 0; }}
.cv-hero {{ flex: 1; min-height: 0; display: flex; align-items: center; justify-content: center; padding: 4mm 20mm;
           background: radial-gradient(ellipse at 50% 60%, #FFF4E6 0%, #fff 62%); }}
.cv-hero svg {{ width: auto !important; height: 128mm; }}
.cv-meta {{ display: flex; gap: 5mm; justify-content: center; margin: 0 16mm 6mm; }}
.cv-meta > div {{ display: flex; align-items: center; gap: 2.5mm; background: #F4F6F8; border-radius: 3mm; padding: 2.5mm 5mm; }}
.cv-meta b {{ font-size: 18pt; color: {ORANGE}; }}
.cv-meta span {{ font-size: 10pt; color: #44505F; }}
.cv-meta .ico {{ width: 8mm; height: 8mm; }}
.cv-ov {{ background: {INK}; padding: 6mm 10mm 9mm; display: flex; align-items: center; justify-content: space-between; }}
.ov {{ width: 30mm; text-align: center; }}
.ovimg {{ background: #fff; border-radius: 2.5mm; height: 26mm; padding: 2mm; display: flex; align-items: center; justify-content: center; }}
.ovimg svg {{ width: 100%; height: 100%; }}
.ovlab {{ color: #fff; font-size: 8.5pt; margin-top: 2.2mm; display: flex; align-items: center; justify-content: center; gap: 1.5mm; }}
.ovlab span {{ background: {ORANGE}; border-radius: 50%; width: 5mm; height: 5mm; display: inline-flex; align-items: center;
              justify-content: center; font-weight: 700; font-size: 8pt; }}
.ovarr {{ color: {ORANGE}; font-size: 22pt; margin-top: -6mm; }}

/* parts page */
.ph {{ margin-bottom: 5mm; }}
.lead {{ margin: 1.5mm 0 0; color: #5B6573; font-size: 10pt; }}
.ovbox {{ display: flex; flex-direction: column; }}
.ovfig {{ flex: 1; display: flex; align-items: center; }}
.parts-grid {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 5mm; }}
.two {{ display: grid; grid-template-columns: 0.8fr 1.2fr; gap: 5mm; margin-top: 5mm; }}
.pbox {{ border: 0.35mm solid #E3E7EC; border-radius: 3mm; padding: 4mm; }}
table.parts {{ width: 100%; border-collapse: collapse; font-size: 9pt; }}
table.parts td {{ border-bottom: 0.3mm solid #EEF1F4; padding: 1.2mm 1.5mm; vertical-align: middle; }}
table.parts tr:last-child td {{ border-bottom: 0; }}
td.pl {{ width: 8mm; }}
td.pl span {{ display: inline-flex; width: 6.5mm; height: 6.5mm; border-radius: 50%; background: {INK}; color: #fff;
             font-weight: 700; align-items: center; justify-content: center; font-size: 9pt; }}
td.pimg {{ width: 30mm; height: 19mm; }}
td.pimg svg {{ width: 28mm !important; height: 17mm; }}
td.pq {{ font-weight: 700; color: {ORANGE}; font-size: 11pt; text-align: right; }}
ul.need {{ margin: 0; padding-left: 5mm; font-size: 9.5pt; line-height: 1.75; }}
.legend {{ display: grid; grid-template-columns: 1fr; gap: 2mm; font-size: 9pt; }}
.legend > div {{ display: flex; align-items: center; gap: 3mm; }}
.legend .ico {{ width: 8mm; height: 8mm; }}

/* step header */
.sh {{ display: flex; align-items: center; gap: 5mm; }}
.snum {{ width: 19mm; height: 19mm; border-radius: 50%; background: {ORANGE}; color: #fff; font-size: 34pt; font-weight: 800;
        display: flex; align-items: center; justify-content: center; flex: none; }}
.stitle {{ flex: 1; }}
.stitle p {{ margin: 1.2mm 0 0; color: #5B6573; font-size: 10pt; }}
.tag {{ display: flex; flex-direction: column; align-items: center; gap: 1mm; font-size: 8pt; font-weight: 800; letter-spacing: .08em;
       border-radius: 3mm; padding: 2.5mm 3.5mm; }}
.tag .ico {{ width: 11mm; height: 11mm; }}
.tag.glue {{ background: #E7F5FF; color: {BLUE}; }}
.tag.noglue {{ background: #FFF5F5; color: {RED}; }}
.tag.led {{ background: #FFF9DB; color: #E67700; }}
.progress {{ display: flex; gap: 1.5mm; margin: 5mm 0 5mm; }}
.pg {{ flex: 1; font-size: 7.5pt; color: #8A94A3; background: #F4F6F8; border-radius: 1.5mm; padding: 1.4mm 2mm;
      display: flex; align-items: center; gap: 1.6mm; }}
.pg span {{ width: 4.2mm; height: 4.2mm; border-radius: 50%; background: #D5DBE2; color: #fff; font-weight: 700; font-size: 7pt;
           display: inline-flex; align-items: center; justify-content: center; }}
.pg.done {{ color: #2F9E44; background: #EBFBEE; }}
.pg.done span {{ background: #2F9E44; }}
.pg.cur {{ color: #fff; background: {INK}; font-weight: 700; }}
.pg.cur span {{ background: {ORANGE}; }}

/* cards */
.grid {{ display: grid; gap: 0; align-items: stretch; flex: 1 1 0; min-height: 0; }}
.grid > * {{ min-height: 0; }}
.g-12 {{ grid-template-columns: 0.82fr 9mm 1.18fr; }}
.g-11 {{ grid-template-columns: 1fr 9mm 1fr; }}
.g-wide {{ grid-template-columns: 1.5fr 0.62fr; gap: 5mm; }}
.g-wide4 {{ grid-template-columns: 1fr; }}
.card {{ border: 0.35mm solid #E3E7EC; border-radius: 3mm; padding: 3.5mm; display: flex; flex-direction: column; background: #fff; }}
.card.result {{ border-color: #B2F2BB; background: linear-gradient(#fff, #fff) padding-box; box-shadow: inset 0 0 0 0.35mm #D3F9D8; }}
.ctop {{ display: flex; gap: 3mm; align-items: flex-start; }}
.cnum {{ font-weight: 700; background: {INK}; color: #fff; border-radius: 1.8mm; padding: 0.8mm 2.2mm; font-size: 10pt; flex: none; }}
.card.result .cnum {{ font-weight: 700; background: #2F9E44; }}
.ctext {{ font-size: 9.5pt; line-height: 1.42; }}
.cfig {{ flex: 1; display: flex; align-items: center; justify-content: center; margin-top: 2mm; min-height: 0; }}
.cfig svg {{ width: 100%; height: 100%; }}
.stack {{ display: flex; flex-direction: column; flex: 1 1 0; min-height: 0; }}
.stack > .card {{ flex: 1 1 0; min-height: 0; }}
.card.h {{ flex-direction: row; gap: 4mm; }}
.card.h .ctop {{ width: 58mm; flex: none; }}
.card.h .cfig {{ margin-top: 0; }}
.two.notes {{ grid-template-columns: 1fr 1fr; }}
.flow {{ display: flex; align-items: center; justify-content: center; }}
.flow svg {{ width: 8mm; height: 8mm; }}
.flow.d {{ height: 9mm; }}
.side {{ display: flex; flex-direction: column; gap: 4mm; }}
.note {{ display: flex; gap: 3mm; border-radius: 3mm; padding: 3.5mm; font-size: 9pt; line-height: 1.42; }}
.note .ico {{ width: 8mm; height: 8mm; }}
.note.info {{ background: #E7F5FF; }}
.note.ok {{ background: #EBFBEE; }}
.note.warn {{ background: #FFF5F5; border: 0.4mm solid #FFC9C9; }}
.note.big {{ margin-top: 5mm; font-size: 10pt; align-items: center; }}
.note.big .ico {{ width: 11mm; height: 11mm; }}
"""

for T in (texts.EN, texts.NO):
    _FIG = 0
    body = "".join(build_pages(T))
    html = (f'<!DOCTYPE html><html lang="{T["lang"]}"><head><meta charset="utf-8"><title>{T["doc"]}</title>'
            f'<style>{CSS}</style></head><body>{body}</body></html>')
    html_path = ROOT / "_work" / f'{T["file"]}.html'
    pdf_path = ROOT / f'{T["file"]}.pdf'
    html_path.write_text(html, encoding="utf-8")
    subprocess.run([EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer", "--no-margins",
                    f"--print-to-pdf={pdf_path}", html_path.as_uri()], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("written", pdf_path)
