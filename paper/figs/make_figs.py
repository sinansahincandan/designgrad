"""Paper figures, rebuilt from run outputs.   python paper/figs/make_figs.py
fig2_loop_health  v1 (one-shot agents) vs v2 (persistent agents) loop health     -> .svg + .png
fig3_results      hidden pass by level (with CI) + success by round                -> .svg + .png
fig4_designs      final designs of seed 0, every problem x level, VTK renders      -> .png
fig5_rounds       one L3 run round by round (keep-best decisions)                   -> .png
Fig 1 (the loop) is a hand-drawn SVG: fig1_loop.svg.
Renders come from paper/figs/vtk_render.py (cached in paper/figs/renders)."""
import json, sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
REN = OUT / "renders"
sys.path.insert(0, str(OUT))

INK, INK2, MUTED, GRID, PAPER = "#1d2433", "#5b6170", "#a3a6ad", "#e9e8e4", "#ffffff"
GOOD, MID, BAD = "#1b9e6e", "#d98a00", "#d64545"
LVC = {"L0": "#9a9a95", "L1": "#6250d6", "L2": "#2a78d6", "L3": "#1baf7a", "L4": "#eb6834"}
LV = ["L0", "L1", "L2", "L3", "L4"]
NAMES = {"L0": "single prompt", "L1": "L0 + text critic", "L2": "L1 + CAD execution", "L3": "L2 + simulation", "L4": "L3 + render review"}
PROB = {"P01_shelf_bracket": "Shelf bracket", "P03_enclosure_base": "Enclosure base", "P07_nema17_mount": "NEMA 17 motor mount"}

plt.rcParams.update({
    "font.family": "Avenir Next", "font.size": 10, "axes.titlesize": 11, "axes.titleweight": "demibold", "axes.titlelocation": "left",
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "axes.linewidth": 1,
    "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False, "figure.facecolor": PAPER, "axes.facecolor": PAPER,
    "xtick.major.size": 0, "ytick.major.size": 0, "svg.fonttype": "none", "text.color": INK})


def save(fig, name, svg=True):
    fig.savefig(OUT / f"{name}.png", dpi=250, bbox_inches="tight", pad_inches=0.08)
    if svg:
        fig.savefig(OUT / f"{name}.svg", bbox_inches="tight", pad_inches=0.08)
    plt.close(fig)


def boot(x, n=10000):
    x = np.asarray(x, float); m = np.random.default_rng(0).choice(x, (n, len(x))).mean(1)
    return np.percentile(m, 2.5), np.percentile(m, 97.5)


def results(run="runs/v2_all"):
    return [r for r in json.loads((ROOT / run / "results.json").read_text()) if r["split"] == "test"]


# ---------------------------------------------------------------- Fig 2: loop health, dumbbell
def fig2():
    rows = [("Rounds ending with a built single part", 0.48, 0.95, "higher is better"),
            ("Simulation verdict = hidden-test verdict", 0.69, 0.93, "higher is better"),
            ("False “fail” on a requirement that passes", 0.41, 0.06, "lower is better")]
    fig, ax = plt.subplots(figsize=(4.4, 2.2))
    for i, (lab, a, b, note) in enumerate(rows):
        y = len(rows) - 1 - i
        ax.plot([0, 1], [y, y], color=GRID, lw=6, solid_capstyle="round", zorder=1)
        ax.annotate("", (b, y), (a, y), arrowprops=dict(arrowstyle="-|>,head_width=0.35,head_length=0.6", color=LVC["L2"], lw=2.2,
                                                         shrinkA=7, shrinkB=7), zorder=2)
        ax.scatter([a], [y], s=90, color=MUTED, zorder=3, edgecolor="white", lw=1.5)
        ax.scatter([b], [y], s=110, color=LVC["L2"], zorder=3, edgecolor="white", lw=1.5)
        ax.text(a, y + 0.27, f"{a:.2f}", ha="center", va="center", fontsize=9.5, color=INK2)
        ax.text(b, y + 0.27, f"{b:.2f}", ha="center", va="center", fontsize=10.5, color=LVC["L2"], weight="demibold")
        ax.text(-0.05, y + 0.02, lab, ha="right", va="center", fontsize=10, color=INK)
        ax.text(-0.05, y - 0.30, note, ha="right", va="center", fontsize=8, color=INK2, style="italic")
    ax.set_xlim(-0.02, 1.03); ax.set_ylim(-0.6, len(rows) - 0.35); ax.set_yticks([])
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1]); ax.spines["bottom"].set_visible(False)
    ax.scatter([], [], s=60, color=MUTED, label="v1  one-shot agents"); ax.scatter([], [], s=60, color=LVC["L2"], label="v2  persistent agents")
    ax.legend(loc="lower center", bbox_to_anchor=(0.5, 1.0), ncol=2, frameon=False, fontsize=9, handletextpad=0.3, columnspacing=1.5)
    save(fig, "fig2_loop_health")


