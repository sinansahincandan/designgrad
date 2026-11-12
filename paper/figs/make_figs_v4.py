"""Figures for the runs of the paper's ladder (v4: L0-L3, every level builds its code).   python paper/figs/make_figs_v4.py [name ...]
Reads runs/v4_s0, runs/v4_s1000, runs/v4_s2000 and runs/v4_all/v4_summary.json (eval/v4_analyze.py). Outputs v4_*.png / .svg.
  example figures (one row per level): part before -> what the critic read and said -> the change in the design document -> part after.
Quotes are copied from the recorded runs (critic: r{parent}/loss.md; design document: d.md of the two rounds); only math markup is
simplified (plain())."""
import json, re, sys, textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_figs import ROOT, OUT, REN, INK, INK2, MUTED, GRID, GOOD, MID, BAD, PROB, save, _ensure_render, _badge, _tile

sys.path.insert(0, str(ROOT / "eval"))
from mechanics import hidden_rows

NLV = ["L0", "L1", "L2", "L3"]
NC = {"L0": "#9a9a95", "L1": "#6250d6", "L2": "#1baf7a", "L3": "#eb6834"}
NAMES = {"L0": "no feedback", "L1": "+ critic", "L2": "+ own analysis", "L3": "+ render review"}
SEEDS = ["s0", "s1000", "s2000"]
import os
TAG = os.environ.get("DG_RUNS", "v6")       # run family: runs/<TAG>_s0, runs/<TAG>_s1000, runs/<TAG>_s2000, runs/<TAG>_all
ANG = {"P01_shelf_bracket": dict(azim=-50, elev=25), "P03_enclosure_base": dict(azim=-55, elev=38), "P07_nema17_mount": dict(azim=-50, elev=28),
       "P08_wall_hook": dict(azim=-50, elev=25), "P04_test_tube_rack": dict(azim=-55, elev=35)}
QUOTE = "#1f3b73"


def plain(t):
    """Readable text from the model's markdown/LaTeX-flavoured writing (content unchanged)."""
    for a, b in [(r"\text{", "{"), (r"\in", "in"), (r"\varnothing", "dia."), (r"\approx", "~"), (r"\le", "<="), (r"\ge", ">="), (r"\times", "x"),
                 (r"\pm", "+-"), (r"\rightarrow", "->"), (r"\%", "%"), ("**", ""), ("`", "")]:
        t = t.replace(a, b)
    t = re.sub(r"\{([^{}]*)\}", r"\1", t).replace("$", "")
    return re.sub(r"\s+", " ", t).strip()


def met(pd, rd):
    return sum(v is True for v in hidden_rows(pd, rd).values())


def _cardbox(ax, title, color):
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.add_patch(FancyBboxPatch((0.01, 0.02), 0.98, 0.96, boxstyle="round,pad=0,rounding_size=0.04", transform=ax.transAxes, fc="white", ec=color, lw=1.2))
    ax.text(0.045, 0.9, title, fontsize=8.2, weight="demibold", color=color, va="center", transform=ax.transAxes)


def _write(ax, items, y=0.78, width=50, fs=6.9, lh=0.087, gap=0.03, x=0.045):
    for txt, col, style, fam in items:
        for ln in textwrap.wrap(txt, width):
            ax.text(x, y, ln, fontsize=fs, color=col, va="center", transform=ax.transAxes, style=style, **({"family": fam} if fam else {}))
            y -= lh
        y -= gap
    return y


