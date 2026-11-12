"""Figures of the v3 paper (L0-L4 narrative), rebuilt from the frozen run outputs.   python paper/figs/make_figs_v3.py [name ...]
All outputs are new files (v3_*.png / .svg); the figures of the earlier paper versions are not touched.
  v3_fig1_loop      the loop diagram (fig1_loop.svg with plain-language labels)
  v3_fig2_measure   what the agent's own measurement code looks at (shelf bracket, L3, repeat 1)
  v3_fig3_results   requirements met per level (9 runs as dots) + design kept after each round
  v3_fig4_designs   reference design + final designs L0-L4 (repeat 1 pictured, all three repeats listed)
  v3_fig5_chain     inside one design round: measurement -> critic -> gradient -> code edit -> result
  v3_fig6_twoloops  same start, two loops (motor mount, repeat 1): L3 vs L4
  v3_fig7_mass      finding vs fixing: bracket mass round by round (L3, three repeats)
Every number and quote is read from runs/v2_* (or copied verbatim from the recorded calls; see QUOTES)."""
import json, sys, textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_figs import (ROOT, OUT, REN, INK, INK2, MUTED, GRID, GOOD, MID, BAD, LVC, LV, PROB, save, results, _ensure_render, _badge, _tile)

# The paper's ladder (every level builds its code):  L0 design + build, no feedback | L1 + critic and textual gradients |
# L2 + the agent's own analysis code | L3 + render review.  It is read from the frozen runs like this:
#   paper L1, L2, L3 = recorded levels L2, L3, L4;  paper L0 = round 0 of the recorded L2 runs (the start design after the CAD agent
#   has repaired its code, before any feedback).  The recorded L0 and L1 (code never executed) are not part of the paper.
NLV = ["L0", "L1", "L2", "L3"]
REC = {"L1": "L2", "L2": "L3", "L3": "L4"}
NC = {"L0": "#9a9a95", "L1": "#2a78d6", "L2": "#1baf7a", "L3": "#eb6834"}
NAMES = {"L0": "no feedback", "L1": "+ critic", "L2": "+ own analysis", "L3": "+ render review"}
SEEDS = ["s0", "s1000", "s2000"]
ANG = {"P01_shelf_bracket": dict(azim=-50, elev=25), "P03_enclosure_base": dict(azim=-55, elev=38), "P07_nema17_mount": dict(azim=-50, elev=28)}


def hidden(rd):
    f = rd / "hidden_rows.json"
    return json.loads(f.read_text()) if f.exists() else {}


def ladder():
    """Rows (level, problem, n_pass, all_pass, curve) of the paper's ladder, read from the frozen runs."""
    old = {(r["level"], r["problem"]): r for r in results()}
    out = []
    for (lv, prob), r in old.items():
        if lv != "L2":
            continue
        p, seed = prob.split("@")
        h = hidden(ROOT / f"runs/v2_{seed}/L2/{p}/r00")
        n = sum(v is True for v in h.values())
        out.append({"level": "L0", "problem": prob, "n_pass": n, "all_pass": n == 7, "curve": None})
    for new, rec in REC.items():
        for (lv, prob), r in old.items():
            if lv == rec:
                out.append({"level": new, "problem": prob, "n_pass": r["n_pass"], "all_pass": r["all_pass"], "curve": [c * 7 for c in r["curve_selected"]]})
    return out


# ---------------------------------------------------------------- Fig 1: the loop as a control diagram
SHADOW = "#dfe2e8"


def _block(ax, x, y, w, h, ec=INK2, fc="white", lw=1.2, r=1.8, shadow=True):
    if shadow:
        ax.add_patch(FancyBboxPatch((x + 0.55, y - 0.75), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=SHADOW, ec="none", zorder=1))
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=lw, zorder=2))


def _pill(ax, x, y, text, color, fs=7.2):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color="white", weight="demibold", zorder=6,
            bbox=dict(boxstyle="round,pad=0.28,rounding_size=0.7", fc=color, ec="none"))


