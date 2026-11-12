"""python -m designgrad.run --problems P08 P04 --levels L0 L4 [--rounds 4] [--repair 5] [--out runs/main]"""
import argparse, json, time, traceback
from pathlib import Path
from .loop import Run

ROOT = Path(__file__).resolve().parents[1]

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--problems", nargs="*", default=[])
    ap.add_argument("--levels", nargs="*", default=["L0", "L1", "L2", "L3", "L4"])
    ap.add_argument("--rounds", type=int, default=4)
    ap.add_argument("--repair", type=int, default=5)
    ap.add_argument("--out", default="runs/main")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--gate-fix", action="store_true", help="L4 post-hoc render-review fix (ablation runs/v2g_*)")
    ap.add_argument("--ladder", default="v2", choices=["v2", "v4", "v5", "v6", "v7"],
                    help="v4: levels L0-L3, every level builds its code; v5: the same with the critic and analysis fixes; v6: v5 with the analysis-channel fixes (the paper's ladder)")
    a = ap.parse_args()
    pds = [p for p in sorted((ROOT / "problems").glob("P*")) if not a.problems or any(x in p.name for x in a.problems)]
    for pd in pds:
        for lv in a.levels:
            out = ROOT / a.out / lv / pd.name
            if (out / "summary.json").exists() and not a.force:
                print(f"skip {lv} {pd.name}", flush=True); continue
            t = time.time()
            try:
                f = Run(pd, lv, ROOT / a.out, rounds=a.rounds, repair_steps=a.repair, gate_fix=a.gate_fix, ladder=a.ladder).run()
                print(f"done {lv} {pd.name} rounds={f['rounds']} best_k={f['k']} proxy={f['proxy']:.2f} calls={f['llm']['calls']} {time.time()-t:.0f}s", flush=True)
            except Exception:
                print(f"ERROR {lv} {pd.name}\n{traceback.format_exc()}", flush=True)
