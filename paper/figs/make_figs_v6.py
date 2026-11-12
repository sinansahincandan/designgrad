"""Further figures for the paper's runs (ladder v6).   python paper/figs/make_figs_v6.py [results parts control limits gallery]
Main runs: runs/v6_s0, v6_s1000, v6_s2000 (three parts, three repeats) and runs/v6_all/v4_summary.json.
Further parts: runs/v6x_s0 (and v6x_s1000 when present). Everything is scored with the frozen independent tests."""
import json, sys, textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Rectangle

sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_figs_v4 as F
from make_figs_v4 import ROOT, REN, INK, INK2, MUTED, GRID, GOOD, MID, BAD, NC, NLV, NAMES, save, _ensure_render, _tile, _cardbox, _write, QUOTE

MAIN = {"P01_shelf_bracket": "Shelf bracket", "P03_enclosure_base": "Enclosure base", "P07_nema17_mount": "Motor mount"}
MORE = {"P02_phone_stand": "Phone stand", "P05_pipe_clamp": "Pipe clamp", "P09_drone_arm": "Drone arm", "P06_heat_sink": "Heat sink"}
# P10_sensor_tilt_mount also ran (runs/v6x_s0) and is left out of the figure: its CAD code ran out of steps in 12 of 16 builds.
F.ANG.update({"P02_phone_stand": dict(azim=-55, elev=22), "P10_sensor_tilt_mount": dict(azim=-50, elev=28), "P05_pipe_clamp": dict(azim=-50, elev=30),
              "P09_drone_arm": dict(azim=-55, elev=32), "P06_heat_sink": dict(azim=-50, elev=32)})
XRUNS = tuple(r for r in ("runs/v6x_s0", "runs/v6x_s1000") if (ROOT / r).exists())
# Runs left out of the figure because the CAD agent ran out of repair steps in most builds (the paper says so): the tilted sensor mount
# (12 of 16 builds, first repeat; not repeated) and the second repeat of the pipe clamp (10 of 16 builds).
LEFT_OUT = {("P05_pipe_clamp", "s1000")}


def nreq(p):
    return sum(1 for l in (ROOT / "problems" / p / "spec.md").read_text().splitlines() if l.strip().startswith("- R"))


def finals(U):
    """{problem: {level: [requirements met by the kept design, one per repeat]}}"""
    out = {}
    for (lv, p, s), u in sorted(U.items()):
        out.setdefault(p, {}).setdefault(lv, []).append(u["met"][u["kept"]])
    return out


