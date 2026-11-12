"""Loop mechanics against the hidden tests (outside the loop).

python eval/mechanics.py runs/main [test|all]
-> runs/main/mechanics.json, runs/main/mechanics_{split}.md

Per level:
  * selection: hidden pass rate of the candidate keep-best kept vs the best candidate the loop ever produced (oracle)
  * score-truth agreement: pairwise agreement between the agent-visible score and the hidden pass rate across candidates of a run
  * simulation verdicts (L3, L4): agent-written s says pass/fail per requirement vs the hidden test of the same requirement
"""
import itertools, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "eval"))
from hidden_eval import evaluate


def _sim_verdict(v):
    """True/False when the agent simulation produced a usable verdict, else None.
    v2 reports: status pass|fail and not judged unfaithful. v1 reports: a bare pass flag."""
    if not isinstance(v, dict):
        return None
    if "status" in v:
        if v["status"] not in ("pass", "fail") or v.get("faithful") is False:
            return None
        return v["status"] == "pass"
    if "pass" in v:
        return bool(v["pass"])
    return None


def hidden_rows(pd, rd):
    """Hidden-test rows of one round folder (uses the part the loop built, or the evaluator's rebuild)."""
    cache = rd / "hidden_rows.json"
    if cache.exists():
        return json.loads(cache.read_text())
    step = rd / "part.step"
    alt = rd.parent / f"eval_{rd.name}" / "part.step"
    m = rd / "metrics.json"
    ok = m.exists() and json.loads(m.read_text()).get("ok")
    if not ok and alt.exists():
        step, ok = alt, True
    rows = {}
    if ok and step.exists():
        r = evaluate(pd, step)
        rows = {x["id"]: bool(x["pass"]) for x in r.get("rows", [])}
    cache.write_text(json.dumps(rows))
    return rows


def main(root: Path, split="test"):
    out = {}
    for lv in ["L1", "L2", "L3", "L4", "L5"]:
        agg = {"runs": 0, "selected": [], "oracle": [], "first": [], "pairs": 0, "agree": 0,
               "sim_pp": 0, "sim_pf": 0, "sim_fp": 0, "sim_ff": 0}
        for rd in sorted((root / lv).glob("P*")):
            pd = ROOT / "problems" / rd.name.split("@")[0]
            meta = json.loads((pd / "meta.json").read_text())
            if split != "all" and meta.get("split") != split:
                continue
            summ = json.loads((rd / "summary.json").read_text())
            n_req = sum(1 for l in (pd / "spec.md").read_text().splitlines() if l.strip().startswith("- R"))
            scored = {t["k"]: t["score"] for t in summ["trace"] if "score" in t}
            hid = {}
            for k in scored:
                r = rd / f"r{k:02d}"
                rows = hidden_rows(pd, r)
                hid[k] = sum(rows.values()) / n_req
                sim = r / "sim.json"
                if lv in ("L3", "L4") and sim.exists() and rows:
                    sj = json.loads(sim.read_text())
                    res = sj.get("result") if isinstance(sj, dict) and sj.get("ok") else None
                    if isinstance(res, dict):
                        for rid, hv in rows.items():
                            v = res.get(rid)
                            sv = _sim_verdict(v)
                            if sv is not None:
                                agg["sim_" + ("p" if sv else "f") + ("p" if hv else "f")] += 1
            agg["runs"] += 1
            agg["selected"].append(hid.get(summ["k"], 0.0))
            agg["oracle"].append(max(hid.values()) if hid else 0.0)
            agg["first"].append(hid.get(0, 0.0))
            for a, b in itertools.combinations(scored, 2):
                if abs(hid[a] - hid[b]) < 1e-9:
                    continue
                agg["pairs"] += 1
                agg["agree"] += (scored[a] - scored[b]) * (hid[a] - hid[b]) > 0
        n = max(agg["runs"], 1)
        sim_n = agg["sim_pp"] + agg["sim_pf"] + agg["sim_fp"] + agg["sim_ff"]
        out[lv] = {
            "runs": agg["runs"],
            "selected_mean": sum(agg["selected"]) / n, "oracle_mean": sum(agg["oracle"]) / n,
            "score_hidden_pair_agreement": agg["agree"] / agg["pairs"] if agg["pairs"] else None, "pairs": agg["pairs"],
            "sim_checks": sim_n,
            "sim_says_pass_hidden_fails": agg["sim_pf"], "sim_says_pass_hidden_passes": agg["sim_pp"],
            "sim_says_fail_hidden_passes": agg["sim_fp"], "sim_says_fail_hidden_fails": agg["sim_ff"],
            "sim_accuracy": (agg["sim_pp"] + agg["sim_ff"]) / sim_n if sim_n else None,
            "sim_false_pass_rate": agg["sim_pf"] / (agg["sim_pf"] + agg["sim_ff"]) if (agg["sim_pf"] + agg["sim_ff"]) else None,
        }
        print(lv, json.dumps(out[lv]), flush=True)
    (root / f"mechanics_{split}.json").write_text(json.dumps(out, indent=1))
    f = lambda x: "n/a" if x is None else f"{x:.2f}"
    md = [f"# Loop mechanics vs hidden tests ({split})", "",
          "| Level | Kept by keep-best | Best ever produced (oracle) | Score/hidden pair agreement | Sim checks | Sim accuracy | Sim false-pass rate |",
          "|---|---|---|---|---|---|---|"]
    for lv, o in out.items():
        md.append(f"| {lv} | {f(o['selected_mean'])} | {f(o['oracle_mean'])} | {f(o['score_hidden_pair_agreement'])} ({o['pairs']} pairs) | "
                  f"{o['sim_checks']} | {f(o['sim_accuracy'])} | {f(o['sim_false_pass_rate'])} |")
    md += ["", "Sim false-pass rate = P(agent simulation says pass | hidden test fails), per requirement-round."]
    (root / f"mechanics_{split}.md").write_text("\n".join(md) + "\n")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), sys.argv[2] if len(sys.argv) > 2 else "test")
