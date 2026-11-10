"""Generate docs/hero.svg: the animated "Magma Glow" landing-page hero.

The hero is an animated take on docs/logo.png (made by docs/logo.py): the
same six bar heights, translucent bars and haloed letters on a magma
gradient. Animation is CSS-only, so it still plays when great-docs loads the
SVG as an image. The wordmark uses Fjalla One, embedded as a subset holding
only the glyphs in "Skimpy" (docs/fjalla-one-skimpy.woff2, SIL Open Font
License), because SVGs loaded as images cannot fetch web fonts.

Run with: uv run python docs/hero.py
"""

import base64
from pathlib import Path

HERE = Path(__file__).parent
BAR_HEIGHTS = [0.85, 0.9, 0.85, 0.85, 0.8, 0.9]  # same as docs/logo.py
LETTERS = ["S", "k", "i", "m", "p", "y"]
WIDTH, HEIGHT = 640, 370
BAR_WIDTH, BAR_SCALE = 76, 205
LETTER_SIZE, LETTER_GAP = 84, 34
# magma colormap stops, top of the sky to bottom
SKY = [
    ("0", "#fdb37c"),
    ("0.26", "#f8765c"),
    ("0.48", "#d2456f"),
    ("0.68", "#8c2981"),
    ("0.84", "#451077"),
    ("1", "#1b0c41"),
]
# halo layers around each letter, outermost first: (stroke width, colour, opacity)
HALO = [
    (44, "#f8765c", 0.55),
    (30, "#fdc58a", 0.8),
    (18, "#fde9ad", 1),
    (8, "#fff8dc", 1),
]
LETTER_COLOUR = "#6b5496"


def build_svg() -> str:
    """Return the hero SVG as a string."""
    font = base64.b64encode((HERE / "fjalla-one-skimpy.woff2").read_bytes()).decode()
    gap = (WIDTH - len(LETTERS) * BAR_WIDTH) / (len(LETTERS) + 1)
    stops = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in SKY)

    bars, letters, rules = [], [], []
    for i, (letter, h) in enumerate(zip(LETTERS, BAR_HEIGHTS)):
        x = gap + i * (BAR_WIDTH + gap)
        top = HEIGHT - h * BAR_SCALE
        baseline = top - LETTER_GAP
        cx = x + BAR_WIDTH / 2
        bars.append(
            f'<path class="bar b{i}" d="M{x:.1f} {HEIGHT + 4} V{top:.1f} H{x + BAR_WIDTH:.1f} V{HEIGHT + 4}"/>'
        )
        halo = "".join(
            f'<text x="{cx:.1f}" y="{baseline:.1f}" stroke="{c}" stroke-width="{w}" '
            f'stroke-opacity="{o}" fill="{c}">{letter}</text>'
            for w, c, o in HALO
        )
        letters.append(
            f'<g class="lt l{i}"><g class="halo">{halo}</g>'
            f'<text x="{cx:.1f}" y="{baseline:.1f}" fill="{LETTER_COLOUR}">{letter}</text></g>'
        )
        rules.append(
            f".b{i}{{animation-delay:{i * 0.08:.2f}s}}"
            f".l{i}{{animation-delay:{0.55 + i * 0.09:.2f}s}}"
            f".l{i} .halo{{animation-delay:{2 + i * 0.3:.2f}s}}"
        )

    style = f"""
@font-face{{font-family:"Fjalla One Hero";src:url(data:font/woff2;base64,{font}) format("woff2")}}
text{{font-family:"Fjalla One Hero","Fjalla One",Impact,sans-serif;font-size:{LETTER_SIZE}px;text-anchor:middle;stroke-linejoin:round;paint-order:stroke}}
.bar{{fill:#ffffff;fill-opacity:.55;stroke:#3b2b30;stroke-opacity:.75;stroke-width:4;transform-box:fill-box;transform-origin:50% 100%;animation:grow .95s cubic-bezier(.2,.8,.2,1) both}}
.lt{{animation:drop .75s cubic-bezier(.2,.9,.3,1.25) both}}
.halo{{animation:glow 5s ease-in-out infinite}}
@keyframes grow{{from{{transform:scaleY(.03)}}}}
@keyframes drop{{from{{transform:translateY(-80px);opacity:0}}}}
@keyframes glow{{50%{{opacity:.7}}}}
{"".join(rules)}
@media (prefers-reduced-motion:reduce){{.bar,.lt,.halo{{animation:none}}}}
"""
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" '
        f'width="{WIDTH}" height="{HEIGHT}" role="img" aria-labelledby="t">'
        f'<title id="t">skimpy</title><style>{style}</style>'
        f'<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">{stops}</linearGradient></defs>'
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#sky)"/>'
        f"{''.join(bars)}{''.join(letters)}</svg>\n"
    )


if __name__ == "__main__":
    (HERE / "hero.svg").write_text(build_svg())
    print(f"Wrote {HERE / 'hero.svg'}")