def inspect(run, problem, level):
    """Print what is available for an example row: per round the verdicts, the critic's lines and the changed design-document lines."""
    import difflib
    rd = ROOT / run / level / problem; pd = ROOT / "problems" / problem
    S = json.loads((rd / "summary.json").read_text())
    for t in S["trace"]:
        r = rd / f"r{t['k']:02d}"
        print(f"\n===== {level} r{t['k']} from {t.get('from', '-')} {'KEPT' if t['accepted'] else 'rejected'} met {met(pd, r)}/7 score {t['score']:.2f}")
        if t["k"] == 0:
            continue
        p = rd / f"r{t['from']:02d}"
        print("--- critic on the parent:"); print("\n".join(plain(l)[:260] for l in (p / "loss.md").read_text().splitlines() if l.strip())[:2600])
        a = (p / "d.md").read_text().splitlines(); b = (r / "d.md").read_text().splitlines()
        print("--- design document change:")
        for l in difflib.unified_diff(a, b, lineterm="", n=0):
            if l[:1] in "+-" and not l.startswith(("+++", "---")):
                print(l[0], plain(l[1:])[:240])


def example(run, problem, rows, name, title=None):
    """rows: dicts(level, k, reads=[str], critic=[str], diff=[(sign, str)], views=bool). One row per level."""
    pd = ROOT / "problems" / problem
    n = len(rows)
    fig = plt.figure(figsize=(8.6, 1.9 * n + (0.25 if title else 0.05)))
    top = 1 - (0.25 / fig.get_figheight() if title else 0.01)
    if title:
        fig.text(0.012, 1 - 0.13 / fig.get_figheight(), title, fontsize=9.4, weight="demibold", color=INK, va="center")
    h = (top - 0.01) / n
    for i, row in enumerate(rows):
        lv, k = row["level"], row["k"]; rd = ROOT / run / lv / problem
        S = json.loads((rd / "summary.json").read_text()); t = {x["k"]: x for x in S["trace"]}[k]; par = t["from"]
        gs = fig.add_gridspec(1, 4, left=0.012, right=0.988, top=top - i * h - 0.012, bottom=top - (i + 1) * h + 0.012,
                              width_ratios=[0.6, 1.5, 1.5, 0.6], wspace=0.035)
        tag = f"{problem[:3]}_{Path(run).name}_{lv}"
        a = fig.add_subplot(gs[0]); _tile(a, _ensure_render(rd / f"r{par:02d}/part.stl", REN / f"v4ex_{tag}_r{par}.png", **ANG[problem]), None, 7, "before")
        a.set_box_aspect(None)
        c = fig.add_subplot(gs[1]); _cardbox(c, f"{lv}  the critic reads {row['head']}", NC[lv])
        items = [(x, INK, "normal", None) for x in row.get("reads", [])] + [("“" + x + "”", QUOTE, "normal", None) for x in row["critic"]]
        if row.get("views"):
            _write(c, items, width=37)
            ia = c.inset_axes([0.66, 0.06, 0.32, 0.7]); ia.imshow(plt.imread(rd / f"r{par:02d}/views.png")); ia.set_xticks([]); ia.set_yticks([])
            for s in ia.spines.values():
                s.set_color("#d0d3da")
        else:
            _write(c, items, width=52)
        d = fig.add_subplot(gs[2]); _cardbox(d, "The design document is rewritten", INK)
        y = 0.78
        for sign, txt in row["diff"]:
            col = {"-": BAD, "+": GOOD}[sign]
            for j, ln in enumerate(textwrap.wrap(txt, 50)):
                d.text(0.045, y, ("− " if sign == "-" else "+ ") if j == 0 else "   ", fontsize=6.9, color=col, va="center", transform=d.transAxes, weight="bold")
                d.text(0.085, y, ln, fontsize=6.9, color=col, va="center", transform=d.transAxes)
                y -= 0.087
            y -= 0.03
        b = fig.add_subplot(gs[3]); _tile(b, _ensure_render(rd / f"r{k:02d}/part.stl", REN / f"v4ex_{tag}_r{k}.png", **ANG[problem]), None, 7, "after")
        b.set_box_aspect(None)
    save(fig, name, svg=False)