# ---------------------------------------------------------------- results: levels, rounds, and each part
def fig_results():
    U = F.units(); Sm = F.summary(); fin = finals(U)
    fig = plt.figure(figsize=(7.6, 4.55))
    g = fig.add_gridspec(2, 6, height_ratios=[1.3, 1], hspace=0.78, wspace=1.1, left=0.095, right=0.985, top=0.925, bottom=0.08)
    a1 = fig.add_subplot(g[0, :3]); a2 = fig.add_subplot(g[0, 3:])
    rng = np.random.default_rng(3)
    for i, l in enumerate(NLV):
        x = np.array([v for p in fin for v in fin[p].get(l, [])]); m = x.mean()
        a1.bar(i, m, 0.62, color=NC[l], zorder=2, alpha=0.92)
        a1.scatter(i + rng.uniform(-0.19, 0.19, len(x)), x + rng.uniform(-0.08, 0.08, len(x)), s=15, color="white", edgecolor=INK, lw=0.9, zorder=4)
        a1.text(i, 7.55, f"{m:.1f}", ha="center", va="center", fontsize=10, color=NC[l] if l != "L0" else INK2, weight="demibold", zorder=4)
        a1.text(i, -1.75, NAMES[l], ha="center", fontsize=7.2, color=INK2)
    a1.set_xticks(range(4)); a1.set_xticklabels(NLV, fontsize=10)
    a1.set_ylim(0, 8); a1.set_yticks(range(0, 8)); a1.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    a1.set_title("Requirements met by the final design", pad=8, fontsize=9.6)
    a1.set_ylabel("requirements met (of 7)", fontsize=8.5)
    a2.set_ylabel("requirements met (of 7)", fontsize=8.5)
    l0 = Sm["levels"]["L0"]["met"]
    a2.plot([-0.2, 4.08], [l0, l0], color=MUTED, ls=(0, (4, 3)), lw=1.2, zorder=1)
    ends = {l: Sm["levels"][l]["curve_kept"] for l in NLV[1:]}
    for l, cur in ends.items():
        a2.plot(range(len(cur)), cur, color=NC[l], lw=2.4, marker="o", ms=5, mec="white", mew=1.2, zorder=3)
    lab = []
    for v, l in sorted([(cur[-1], l) for l, cur in ends.items()] + [(l0, "L0")]):
        lab.append((v if not lab else max(v, lab[-1][0] + 0.68), l))
    for y, l in lab:
        a2.text(4.2, y, l, va="center", fontsize=8, color=NC[l] if l != "L0" else INK2, weight="demibold")
    a2.set_xlim(-0.2, 4.75); a2.set_ylim(0, 8); a2.set_yticks(range(0, 8)); a2.set_xticks(range(5))
    a2.set_xlabel("design round", fontsize=8.5); a2.grid(axis="y", color=GRID, lw=0.8, zorder=0)
    a2.set_title("Design held by the loop after each round", pad=8, fontsize=9.6)
    for j, (p, name) in enumerate(MAIN.items()):
        a = fig.add_subplot(g[1, 2 * j:2 * j + 2])
        means = [np.mean(fin[p][l]) for l in NLV]
        a.plot(range(4), means, color="#c9ccd3", lw=2.2, zorder=2)
        for i, l in enumerate(NLV):
            v = np.array(fin[p][l]); off = np.linspace(-0.13, 0.13, len(v)) if len(v) > 1 else [0]
            a.scatter(i + np.array(off), sorted(v), s=17, color="white", edgecolor=NC[l] if l != "L0" else INK2, lw=1.1, zorder=4)
            a.plot([i - 0.24, i + 0.24], [means[i]] * 2, color=NC[l], lw=3, zorder=3, solid_capstyle="round")
        a.set_xticks(range(4)); a.set_xticklabels(NLV, fontsize=8.5); a.set_xlim(-0.5, 3.5)
        a.set_ylim(0, 7.6); a.set_yticks([0, 2, 4, 6, 7]); a.tick_params(axis="y", labelsize=8); a.grid(axis="y", color=GRID, lw=0.8, zorder=0)
        a.set_title(name, fontsize=9.2, pad=5)
        a.set_ylabel("requirements met", fontsize=7.6)
    save(fig, "v6_fig_results", svg=False)