def _line(ax, pts, color=INK2, lw=1.3, arrow=True, ls="-"):
    xs, ys = zip(*pts)
    if arrow:
        ax.plot(xs[:-1], ys[:-1], color=color, lw=lw, ls=ls, solid_capstyle="round", solid_joinstyle="round", zorder=3)
        ax.annotate("", pts[-1], pts[-2], arrowprops=dict(arrowstyle="-|>,head_width=0.26,head_length=0.5", color=color, lw=lw, shrinkA=0, shrinkB=0), zorder=3)
    else:
        ax.plot(xs, ys, color=color, lw=lw, ls=ls, solid_capstyle="round", solid_joinstyle="round", zorder=3)


def _sum(ax, x, y, color=INK, r=2.3):
    from matplotlib.patches import Circle
    ax.add_patch(Circle((x, y), r, fc="white", ec=color, lw=1.4, zorder=5))
    ax.plot([x - r * 0.55, x + r * 0.55], [y, y], color=color, lw=1.4, zorder=6)
    ax.plot([x, x], [y - r * 0.55, y + r * 0.55], color=color, lw=1.4, zorder=6)


def _met_bar(ax, x, y, w, value, color):
    """Small summary bar: requirements met by the final designs of this level (of 7)."""
    ax.add_patch(Rectangle((x, y), w, 1.5, fc=GRID, ec="none", zorder=3))
    ax.add_patch(Rectangle((x, y), w * value / 7, 1.5, fc=color, ec="none", zorder=4))
    ax.text(x + w + 1.2, y + 0.75, f"{value:.1f}", fontsize=7.4, color=color, weight="demibold", va="center", zorder=4)


def _tint(c, a=0.09):
    r, g, b = matplotlib.colors.to_rgb(c)
    return (1 - a + a * r, 1 - a + a * g, 1 - a + a * b)