# ---------------------------------------------------------------- data of the three seeds
def units(runs=tuple(f"runs/{TAG}_{x}" for x in SEEDS)):
    """{(level, problem, seed): dict(dir, kept, met per round, accepted per round)}"""
    U = {}
    for run in runs:
        seed = "s" + re.search(r"s(\d+)$", run).group(1)
        for lv in NLV:
            for rd in sorted((ROOT / run / lv).glob("P*")):
                if not (rd / "summary.json").exists():
                    continue
                pd = ROOT / "problems" / rd.name; S = json.loads((rd / "summary.json").read_text())
                tr = {t["k"]: t for t in S["trace"]}
                U[(lv, rd.name, seed)] = {"dir": rd, "kept": S["k"], "met": {k: met(pd, rd / f"r{k:02d}") for k in tr}, "trace": tr}
    return U


def summary():
    return json.loads((ROOT / f"runs/{TAG}_all/v4_summary.json").read_text())


# ---------------------------------------------------------------- results
def fig_results():
    U = units(); Sm = summary()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1, 1.35], "wspace": 0.26})
    rng = np.random.default_rng(3)
    for i, l in enumerate(NLV):
        x = np.array([u["met"][u["kept"]] for (lv, _, _), u in U.items() if lv == l]); m = x.mean()
        a1.bar(i, m, 0.62, color=NC[l], zorder=2, alpha=0.92)
        a1.scatter(i + rng.uniform(-0.19, 0.19, len(x)), x + rng.uniform(-0.08, 0.08, len(x)), s=16, color="white", edgecolor=INK, lw=0.9, zorder=4)
        a1.text(i, 7.5, f"{m:.1f}", ha="center", va="center", fontsize=10, color=NC[l] if l != "L0" else INK2, weight="demibold", zorder=4)
        a1.text(i, -1.35, f"{int((x == 7).sum())} of {len(x)}", ha="center", fontsize=8, color=INK2)
    a1.text(-0.6, -1.35, "all 7 met:", ha="right", fontsize=8, color=INK2)
    a1.set_xticks(range(4)); a1.set_xticklabels(NLV, fontsize=10)
    a1.set_ylim(0, 7.9); a1.set_yticks(range(0, 8)); a1.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    a1.set_title("Requirements met, final design", pad=10)
    l0 = Sm["levels"]["L0"]["met"]
    a2.axhline(l0, color=MUTED, ls=(0, (4, 3)), lw=1.2, zorder=1)
    ends = {l: Sm["levels"][l]["curve_kept"] for l in NLV[1:]}
    for l, cur in ends.items():
        a2.plot(range(len(cur)), cur, color=NC[l], lw=2.4, marker="o", ms=5, mec="white", mew=1.2, zorder=3)
    ys = sorted([(cur[-1], l) for l, cur in ends.items()] + [(l0, "L0")])
    lab = []
    for v, l in ys:                      # keep the labels at least 0.42 apart
        y = v if not lab else max(v, lab[-1][0] + 0.42)
        lab.append((y, l))
    for y, l in lab:
        a2.text(4.18, y, f"{l}  {NAMES[l]}", va="center", fontsize=8.5, color=NC[l] if l != "L0" else INK2, weight="demibold")
    a2.set_xlim(-0.2, 4.1); a2.set_ylim(0, 7.9); a2.set_yticks(range(0, 8)); a2.set_xticks(range(5))
    a2.set_xlabel("design round", fontsize=9); a2.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    a2.set_title("Requirements met by the design held after each round", pad=10)
    save(fig, "v4_fig_results")


# ---------------------------------------------------------------- gallery
def _reference_stl(p):
    stl = REN / f"ref_{p}.stl"
    if not stl.exists():
        import cadquery as cq
        ns = {}
        exec((ROOT / "problems" / p / "reference.py").read_text(), ns)
        cq.exporters.export(ns["result"], str(stl))
    return stl