# ---------------------------------------------------------------- Fig 3: results
def fig3():
    res = results()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.28})
    for i, l in enumerate(LV):
        x = [r["pass_rate"] for r in res if r["level"] == l]; m = np.mean(x); lo, hi = boot(x)
        a1.bar(i, m, 0.66, color=LVC[l], zorder=2)
        a1.plot([i, i], [lo, hi], color=INK, lw=1.1, zorder=3, alpha=0.75)
        a1.plot([i - 0.08, i + 0.08], [lo, lo], color=INK, lw=1.1, zorder=3, alpha=0.75)
        a1.plot([i - 0.08, i + 0.08], [hi, hi], color=INK, lw=1.1, zorder=3, alpha=0.75)
        a1.text(i, 0.07, f"{m:.2f}", ha="center", va="center", fontsize=10, color="white", weight="demibold", zorder=4)
        allp = sum(r["all_pass"] for r in res if r["level"] == l)
        a1.text(i, -0.1, f"{allp}/9", ha="center", fontsize=8, color=INK2)
    a1.text(-0.62, -0.1, "7/7:", ha="right", fontsize=8, color=INK2)
    a1.set_xticks(range(5)); a1.set_xticklabels(LV, fontsize=10); a1.tick_params(axis="x", pad=16)
    a1.set_ylim(0, 1.0); a1.set_yticks([0, .25, .5, .75, 1]); a1.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    a1.set_title("Final design: hidden requirements met")
    l0 = np.mean([r["pass_rate"] for r in res if r["level"] == "L0"])
    a2.axhline(l0, color=MUTED, ls=(0, (4, 3)), lw=1.2, zorder=1)
    ends = {}
    for l in LV[1:]:
        cur = np.mean([r["curve_selected"] for r in res if r["level"] == l], axis=0)
        a2.plot(range(len(cur)), cur, color=LVC[l], lw=2.4, marker="o", ms=5, mec="white", mew=1.2, zorder=3)
        ends[l] = cur[-1]
    nudge = {"L1": 0, "L2": -0.012, "L3": 0.03, "L4": -0.035, "L0": 0}
    for l, v in {**ends, "L0": l0}.items():
        a2.text(4.18, v + nudge[l], (f"{l} = {NAMES[l]}" if l != "L0" else f"L0  {NAMES[l]}"), va="center", fontsize=8.5, color=LVC[l] if l != "L0" else INK2, weight="demibold")
    a2.set_xlim(-0.2, 4.1); a2.set_ylim(0, 1.0); a2.set_yticks([0, .25, .5, .75, 1]); a2.set_xticks(range(5))
    a2.set_xlabel("design round", fontsize=9); a2.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    a2.set_title("Design held by keep-best, by round")
    save(fig, "fig3_results")


# ---------------------------------------------------------------- Fig 4: design gallery
def _ensure_render(stl, png, **kw):
    if not png.exists() and stl.exists():
        from vtk_render import render
        png.parent.mkdir(parents=True, exist_ok=True)      # the render cache is not part of the repository
        render(stl, png, 700, **kw)
    return png if png.exists() else None