def _panel(ax, x, y, w, h, ec="#c5c9d2", fc="white", lw=0.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=2.2", fc=fc, ec=ec, lw=lw, zorder=2))


LINE = "#3a4152"


def fig1(run="runs/v2_s2000/L3/P07_nema17_mount", run4="runs/v2_s2000/L4/P07_nema17_mount"):
    """The loop: specification -> designer -> design -> built part; the levels' evidence -> critic -> textual gradient -> designer."""
    from matplotlib.patches import Circle
    res = ladder(); met = {l: float(np.mean([r["n_pass"] for r in res if r["level"] == l])) for l in NLV}
    sim = json.loads((ROOT / run / "r00/sim.json").read_text())["result"]; m = json.loads((ROOT / run / "r00/metrics.json").read_text())
    verdict = [sim[f"R{k}"]["status"] == "pass" for k in range(1, 8)]
    fig = plt.figure(figsize=(8.6, 4.55)); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 200); ax.set_ylim(0, 105.8); ax.axis("off")
    head = dict(ha="center", va="center", fontsize=8.8, weight="demibold", color=INK)
    sub = dict(ha="center", va="center", fontsize=6.3, color=INK2)
    # ---- row 1: specification -> designer -> design -> built part
    T, H = 76, 23; yc = T + H / 2
    X = {"spec": (8, 32), "designer": (56, 32), "des": (104, 32)}
    for k, (x, w) in X.items():
        _panel(ax, x, T, w, H, ec=INK if k == "designer" else "#c5c9d2", lw=1.3 if k == "designer" else 0.9)
    px0, pw = 156, 24
    for a, b in [((40, yc), (56, yc)), ((88, yc), (104, yc)), ((136, yc), (px0 + 1.5, yc))]:
        _line(ax, [a, b], color=LINE, lw=1.2)
    ax.text(146.5, yc + 3.4, "CAD agent", **{**sub, "color": INK, "fontsize": 6.6}); ax.text(146.5, yc - 3.4, "runs and repairs", **sub)
    x, w = X["spec"]; ax.text(x + w / 2, T + H - 4.4, "Specification", **head)
    for k in range(7):
        ax.add_patch(Rectangle((x + 6.5, T + H - 9.2 - k * 1.95), [16, 19, 13, 17, 15, 19, 12][k], 0.75, fc="#b9bdc7", ec="none", zorder=3))
    x, w = X["designer"]; ax.text(x + w / 2, T + H - 4.4, "Designer", **head)
    ax.text(x + w / 2, T + 10.2, "writes the design,", **{**sub, "fontsize": 6.9, "color": INK}); ax.text(x + w / 2, T + 6.6, "then rewrites it", **{**sub, "fontsize": 6.9, "color": INK})
    x, w = X["des"]; ax.text(x + w / 2, T + H - 4.4, "Design", **head)
    for k, t in enumerate(["document  d", "code  c"]):
        ax.add_patch(FancyBboxPatch((x + 5.5, T + 9.2 - 6 * k), w - 11, 4.7, boxstyle="round,pad=0,rounding_size=1", fc="#f1f2f5", ec="none", zorder=3))
        ax.text(x + w / 2, T + 11.55 - 6 * k, t, ha="center", va="center", fontsize=6.8, color=INK)
    img = _ensure_render(ROOT / run / "r00/part.stl", REN / "case_p07_s2000_r0.png", azim=-50, elev=28)
    ax.imshow(plt.imread(img), extent=(px0 + 2.5, px0 + pw - 2.5, T + 3.6, T + H - 0.6), zorder=3, aspect="auto")
    ax.text(px0 + pw / 2, T + 1.6, "the built part", **sub)
    # ---- row 2: the four levels
    B, HB, W = 41, 24.5, 36
    C = {"L0": 8, "L1": 56, "L2": 104, "L3": 152}
    title = {"L0": "no feedback", "L1": "reads design and part", "L2": "own analysis code", "L3": "looks at the part"}
    for l, x in C.items():
        _panel(ax, x, B, W, HB, ec=NC[l], fc=_tint(NC[l], 0.07), lw=1.1)
        _pill(ax, x + 4.8, B + HB - 4.3, l, NC[l], fs=6.8)
        ax.text(x + 9.6, B + HB - 4.3, title[l], fontsize=7.6, weight="demibold", color=NC[l] if l != "L0" else INK2, va="center")
        ax.add_patch(Rectangle((x + 4.5, B + 3.1), W - 15, 1.5, fc="white", ec="none", zorder=3))
        ax.add_patch(Rectangle((x + 4.5, B + 3.1), (W - 15) * met[l] / 7, 1.5, fc=NC[l], ec="none", zorder=4))
        ax.text(x + W - 4.5, B + 3.85, f"{met[l]:.1f}", fontsize=7.6, color=NC[l] if l != "L0" else INK2, weight="demibold", va="center", ha="right")
    gy = B + 12.3

    def page(px, col, widths):
        ax.add_patch(Rectangle((px, gy - 3.6), 5.8, 7.2, fc="white", ec=col, lw=0.8, zorder=3))
        for q, ww in enumerate(widths):
            ax.add_patch(Rectangle((px + 0.9, gy + 2.0 - q * 1.3), ww, 0.5, fc=col, ec="none", zorder=4))
    ax.text(C["L0"] + W / 2, gy, "the first design, as built", fontsize=6.3, color=INK2, ha="center", va="center", style="italic")
    x = C["L1"]; sz = m["size_mm"]
    page(x + 5, NC["L1"], [3.8, 3, 4, 2.4, 3.4])
    ax.text(x + 14, gy + 1.6, f"{sz[0]:.0f} × {sz[1]:.0f} × {sz[2]:.0f} mm", fontsize=6, color=INK, va="center")
    ax.text(x + 14, gy - 1.6, f"{m['mass_g']:.0f} g", fontsize=6, color=INK, va="center")
    x = C["L2"]
    for k, ok in enumerate(verdict):
        ax.text(x + 6 + k * 4.0, gy + 0.2, "✓" if ok else "✗", fontsize=7.4, color=GOOD if ok else BAD, va="center", ha="center",
                family="DejaVu Sans", weight="bold")
    x = C["L3"]
    ax.imshow(plt.imread(ROOT / run4 / "r00/views.png"), extent=(x + W / 2 - 4.5, x + W / 2 + 4.5, gy - 4.4, gy + 4.6), zorder=3, aspect="auto")
    # the design and its part are observed
    by = T - 5.2; xs = {l: C[l] + W / 2 for l in C}
    dx = X["des"][0] + X["des"][1] / 2; ppx = px0 + pw / 2
    _line(ax, [(dx, T), (dx, by)], color=LINE, lw=1.1, arrow=False); _line(ax, [(ppx, T), (ppx, by)], color=LINE, lw=1.1, arrow=False)
    _line(ax, [(xs["L1"], by), (xs["L3"], by)], color=LINE, lw=1.1, arrow=False)
    for q in (dx, ppx):
        ax.add_patch(Circle((q, by), 0.75, fc=LINE, ec="none", zorder=4))
    for l in ("L1", "L2", "L3"):
        _line(ax, [(xs[l], by), (xs[l], B + HB)], color=LINE, lw=1.1)
    # ---- row 3: evidence -> critic -> textual gradient -> back to the designer
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
    ax.text((xs["L2"] + xs["L3"]) / 2, sy - 6.3, "each level adds its evidence to what the critic reads", fontsize=7, color=INK2, ha="center", va="center", style="italic")
    _line(ax, [(cxk, sy), (gx + gw, sy)], color=LINE, lw=1.2)
    dcx = X["designer"][0] + X["designer"][1] / 2
    _line(ax, [(gx, sy), (3.2, sy), (3.2, T + H + 3.6), (dcx, T + H + 3.6), (dcx, T + H)], color=NC["L1"], lw=1.3)
    ax.text((3.2 + dcx) / 2 + 2, T + H + 5.3, "rewrite d and c, four rounds", fontsize=6.6, color=NC["L1"], ha="center", va="center")
    save(fig, "v3_fig1_loop", svg=False)