def fig_gallery(seed="s0"):
    U = units()
    fig, axs = plt.subplots(3, 5, figsize=(8.2, 5.25), gridspec_kw={"wspace": 0.06, "hspace": 0.1})
    for i, p in enumerate(PROB):
        ax = axs[i, 0]
        _tile(ax, _ensure_render(_reference_stl(p), REN / f"ref_{p}.png", color=(0.62, 0.66, 0.72), **ANG[p]), 7, 7)
        ax.text(-0.06, 0.5, PROB[p].replace("NEMA 17 m", "M"), ha="right", va="center", rotation=90, fontsize=9.5, color=INK, weight="demibold", transform=ax.transAxes)
        if i == 0:
            ax.set_title("Reference\n", fontsize=11, color=INK, loc="center", weight="demibold", pad=2)
            ax.text(0.5, 1.04, "a correct design", ha="center", va="bottom", fontsize=8.5, color=INK2, transform=ax.transAxes)
        for j, l in enumerate(NLV, start=1):
            us = [U[(l, p, s)] for s in SEEDS]; u = U[(l, p, seed)]
            stl = u["dir"] / f"r{u['kept']:02d}/part.stl"
            img = _ensure_render(stl, REN / f"{TAG}_{p}_{l}_{seed}.png", **ANG[p]) if stl.exists() else None
            _tile(axs[i, j], img, u["met"][u["kept"]], 7, note="runs: " + "  ".join(str(x["met"][x["kept"]]) for x in us))
            if i == 0:
                axs[i, j].set_title(f"{l}\n", fontsize=11, color=NC[l], loc="center", weight="demibold", pad=2)
                axs[i, j].text(0.5, 1.04, NAMES[l], ha="center", va="bottom", fontsize=8.5, color=INK2, transform=axs[i, j].transAxes)
    save(fig, "v4_fig_gallery", svg=False)


