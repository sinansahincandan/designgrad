"""Loop validation against pre-registered thresholds. Run on the pilot problems before any long run.

python eval/loopcheck.py runs/v2pilot      -> runs/v2pilot/loopcheck.md  (exit code 1 if any criterion fails)

Requires eval/evaluate_runs.py and eval/mechanics.py to have been run on the same folder (it runs them if missing).
"""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "eval"))

THRESH = {
    "rounds_with_built_part": (">=", 0.90),
    "sim_measured_share": (">=", 0.85),
    "sim_false_fail_rate": ("<=", 0.10),
    "sim_hidden_agreement": (">=", 0.85),
    "review_fix_rate": (">=", 0.70),
    "score_hidden_pair_agreement": (">=", 0.80),
    "repair_exhausted_rate": ("<=", 0.15),
    "gate_code_error_as_systemic": ("<=", 0),
}


def main(root: Path, split="all"):
    if not (root / "results.json").exists():
        subprocess.run([sys.executable, str(ROOT / "eval/evaluate_runs.py"), str(root)], check=True)
    if not (root / f"mechanics_{split}.json").exists():
        subprocess.run([sys.executable, str(ROOT / "eval/mechanics.py"), str(root), split], check=True)
    rows = json.loads((root / "results.json").read_text())
    mech = json.loads((root / f"mechanics_{split}.json").read_text())
    traces = []
    for r in rows:
        if r["level"] == "L0":
            continue
        summ = json.loads((root / r["level"] / r["problem"] / "summary.json").read_text())
        for t in summ["trace"]:
            traces.append((r["level"], r["problem"], t))
    built = 0; n_rounds = 0; exh = 0; n_rep = 0; measured = 0; total_req = 0
    rev_flagged = 0; rev_fixed = 0; systemic_code_errors = 0
    for lv, p, t in traces:
        rd = root / lv / p / f"r{t['k']:02d}"
        if lv in ("L2", "L3", "L4"):
            n_rounds += 1
            m = rd / "metrics.json"
            built += bool(m.exists() and json.loads(m.read_text()).get("ok") and json.loads(m.read_text()).get("n_solids") == 1)
            if t.get("cad_steps") is not None:
                n_rep += 1; exh += bool(t.get("cad_exhausted"))
        if lv in ("L3", "L4") and t.get("n_measured") is not None:
            measured += t["n_measured"]; total_req += t["n_measured"] + (t.get("n_unmeasured") or 0)
            if t.get("sim_steps") is not None:
                n_rep += 1; exh += bool(t.get("sim_exhausted"))
            rev = t.get("review") or []
            if rev:
                first = len(rev[0]["unfaithful"]); last = len(rev[-1]["unfaithful"])
                rev_flagged += first; rev_fixed += max(first - last, 0) if len(rev) > 1 else 0
        if lv == "L4" and t.get("gate"):
            # a code error (several solids / failed build) counted as systemic -> restart from design
            m = rd / "metrics.json"
            mm = json.loads(m.read_text()) if m.exists() else {}
            if t["gate"]["systemic"] and (not mm.get("ok") or mm.get("n_solids", 1) != 1):
                systemic_code_errors += 1
    sim_levels = [mech[l] for l in ("L3", "L4") if l in mech and mech[l]["runs"]]
    def wsum(key): return sum(m[key] for m in sim_levels)
    pf, ff = wsum("sim_says_pass_hidden_fails"), wsum("sim_says_fail_hidden_fails")
    pp, fp = wsum("sim_says_pass_hidden_passes"), wsum("sim_says_fail_hidden_passes")
    n_checks = pf + ff + pp + fp
    pairs = sum(mech[l]["pairs"] for l in mech if l != "L1"); agree = sum((mech[l]["score_hidden_pair_agreement"] or 0) * mech[l]["pairs"] for l in mech if l != "L1")
    vals = {
        "rounds_with_built_part": built / n_rounds if n_rounds else None,
        "sim_measured_share": measured / total_req if total_req else None,
        "sim_false_fail_rate": fp / (fp + pp) if (fp + pp) else None,
        "sim_hidden_agreement": (pp + ff) / n_checks if n_checks else None,
        "review_fix_rate": rev_fixed / rev_flagged if rev_flagged else None,
        "score_hidden_pair_agreement": agree / pairs if pairs else None,
        "repair_exhausted_rate": exh / n_rep if n_rep else None,
        "gate_code_error_as_systemic": systemic_code_errors,
    }
    notes = {"sim_false_fail_rate": f"{fp} of {fp + pp} hidden-passing checks", "sim_hidden_agreement": f"{n_checks} measured checks",
             "review_fix_rate": f"{rev_fixed} of {rev_flagged} flagged", "rounds_with_built_part": f"{built}/{n_rounds}",
             "sim_measured_share": f"{measured}/{total_req}", "repair_exhausted_rate": f"{exh}/{n_rep} agent loops",
             "score_hidden_pair_agreement": f"{pairs} pairs (L2-L4)"}
    md = [f"# Loop check: {root.name}", "", "| Criterion | Value | Threshold | Result |", "|---|---|---|---|"]
    ok_all = True
    for k, (op, th) in THRESH.items():
        v = vals[k]
        if v is None:
            res, ok = "n/a (no data)", True
        else:
            ok = v >= th if op == ">=" else v <= th
            res = "PASS" if ok else "FAIL"
        ok_all &= ok
        vs = f"{v:.2f}" if isinstance(v, float) else str(v)
        md.append(f"| {k} | {vs} ({notes.get(k, '')}) | {op} {th} | {res} |")
    md += ["", "ALL PASS" if ok_all else "SOME CRITERIA FAIL - inspect sim.json / agent.json / gate.json before any long run."]
    (root / "loopcheck.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))
    return ok_all


if __name__ == "__main__":
    ok = main(Path(sys.argv[1]).resolve(), sys.argv[2] if len(sys.argv) > 2 else "all")
    sys.exit(0 if ok else 1)