# ---------------------------------------------------------------- all parts
def fig_parts():
    """Seven parts, one row each: a correct reference, requirements met at each level (mean over the repeats), the part L3 kept."""
    U = F.units(); X = F.units(runs=XRUNS) if XRUNS else {}
    X = {k: v for k, v in X.items() if (k[1], k[2]) not in LEFT_OUT}
    rows = [(p, n, U) for p, n in MAIN.items()] + [(p, n, X) for p, n in MORE.items() if any(k[1] == p for k in X)]
    nR = len(rows); fig = plt.figure(figsize=(7.6, 0.78 * nR + 0.75)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis("off")
    W, Hh = 100.0, (0.78 * nR + 0.75) / 7.6 * 100; ax.set_xlim(0, W); ax.set_ylim(0, Hh)
    rh = 0.78 / 7.6 * 100; top = Hh - 0.75 / 7.6 * 100
    cx = {"ref": 6.5, "name": 13.5, "L0": 44, "L1": 56, "L2": 68, "L3": 80, "part": 93.5}
    ax.text(cx["ref"], top + 3.2, "reference", ha="center", fontsize=7.6, color=INK2)
    ax.text(cx["part"], top + 3.2, "L3, first repeat", ha="center", fontsize=7.6, color=INK2)
    for l in NLV:
        ax.text(cx[l], top + 5.2, l, ha="center", fontsize=9.6, weight="demibold", color=NC[l] if l != "L0" else INK2)
        ax.text(cx[l], top + 2.0, NAMES[l], ha="center", fontsize=6.6, color=INK2)
    for i, (p, name, D) in enumerate(rows):
        y = top - (i + 0.5) * rh; n = nreq(p); fin = finals(D)[p]
        if i == len(MAIN):
            ax.plot([2, 98], [y + rh / 2] * 2, color="#d8dae0", lw=0.8)
        ref = _ensure_render(F._reference_stl(p), REN / f"ref_{p}.png", color=(0.62, 0.66, 0.72), **F.ANG[p])
        ax.imshow(plt.imread(ref), extent=(cx["ref"] - rh * 0.47, cx["ref"] + rh * 0.47, y - rh * 0.47, y + rh * 0.47), zorder=3, aspect="auto")
        ax.text(cx["name"], y + 1.1, name, fontsize=9, color=INK, weight="demibold", va="center")
        k = len(fin.get("L0", []))
        ax.text(cx["name"], y - 2.3, f"{n} requirements, {k} repeat{'s' if k > 1 else ''}", fontsize=6.8, color=INK2, va="center")
        for l in NLV:
            v = fin.get(l)
            if not v:
                continue
            m = float(np.mean(v)); fr = m / n
            ax.add_patch(FancyBboxPatch((cx[l] - 5, y - rh * 0.33), 10, rh * 0.66, boxstyle="round,pad=0,rounding_size=1.2",
                                        fc=F_tint(NC[l], 0.10 + 0.55 * fr ** 2), ec="none", zorder=2))
            ax.text(cx[l], y + 0.1, f"{m:.1f}" if len(v) > 1 else f"{int(m)}", ha="center", va="center", fontsize=10, weight="demibold",
                    color=INK if fr < 0.99 else "white" if l != "L0" else INK, zorder=3)
        seeds = sorted({s for (lv, pp, s) in D if pp == p and lv == "L3"})
        if seeds:
            u = D[("L3", p, seeds[0])]; stl = u["dir"] / f"r{u['kept']:02d}/part.stl"
            img = _ensure_render(stl, REN / f"v6parts_{p}_{seeds[0]}.png", **F.ANG[p]) if stl.exists() else None
            if img:
                ax.imshow(plt.imread(img), extent=(cx["part"] - rh * 0.47, cx["part"] + rh * 0.47, y - rh * 0.47, y + rh * 0.47), zorder=3, aspect="auto")
    save(fig, "v6_fig_parts", svg=False)


def F_tint(c, a):
    import matplotlib.colors as mc
    r, g, b = mc.to_rgb(c)
    return (1 - a + a * r, 1 - a + a * g, 1 - a + a * b)


# ---------------------------------------------------------------- testing the tests: the control part
def _pill(ax, x, y, text, color, fs=7.2):
    ax.text(x, y, text, ha="center", va="center", fontsize=fs, color="white", weight="demibold", transform=ax.transAxes,
            bbox=dict(boxstyle="round,pad=0.3,rounding_size=0.6", fc=color, ec="none"), zorder=5)


def fig_control(run="runs/v6_s0", problem="P07_nema17_mount", req="R4",
                what="four motor screw holes, diameter 3.4 mm"):
    """A check that passes on a part with nothing in it. All quotes are copied from the recorded run (calls.jsonl, sim.json)."""
    rd = ROOT / run / "L2" / problem
    calls = [json.loads(l) for l in (rd / "calls.jsonl").read_text().splitlines()]
    c = next(x for x in calls if x.get("role") == "sim_reviewer")
    u = c["user"] if isinstance(c["user"], str) else json.dumps(c["user"])
    rep = u[u.index("# Its report"):u.index("For every requirement")]
    before = json.loads(rep[rep.index("{"):rep.rindex("}") + 1])[req]
    ctl = u[u.index("# Control run"):]
    assert req in ctl[ctl.index("- pass:"):ctl.index("- fail or error")], "the check must pass on the control part"
    out = json.loads(c["output"][c["output"].index("{"):c["output"].rindex("}") + 1])[req]; assert out["faithful"] is False
    after = json.loads((rd / "r00/sim.json").read_text())["result"][req]
    truth = json.loads((rd / "r00/hidden_rows.json").read_text())[req]
    assert before["status"] == "pass" and after["status"] == "fail" and truth is False
    fig = plt.figure(figsize=(8.6, 2.25))
    gs = fig.add_gridspec(1, 4, left=0.012, right=0.988, top=0.985, bottom=0.02, width_ratios=[0.62, 1.2, 1.5, 1.2], wspace=0.035)
    a = fig.add_subplot(gs[0]); pd = ROOT / "problems" / problem
    _tile(a, _ensure_render(rd / "r00/part.stl", REN / f"v6ctl_{problem[:3]}.png", **F.ANG[problem]), F.met(pd, rd / "r00"), nreq(problem), "built"); a.set_box_aspect(None)
    b = fig.add_subplot(gs[1]); _cardbox(b, "1  The agent writes a check", NC["L2"])
    y = _write(b, [(f"{req}: {what}", INK, "normal", None), ("“" + before["method"] + "”", QUOTE, "normal", None)], width=36, y=0.76)
    b.text(0.045, 0.2, "on the built part", fontsize=6.9, color=INK2, va="center", transform=b.transAxes); _pill(b, 0.8, 0.2, "met", "#7a8194")
    c2 = fig.add_subplot(gs[2]); _cardbox(c2, "2  The same check on a part with nothing in it", INK)
    c2.add_patch(Rectangle((0.06, 0.6), 0.035, 0.055, fc="#8fa8d6", ec="#5f7fb8", lw=0.6, transform=c2.transAxes))
    c2.text(0.125, 0.63, "a 1 mm cube: no plate, no holes", fontsize=6.9, color=INK, va="center", transform=c2.transAxes); _pill(c2, 0.87, 0.63, "met", BAD)
    why = out["why"]; cut = why.split(". ")[0] + "."
    _write(c2, [("The reviewer: “" + cut + "”", QUOTE, "normal", None)], width=47, y=0.44)
    d = fig.add_subplot(gs[3]); _cardbox(d, "3  The check is rewritten", NC["L2"])
    _write(d, [("“" + after["method"] + "”", QUOTE, "normal", None)], width=36, y=0.76)
    d.text(0.045, 0.36, "on the cube", fontsize=6.9, color=INK2, va="center", transform=d.transAxes); _pill(d, 0.8, 0.36, "not met", INK)
    d.text(0.045, 0.2, "on the built part", fontsize=6.9, color=INK2, va="center", transform=d.transAxes); _pill(d, 0.8, 0.2, "not met", INK)
    d.text(0.045, 0.07, "the independent test agrees: not met", fontsize=6.5, color=GOOD, va="center", transform=d.transAxes)
    save(fig, "v6_fig_control", svg=False)


# ---------------------------------------------------------------- what limits the loop
def fig_limits():
    Sm = F.summary()["levels"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 2.55), gridspec_kw={"width_ratios": [1, 1.25], "wspace": 0.3, "left": 0.095, "right": 0.985, "top": 0.86, "bottom": 0.2})
    for i, l in enumerate(NLV[1:]):
        fx, bk = Sm[l]["fix"], Sm[l]["break"]
        f, b = fx[0] / max(fx[1], 1), bk[0] / max(bk[1], 1)
        a1.bar(i - 0.21, f * 100, 0.36, color=NC[l], zorder=2); a1.bar(i + 0.21, b * 100, 0.36, color=NC[l], alpha=0.35, zorder=2, hatch="////", edgecolor="white", lw=0)
        a1.text(i - 0.21, f * 100 + 2, f"{fx[0]}/{fx[1]}", ha="center", fontsize=7, color=INK)
        a1.text(i + 0.21, b * 100 + 2, f"{bk[0]}/{bk[1]}", ha="center", fontsize=7, color=INK2)
    a1.set_xticks(range(3)); a1.set_xticklabels(NLV[1:], fontsize=9.5); a1.set_ylim(0, 60); a1.set_yticks([0, 20, 40, 60]); a1.set_yticklabels(["0", "20%", "40%", "60%"], fontsize=8)
    a1.grid(axis="y", color=GRID, lw=0.8, zorder=0); a1.set_title("One design round", fontsize=9.6, pad=7)
    a1.set_ylabel("share of requirements", fontsize=8.5)
    a2.set_ylabel("level", fontsize=8.5)
    a1.text(0.02, -0.26, "solid: unmet requirements it fixes     hatched: met requirements it breaks", fontsize=6.9, color=INK2, transform=a1.transAxes)
    cols = [("agree", "agrees with the tests", GOOD), ("false_alarm", "false alarm", MID), ("missed", "missed", BAD), ("disputed", "disputed by the reviewer", "#b9bdc7")]
    for i, l in enumerate(("L3", "L2")):
        c = Sm[l]["analysis_counts"]; tot = sum(c[k] for k, _, _ in cols) + c["unmeasured"]; x = 0
        for k, _, col in cols:
            w = c[k] / tot * 100
            a2.barh(i, w, 0.5, left=x, color=col, zorder=2)
            if w > 4:
                a2.text(x + w / 2, i, str(c[k]), ha="center", va="center", fontsize=7.6, color="white" if col != "#b9bdc7" else INK, weight="demibold")
            x += w
    a2.set_yticks([0, 1]); a2.set_yticklabels(["L3", "L2"], fontsize=9.5); a2.set_xlim(0, 100); a2.set_xticks([0, 25, 50, 75, 100]); a2.set_xticklabels(["0", "25%", "50%", "75%", "100%"], fontsize=8)
    a2.set_ylim(-0.55, 1.55); a2.set_title("The agent's own checks against the independent tests", fontsize=9.6, pad=7)
    for (_, name, col), x0 in zip(cols, [0.0, 0.335, 0.525, 0.685]):
        a2.add_patch(Rectangle((x0, -0.285), 0.022, 0.05, fc=col, ec="none", transform=a2.transAxes, clip_on=False))
        a2.text(x0 + 0.03, -0.26, name, fontsize=6.9, color=INK2, va="center", transform=a2.transAxes)
    save(fig, "v6_fig_limits", svg=False)


