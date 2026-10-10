"""Build every SVG in ../assets for both GitHub themes.

    python scripts/build_assets.py

Real numbers come only from data/metrics.json (each entry cites its source
notebook in pv-afk/pv_afk). Decorative signals are synthetic and labelled so.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

from svgkit import THEMES, eeg_points, font_css, polyline_path, svg, text, text_width, trace_path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
M = json.loads((ROOT / "data" / "metrics.json").read_text())
W = 1200

REDUCED = "@media (prefers-reduced-motion: reduce){.anim{animation:none!important}.sweep{display:none}}"


def frame(c, h, rx=0):
    return f'<rect width="{W}" height="{h}" rx="{rx}" fill="{c["bg"]}"/>'


# ============================================================================ hero
def hero(c):
    H = 500
    b = [frame(c, H)]
    # 12-column hairline grid (Swiss structure, barely visible)
    for k in range(1, 12):
        x = 48 + k * (1104 / 12)
        b.append(f'<line x1="{x:.1f}" y1="72" x2="{x:.1f}" y2="440" stroke="{c["grid"]}"/>')
    b.append(f'<line x1="48" y1="72" x2="1152" y2="72" stroke="{c["line"]}"/>')
    b.append(f'<line x1="48" y1="440" x2="1152" y2="440" stroke="{c["line"]}"/>')
    b.append(text(48, 50, "PV—AFK", "mono-600", 14, c["ink"], ls=3))
    b.append(text(140, 50, "/  MACHINE LEARNING RESEARCH ENGINEER", "mono-400", 14, c["muted"], ls=3))
    b.append(text(1152, 50, "SIGNAL OVER NOISE", "mono-400", 14, c["accent"], "end", ls=3))

    # monumental name
    b.append(text(40, 214, "Pavel", "inter-600", 134, c["ink"], ls=-6))
    b.append(text(40, 340, "Chirkin", "inter-600", 134, c["ink"], ls=-6))
    sx = 40 + text_width("Chirkin", "inter-600", 134, -6) + 10
    b.append(f'<rect x="{sx:.1f}" y="318" width="22" height="22" fill="{c["accent"]}"/>')
    # role line: sans + serif-italic ampersand
    b.append(f'<text x="48" y="398" font-size="32" fill="{c["ink"]}">'
             f'<tspan class="inter-300" letter-spacing="-0.6">Machine Learning </tspan>'
             f'<tspan class="serif-it" font-size="38" fill="{c["accent"]}">&amp;</tspan>'
             f'<tspan class="inter-300" letter-spacing="-0.6"> AI Research</tspan></text>')

    # synthetic stereo-EEG panel (decorative)
    x0, x1, top = 676, 1152, 112
    labels = ["A1–A2", "A2–A3", "B4–B5", "B5–B6", "C2–C3", "C3–C4", "D7–D8"]
    for i, lab in enumerate(labels):
        y = top + 18 + i * 42
        burst = (0.58, 0.03) if i == 3 else None
        col = c["accent2"] if i == 3 else c["trace"]
        w = 1.6 if i == 3 else 1.1
        b.append(text(x0 - 14, y + 4, lab, "mono-400", 11, c["faint"], "end"))
        b.append(f'<path d="{trace_path(x0, x1, y, 30, eeg_points(380, 21 + i, 0.95, burst))}" '
                 f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linejoin="round"/>')
    bx = x0 + (x1 - x0) * 0.58
    b.append(f'<rect x="{bx-26:.1f}" y="{top+122}" width="52" height="44" fill="none" stroke="{c["accent2"]}" stroke-dasharray="2 3"/>')
    b.append(text(bx, top + 114, "HFO-LIKE", "mono-400", 10, c["accent2"], "middle", ls=1.5))
    # time axis
    b.append(f'<line x1="{x0}" y1="420" x2="{x1}" y2="420" stroke="{c["faint"]}"/>')
    for k in range(5):
        tx = x0 + (x1 - x0) * k / 4
        b.append(f'<line x1="{tx:.1f}" y1="420" x2="{tx:.1f}" y2="426" stroke="{c["faint"]}"/>')
        b.append(text(tx, 434 - 20, f"{k*0.5:.1f}s", "mono-400", 10, c["faint"], "middle"))
    # sweep cursor (the single animation); static frame = cursor at panel start
    b.append(f'<defs><linearGradient id="trail" x1="0" x2="1"><stop offset="0" stop-color="{c["accent"]}" stop-opacity="0"/>'
             f'<stop offset="1" stop-color="{c["accent"]}" stop-opacity=".16"/></linearGradient></defs>')
    b.append(f'<g class="sweep anim"><rect x="-90" y="{top}" width="90" height="300" fill="url(#trail)"/>'
             f'<line x1="0" y1="{top}" x2="0" y2="{top+300}" stroke="{c["accent"]}" stroke-width="1.5"/>'
             f'<circle cx="0" cy="{top}" r="3" fill="{c["accent"]}"/></g>')

    cols = [("01", "CREDIT RISK MODELING"), ("02", "COMPUTATIONAL NEUROSCIENCE"), ("03", "APPLIED ML · RETRIEVAL")]
    for k, (n, s) in enumerate(cols):
        x = (48, 290, 588)[k]
        b.append(text(x, 472, n, "mono-600", 12, c["accent"], ls=1))
        b.append(text(x + 28, 472, s, "mono-400", 12, c["muted"], ls=1.2))
    b.append(text(1152, 472, "fig. 0 — synthetic signal · decorative", "mono-400", 12, c["faint"], "end"))

    css = (font_css("inter-600", "inter-300", "serif-it", "mono-400", "mono-600") +
           f"\n.sweep{{animation:sweep 9s cubic-bezier(.45,.05,.55,.95) infinite;transform:translateX({x0}px)}}"
           f"\n@keyframes sweep{{0%{{transform:translateX({x0}px)}}100%{{transform:translateX({x1}px)}}}}\n" + REDUCED)
    return svg(W, H, "\n".join(b), css, "Pavel Chirkin — Machine Learning & AI Research",
               "Name and role, with a decorative synthetic stereo-EEG panel.")


# ============================================================================ section divider
def divider(c, num, title, note):
    H = 110
    b = []  # transparent: blends into any GitHub theme background
    b.append(text(48, 70, num, "mono-600", 18, c["accent"], ls=1))
    b.append(text(100, 74, title, "inter-600", 46, c["ink"], ls=-1.6))
    b.append(f'<line x1="48" y1="100" x2="1152" y2="100" stroke="{c["line"]}"/>')
    b.append(f'<line x1="48" y1="100" x2="96" y2="100" stroke="{c["accent"]}" stroke-width="2"/>')
    b.append(text(1152, 70, note, "mono-400", 14, c["muted"], "end", ls=2))
    return svg(W, H, "\n".join(b), font_css("inter-600", "mono-400", "mono-600"), f"{num} {title}", note)


# ============================================================================ project cards
def card_shell(c, idx, domain, title, subtitle, stack, metric, metric_label, delta, chart):
    H = 330
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="2"/>']
    b.append(text(48, 64, idx, "mono-600", 15, c["accent"], ls=1.5))
    b.append(text(100, 64, domain, "mono-400", 15, c["muted"], ls=2))
    b.append(text(46, 140, title, "inter-600", 54, c["ink"], ls=-2))
    for k, line in enumerate(subtitle):
        b.append(text(48, 184 + k * 32, line, "inter-300", 24, c["muted"], ls=-0.2))
    b.append(text(48, 290, stack, "mono-400", 15, c["faint"], ls=0.5))
    b.append(text(1152, 140, metric, "inter-600", 92, c["ink"], "end", ls=-4))
    b.append(text(1152, 172, metric_label, "mono-400", 14, c["muted"], "end", ls=1.5))
    if delta:
        b.append(text(1152, 198, delta, "mono-600", 14, c["accent"], "end", ls=1))
    b.append(chart)
    b.append(text(1152, 296, "source ↗", "mono-400", 14, c["accent"], "end", ls=1))
    return H, "\n".join(b)


def chart_axes(c, x0, y0, x1, y1):
    return (f'<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="{c["faint"]}"/>')


def card_credit(c):
    d = M["credit_scoring"]
    lr, xg = d["per_class_f1"]["logreg"], d["per_class_f1"]["xgboost"]
    x0, y1, hmax = 640, 270, 150
    g = [chart_axes(c, x0 - 10, 0, 900, y1)]
    for k, (a, v) in enumerate(zip(lr, xg)):
        X = x0 + k * 66
        g.append(f'<rect x="{X}" y="{y1-a*hmax:.1f}" width="22" height="{a*hmax:.1f}" fill="{c["trace"]}"/>')
        g.append(f'<rect x="{X+25}" y="{y1-v*hmax:.1f}" width="22" height="{v*hmax:.1f}" fill="{c["accent"]}"/>')
        g.append(text(X + 23, y1 + 20, f"cls {k}", "mono-400", 11, c["faint"], "middle"))
    g.append(f'<rect x="{x0}" y="92" width="10" height="10" fill="{c["trace"]}"/>')
    g.append(text(x0 + 16, 101, "LogReg", "mono-400", 12, c["muted"]))
    g.append(f'<rect x="{x0+86}" y="92" width="10" height="10" fill="{c["accent"]}"/>')
    g.append(text(x0 + 102, 101, "XGBoost", "mono-400", 12, c["muted"]))
    g.append(text(x0 - 10, 76, "F1 PER CLASS · TEST n=10,268", "mono-400", 11, c["faint"], ls=1))
    H, body = card_shell(c, "P/01", "CREDIT RISK · MULTICLASS", "Credit Scoring",
                         ["4-class approval outcome from credit", "history · 51,336 applicants"],
                         "scikit-learn · imbalanced-learn · XGBoost",
                         f'{d["macro_f1"]["xgboost"]:.2f}', "MACRO-F1 · XGBOOST",
                         f'+{d["macro_f1"]["xgboost"]-d["macro_f1"]["logreg"]:.2f} VS LOGREG', "\n".join(g))
    return svg(W, H, body, font_css("inter-600", "inter-300", "mono-400", "mono-600"),
               "Credit Scoring — macro-F1 0.71",
               "Per-class F1 of Logistic Regression vs XGBoost on the held-out test split.")


def card_leads(c):
    d = M["lead_prioritization"]
    lo, hi = 0.70, 0.77
    x0, x1, ytop, ybot = 640, 790, 110, 250
    Y = lambda v: ybot - (v - lo) / (hi - lo) * (ybot - ytop)
    g = [text(x0 - 30, 76, "DAILY AP · 2 TEMPORAL HOLDOUTS", "mono-400", 11, c["faint"], ls=1)]
    g.append(f'<line x1="{x0}" y1="{ytop-6}" x2="{x0}" y2="{ybot+6}" stroke="{c["faint"]}"/>')
    g.append(f'<line x1="{x1}" y1="{ytop-6}" x2="{x1}" y2="{ybot+6}" stroke="{c["faint"]}"/>')
    g.append(text(x0, ybot + 22, "baseline", "mono-400", 11, c["faint"], "middle"))
    g.append(text(x1, ybot + 22, "v2 blend", "mono-400", 11, c["faint"], "middle"))
    for k, (a, v, w) in enumerate(zip(d["baseline"], d["v2"], d["windows"])):
        col = c["accent"] if k == 1 else c["trace"]
        g.append(f'<line x1="{x0}" y1="{Y(a):.1f}" x2="{x1}" y2="{Y(v):.1f}" stroke="{col}" stroke-width="2.5"/>')
        for X, val in ((x0, a), (x1, v)):
            g.append(f'<circle cx="{X}" cy="{Y(val):.1f}" r="5" fill="{c["surface"]}" stroke="{col}" stroke-width="2.5"/>')
        g.append(text(x0 - 12, Y(a) + 4, f"{a:.3f}", "mono-400", 11, c["muted"], "end"))
        g.append(text(x1 + 12, Y(v) + 4, f"{v:.3f}", "mono-400", 11, c["muted"]))
        g.append(f'<line x1="{x0+(0 if k == 0 else 110)}" y1="291" x2="{x0+(20 if k == 0 else 130)}" y2="291" stroke="{col}" stroke-width="2.5"/>')
        g.append(text(x0 + (26 if k == 0 else 136), 295, w, "mono-400", 11, c["muted"]))
    H, body = card_shell(c, "P/02", "RANKING · AVITO DS BOOTCAMP", "Lead Prioritization",
                         ["Rank leads by P(target action ≤ 5 days),", "leakage-safe temporal features"],
                         "LightGBM · CatBoost · pandas",
                         f'{d["v2"][1]:.3f}', "DAILY AP · LOCAL HOLDOUT",
                         f'+{d["v2"][1]-d["baseline"][1]:.3f} VS BASELINE', "\n".join(g))
    return svg(W, H, body, font_css("inter-600", "inter-300", "mono-400", "mono-600"),
               "Lead Prioritization — Daily AP 0.760",
               "Baseline vs final blend on two sequential local temporal holdouts.")


def card_matching(c):
    d = M["product_matching"]
    ns, f1 = d["ngram_n"], d["best_f1"]
    x0, x1, ytop, ybot, lo, hi = 640, 880, 110, 260, 0.35, 0.75
    X = lambda i: x0 + (x1 - x0) * i / (len(ns) - 1)
    Y = lambda v: ybot - (v - lo) / (hi - lo) * (ybot - ytop)
    g = [text(x0 - 10, 76, "BEST F1 BY CHAR N-GRAM SIZE", "mono-400", 11, c["faint"], ls=1), chart_axes(c, x0 - 10, 0, x1 + 10, ybot)]
    g.append(f'<path d="{polyline_path([X(i) for i in range(len(ns))], [Y(v) for v in f1])}" fill="none" stroke="{c["accent"]}" stroke-width="2.5"/>')
    for i, (n, v) in enumerate(zip(ns, f1)):
        last = i == len(ns) - 1
        g.append(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="{6 if last else 4}" fill="{c["accent"] if last else c["surface"]}" stroke="{c["accent"]}" stroke-width="2"/>')
        g.append(text(X(i), ybot + 20, f"n={n}", "mono-400", 11, c["faint"], "middle"))
        g.append(text(X(i), Y(v) - 12, f"{v:.2f}", "mono-400", 11, c["muted"], "middle"))
    b = d["best"]
    H, body = card_shell(c, "P/03", "ENTITY MATCHING · NLP", "Product Matching",
                         ["Match the same drug across 3 messy", f"price lists ({sum(d['items'])} items)"],
                         "pandas · regex · Jaccard · seaborn",
                         f'{b["f1"]:.2f}', f'F1 · n={b["n"]}, JACCARD ≥ {b["threshold"]:.2f}',
                         f'P {b["precision"]:.2f} · R {b["recall"]:.2f}', "\n".join(g))
    return svg(W, H, body, font_css("inter-600", "inter-300", "mono-400", "mono-600"),
               "Product Matching — F1 0.69",
               "Best F1 of character n-gram Jaccard matching for n = 1..5.")


def card_salary(c):
    d = M["salary_forecast"]
    s = [math.log10(v) for v in d["series"]]
    n, h = len(s), d["horizon_months"]
    x0, x1, ytop, ybot = 640, 880, 110, 260
    xf = x0 + (x1 - x0) * n / (n + h)
    lo, hi = min(s), max(s)
    xs = [x0 + (xf - x0) * i / (n - 1) for i in range(n)]
    ys = [ybot - (v - lo) / (hi - lo) * (ybot - ytop) for v in s]
    g = [text(x0 - 10, 76, "AVG. SALARY 1993–2026 · LOG SCALE", "mono-400", 11, c["faint"], ls=1), chart_axes(c, x0 - 10, 0, x1 + 10, ybot)]
    g.append(f'<rect x="{xf:.1f}" y="{ytop-10}" width="{x1-xf:.1f}" height="{ybot-ytop+10}" fill="{c["accent"]}" fill-opacity=".08"/>')
    g.append(f'<line x1="{xf:.1f}" y1="{ytop-10}" x2="{xf:.1f}" y2="{ybot}" stroke="{c["accent"]}" stroke-dasharray="3 3"/>')
    g.append(f'<path d="{polyline_path(xs, ys)}" fill="none" stroke="{c["ink"]}" stroke-width="1.6" stroke-linejoin="round"/>')
    g.append(text(x0, ybot + 20, "1993", "mono-400", 11, c["faint"], "middle"))
    g.append(text(xf, ybot + 20, "2026", "mono-400", 11, c["faint"], "middle"))
    g.append(text((xf + x1) / 2, ybot - 10, "+36", "mono-400", 11, c["accent"], "middle"))
    H, body = card_shell(c, "P/04", "TIME SERIES · FORECASTING", "Salary Forecast",
                         ["399 monthly observations, Box-Cox,", "seasonal differencing, 36-month horizon"],
                         "statsmodels · pmdarima · SciPy",
                         "36 mo", "FORECAST HORIZON",
                         "SARIMAX(6,1,2)(0,1,0)₁₂", "\n".join(g))
    return svg(W, H, body, font_css("inter-600", "inter-300", "mono-400", "mono-600"),
               "Salary Forecast — SARIMAX, 36-month horizon",
               "Real monthly average salary series on a log scale; shaded area marks the forecast horizon.")


# ============================================================================ research pipeline
def research(c):
    H = 360
    b = [f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{c["surface"]}" stroke="{c["line"]}" stroke-width="2"/>']
    b.append(text(48, 64, "R/01", "mono-600", 15, c["accent2"], ls=1.5))
    b.append(text(100, 64, "STEREO-EEG · EPILEPTOGENIC ZONE LOCALIZATION", "mono-400", 15, c["muted"], ls=2))
    b.append(text(46, 128, "From raw sEEG to per-channel predictions", "inter-600", 44, c["ink"], ls=-1.6))
    steps = [("EDF", "multichannel"), ("MONTAGE", "bipolar"), ("WINDOWS", "filter · QC"),
             ("FEATURES", "DFA · HFO"), ("MODEL", "PyTorch"), ("OUTPUT", "per channel")]
    bw, gap, y = 160, 28.8, 176
    for k, (t, s) in enumerate(steps):
        x = 48 + k * (bw + gap)
        hl = k == 3
        b.append(f'<rect x="{x:.1f}" y="{y}" width="{bw}" height="96" rx="8" fill="{c["bg"]}" '
                 f'stroke="{c["accent2"] if hl else c["line"]}" stroke-width="{2 if hl else 1.5}"/>')
        b.append(text(x + 16, y + 34, f"{k+1:02d}", "mono-400", 12, c["faint"]))
        b.append(text(x + 16, y + 60, t, "mono-600", 17, c["ink"], ls=1))
        b.append(text(x + 16, y + 82, s, "mono-400", 13, c["muted"]))
        if k < len(steps) - 1:
            ax = x + bw
            b.append(f'<line x1="{ax+4:.1f}" y1="{y+48}" x2="{ax+gap-6:.1f}" y2="{y+48}" stroke="{c["faint"]}" stroke-width="1.5"/>')
            b.append(f'<path d="M{ax+gap-10:.1f},{y+44} L{ax+gap-5:.1f},{y+48} L{ax+gap-10:.1f},{y+52}" fill="none" stroke="{c["faint"]}" stroke-width="1.5"/>')
    b.append(text(48, 318, "AI Lab, Plekhanov University × Pirogov National Medical & Surgical Center", "inter-300", 20, c["muted"]))
    b.append(text(1152, 318, "pipeline only · clinical data and code are private", "mono-400", 13, c["faint"], "end"))
    return svg(W, H, "\n".join(b), font_css("inter-600", "inter-300", "mono-400", "mono-600"),
               "sEEG research pipeline",
               "EDF → bipolar montage → windows and QC → DFA/HFO features → PyTorch model → per-channel output.")


# ============================================================================ footer
def footer(c):
    H = 150
    b = []
    vals = eeg_points(300, 99, 0.55)
    xs = [48 + 1104 * i / 299 for i in range(300)]
    # signal decays into a flat line: "signal over noise"
    ys = [80 - v * 26 * max(0.0, 1 - i / 190) for i, v in enumerate(vals)]
    b.append(f'<path d="{polyline_path(xs, ys)}" fill="none" stroke="{c["trace"]}" stroke-width="1.3"/>')
    b.append(f'<circle cx="1152" cy="80" r="5" fill="{c["accent"]}"/>')
    b.append(text(48, 134, "PV—AFK · 2026", "mono-400", 13, c["faint"], ls=2))
    b.append(text(1152, 134, "signal over noise", "serif-it", 22, c["muted"], "end"))
    return svg(W, H, "\n".join(b), font_css("mono-400", "serif-it"), "Signal over noise", "Decorative footer.")


# ============================================================================ main
SECTIONS = [("01", "Focus", "INDUSTRY × RESEARCH"), ("02", "Selected Work", "VERIFIED METRICS"),
            ("03", "Toolkit", "WHAT I USE"), ("04", "Background", "EDUCATION · CONTACT")]


def main():
    ASSETS.mkdir(exist_ok=True)
    for theme, c in THEMES.items():
        files = {
            "hero": hero(c), "research": research(c), "footer": footer(c),
            "card-credit-scoring": card_credit(c), "card-lead-prioritization": card_leads(c),
            "card-product-matching": card_matching(c), "card-salary-forecast": card_salary(c),
        }
        for num, title, note in SECTIONS:
            files[f"section-{num}"] = divider(c, num, title, note)
        for name, content in files.items():
            (ASSETS / f"{name}-{theme}.svg").write_text(content, encoding="utf-8")
    print(f"built {len(list(ASSETS.glob('*.svg')))} SVGs → {ASSETS}")


if __name__ == "__main__":
    main()