def _badge(ax, x, y, n, tot, fs=10):
    c = GOOD if n == tot else (MID if n >= tot - 2 else BAD)
    ax.text(x, y, f"{n}/{tot}", ha="center", va="center", fontsize=fs, color="white", weight="demibold", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.32,rounding_size=0.6", fc=c, ec="none"))


def _tile(ax, img, n, tot, note=None):
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)
    ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0,rounding_size=0.06", transform=ax.transAxes,
                                fc="#f6f7f9", ec="#e4e6ea", lw=0.8, zorder=0))
    if img is not None:
        ax.imshow(plt.imread(img), extent=(0.07, 0.93, 0.12, 0.98), zorder=1, aspect="auto")
    else:
        ax.text(0.5, 0.55, "did not build", ha="center", va="center", fontsize=9.5, color=INK2, transform=ax.transAxes, style="italic")
    ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_box_aspect(1)
    if n is not None:
        _badge(ax, 0.82, 0.12, n, tot, fs=9)
    if note:
        ax.text(0.08, 0.12, note, ha="left", va="center", fontsize=8, color=INK2, transform=ax.transAxes)


def fig4(seed="s0"):
    res = {(r["level"], r["problem"]): r for r in results()}
    ang = {"P01_shelf_bracket": dict(azim=-50, elev=25), "P03_enclosure_base": dict(azim=-55, elev=38), "P07_nema17_mount": dict(azim=-50, elev=28)}
    fig, axs = plt.subplots(3, 5, figsize=(8.2, 5.4), gridspec_kw={"wspace": 0.06, "hspace": 0.1})
    for i, p in enumerate(PROB):
        for j, l in enumerate(LV):
            r = res[(l, f"{p}@{seed}")]
            img = _ensure_render(ROOT / f"runs/v2_{seed}/{l}/{p}/eval_final/part.stl", REN / f"{p}_{l}.png", **ang[p]) if r["executed"] else None
            _tile(axs[i, j], img, r["n_pass"], r["n_req"])
            if i == 0:
                axs[i, j].set_title(f"{l}\n", fontsize=11, color=LVC[l], loc="center", weight="demibold", pad=2)
                axs[i, j].text(0.5, 1.04, NAMES[l], ha="center", va="bottom", fontsize=8.5, color=INK2, transform=axs[i, j].transAxes)
            if j == 0:
                axs[i, j].text(-0.06, 0.5, PROB[p], ha="right", va="center", rotation=90, fontsize=9.5, color=INK, weight="demibold",
                               transform=axs[i, j].transAxes)
    save(fig, "fig4_designs", svg=False)


# ---------------------------------------------------------------- Fig 5: one run, round by round
def fig5(run="runs/v2_s0/L3/P07_nema17_mount", key=("L3", "P07_nema17_mount@s0")):
    res = {(r["level"], r["problem"]): r for r in results()}[key]
    S = json.loads((ROOT / run / "summary.json").read_text())
    tr = {t["k"]: t for t in S["trace"]}
    fig, axs = plt.subplots(1, 5, figsize=(8.2, 2.25), gridspec_kw={"wspace": 0.06})
    for k in range(5):
        img = _ensure_render(ROOT / f"{run}/r{k:02d}/part.stl", REN / f"evo_P07_L3_r{k}.png", azim=-50, elev=28)
        t = tr[k]; n = round(res["curve"][k] * res["n_req"])
        note = "start" if k == 0 else ("kept" if t["accepted"] else "rejected")
        _tile(axs[k], img, n, res["n_req"], note)
        axs[k].set_title(f"round {k}", fontsize=9.5, loc="center", color=INK, weight="demibold" if k == S["k"] else "normal", pad=3)
        axs[k].text(0.5, -0.07, f"agent score {t['score']:.2f}", ha="center", va="top", fontsize=8, color=INK2, transform=axs[k].transAxes)
        if k == S["k"]:
            axs[k].add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0,rounding_size=0.06", transform=axs[k].transAxes,
                                            fc="none", ec=LVC["L3"], lw=2, zorder=5))
    save(fig, "fig5_rounds", svg=False)


if __name__ == "__main__":
    fig2(); fig3(); fig4(); fig5(); print("figures written to", OUT)
