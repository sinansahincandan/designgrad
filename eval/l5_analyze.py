"""L5 study on the phone stand (P02): levels L0, L2, L3, L5, three seeds.

python eval/l5_analyze.py runs/l5_s0 runs/l5_s1000 runs/l5_s2000   -> runs/l5_study.md + runs/l5_study.json
Each runs/l5_s* must have been evaluated (eval/evaluate_runs.py writes results.json) and mechanics.py run (hidden_rows.json).
"""
import json, sys
from pathlib import Path

import numpy as np

LV = ["L0", "L2", "L3", "L5"]
NAME = {"L0": "L0 single prompt", "L2": "L2 = L1 + CAD execution", "L3": "L3 = L2 + simulation", "L5": "L5 = L2 + MuJoCo scenarios"}


def rows(run):
    return {r["level"]: r for r in json.loads((Path(run) / "results.json").read_text()) if r["problem"].startswith("P02")}


def scen_stats(run):
    d = Path(run) / "L5" / "P02_phone_stand"
    n = faithful = fails = fb_ok = 0
    exh = loops = 0
    tilts = []
    for rd in sorted(d.glob("r0*")):
        try:
            sim = json.loads((rd / "sim.json").read_text()); A = json.loads((rd / "agent.json").read_text())
        except Exception:
            continue
        loops += 1; exh += bool(A.get("sim_exhausted"))
        for v in (sim.get("result") or {}).values():
            n += 1; faithful += v.get("faithful") is not False
            if v.get("status") == "fail":
                fails += 1
                fb_ok += any(ch.isdigit() for ch in str(v.get("design_feedback", "")))
        for e in sim.get("motion") or []:
            for name, b in e["bodies"].items():
                if name != "part" and "placed_tilt_deg" in b:
                    tilts.append(b["placed_tilt_deg"])
    return {"scenarios": n, "faithful": faithful, "failed": fails, "failed_with_numeric_feedback": fb_ok,
            "scenario_loops": loops, "exhausted": exh, "object_tilts_deg": sorted(set(round(t) for t in tilts))}


def main(runs):
    R = {Path(r).name: rows(r) for r in runs}
    seeds = list(R)
    out = {"seeds": seeds, "levels": {}, "paired": {}, "scenarios": {s: scen_stats(r) for s, r in zip(seeds, runs)}}
    md = ["# L5 study: phone stand (P02), 3 seeds", "",
          "P02 is the problem on which L5 was developed (its prompts and harness checks were tuned on it): a development problem for L5.", "",
          "| Level | Hidden pass per seed | Mean | All 7/7 | Kept = best? | Calls | Min |", "|---|---|---|---|---|---|---|"]
    for lv in LV:
        pr = [R[s][lv]["pass_rate"] for s in seeds if lv in R[s]]
        ap = sum(R[s][lv]["all_pass"] for s in seeds if lv in R[s])
        calls = np.mean([R[s][lv]["calls"] for s in seeds if lv in R[s]])
        mins = np.mean([R[s][lv]["seconds"] for s in seeds if lv in R[s]]) / 60
        kept = []
        for s in seeds:
            c = R[s].get(lv, {}).get("curve") or []
            if c:
                kept.append(f"{R[s][lv]['n_pass']}/{R[s][lv]['n_req']} vs {round(max(c) * R[s][lv]['n_req'])}")
        out["levels"][lv] = {"pass_rates": pr, "mean": float(np.mean(pr)), "all_pass": ap, "calls": float(calls), "minutes": float(mins)}
        md.append(f"| {NAME[lv]} | {', '.join(f'{x:.2f}' for x in pr)} | {np.mean(pr):.2f} | {ap}/{len(pr)} | {'; '.join(kept) or '-'} | "
                  f"{calls:.0f} | {mins:.0f} |")
    md += ["", "| Step | Difference per seed | Mean | W/T/L |", "|---|---|---|---|"]
    for a, b in [("L0", "L2"), ("L2", "L3"), ("L2", "L5"), ("L3", "L5")]:
        dd = [R[s][b]["pass_rate"] - R[s][a]["pass_rate"] for s in seeds if a in R[s] and b in R[s]]
        out["paired"][f"{a}->{b}"] = dd
        md.append(f"| {a} -> {b} | {', '.join(f'{x:+.2f}' for x in dd)} | {np.mean(dd):+.2f} | "
                  f"{sum(x > 0 for x in dd)}/{sum(x == 0 for x in dd)}/{sum(x < 0 for x in dd)} |")
    md += ["", "| Seed | L5 scenarios | judged faithful | failed | failed with numeric feedback | scenario loops exhausted | object tilts placed (deg) |",
           "|---|---|---|---|---|---|---|"]
    for s, st in out["scenarios"].items():
        md.append(f"| {s} | {st['scenarios']} | {st['faithful']} | {st['failed']} | {st['failed_with_numeric_feedback']} | "
                  f"{st['exhausted']}/{st['scenario_loops']} | {st['object_tilts_deg']} |")
    Path("runs/l5_study.md").write_text("\n".join(md) + "\n")
    Path("runs/l5_study.json").write_text(json.dumps(out, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main(sys.argv[1:])
