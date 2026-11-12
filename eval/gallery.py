"""Gallery PDF: every problem's final design per level, rendered, with hidden-test results.

python eval/gallery.py runs/main [out.pdf]
Needs runs/<run>/results.json (from eval/evaluate_runs.py).
"""
import json, sys, textwrap
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

ROOT = Path(__file__).resolve().parents[1]
LV = ["L0", "L1", "L2", "L3", "L4"]
NAMES = {"L0": "L0 single prompt", "L1": "L1 + text critic", "L2": "L2 + CAD execution",
         "L3": "L3 + agent simulation", "L4": "L4 + render & gate"}
VIEWS = [("iso", 25, -60), ("front", 0, -90), ("top", 90, -90), ("right", 0, 0)]


def draw_mesh(ax, stl, elev, azim):
    m = trimesh.load(stl)
    lo, hi = m.bounds
    span = (hi - lo).max(); ctr = (hi + lo) / 2
    e, a = np.radians(elev), np.radians(azim)
    view = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
    light = view + np.array([0.3, -0.2, 0.5]); light /= np.linalg.norm(light)
    shade = 0.35 + 0.65 * np.clip(np.abs(m.face_normals @ light), 0, 1)
    cols = np.stack([0.55 * shade, 0.65 * shade, 0.8 * shade, np.ones_like(shade)], 1)
    ax.add_collection3d(Poly3DCollection(m.vertices[m.faces], facecolors=cols, edgecolors=(0, 0, 0, 0.05), linewidths=0.15))
    for i, setlim in enumerate((ax.set_xlim, ax.set_ylim, ax.set_zlim)):
        setlim(ctr[i] - span * 0.5, ctr[i] + span * 0.5)
    ax.set_box_aspect((1, 1, 1), zoom=1.25); ax.view_init(elev=elev, azim=azim); ax.set_proj_type("ortho")
    ax.set_axis_off()


def main(root: Path, out: Path | None = None):
    rows = {(r["level"], r["problem"]): r for r in json.loads((root / "results.json").read_text())}
    probs = sorted({p for _, p in rows})
    out = out or root / "gallery.pdf"
    with PdfPages(out) as pdf:
        # cover / summary
        fig = plt.figure(figsize=(11.7, 8.3))
        fig.text(0.5, 0.93, f"DesignGrad gallery: {root.name}", ha="center", fontsize=18, weight="bold")
        fig.text(0.5, 0.89, "Final design per level, scored by the frozen hidden tests (never seen by the loop)", ha="center", fontsize=10)
        img = root / "fig_results_test.png"
        if img.exists():
            ax = fig.add_axes([0.08, 0.42, 0.84, 0.44]); ax.imshow(plt.imread(img)); ax.set_axis_off()
        md = root / "results_test.md"
        if md.exists():
            tbl = [l for l in md.read_text().split("\n## ")[0].splitlines() if l.startswith("| L")]
            cells = [[c.strip() for c in l.strip("|").split("|")] for l in tbl]
            cells = [[c[0], c[1], c[2], c[3], c[4], c[6], c[8]] for c in cells if len(c) >= 9]
            ax = fig.add_axes([0.06, 0.08, 0.88, 0.3]); ax.set_axis_off()
            t = ax.table(cellText=cells[1:], colLabels=cells[0], loc="center", cellLoc="center")
            t.auto_set_font_size(False); t.set_fontsize(8); t.scale(1, 1.4)
        pdf.savefig(fig); plt.close(fig)
        for p in probs:
            spec = (ROOT / "problems" / p.split("@")[0] / "spec.md").read_text().splitlines()
            title = spec[0].lstrip("# ").strip()
            reqs = [l.strip()[2:] for l in spec if l.strip().startswith("- R")]
            meta = json.loads((ROOT / "problems" / p.split("@")[0] / "meta.json").read_text())
            fig = plt.figure(figsize=(11.7, 8.3))
            fig.text(0.02, 0.965, f"{p}: {title}   [{meta.get('split')}]", fontsize=13, weight="bold")
            # requirements block
            txt = "\n".join(textwrap.fill(r, 150, subsequent_indent="      ") for r in reqs)
            fig.text(0.02, 0.945, txt, fontsize=6.3, va="top", family="monospace")
            top = 0.945 - 0.0115 * (txt.count("\n") + 1) - 0.02
            h = (top - 0.05)
            for j, lv in enumerate(LV):
                r = rows.get((lv, p))
                x0 = 0.02 + j * 0.194
                fig.text(x0 + 0.09, top, NAMES[lv], ha="center", fontsize=8.5, weight="bold")
                if r is None:
                    continue
                stl = root / lv / p / "eval_final" / "part.stl"
                vh = h * 0.36  # height of one view cell
                if r["executed"] and stl.exists():
                    for k, (vn, el, az) in enumerate(VIEWS):
                        ax = fig.add_axes([x0 - 0.01 + (k % 2) * 0.1, top - 0.03 - (k // 2 + 1) * vh, 0.1, vh], projection="3d")
                        draw_mesh(ax, stl, el, az)
                        ax.set_title(vn, fontsize=6, pad=-2)
                else:
                    m = root / lv / p / "eval_final" / "metrics.json"
                    err = json.loads(m.read_text()).get("error", "") if m.exists() else ""
                    err = str(err).strip().splitlines()[-1][:160] if err else "did not build"
                    fig.text(x0 + 0.09, top - 0.03 - vh, "DOES NOT BUILD\n" + textwrap.fill(err, 34), ha="center", va="center", fontsize=6.5, color="#B3261E")
                ok = r["n_pass"] == r["n_req"]
                col = "#1D7A46" if ok else ("#B3261E" if r["n_pass"] <= r["n_req"] // 3 else "#8A6D00")
                fig.text(x0 + 0.09, top - 0.05 - 2 * vh, f"hidden tests {r['n_pass']} / {r['n_req']}", ha="center", fontsize=10, weight="bold", color=col)
                passed = [f"R{i}" for i in range(1, r["n_req"] + 1) if f"R{i}" not in r["failed_reqs"]]
                lines = [f"pass: {' '.join(passed) or '-'}", f"fail: {' '.join(r['failed_reqs']) or '-'}",
                         f"calls {r['calls']}, {r['tokens_in'] + r['tokens_out']}k tok" if False else f"calls {r['calls']}  tokens {(r['tokens_in'] + r['tokens_out']) / 1000:.0f}k  {r['seconds'] / 60:.1f} min",
                         f"rounds {r['rounds']}  kept round {r['best_round']}  rejected {r['rejected_updates']}"]
                if lv == "L4":
                    lines.append(f"gate: {r['gate_mismatch']} to code, {r['gate_systemic']} to design, {r['restarts']} restarts")
                if lv in ("L3", "L4"):
                    lines.append(f"sim rewrites {r['sim_updates']}")
                if r.get("curve"):
                    lines.append("hidden by round: " + " ".join(f"{c:.2f}" for c in r["curve"]))
                fig.text(x0 + 0.005, top - 0.08 - 2 * vh, "\n".join(lines), fontsize=5.8, va="top", family="monospace")
            pdf.savefig(fig); plt.close(fig)
    print(out)
    return out


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None)