# ---------------------------------------------------------------- Fig 3: results
def fig3():
    res = ladder()
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.4, 3.0), gridspec_kw={"width_ratios": [1, 1.35], "wspace": 0.26})
    rng = np.random.default_rng(3)
    for i, l in enumerate(NLV):
        x = np.array([r["n_pass"] for r in res if r["level"] == l]); m = x.mean()
        a1.bar(i, m, 0.62, color=NC[l], zorder=2, alpha=0.92)
        a1.scatter(i + rng.uniform(-0.19, 0.19, len(x)), x + rng.uniform(-0.08, 0.08, len(x)), s=16, color="white", edgecolor=INK, lw=0.9, zorder=4)
        a1.text(i, 7.5, f"{m:.1f}", ha="center", va="center", fontsize=10, color=NC[l] if l != "L0" else INK2, weight="demibold", zorder=4)
        a1.text(i, -1.35, f"{sum(r['all_pass'] for r in res if r['level'] == l)} of 9", ha="center", fontsize=8, color=INK2)
    a1.text(-0.6, -1.35, "all 7 met:", ha="right", fontsize=8, color=INK2)
    a1.set_xticks(range(4)); a1.set_xticklabels(NLV, fontsize=10)
    a1.set_ylim(0, 7.9); a1.set_yticks(range(0, 8)); a1.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    a1.set_title("Requirements met, final design", pad=10)
    l0 = np.mean([r["n_pass"] for r in res if r["level"] == "L0"])
    a2.axhline(l0, color=MUTED, ls=(0, (4, 3)), lw=1.2, zorder=1)
    ends = {}
    for l in NLV[1:]:
        cur = np.mean([r["curve"] for r in res if r["level"] == l], axis=0)
        a2.plot(range(len(cur)), cur, color=NC[l], lw=2.4, marker="o", ms=5, mec="white", mew=1.2, zorder=3)
        ends[l] = cur[-1]
    nudge = {"L1": 0.0, "L2": 0.28, "L3": -0.3, "L0": 0}
    for l, v in {**ends, "L0": l0}.items():
        a2.text(4.18, v + nudge[l], f"{l}  {NAMES[l]}", va="center", fontsize=8.5, color=NC[l] if l != "L0" else INK2, weight="demibold")
    a2.set_xlim(-0.2, 4.1); a2.set_ylim(0, 7.9); a2.set_yticks(range(0, 8)); a2.set_xticks(range(5))
    a2.set_xlabel("design round", fontsize=9); a2.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    a2.set_title("Requirements met by the design held after each round", pad=10)
    save(fig, "v3_fig3_results")


# ---------------------------------------------------------------- Fig 4: gallery with the reference design
def _reference_stl(p):
    stl = REN / f"ref_{p}.stl"
    if not stl.exists():
        import cadquery as cq
        ns = {}
        exec((ROOT / "problems" / p / "reference.py").read_text(), ns)
        cq.exporters.export(ns["result"], str(stl))
    return stl


