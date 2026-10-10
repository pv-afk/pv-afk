"""Small toolkit for building GitHub-safe SVGs.

GitHub renders README images through <img>, so SVGs must be fully
self-contained: no scripts, no external fonts, no remote resources.
Fonts are embedded as base64 WOFF2 subsets (SIL OFL, see fonts/).
"""
from __future__ import annotations

import base64
import math
import random
from functools import lru_cache
from pathlib import Path
from xml.sax.saxutils import escape

FONT_DIR = Path(__file__).parent / "fonts"

# family name -> (file, weight, style)
FONTS = {
    "inter-300": ("inter-300.woff2", 300, "normal"),
    "inter-500": ("inter-500.woff2", 500, "normal"),
    "inter-600": ("inter-600.woff2", 600, "normal"),
    "mono-400": ("mono-400.woff2", 400, "normal"),
    "mono-600": ("mono-600.woff2", 600, "normal"),
    "serif-it": ("serif-it.woff2", 400, "italic"),
}
FALLBACK = {
    "inter": "'Inter Tight','Inter',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif",
    "mono": "'JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace",
    "serif": "'Instrument Serif',Georgia,'Times New Roman',serif",
}

# ---------------------------------------------------------------- design tokens
THEMES = {
    "dark": {
        "bg": "#0A0E16", "surface": "#0F1520", "line": "#1C2433", "grid": "#141B27",
        "ink": "#E9EEF6", "muted": "#8A94A6", "faint": "#4A5466",
        "accent": "#5CE1E6", "accent2": "#8B7CF6", "trace": "#3A4A63",
    },
    "light": {
        "bg": "#F6F7F9", "surface": "#FFFFFF", "line": "#DDE2EA", "grid": "#E9ECF1",
        "ink": "#0D1320", "muted": "#5A6476", "faint": "#9AA3B2",
        "accent": "#0A8EA0", "accent2": "#5B48D9", "trace": "#AEB8C8",
    },
}


@lru_cache(maxsize=None)
def _b64(file: str) -> str:
    return base64.b64encode((FONT_DIR / file).read_bytes()).decode()


def font_css(*keys: str) -> str:
    """@font-face rules + utility classes for the requested font keys."""
    rules = []
    for key in keys:
        file, weight, style = FONTS[key]
        rules.append(
            f"@font-face{{font-family:'{key}';font-weight:{weight};font-style:{style};"
            f"src:url(data:font/woff2;base64,{_b64(file)}) format('woff2');}}"
        )
        family = FALLBACK[key.split("-")[0]]
        rules.append(f".{key}{{font-family:'{key}',{family};font-weight:{weight};font-style:{style};}}")
    return "\n".join(rules)


def text(x, y, s, cls, size, fill, anchor="start", ls=None, extra=""):
    spacing = f' letter-spacing="{ls}"' if ls is not None else ""
    return (f'<text x="{x:g}" y="{y:g}" class="{cls}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{spacing}{extra}>{escape(s)}</text>')


def svg(width, height, body, css="", title="", desc=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-labelledby="t d">\n'
        f"<title id=\"t\">{escape(title)}</title><desc id=\"d\">{escape(desc)}</desc>\n"
        f"<style>\n{css}\n</style>\n{body}\n</svg>\n"
    )


# ---------------------------------------------------------------- synthetic signal
def eeg_points(n, seed, amp=1.0, burst=None):
    """Deterministic, *synthetic* sEEG-like trace in [-1, 1] (decorative only).

    Mix of alpha/theta-band sines and smoothed noise; optional high-frequency
    burst (center, width) to evoke an HFO-like event.
    """
    rnd = random.Random(seed)
    phases = [rnd.uniform(0, 2 * math.pi) for _ in range(5)]
    freqs = [rnd.uniform(1.2, 2.2), rnd.uniform(3.5, 5.0), rnd.uniform(7.5, 10.5),
             rnd.uniform(13, 17), rnd.uniform(0.3, 0.6)]
    weights = [0.42, 0.28, 0.18, 0.08, 0.35]
    noise, out = 0.0, []
    for i in range(n):
        t = i / n
        v = sum(w * math.sin(2 * math.pi * f * t * 4 + p) for w, f, p in zip(weights, freqs, phases))
        noise = 0.75 * noise + 0.25 * rnd.gauss(0, 0.55)
        v += noise
        if burst:
            c, w = burst
            env = math.exp(-((t - c) / w) ** 2)
            v += env * 1.25 * math.sin(2 * math.pi * 90 * t + phases[0])
        out.append(max(-1.6, min(1.6, v * amp)) / 1.6)
    return out


def polyline_path(xs, ys):
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))


def trace_path(x0, x1, y_mid, height, values):
    n = len(values)
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    ys = [y_mid - v * height / 2 for v in values]
    return polyline_path(xs, ys)


@lru_cache(maxsize=None)
def _metrics(key: str):
    from fontTools.ttLib import TTFont
    font = TTFont(FONT_DIR / FONTS[key][0])
    return font.getBestCmap(), font["hmtx"].metrics, font["head"].unitsPerEm


def text_width(s: str, key: str, size: float, ls: float = 0.0) -> float:
    """Advance width of `s` in px (no kerning) — used to place marks after words."""
    cmap, hmtx, upm = _metrics(key)
    adv = sum(hmtx[cmap[ord(ch)]][0] for ch in s if ord(ch) in cmap)
    return adv * size / upm + ls * len(s)
