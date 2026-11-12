"""Independent evaluation of finished runs with the frozen hidden tests (never visible to the loop).

python eval/evaluate_runs.py runs/main          -> runs/main/results.json + results.md
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "eval"))
from designgrad.sandbox import run_cad
from hidden_eval import evaluate


def eval_code(pd, code_path, workdir, density):
    if not code_path.exists():
        return {"executed": False, "pass_rate": 0.0, "n_pass": 0, "rows": []}
    step = workdir / "part.step"
    m = json.loads((workdir / "metrics.json").read_text()) if (workdir / "metrics.json").exists() else None
    if m is None or not step.exists() or (workdir / "c.py").exists() and (workdir / "c.py").read_text() != code_path.read_text():
        m = run_cad(code_path.read_text(), workdir, density)
    r = evaluate(pd, step) if m.get("ok") else {"ran": False, "rows": [], "pass_rate": 0.0, "n_pass": 0,
                                                 "n_req": sum(1 for l in (pd / "spec.md").read_text().splitlines() if l.strip().startswith("- R"))}
    r["executed"] = bool(m.get("ok"))
    r["single_solid"] = bool(m.get("ok") and m.get("n_solids") == 1)
    return r


def main(run_root: Path):
    rows = []
    for lvdir in sorted(p for p in run_root.glob("L*") if p.is_dir()):
        for rd in sorted(p for p in lvdir.glob("P*") if p.is_dir()):
            if not (rd / "summary.json").exists():
                continue
            pd = ROOT / "problems" / rd.name.split("@")[0]  # "P01_x@s1000" = seed replicate
            meta = json.loads((pd / "meta.json").read_text())
            summ = json.loads((rd / "summary.json").read_text())
            fin = eval_code(pd, rd / "final_c.py", rd / "eval_final", meta["density"])
            curve = []
            for r in sorted(rd.glob("r[0-9][0-9]")):
                cp = r / "c.py"
                wd = r if (r / "part.step").exists() else rd / f"eval_{r.name}"
                if not cp.exists():
                    continue
                if wd != r:
                    wd.mkdir(exist_ok=True)
                curve.append(round(eval_code(pd, cp, wd, meta["density"])["pass_rate"], 3))
            gates = [t.get("gate") for t in summ["trace"] if t.get("gate")]
            # reward hacking: an update the agent accepted (its own score did not drop) while hidden pass-rate dropped
            hack, best_hidden = 0, curve[0] if curve else 0
            for t in summ["trace"]:
                kk = t["k"]
                if kk < len(curve) and t.get("accepted"):
                    if curve[kk] < best_hidden - 1e-9:
                        hack += 1
                    best_hidden = curve[kk]
            # hidden pass-rate of the candidate the agent holds as "best" after each round, and good updates it threw away
            sel, cur, rejected_good = [], (curve[0] if curve else 0), 0
            for t in summ["trace"]:
                kk = t["k"]
                if kk < len(curve):
                    if t.get("accepted"):
                        cur = curve[kk]
                    elif curve[kk] > cur + 1e-9:
                        rejected_good += 1
                sel.append(cur)
            rows.append({
                "problem": rd.name, "split": meta.get("split"), "level": lvdir.name,
                "pass_rate": round(fin["pass_rate"], 3), "n_pass": fin.get("n_pass", 0), "n_req": fin.get("n_req"),
                "all_pass": fin.get("n_pass", 0) == fin.get("n_req"), "executed": fin["executed"], "single_solid": fin.get("single_solid", False),
                "failed_reqs": [x["id"] for x in fin.get("rows", []) if not x["pass"]],
                "curve": curve, "rounds": summ["rounds"], "best_round": summ["k"],
                "calls": summ["llm"]["calls"], "tokens_in": summ["llm"]["tokens_in"], "tokens_out": summ["llm"]["tokens_out"],
                "seconds": summ["llm"]["seconds"],
                "gate_mismatch": sum(len(g["mismatches"]) for g in gates), "gate_systemic": sum(len(g["systemic"]) for g in gates),
                "restarts": sum(1 for t in summ["trace"] if t.get("restart_from_design")),
                "sim_updates": sum(1 for t in summ["trace"] if t.get("sim_updated")),
                "rejected_updates": sum(1 for t in summ["trace"] if t.get("accepted") is False),
                "reward_hacking_events": hack, "rejected_good": rejected_good, "curve_selected": sel,
                "cad_steps": sum(t.get("cad_steps") or 0 for t in summ["trace"]),
                "cad_exhausted": sum(1 for t in summ["trace"] if t.get("cad_exhausted")),
                "sim_steps": sum(t.get("sim_steps") or 0 for t in summ["trace"]),
                "sim_exhausted": sum(1 for t in summ["trace"] if t.get("sim_exhausted")),
                "n_measured": sum(t.get("n_measured") or 0 for t in summ["trace"]),
                "n_unmeasured": sum(t.get("n_unmeasured") or 0 for t in summ["trace"]),
            })
            print(rows[-1]["level"], rows[-1]["problem"], rows[-1]["n_pass"], "/", rows[-1]["n_req"], rows[-1]["curve"], flush=True)
    (run_root / "results.json").write_text(json.dumps(rows, indent=1))
    return rows


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve())