def fig4():
    res = {(r["level"], r["problem"]): r for r in ladder()}
    fig, axs = plt.subplots(3, 5, figsize=(8.2, 5.25), gridspec_kw={"wspace": 0.06, "hspace": 0.1})
    for i, p in enumerate(PROB):
        ax = axs[i, 0]
        _tile(ax, _ensure_render(_reference_stl(p), REN / f"ref_{p}.png", color=(0.62, 0.66, 0.72), **ANG[p]), 7, 7)
        ax.text(-0.06, 0.5, PROB[p].replace("NEMA 17 m", "M"), ha="right", va="center", rotation=90, fontsize=9.5, color=INK, weight="demibold", transform=ax.transAxes)
        if i == 0:
            ax.set_title("Reference\n", fontsize=11, color=INK, loc="center", weight="demibold", pad=2)
            ax.text(0.5, 1.04, "a correct design", ha="center", va="bottom", fontsize=8.5, color=INK2, transform=ax.transAxes)
        for j, l in enumerate(NLV, start=1):
            rr = [res[(l, f"{p}@{s}")] for s in SEEDS]
            stl = ROOT / (f"runs/v2_s0/L2/{p}/r00/part.stl" if l == "L0" else f"runs/v2_s0/{REC[l]}/{p}/eval_final/part.stl")
            img = _ensure_render(stl, REN / (f"{p}_start.png" if l == "L0" else f"{p}_{REC[l]}.png"), **ANG[p])
            _tile(axs[i, j], img, rr[0]["n_pass"], 7, note="runs: " + "  ".join(str(x["n_pass"]) for x in rr))
            if i == 0:
                axs[i, j].set_title(f"{l}\n", fontsize=11, color=NC[l], loc="center", weight="demibold", pad=2)
                axs[i, j].text(0.5, 1.04, NAMES[l], ha="center", va="bottom", fontsize=8.5, color=INK2, transform=axs[i, j].transAxes)
    save(fig, "v3_fig4_designs", svg=False)


# ---------------------------------------------------------------- Fig 2: what the agent's measurement code looks at
def _section(mesh, origin, normal, ix, iy):
    """Filled outline of the cut of `mesh` by a plane, as lists of (u, v) loops in the two kept world axes."""
    sec = mesh.section(plane_origin=origin, plane_normal=normal)
    return [] if sec is None else [np.asarray(d)[:, [ix, iy]] for d in sec.discrete]