# ---------------------------------------------------------------- gallery of the three main parts
def fig_gallery(seed="s0"):
    U = F.units(); seeds = sorted({s for (_, _, s) in U}, key=lambda s: int(s[1:]))
    fig, axs = plt.subplots(3, 5, figsize=(8.2, 5.25), gridspec_kw={"wspace": 0.06, "hspace": 0.1})
    for i, (p, name) in enumerate(MAIN.items()):
        ax = axs[i, 0]
        _tile(ax, _ensure_render(F._reference_stl(p), REN / f"ref_{p}.png", color=(0.62, 0.66, 0.72), **F.ANG[p]), 7, 7)
        ax.text(-0.06, 0.5, name, ha="right", va="center", rotation=90, fontsize=9.5, color=INK, weight="demibold", transform=ax.transAxes)
        if i == 0:
            ax.set_title("Reference\n", fontsize=11, color=INK, loc="center", weight="demibold", pad=2)
            ax.text(0.5, 1.04, "a correct design", ha="center", va="bottom", fontsize=8.5, color=INK2, transform=ax.transAxes)
        for j, l in enumerate(NLV, start=1):
            us = [U[(l, p, s)] for s in seeds if (l, p, s) in U]; u = U[(l, p, seed)]
            stl = u["dir"] / f"r{u['kept']:02d}/part.stl"
            img = _ensure_render(stl, REN / f"{F.TAG}_{p}_{l}_{seed}.png", **F.ANG[p]) if stl.exists() else None
            _tile(axs[i, j], img, u["met"][u["kept"]], 7, note="runs: " + "  ".join(str(x["met"][x["kept"]]) for x in us))
            if i == 0:
                axs[i, j].set_title(f"{l}\n", fontsize=11, color=NC[l], loc="center", weight="demibold", pad=2)
                axs[i, j].text(0.5, 1.04, NAMES[l], ha="center", va="bottom", fontsize=8.5, color=INK2, transform=axs[i, j].transAxes)
    save(fig, "v6_fig_gallery", svg=False)


