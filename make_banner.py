"""Builds banner.svg: animated ASCII axolotl beside a neofetch-style info block."""
from html import escape

HEAD = [
    "   .--------.   ",
    "  /          \\  ",
    " /            \\ ",
    "|   o      o   |",
    "|  *  \\__/  *  |",
    " \\            / ",
    "  '-.______.-'  ",
    "   /|      |\\   ",
    "  (_|      |_)  ",
]
# Left gills per frame; the right side is the mirror image.
GILLS_A = ["  \\\\\\\\  ", "   \\\\\\\\ ", "==\\\\\\\\  ", " ====   ", "==////  ", "   //// ", "  ////  ", "", ""]
GILLS_B = ["   \\\\\\\\ ", "  \\\\\\\\  ", "=-\\\\\\\\  ", "-=-=    ", "=-////  ", "  ////  ", "   //// ", "", ""]
GILL_W = 8


def mirror(s):
    return s[::-1].translate(str.maketrans("\\/", "/\\"))


def gill_rows(left):
    rows = []
    for g in left:
        g = g.ljust(GILL_W)
        rows.append(g + " " * len(HEAD[0]) + mirror(g))
    return rows


def body_rows(keep):
    """Full-width rows with only the head characters `keep` accepts; the rest become spaces."""
    pad = " " * GILL_W
    return [pad + "".join(c if keep(r, c) else " " for c in row) + pad for r, row in enumerate(HEAD)]


FONT = "Menlo, Consolas, 'DejaVu Sans Mono', 'Courier New', monospace"
LINE_H = 19
ART_X, ART_Y = 34, 92


def text_layer(rows, color, cls="", recolor=None):
    out = [f'<g class="{cls}" fill="{color}">'] if cls else [f'<g fill="{color}">']
    for i, row in enumerate(rows):
        if not row.strip():
            continue
        body = escape(row)
        if recolor:
            for ch, col in recolor.items():
                body = body.replace(escape(ch), f'<tspan fill="{col}">{escape(ch)}</tspan>')
        out.append(f'<text x="{ART_X}" y="{ART_Y + i * LINE_H}">{body}</text>')
    out.append("</g>")
    return "\n".join(out)


body = body_rows(lambda r, c: not (r == 3 and c == "o"))
eyes_open = body_rows(lambda r, c: r == 3 and c == "o")
eyes_shut = [row.replace("o", "-") for row in eyes_open]

INFO = [
    ("role", "game programmer"),
    ("school", "Cornell CS + Game Design '28"),
    ("now", "The Veil Sur @ DGA Studios"),
    ("prev", "Beastwoe Games (Nexus Rush)"),
    ("stack", "Unity, C#, TypeScript, React, Python"),
    ("likes", "axolotls, Smash Ultimate, volleyball"),
]
INFO_X, INFO_Y = 385, 84

info = [
    f'<text x="{INFO_X}" y="{INFO_Y}"><tspan fill="#ff7eb6" font-weight="bold">jared</tspan>'
    f'<tspan fill="#8b949e">@</tspan><tspan fill="#79c0ff" font-weight="bold">cornell</tspan></text>',
    f'<text x="{INFO_X}" y="{INFO_Y + 20}" fill="#30363d">{"-" * 13}</text>',
]
for i, (key, value) in enumerate(INFO):
    y = INFO_Y + 46 + i * 23
    info.append(
        f'<text x="{INFO_X}" y="{y}"><tspan fill="#ff7eb6" font-weight="bold">{key}</tspan>'
        f'<tspan fill="#8b949e">:</tspan>'
        f'<tspan x="{INFO_X + 72}" fill="#c9d1d9">{escape(value)}</tspan></text>'
    )
swatches = ["#484f58", "#ff7b72", "#7ee787", "#e3b341", "#79c0ff", "#ff7eb6", "#a5d6ff", "#f0f6fc"]
sw_y = INFO_Y + 46 + len(INFO) * 23 - 4
for i, col in enumerate(swatches):
    info.append(f'<rect x="{INFO_X + i * 26}" y="{sw_y}" width="22" height="12" rx="2" fill="{col}"/>')

bubbles = []
for i, (x, size, delay) in enumerate([(342, 13, 0), (356, 9, 1.4), (336, 11, 2.8)]):
    bubbles.append(
        f'<text class="bubble" x="{x}" y="240" font-size="{size}" fill="#79c0ff" '
        f'style="animation-delay:{delay}s">o</text>'
    )

W, H = 840, 330
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Jared Rojas: game programmer, Cornell CS and Game Design 2028. An animated ASCII axolotl waves its gills beside a terminal-style info card.">
<title>Jared Rojas</title>
<style>
  text {{ font-family: {FONT}; font-size: 15px; white-space: pre; }}
  .gillA {{ animation: gillA 1.6s steps(1) infinite; }}
  .gillB {{ animation: gillB 1.6s steps(1) infinite; }}
  .eyesOpen {{ animation: blinkOpen 5s steps(1) infinite; }}
  .eyesShut {{ animation: blinkShut 5s steps(1) infinite; }}
  .bubble {{ opacity: 0; animation: rise 4.2s linear infinite; }}
  .cursor {{ animation: cursor 1.1s steps(1) infinite; }}
  @keyframes gillA {{ 0% {{ opacity: 1 }} 50% {{ opacity: 0 }} }}
  @keyframes gillB {{ 0% {{ opacity: 0 }} 50% {{ opacity: 1 }} }}
  @keyframes blinkOpen {{ 0% {{ opacity: 1 }} 94% {{ opacity: 0 }} 97% {{ opacity: 1 }} }}
  @keyframes blinkShut {{ 0% {{ opacity: 0 }} 94% {{ opacity: 1 }} 97% {{ opacity: 0 }} }}
  @keyframes rise {{
    0% {{ opacity: 0; transform: translateY(0) }}
    15% {{ opacity: .9 }}
    100% {{ opacity: 0; transform: translateY(-150px) }}
  }}
  @keyframes cursor {{ 0% {{ opacity: 1 }} 50% {{ opacity: 0 }} }}
  @media (prefers-reduced-motion: reduce) {{
    .gillA, .gillB, .eyesOpen, .eyesShut, .bubble, .cursor {{ animation: none; }}
    .gillB, .eyesShut, .bubble {{ opacity: 0; }}
  }}
</style>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="#0d1117" stroke="#30363d" stroke-width="2"/>
<circle cx="24" cy="22" r="6" fill="#ff5f57"/><circle cx="44" cy="22" r="6" fill="#febc2e"/><circle cx="64" cy="22" r="6" fill="#28c840"/>
<text x="{W // 2}" y="27" fill="#8b949e" font-size="13" text-anchor="middle">jared@cornell: ~</text>
<line x1="1" y1="42" x2="{W - 1}" y2="42" stroke="#30363d" stroke-width="1"/>
{text_layer(gill_rows(GILLS_A), "#ff5fa2", "gillA")}
{text_layer(gill_rows(GILLS_B), "#ff5fa2", "gillB")}
{text_layer(body, "#ffb3d1", recolor={"*": "#ff7b72"})}
{text_layer(eyes_open, "#f0f6fc", "eyesOpen")}
{text_layer(eyes_shut, "#f0f6fc", "eyesShut")}
{chr(10).join(bubbles)}
{chr(10).join(info)}
<text x="34" y="{H - 24}"><tspan fill="#7ee787">jared@cornell</tspan><tspan fill="#8b949e">:~$ </tspan><tspan class="cursor" fill="#c9d1d9">_</tspan></text>
</svg>
'''

with open("banner.svg", "w") as f:
    f.write(svg)