def fig2(run="runs/v2_s0/L3/P01_shelf_bracket"):
    import trimesh
    S = json.loads((ROOT / run / "summary.json").read_text()); rd = ROOT / run / f"r{S['k']:02d}"
    sim = json.loads((rd / "sim.json").read_text())["result"]; hid = hidden(rd)
    mesh = trimesh.load(rd / "part.stl")
    fig = plt.figure(figsize=(8.6, 3.5))
    ax = fig.add_axes([0.02, 0.06, 0.52, 0.86]); ax2 = fig.add_axes([0.555, 0.2, 0.1, 0.6]); tx = fig.add_axes([0.68, 0.02, 0.32, 0.96]); tx.axis("off")
    loops = sorted(_section(mesh, [0, 0.0, 0], [0, 1, 0], 0, 2), key=lambda q: -np.ptp(q[:, 0]) * np.ptp(q[:, 1]))
    for n, q in enumerate(loops):
        ax.fill(q[:, 0], q[:, 1], color="#8fb0dc" if n == 0 else "white", ec=INK, lw=0.9, zorder=2)
    for z in (20, 60):   # screwdriver access: nothing within 4 mm of each hole axis for x >= 10
        ax.add_patch(Rectangle((10, z - 4), 165, 8, fc=BAD, alpha=0.16, ec=BAD, lw=0.8, ls=(0, (3, 2)), zorder=3))
    ax.text(96, 64.6, "must stay empty: screwdriver access", fontsize=7.6, color=BAD, ha="center", va="bottom")
    ax.plot([10, 10], [-8, 124], color=LVC["L3"], lw=1.4, ls=(0, (5, 3)), zorder=4)
    ax.text(12, 121, "cut at x = 10", fontsize=7.6, color=LVC["L3"], va="center")
    ax.add_patch(Rectangle((140, 106), 10, 4, fc=MID, alpha=0.5, ec=MID, lw=0.8, zorder=4))
    ax.text(146, 100, "shelf seat", fontsize=7.6, color=MID, ha="center", va="top")
    ax.annotate("", (150, 111), (150, 134), arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.4))
    ax.text(153, 128, "150 N", fontsize=8, color=INK, va="center")
    ax.plot([0, 0], [-8, 124], color=INK2, lw=2.2); ax.text(-3, 58, "wall", rotation=90, fontsize=8, color=INK2, ha="right", va="center")
    ax.set_xlim(-12, 182); ax.set_ylim(-12, 138); ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Side view of the built bracket (cut at y = 0)", fontsize=9.5, loc="left", pad=0)
    loops = sorted(_section(mesh, [10.0, 0, 0], [1, 0, 0], 1, 2), key=lambda q: -np.ptp(q[:, 0]) * np.ptp(q[:, 1]))
    for n, q in enumerate(loops):
        ax2.fill(q[:, 0], q[:, 1], color="#7fd3b3" if n == 0 else "white", ec=INK, lw=0.9)
    ax2.set_xlim(-26, 26); ax2.set_ylim(-12, 138); ax2.set_aspect("equal"); ax2.axis("off")
    ax2.set_title("section at x = 10", fontsize=7.8, color=LVC["L3"], loc="center", pad=0)
    val = lambda r: sim[r]["value"]
    rows = [("R1", "one solid", "1 solid"),
            ("R2", "fits its envelope, touches the wall", "x 0–160, y ±20, z 0–110 mm"),
            ("R3", "screw holes with screwdriver access", "material found in the access zone"),
            ("R4", "flat shelf seat at z = 110", "seat volume only partly filled"),
            ("R5", "bending stress at the cut ≤ 20 MPa", f"{val('R5'):.2f} MPa"),
            ("R6", "tip deflection ≤ 2 mm", f"{val('R6'):.2f} mm"),
            ("R7", "mass ≤ 90 g", f"{val('R7'):.0f} g")]
    tx.text(0.0, 0.97, "What its own code measured", fontsize=9.5, weight="demibold", va="top")
    y = 0.86
    for r, what, got in rows:
        ok = sim[r]["status"] == "pass"; agree = ok == (hid.get(r) is True)
        tx.text(0.0, y, "✓" if ok else "✗", fontsize=11, color=GOOD if ok else BAD, weight="bold", va="center", family="DejaVu Sans")
        tx.text(0.07, y + 0.022, f"{r}  {what}", fontsize=7.9, color=INK, va="center")
        tx.text(0.07, y - 0.03, got + ("" if agree else "   (independent test: met)"), fontsize=7.4, color=INK2 if agree else BAD, va="center")
        y -= 0.118
    n_agree = sum((sim[r]["status"] == "pass") == (hid.get(r) is True) for r, _, _ in rows)
    tx.text(0.0, y + 0.01, f"{n_agree} of 7 verdicts agree with the independent tests.", fontsize=7.8, color=INK2, style="italic", va="center")
    save(fig, "v3_fig2_measure", svg=False)


# ---------------------------------------------------------------- Fig 5: inside one design round
QUOTES = {  # verbatim from runs/v2_s2000/L3/P07_nema17_mount (r00/loss.md; calls.jsonl gradient call for c; r00/c.py -> r01/c.py)
    "critic": ["“The entire part is shifted in Z (bbox_min z = -27.5), causing it to fail the table mounting requirement (R6) …”",
               "“The central bore (R3) and motor screw holes (R4) are not correctly subtracted through the face plate along the Y axis …”"],
    "grad": ["“The current `face_plate` uses `centered=(True, False, True)`, which places the center of the plate's height at z=0. "
             "This causes half the plate to be below the table …”",
             "“On the \"XY\" plane, a cylinder's axis is Z. To drill through the face plate along the Y-axis, you must use "
             "`cq.Workplane(\"XZ\")` …”"],
    "diff": [("-", "face_plate = cq.Workplane(\"XY\").box(\u2026,"), ("-", "    centered=(True, False, True))"),
             ("+", "face_plate = cq.Workplane(\"XY\").box(\u2026)"), ("+", "    .translate((0, 2, 27.5))"), ("", ""),
             ("-", ".cut(cq.Workplane(\"XY\").cylinder(\u2026))"), ("+", ".cut(cq.Workplane(\"XZ\").cylinder(\u2026))")]}