# ---------------------------------------------------------------- round by round: the loop at work
def _first_problem(loss, n=82):
    """First line of the critic's problem list (verbatim; cut at a word boundary, marked with '...')."""
    import re
    m = re.search(r"^\W*Problems\b.*$", loss, flags=re.I | re.M)
    tail = loss[m.end():] if m else loss
    for ln in tail.splitlines():
        ln = F.plain(ln).strip().lstrip("-*0123456789. ").strip()
        if ln and not ln.upper().startswith("SIM_CODE_ISSUE") and ln.lower() != "none":
            return ln if len(ln) <= n else ln[:n].rsplit(" ", 1)[0] + " ..."
    return ""


def fig_rounds(rows=None, name="v6_fig_rounds"):
    """rows: [(run, level, problem)]. One strip per unit: the part produced in every round, the requirements it meets, whether the
    loop kept it, and the first problem the critic named in the design it was rewritten from."""
    rows = rows or [("runs/v6_s2000", "L2", "P01_shelf_bracket"), ("runs/v6_s1000", "L3", "P07_nema17_mount")]   # the paper's Fig. 6
    n = len(rows); fig = plt.figure(figsize=(8.6, 2.5 * n))
    names = {**MAIN, **MORE}
    for i, (run, lv, p) in enumerate(rows):
        rd = ROOT / run / lv / p; pd = ROOT / "problems" / p; S = json.loads((rd / "summary.json").read_text()); tr = {t["k"]: t for t in S["trace"]}
        top = 1 - i / n; h = 1 / n
        fig.text(0.012, top - 0.075 * h, f"{names[p]}", fontsize=9.6, weight="demibold", color=INK, va="center")
        fig.text(0.012 + 0.0115 * len(names[p]) + 0.012, top - 0.075 * h, f"{lv}  {NAMES[lv]}", fontsize=8.6, weight="demibold", color=NC[lv], va="center")
        ks = sorted(tr); w = 0.976 / 5
        held = 0
        for j in range(5):
            if j >= len(ks):
                fig.text(0.012 + j * w + w / 2, top - 0.42 * h, "stopped:\nnothing left to fix", ha="center", va="center", fontsize=7.4, color=INK2, style="italic")
                continue
            k = ks[j]; t = tr[k]
            ax = fig.add_axes([0.012 + j * w + 0.012, top - 0.70 * h, w - 0.024, 0.56 * h])
            stl = rd / f"r{k:02d}/part.stl"
            img = _ensure_render(stl, REN / f"v6rounds_{Path(run).name}_{lv}_{p[:3]}_r{k}.png", **F.ANG[p]) if stl.exists() else None
            kept = k == 0 or bool(t.get("accepted")); held = k if kept else held
            _tile(ax, img, None, nreq(p), note=("first design" if k == 0 else f"round {k}")); ax.set_box_aspect(None)
            if False:
                ax.add_patch(FancyBboxPatch((0.02, 0.02), 0.96, 0.96, boxstyle="round,pad=0,rounding_size=0.06", transform=ax.transAxes, fc="none", ec=NC[lv], lw=2.0, zorder=6))
            if k > 0:
                fig.text(0.012 + j * w + w / 2, top - 0.735 * h, "", ha="center", va="top", fontsize=6.8,
                         color=GOOD if kept else INK2, weight="demibold")
                q = _first_problem((rd / f"r{t['from']:02d}/loss.md").read_text())
                if j > 1 and tr[ks[j - 1]].get("from") == t["from"]:
                    fig.text(0.012 + j * w + w / 2, top - 0.80 * h, "the same critique,\na new attempt", ha="center", va="top", fontsize=6.0, color=INK2, style="italic", linespacing=1.25)
                else:
                    fig.text(0.012 + j * w + w / 2, top - 0.80 * h, "\n".join(textwrap.wrap("“" + q + "”", 34)[:4]), ha="center", va="top", fontsize=6.0, color=QUOTE, linespacing=1.25)
    save(fig, name, svg=False)


