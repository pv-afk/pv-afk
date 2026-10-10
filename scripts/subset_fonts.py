"""Re-create the embedded WOFF2 subsets from Google Fonts sources (SIL OFL).

    python scripts/subset_fonts.py <dir with InterTight[wght].ttf, JetBrainsMono[wght].ttf, InstrumentSerif-Italic.ttf>
"""
import sys
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

SRC = Path(sys.argv[1])
OUT = Path(__file__).parent / "fonts"
CHARS = "".join(map(chr, range(0x20, 0x7F))) + "·—–×→↗←§°Δ≈±•…’“”≤≥₁₂"
JOBS = [("InterTight[wght].ttf", 300, "inter-300"), ("InterTight[wght].ttf", 500, "inter-500"),
        ("InterTight[wght].ttf", 600, "inter-600"), ("JetBrainsMono[wght].ttf", 400, "mono-400"),
        ("JetBrainsMono[wght].ttf", 600, "mono-600"), ("InstrumentSerif-Italic.ttf", None, "serif-it")]

for src, wght, name in JOBS:
    font = TTFont(SRC / src)
    if wght:
        font = instancer.instantiateVariableFont(font, {"wght": wght})
    opts = subset.Options()
    opts.flavor, opts.hinting, opts.name_IDs = "woff2", False, []
    opts.layout_features = ["kern", "liga", "calt", "tnum"]
    sub = subset.Subsetter(opts)
    sub.populate(text=CHARS)
    sub.subset(font)
    font.flavor = "woff2"
    font.save(OUT / f"{name}.woff2")
    print(name, (OUT / f"{name}.woff2").stat().st_size)