def _card(ax, num, title, color):
    ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.add_patch(FancyBboxPatch((0.01, 0.02), 0.98, 0.96, boxstyle="round,pad=0,rounding_size=0.04", transform=ax.transAxes, fc="white", ec=color, lw=1.3))
    ax.text(0.06, 0.9, f"{num}  {title}", fontsize=9, weight="demibold", color=color, va="center", transform=ax.transAxes)


def _para(ax, texts, y=0.79, width=47, fs=7.5, gap=0.035, lh=0.072, color=INK, family=None):
    for t in texts:
        for line in textwrap.wrap(t, width):
            ax.text(0.06, y, line, fontsize=fs, color=color, va="center", transform=ax.transAxes, **({"family": family} if family else {}))
            y -= lh
        y -= gap
    return y


def fig5(run="runs/v2_s2000/L3/P07_nema17_mount"):
    sim = json.loads((ROOT / run / "r00/sim.json").read_text())["result"]
    h0, h1 = hidden(ROOT / run / "r00"), hidden(ROOT / run / "r01")
    n0, n1 = sum(v is True for v in h0.values()), sum(v is True for v in h1.values())
    fig = plt.figure(figsize=(8.6, 5.0))
    g1 = fig.add_gridspec(1, 3, width_ratios=[0.78, 1, 1], wspace=0.05, top=0.98, bottom=0.52, left=0.01, right=0.99)
    g2 = fig.add_gridspec(1, 3, width_ratios=[1, 1, 0.78], wspace=0.05, top=0.48, bottom=0.02, left=0.01, right=0.99)
    axs = np.array([[fig.add_subplot(g1[0, j]) for j in range(3)], [fig.add_subplot(g2[0, j]) for j in range(3)]])
    b = axs[0, 0]; _tile(b, _ensure_render(ROOT / run / "r00/part.stl", REN / "case_p07_s2000_r0.png", azim=-50, elev=28), n0, 7, "before")
    a = axs[1, 2]; _tile(a, _ensure_render(ROOT / run / "r01/part.stl", REN / "case_p07_s2000_r1.png", azim=-50, elev=28), n1, 7, "after")
    c1, c2, c3, c4 = axs[0, 1], axs[0, 2], axs[1, 0], axs[1, 1]
    _card(c1, "1", "The agent measures its own part", LVC["L3"])
    r6, r3, r4 = sim["R6"]["value"], sim["R3"]["value"], sim["R4"]["value"]
    _para(c1, [f"lowest point of the part: z = {r6['z_min']} mm (the table is z = 0)",
               f"material inside the motor bore: {r3:.0f} mm³ (must be 0)",
               f"material in the four screw holes: {', '.join(f'{x:.0f}' for x in r4)} mm³",
               "material in the face plate around the bore: none"], width=44)
    _card(c2, "2", "The critic reads the numbers", LVC["L1"]); _para(c2, QUOTES["critic"], width=44)
    _card(c3, "3", "The gradient names the lines", LVC["L2"]); _para(c3, QUOTES["grad"], width=44)
    _card(c4, "4", "The code is edited", INK)
    y = 0.78
    for sign, line in QUOTES["diff"]:
        c4.text(0.06, y, f"{sign} {line}" if sign else "", fontsize=6.6, family="Menlo", va="center", transform=c4.transAxes,
                color={"-": BAD, "+": GOOD}.get(sign, INK))
        y -= 0.085
    c4.text(0.06, 0.13, "Next round: every requirement is met.", fontsize=7.6, color=INK2, style="italic", va="center", transform=c4.transAxes)
    for ax in (b, a):
        ax.set_box_aspect(None)
    save(fig, "v3_fig5_chain", svg=False)