def casebook(runs=None):
    """Print every round that the loop kept and that met more requirements than the design it came from."""
    runs = runs or [r for r in (f"runs/{F.TAG}_s0", f"runs/{F.TAG}_s1000", f"runs/{F.TAG}_s2000", *XRUNS) if (ROOT / r).exists()]
    for run in runs:
        for lv in NLV[1:]:
            for rd in sorted((ROOT / run / lv).glob("P*")):
                if not (rd / "summary.json").exists():
                    continue
                pd = ROOT / "problems" / rd.name; S = json.loads((rd / "summary.json").read_text())
                tr = {t["k"]: t for t in S["trace"]}; path = [F.met(pd, rd / f"r{k:02d}") for k in sorted(tr)]
                for k, t in tr.items():
                    if k and t.get("accepted") and F.met(pd, rd / f"r{k:02d}") > F.met(pd, rd / f"r{t['from']:02d}"):
                        print(f"{run} {lv} {rd.name[:3]} r{t['from']}->r{k}: {F.met(pd, rd / f'r{t['from']:02d}')} -> {F.met(pd, rd / f'r{k:02d}')}  (all rounds {path}, kept r{S['k']})")
                        print("     ", _first_problem((rd / f"r{t['from']:02d}/loss.md").read_text(), 200))