# ---------------------------------------------------------------- the loop
def fig_loop(run=f"runs/{TAG}_s0", problem="P07_nema17_mount", summ=f"runs/{TAG}_all/v4_summary.json"):
    """Specification -> designer -> design -> built part; the levels' evidence -> critic -> textual gradient -> designer."""
    from matplotlib.patches import Circle
    from make_figs_v3 import _panel, _pill, _line, _tint, LINE
    Sm = json.loads((ROOT / summ).read_text()); metv = {l: Sm["levels"][l]["met"] for l in NLV}
    r2 = ROOT / run / "L2" / problem / "r00"; r3 = ROOT / run / "L3" / problem / "r00"
    sim = (json.loads((r2 / "sim.json").read_text()).get("result") or {}) if (r2 / "sim.json").exists() else {}
    verdict = [(sim.get(f"R{k}") or {}).get("status") == "pass" for k in range(1, 8)]
    fig = plt.figure(figsize=(8.6, 4.55)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 200); ax.set_ylim(0, 105.8); ax.axis("off")
    head = dict(ha="center", va="center", fontsize=8.8, weight="demibold", color=INK)
    sub = dict(ha="center", va="center", fontsize=6.3, color=INK2)
    T, H = 76, 23; yc = T + H / 2
    X = {"spec": (8, 32), "designer": (56, 32), "des": (104, 32)}
    for k, (x, w) in X.items():
        _panel(ax, x, T, w, H, ec=INK if k == "designer" else "#c5c9d2", lw=1.3 if k == "designer" else 0.9)
    px0, pw = 156, 24
    for a, b in [((40, yc), (56, yc)), ((88, yc), (104, yc)), ((136, yc), (px0 + 1.5, yc))]:
        _line(ax, [a, b], color=LINE, lw=1.2)
    ax.text(146.5, yc + 3.4, "CAD agent", **{**sub, "color": INK, "fontsize": 6.6}); ax.text(146.5, yc - 3.4, "builds the part", **sub)
    x, w = X["spec"]; ax.text(x + w / 2, T + H - 4.4, "Specification", **head)
    for k in range(7):
        ax.add_patch(Rectangle((x + 6.5, T + H - 9.2 - k * 1.95), [16, 19, 13, 17, 15, 19, 12][k], 0.75, fc="#b9bdc7", ec="none", zorder=3))
    x, w = X["designer"]; ax.text(x + w / 2, T + H - 4.4, "Designer", **head)
    ax.text(x + w / 2, T + 10.2, "writes the design,", **{**sub, "fontsize": 6.9, "color": INK}); ax.text(x + w / 2, T + 6.6, "then rewrites it", **{**sub, "fontsize": 6.9, "color": INK})
    x, w = X["des"]; ax.text(x + w / 2, T + H - 4.4, "Design", **head)
    for k, t in enumerate(["document  d", "code  c"]):
        ax.add_patch(FancyBboxPatch((x + 5.5, T + 9.2 - 6 * k), w - 11, 4.7, boxstyle="round,pad=0,rounding_size=1", fc="#f1f2f5", ec="none", zorder=3))
        ax.text(x + w / 2, T + 11.55 - 6 * k, t, ha="center", va="center", fontsize=6.8, color=INK)
    img = _ensure_render(r2 / "part.stl", REN / f"v4loop_{problem[:3]}.png", **ANG[problem])
    ax.imshow(plt.imread(img), extent=(px0 + 2.5, px0 + pw - 2.5, T + 3.6, T + H - 0.6), zorder=3, aspect="auto")
    ax.text(px0 + pw / 2, T + 1.6, "the built part", **sub)
    B, HB, W = 41, 24.5, 36
    C = {"L0": 8, "L1": 56, "L2": 104, "L3": 152}
    title = {"L0": "no feedback", "L1": "+ design document", "L2": "+ its own analysis", "L3": "+ rendered views"}
    kind = {"L0": "", "L1": "conceptual", "L2": "numerical", "L3": "visual"}
    for l, x in C.items():
        _panel(ax, x, B, W, HB, ec=NC[l], fc=_tint(NC[l], 0.07), lw=1.1)
        _pill(ax, x + 4.8, B + HB - 4.3, l, NC[l], fs=6.8)
        ax.text(x + 9.6, B + HB - 4.3, title[l], fontsize=7.6, weight="demibold", color=NC[l] if l != "L0" else INK2, va="center")
        ax.add_patch(Rectangle((x + 4.5, B + 3.1), W - 15, 1.5, fc="white", ec="none", zorder=3))
        ax.add_patch(Rectangle((x + 4.5, B + 3.1), (W - 15) * metv[l] / 7, 1.5, fc=NC[l], ec="none", zorder=4))
        ax.text(x + W - 4.5, B + 3.85, f"{metv[l]:.1f}", fontsize=7.6, color=NC[l] if l != "L0" else INK2, weight="demibold", va="center", ha="right")
    gy = B + 12.3
    ax.text(C["L0"] + W / 2, gy, "designed and built once", fontsize=6.3, color=INK2, ha="center", va="center", style="italic")
    x = C["L1"]
    for q, px in enumerate([x + W / 2 - 2.9]):
        ax.add_patch(Rectangle((px, gy - 3.6), 5.8, 7.2, fc="white", ec=NC["L1"], lw=0.8, zorder=3))
        for j, ww in enumerate([3.8, 3, 4, 2.4, 3.4]):
            ax.add_patch(Rectangle((px + 0.9, gy + 2.0 - j * 1.3), ww, 0.5, fc=NC["L1"], ec="none", zorder=4))
    x = C["L2"]
    for k, ok in enumerate(verdict):
        ax.text(x + 6 + k * 4.0, gy + 0.2, "✓" if ok else "✗", fontsize=7.4, color=GOOD if ok else BAD, va="center", ha="center",
                family="DejaVu Sans", weight="bold")
    x = C["L3"]
    if (r3 / "views.png").exists():
        ax.imshow(plt.imread(r3 / "views.png"), extent=(x + W / 2 - 4.5, x + W / 2 + 4.5, gy - 4.4, gy + 4.6), zorder=3, aspect="auto")
    by = T - 5.2; xs = {l: C[l] + W / 2 for l in C}
    dx = X["des"][0] + X["des"][1] / 2; ppx = px0 + pw / 2
    _line(ax, [(dx, T), (dx, by)], color=LINE, lw=1.1, arrow=False); _line(ax, [(ppx, T), (ppx, by)], color=LINE, lw=1.1, arrow=False)
    _line(ax, [(xs["L1"], by), (xs["L3"], by)], color=LINE, lw=1.1, arrow=False)
    for q in (dx, ppx):
        ax.add_patch(Circle((q, by), 0.75, fc=LINE, ec="none", zorder=4))
    for l in ("L1", "L2", "L3"):
        _line(ax, [(xs[l], by), (xs[l], B + HB)], color=LINE, lw=1.1)
    R3, H3 = 6, 22; sy = R3 + H3 / 2; r = 2.1
    cw = 38; cxk = xs["L1"] - cw / 2; gx, gw = 8, 32
    _panel(ax, cxk, R3, cw, H3, ec=INK, lw=1.3); _panel(ax, gx, R3, gw, H3)
    ax.text(cxk + cw / 2, R3 + H3 - 4.2, "Critic", **head)
    for k, ok in enumerate(verdict):
        ax.add_patch(FancyBboxPatch((cxk + 5.3 + k * 4.0, R3 + 7.6), 3.2, 4.4, boxstyle="round,pad=0,rounding_size=0.6", fc=GOOD if ok else BAD, ec="none", zorder=3))
    ax.text(cxk + cw / 2, R3 + 3.7, "met or not, for each requirement", **sub)
    ax.text(gx + gw / 2, R3 + H3 - 4.2, "Textual gradient", **head)
    for k, (c, ww) in enumerate([(BAD, 16), (BAD, 11), (GOOD, 18), (GOOD, 13)]):
        ax.add_patch(Rectangle((gx + 7, R3 + 13.2 - k * 2.2), ww, 1.0, fc=c, alpha=0.8, ec="none", zorder=3))
    ax.text(gx + gw / 2, R3 + 3.2, "advice for the rewrite", **sub)
    _line(ax, [(xs["L1"], B), (xs["L1"], R3 + H3)], color=LINE, lw=1.2)
    _line(ax, [(xs["L3"], B), (xs["L3"], sy), (xs["L2"] + r, sy)], color=LINE, lw=1.2)
    _line(ax, [(xs["L2"] - r, sy), (cxk + cw, sy)], color=LINE, lw=1.2)
    _line(ax, [(xs["L2"], B), (xs["L2"], sy + r)], color=LINE, lw=1.2)
    ax.add_patch(Circle((xs["L2"], sy), r, fc="white", ec=LINE, lw=1.2, zorder=5))
    ax.plot([xs["L2"] - r * 0.5, xs["L2"] + r * 0.5], [sy, sy], color=LINE, lw=1.2, zorder=6)
    ax.plot([xs["L2"], xs["L2"]], [sy - r * 0.5, sy + r * 0.5], color=LINE, lw=1.2, zorder=6)
    for l in ("L1", "L2", "L3"):
        ax.text(xs[l] + 2, (B + (R3 + H3 if l == "L1" else sy)) / 2 + (0 if l == "L1" else 4), kind[l], fontsize=6.6, color=NC[l], va="center", style="italic")
    ax.text((xs["L2"] + xs["L3"]) / 2, sy - 6.3, "each level adds its evidence to what the critic reads", fontsize=7, color=INK2, ha="center", va="center", style="italic")
    _line(ax, [(cxk, sy), (gx + gw, sy)], color=LINE, lw=1.2)
    dcx = X["designer"][0] + X["designer"][1] / 2
    _line(ax, [(gx, sy), (3.2, sy), (3.2, T + H + 3.6), (dcx, T + H + 3.6), (dcx, T + H)], color=NC["L1"], lw=1.3)
    ax.text((3.2 + dcx) / 2 + 2, T + H + 5.3, "rewrite the design, four rounds", fontsize=6.6, color=NC["L1"], ha="center", va="center")
    save(fig, "v4_fig_loop", svg=False)


FIGS = {"loop": fig_loop, "results": fig_results, "gallery": fig_gallery}

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "inspect":
        inspect(*sys.argv[2:5])
    else:
        for n in sys.argv[1:] or list(FIGS):
            FIGS[n](); print("wrote", n)