# ---------------------------------------------------------------- Fig 6: same start, two loops
def fig6(p="P07_nema17_mount"):
    notes = {"L2": ["half the part is below the table", "code edited: part lifted onto the table, holes drilled through", "all its own checks pass",
                    "no gain", "one requirement lost"],
             "L3": ["render reviewer: \u201corientation \u2026 fundamentally broken\u201d", "code rewritten from the design text: same flaw",
                    "a better part, but its own checks wrongly fail two requirements", "rewritten again: same flaw", "rewritten again: same flaw"]}
    fig, axs = plt.subplots(2, 5, figsize=(8.6, 4.6), gridspec_kw={"wspace": 0.06, "hspace": 0.42})
    for i, l in enumerate(("L2", "L3")):
        run = ROOT / f"runs/v2_s0/{REC[l]}/{p}"; S = json.loads((run / "summary.json").read_text()); tr = {t["k"]: t for t in S["trace"]}
        for k in range(5):
            ax = axs[i, k]
            img = _ensure_render(run / f"r{k:02d}/part.stl", REN / f"evo_P07_{REC[l]}_r{k}.png", azim=-50, elev=28)
            h = hidden(run / f"r{k:02d}")
            _tile(ax, img, sum(v is True for v in h.values()), 7, "start" if k == 0 else ("kept" if tr[k]["accepted"] else "rejected"))
            if i == 0:
                ax.set_title(f"round {k}", fontsize=9.5, loc="center", color=INK, pad=3)
            for n, line in enumerate(textwrap.wrap(notes[l][k], 25)):
                ax.text(0.5, -0.07 - 0.095 * n, line, ha="center", va="top", fontsize=7.3, color=INK2, transform=ax.transAxes)
            if k == S["k"]:
                ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0,rounding_size=0.06", transform=ax.transAxes,
                                            fc="none", ec=NC[l], lw=2, zorder=5))
        axs[i, 0].text(-0.07, 0.5, f"{l}  {NAMES[l]}", ha="right", va="center", rotation=90, fontsize=9, color=NC[l], weight="demibold",
                       transform=axs[i, 0].transAxes)
    save(fig, "v3_fig6_twoloops", svg=False)


# ---------------------------------------------------------------- Fig 7: finding vs fixing (bracket mass)
def fig7(p="P01_shelf_bracket"):
    fig, ax = plt.subplots(figsize=(6.4, 2.9))
    cols = ["#1baf7a", "#2a78d6", "#8a5cd6"]
    for n, s in enumerate(SEEDS):
        run = ROOT / f"runs/v2_{s}/L3/{p}"; S = json.loads((run / "summary.json").read_text())
        mass = [json.loads((run / f"r{t['k']:02d}/metrics.json").read_text())["mass_g"] for t in S["trace"]]
        ax.plot(range(5), mass, color=cols[n], lw=2, zorder=2, label=f"run {n + 1}")
        for t, m in zip(S["trace"], mass):
            ax.scatter(t["k"], m, s=46, zorder=3, color=cols[n] if t["accepted"] else "white", edgecolor=cols[n], lw=1.6)
    ax.axhline(90, color=BAD, lw=1.3, ls=(0, (5, 3)), zorder=1); ax.text(-0.3, 80, "limit: 90 g", color=BAD, fontsize=8.5, va="top")
    ax.annotate("94 g: closest yet, still a “fail”,\nso the loop discards it", (4, 93.6), (2.45, 30), fontsize=7.8, color=INK2, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8))
    ax.annotate("49 g, but now too weak:\nstress 193 MPa (limit 20)", (4, 49.3), (4.18, 150), fontsize=7.8, color=INK2, ha="left", va="center",
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8), annotation_clip=False)
    ax.scatter([], [], s=40, color=INK2, label="kept"); ax.scatter([], [], s=40, color="white", edgecolor=INK2, lw=1.4, label="rejected")
    ax.set_xticks(range(5)); ax.set_xlabel("design round", fontsize=9); ax.set_ylabel("mass of the bracket (g)", fontsize=9)
    ax.set_ylim(0, 330); ax.set_xlim(-0.35, 4.3); ax.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    ax.legend(frameon=False, fontsize=8, ncol=5, loc="upper left", bbox_to_anchor=(0.0, 1.14), handletextpad=0.3, columnspacing=1.2)
    save(fig, "v3_fig7_mass")




FIGS = {"fig1": fig1, "fig2": fig2, "fig3": fig3, "fig4": fig4, "fig5": fig5, "fig6": fig6, "fig7": fig7}

if __name__ == "__main__":
    for n in (sys.argv[1:] or list(FIGS)):
        FIGS[n](); print("wrote", n)