# ---------------------------------------------------------------- the prompts
def fig_prompts():
    """Three of the prompts, verbatim from designgrad/prompts.py."""
    sys.path.insert(0, str(ROOT))
    import designgrad.prompts as P
    crit = P.CRITIC_USER_V5[P.CRITIC_USER_V5.index("Review the design."):].replace("{sim_question}", "").strip()
    cards = [("Critic", NC["L1"], crit, 66),
             ("Critic at L1: nothing but the design document", NC["L1"], P.EVIDENCE_NONE_V5.replace("# Evidence", "").strip(), 66),
             ("Reviewer of the agent's checks: the control run", NC["L2"], P.SIM_REVIEW_CONTROL_V6.replace("{passed}", "R1, R4, R7").replace("{failed}", "R2, R3, R5, R6").replace("# Control run", "").strip(), 66),
             ("Analysis agent: two of its rules", NC["L2"], P.SIM_RULES_V5.strip(), 66)]
    FH = 4.75; fig = plt.figure(figsize=(8.6, FH)); pos = [(0.012, 0.375, 0.482, 0.615), (0.506, 0.375, 0.482, 0.615), (0.012, 0.012, 0.482, 0.345), (0.506, 0.012, 0.482, 0.345)]
    order = [0, 2, 1, 3]
    for (x, y, w, h), ci in zip(pos, order):
        title, col, txt, width = cards[ci]
        ax = fig.add_axes([x, y, w, h]); ax.set_xticks([]); ax.set_yticks([]); ax.set_xlim(0, 1); ax.set_ylim(0, 1)
        for sp in ax.spines.values():
            sp.set_visible(False)
        ax.add_patch(FancyBboxPatch((0.008, 0.012), 0.984, 0.976, boxstyle="round,pad=0,rounding_size=0.025", transform=ax.transAxes, fc="#fbfbfc", ec=col, lw=1.1))
        ax.text(0.035, 1 - 14 / (h * FH * 72), title, fontsize=8.4, weight="demibold", color=col, va="center", transform=ax.transAxes)
        paras = []                                   # reflow: the source wraps mid-sentence; headings, bullets and blank lines start a paragraph
        for ln in txt.split("\n"):
            st = ln.strip()
            if not st:
                paras.append("")
            elif (st.startswith(("#", "- ")) or not paras or paras[-1] == "" or paras[-1].startswith("#")
                  or (paras[-1].startswith("- ") and not ln.startswith("  "))):
                paras.append(st)
            else:
                paras[-1] += " " + st
        lines = []
        for para in paras:
            lines += textwrap.wrap(para, width, subsequent_indent="  " if para.startswith("- ") else "") or [""]
        ph = h * FH * 72; lh = 8.3 / ph
        for j, ln in enumerate(lines):
            ax.text(0.035, 1 - 30 / (h * FH * 72) - j * lh, ln, fontsize=5.9, family="DejaVu Sans Mono", color=INK, va="center", transform=ax.transAxes)
    save(fig, "v6_fig_prompts", svg=False)


FIGS = {"results": fig_results, "parts": fig_parts, "control": fig_control, "limits": fig_limits, "gallery": fig_gallery, "rounds": fig_rounds, "prompts": fig_prompts}

if __name__ == "__main__":
    if sys.argv[1:2] == ["casebook"]:
        casebook()
    else:
        for n in sys.argv[1:] or list(FIGS):
            FIGS[n](); print("wrote", n)
