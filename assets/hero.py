"""Generates the profile hero banner in light and dark variants.

Single source of truth for assets/hero-dark.svg and assets/hero-light.svg.
Run `python assets/hero.py` from the repo root after editing.
"""

from pathlib import Path

MONO = "ui-monospace,'SF Mono','Cascadia Mono',Menlo,Consolas,monospace"
SANS = "'Helvetica Neue',Helvetica,Arial,sans-serif"

# The pipeline reads left to right: the real shape of the work.
STAGES = [
    (110, "documents", "pdf / xlsx / docx"),
    (306, "ocr", "Document AI"),
    (502, "embed", "OpenAI"),
    (698, "retrieve", "Qdrant"),
    (894, "agents", "supervisor"),
    (1090, "stream", "SSE"),
]
GATE_X = 992  # human-in-the-loop approval, between agents and stream

LINE_Y = 96
X0, X1 = 60, 1140

THEMES = {
    "dark": {
        "ground": "#0B0F14",
        "rule": "#1E2A38",
        "muted": "#7D8FA3",
        "name": "#F2F6FA",
        "role": "#9FB3C8",
        "signal": "#00D4FF",
        "warn": "#FF7A5C",
        "glow": "0.85",
    },
    "light": {
        "ground": "#FFFFFF",
        "rule": "#D3DDE6",
        "muted": "#5A6B7D",
        "name": "#0B0F14",
        "role": "#41586D",
        "signal": "#0077A3",
        "warn": "#C2410C",
        "glow": "0.3",
    },
}

TEMPLATE = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 286" width="1200" height="286" role="img" aria-label="Mahmoud Abdulhamid, AI engineer. A pipeline: documents, OCR with Document AI, embeddings, retrieval with Qdrant, a supervisor agent, human approval, then a stream over SSE.">
<defs>
  <linearGradient id="trail" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="__SIGNAL__" stop-opacity="0"/>
    <stop offset="1" stop-color="__SIGNAL__" stop-opacity="0.55"/>
  </linearGradient>
  <radialGradient id="glow">
    <stop offset="0" stop-color="__SIGNAL__" stop-opacity="__GLOW__"/>
    <stop offset="1" stop-color="__SIGNAL__" stop-opacity="0"/>
  </radialGradient>
</defs>
<style>
  @keyframes flow {
    0%   { transform: translateX(0px);    opacity: 0 }
    10%  { opacity: 1 }
    88%  { opacity: 1 }
    100% { transform: translateX(__SPAN__px); opacity: 0 }
  }
  .pulse { animation: flow 4.4s cubic-bezier(.45,.05,.55,.95) infinite }
  @media (prefers-reduced-motion: reduce) { .pulse { animation: none; opacity: 0 } }
</style>

<rect width="1200" height="286" fill="__GROUND__"/>

<!-- the spine -->
<line x1="__X0__" y1="__LINE_Y__" x2="__X1__" y2="__LINE_Y__" stroke="__RULE__" stroke-width="2.5"/>
__STAGES__
__GATE__

<!-- one orchestrated moment: data moving through the system -->
<g class="pulse" transform="translate(__X0__ 0)">
  <rect x="-118" y="__PULSE_TOP__" width="118" height="2.5" fill="url(#trail)"/>
  <circle cx="0" cy="__LINE_Y__" r="17" fill="url(#glow)"/>
  <circle cx="0" cy="__LINE_Y__" r="4.5" fill="__SIGNAL__"/>
</g>

<text x="60" y="222" font-family="__SANS__" font-size="43" font-weight="700" letter-spacing="-1.3" fill="__NAME__">MAHMOUD ABDULHAMID</text>
<text x="62" y="252" font-family="__MONO__" font-size="16.5" fill="__ROLE__">AI engineer, production RAG and multi-agent systems</text>
<text x="1140" y="222" text-anchor="end" font-family="__MONO__" font-size="14" fill="__MUTED__">retries, dead letters, checkpoints</text>
<text x="1140" y="248" text-anchor="end" font-family="__MONO__" font-size="14" fill="__MUTED__">so one bad document never stops the queue</text>
</svg>
"""

STAGE_TPL = """<g>
  <line x1="__X__" y1="__TICK_TOP__" x2="__X__" y2="__TICK_BOT__" stroke="__RULE__" stroke-width="1.5"/>
  <circle cx="__X__" cy="__LINE_Y__" r="5" fill="__GROUND__" stroke="__SIGNAL__" stroke-width="2"/>
  <text x="__X__" y="62" text-anchor="middle" font-family="__MONO__" font-size="20" fill="__NAME__">__LABEL__</text>
  <text x="__X__" y="130" text-anchor="middle" font-family="__MONO__" font-size="14" fill="__MUTED__">__SUB__</text>
</g>"""

GATE_TPL = """<g>
  <path d="M __X__ __D_TOP__ L __D_R__ __LINE_Y__ L __X__ __D_BOT__ L __D_L__ __LINE_Y__ Z" fill="__GROUND__" stroke="__WARN__" stroke-width="2"/>
  <line x1="__X__" y1="__D_BOT__" x2="__X__" y2="146" stroke="__WARN__" stroke-width="1" stroke-opacity="0.5"/>
  <text x="__X__" y="162" text-anchor="middle" font-family="__MONO__" font-size="14" fill="__WARN__">you approve</text>
</g>"""


def fill(template, mapping):
    for key, value in mapping.items():
        template = template.replace(f"__{key}__", str(value))
    return template


def build(theme):
    base = dict(
        theme,
        MONO=MONO,
        SANS=SANS,
        LINE_Y=LINE_Y,
        X0=X0,
        X1=X1,
        GROUND=theme["ground"],
        RULE=theme["rule"],
        MUTED=theme["muted"],
        NAME=theme["name"],
        ROLE=theme["role"],
        SIGNAL=theme["signal"],
        WARN=theme["warn"],
        GLOW=theme["glow"],
    )

    stages = "\n".join(
        fill(STAGE_TPL, dict(base, X=x, LABEL=label, SUB=sub, TICK_TOP=LINE_Y - 13, TICK_BOT=LINE_Y + 13))
        for x, label, sub in STAGES
    )
    gate = fill(
        GATE_TPL,
        dict(base, X=GATE_X, D_TOP=LINE_Y - 11, D_BOT=LINE_Y + 11, D_L=GATE_X - 11, D_R=GATE_X + 11),
    )

    return fill(
        TEMPLATE,
        dict(base, STAGES=stages, GATE=gate, SPAN=X1 - X0, PULSE_TOP=LINE_Y - 1.5),
    )


if __name__ == "__main__":
    out = Path(__file__).parent
    for name, theme in THEMES.items():
        (out / f"hero-{name}.svg").write_text(build(theme), encoding="utf-8")
        print(f"wrote hero-{name}.svg")
