"""Analysis of the paper's ladder (v4: L0-L3, every level builds its code), outside the loop, with the frozen independent tests.

python eval/v4_analyze.py runs/v4_s0 runs/v4_s1000 runs/v4_s2000 [--out runs/v4_all]   -> <out>/v4_summary.json + v4_summary.md
python eval/v4_analyze.py runs/v4pilot --out runs/v4pilot                               (one folder works too)

For every unit (problem x seed) and level it scores every round's built part with the independent tests (cached in hidden_rows.json),
then reports: requirements met by the final design, paired steps with bootstrap intervals, cost, agreement of the agent's own analysis
with the tests, how often a round fixes an unmet requirement or breaks a met one, what the loop kept, and how often a render complaint
names a requirement that is in fact met."""
import json, re, sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "eval"))
from mechanics import hidden_rows, _sim_verdict

LV = ["L0", "L1", "L2", "L3"]


def boot(x, n=10000):
    x = np.asarray(x, float); m = np.random.default_rng(0).choice(x, (n, len(x))).mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def load(runs):
    U = {}
    for run in runs:
        seed = re.search(r"s(\d+)$", run.name); seed = f"s{seed.group(1)}" if seed else run.name
        for lv in LV:
            for rd in sorted((run / lv).glob("P*")):
                if not (rd / "summary.json").exists():
                    continue
                pd = ROOT / "problems" / rd.name
                S = json.loads((rd / "summary.json").read_text())
                rounds = {}
                for t in S["trace"]:
                    r = rd / f"r{t['k']:02d}"
                    rows = hidden_rows(pd, r)
                    sim = json.loads((r / "sim.json").read_text()) if (r / "sim.json").exists() else {}
                    rounds[t["k"]] = {"rows": rows, "met": sum(v is True for v in rows.values()), "score": t.get("score"), "accepted": t.get("accepted"),
                                      "from": t.get("from"), "sim": (sim.get("result") or {}) if sim.get("ok") else {}, "gate": t.get("gate"),
                                      "exhausted": [bool(t.get("cad_exhausted")), bool(t.get("sim_exhausted"))], "has_sim": t.get("n_measured") is not None,
                                      "control": [x.get("control_pass") for x in (t.get("review") or []) if "control_pass" in x],
                                      "unfaithful": [x.get("unfaithful") for x in (t.get("review") or [])]}
                U[(lv, rd.name, seed)] = {"dir": rd, "kept": S["k"], "rounds": rounds, "calls": S["llm"]["calls"], "seconds": S["llm"].get("seconds", 0),
                                          "n_req": sum(1 for l in (pd / "spec.md").read_text().splitlines() if l.strip().startswith("- R"))}
    return U


def main(runs, out):
    U = load(runs)
    units = sorted({(p, s) for (_, p, s) in U})
    R = {"units": [f"{p}@{s}" for p, s in units], "levels": {}, "steps": {}, "per_unit": {}}
    final = {}
    for lv in LV:
        ks = [(lv, p, s) for p, s in units if (lv, p, s) in U]
        if not ks:
            continue
        met = [U[k]["rounds"][U[k]["kept"]]["met"] for k in ks]
        final[lv] = {(p, s): U[(lv, p, s)]["rounds"][U[(lv, p, s)]["kept"]]["met"] for (_, p, s) in ks}
        best = [max(r["met"] for r in U[k]["rounds"].values()) for k in ks]
        frac = [m / U[k]["n_req"] for m, k in zip(met, ks)]
        byp = {}
        for m, k in zip(met, ks):
            byp.setdefault(k[1], []).append(m)
        d = {"n": len(ks), "met_frac": float(np.mean(frac)), "by_problem": {p_: [float(np.mean(v)), len(v)] for p_, v in byp.items()},
             "met": float(np.mean(met)), "met_ci": boot(met), "all_met": int(sum(m == U[k]["n_req"] for m, k in zip(met, ks))),
             "best_produced": float(np.mean(best)), "calls": float(np.mean([U[k]["calls"] for k in ks])),
             "minutes": float(np.mean([U[k]["seconds"] for k in ks]) / 60),
             "curve_kept": None}
        # the design the loop holds after each round
        if lv != "L0":
            cur = []
            for k in ks:
                held, c = U[k]["rounds"][0]["met"], []
                for kk in sorted(U[k]["rounds"]):
                    r = U[k]["rounds"][kk]
                    if kk == 0 or r["accepted"]:
                        held = r["met"]
                    c.append(held)
                cur.append(c)
            L = max(len(c) for c in cur)                      # a loop that stopped early (nothing left to improve) keeps holding its design
            cur = [c + [c[-1]] * (L - len(c)) for c in cur]
            d["curve_kept"] = [float(np.mean([c[i] for c in cur])) for i in range(L)]
        # agent loops that ran out of steps
        ex = [e for k in ks for r in U[k]["rounds"].values() for e in r["exhausted"][: (2 if lv in ("L2", "L3") else 1)]]
        d["agent_loops"] = len(ex); d["exhausted"] = int(sum(ex))
        # own analysis vs tests
        if lv in ("L2", "L3"):
            agree = tot = flagged = unmet = 0
            for k in ks:
                for r in U[k]["rounds"].values():
                    for rid, hv in r["rows"].items():
                        sv = _sim_verdict(r["sim"].get(rid))
                        if sv is not None:
                            tot += 1; agree += (sv == bool(hv))
                        if not hv:
                            unmet += 1; flagged += (sv is False)
            d.update({"analysis_checks": tot, "analysis_agreement": agree / tot if tot else None, "unmet_flagged": [flagged, unmet]})
            # entry by entry: faithful verdicts against the tests; disputed (reviewer) and unmeasured entries counted apart
            c = {"agree": 0, "false_alarm": 0, "missed": 0, "disputed": 0, "unmeasured": 0, "unmet": 0, "unmet_reported": 0}
            for k in ks:
                for r in U[k]["rounds"].values():
                    for rid, hv in r["rows"].items():
                        e = r["sim"].get(rid) or {}
                        c["unmet"] += (not hv)
                        if e.get("status") not in ("pass", "fail"):
                            c["unmeasured"] += 1; continue
                        if e.get("faithful") is False:
                            c["disputed"] += 1; c["unmet_reported"] += ((not hv) and e["status"] == "fail"); continue
                        ok = e["status"] == "pass"
                        c["agree"] += (ok == bool(hv)); c["false_alarm"] += (bool(hv) and not ok); c["missed"] += ((not hv) and ok)
                        c["unmet_reported"] += ((not hv) and not ok)
            d["analysis_counts"] = c
        # one round: unmet -> met (fix), met -> unmet (break); improved candidates kept or lost
        if lv != "L0":
            fix = [0, 0]; brk = [0, 0]; better = kept_better = 0; acc = rej = 0
            for k in ks:
                for kk, r in U[k]["rounds"].items():
                    if kk == 0 or r["from"] is None:
                        continue
                    p = U[k]["rounds"][r["from"]]
                    acc += bool(r["accepted"]); rej += not r["accepted"]
                    for rid, hv in p["rows"].items():
                        now = r["rows"].get(rid, False)
                        if hv:
                            brk[1] += 1; brk[0] += (not now)
                        else:
                            fix[1] += 1; fix[0] += bool(now)
                    if r["met"] > p["met"]:
                        better += 1; kept_better += bool(r["accepted"])
            d.update({"fix": fix, "break": brk, "rounds_accepted": acc, "rounds_rejected": rej, "improved_candidates": better, "improved_kept": kept_better})
        if lv == "L3":
            named = wrong = 0
            for k in ks:
                for r in U[k]["rounds"].values():
                    g = r["gate"] or {}
                    for txt in (g.get("mismatches") or []) + (g.get("systemic") or []):
                        ids = set(re.findall(r"\bR\d+\b", str(txt)))
                        if ids:
                            named += 1; wrong += all(r["rows"].get(i) is True for i in ids)
            d["render_complaints_naming_a_requirement"] = named; d["render_complaints_about_met_requirements"] = wrong
        R["levels"][lv] = d
    for a, b in [("L0", "L1"), ("L1", "L2"), ("L2", "L3"), ("L0", "L2"), ("L0", "L3")]:
        if a in final and b in final:
            dd = [final[b][u] - final[a][u] for u in units if u in final[a] and u in final[b]]
            R["steps"][f"{a}->{b}"] = {"mean": float(np.mean(dd)), "ci": boot(dd), "wtl": [int(sum(x > 0 for x in dd)), int(sum(x == 0 for x in dd)), int(sum(x < 0 for x in dd))]}
    for p, s in units:
        R["per_unit"][f"{p}@{s}"] = {lv: final[lv].get((p, s)) for lv in final}
    out.mkdir(parents=True, exist_ok=True)
    (out / "v4_summary.json").write_text(json.dumps(R, indent=1))
    md = ["# Ladder v4: requirements met (independent tests)", "", "| Level | n | Met (of 7) | 95% CI | All met | Best produced | Calls | Min | Loops exhausted |", "|---|---|---|---|---|---|---|---|---|"]
    for lv, d in R["levels"].items():
        md.append(f"| {lv} | {d['n']} | {d['met']:.2f} | [{d['met_ci'][0]:.2f}, {d['met_ci'][1]:.2f}] | {d['all_met']} | {d['best_produced']:.2f} | {d['calls']:.0f} | "
                  f"{d['minutes']:.1f} | {d['exhausted']}/{d['agent_loops']} |")
    md += ["", "| Step | Mean | 95% CI | W/T/L |", "|---|---|---|---|"]
    for k, v in R["steps"].items():
        md.append(f"| {k} | {v['mean']:+.2f} | [{v['ci'][0]:+.2f}, {v['ci'][1]:+.2f}] | {v['wtl'][0]}/{v['wtl'][1]}/{v['wtl'][2]} |")
    md += ["", "| Level | Fix (unmet -> met) | Break (met -> unmet) | Rounds kept/rejected | Improved candidates kept | Curve (kept design) |", "|---|---|---|---|---|---|"]
    for lv, d in R["levels"].items():
        if lv != "L0":
            md.append(f"| {lv} | {d['fix'][0]}/{d['fix'][1]} | {d['break'][0]}/{d['break'][1]} | {d['rounds_accepted']}/{d['rounds_rejected']} | "
                      f"{d['improved_kept']}/{d['improved_candidates']} | {[round(x, 2) for x in d['curve_kept']]} |")
    for lv in ("L2", "L3"):
        d = R["levels"].get(lv)
        if d and d.get("analysis_checks"):
            md.append(f"\n{lv}: own analysis agrees with the tests in {d['analysis_agreement']:.3f} of {d['analysis_checks']} checks; "
                      f"of {d['unmet_flagged'][1]} unmet requirement-rounds it had flagged {d['unmet_flagged'][0]}.")
    for lv in ("L2", "L3"):
        c = (R["levels"].get(lv) or {}).get("analysis_counts")
        if c:
            md.append(f"\n{lv} analysis entries: agree {c['agree']}, false alarm {c['false_alarm']}, missed {c['missed']}, disputed {c['disputed']}, "
                      f"unmeasured {c['unmeasured']}; unmet requirement-rounds {c['unmet']}, reported as not met {c['unmet_reported']}.")
    d = R["levels"].get("L3")
    if d:
        md.append(f"\nL3: {d['render_complaints_naming_a_requirement']} render complaints name a requirement; "
                  f"{d['render_complaints_about_met_requirements']} of them are about requirements that are met.")
    md += ["", "| Unit | " + " | ".join(final) + " |", "|---|" + "---|" * len(final)]
    for u, v in R["per_unit"].items():
        md.append(f"| {u} | " + " | ".join(str(v[lv]) for lv in final) + " |")
    (out / "v4_summary.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    args = sys.argv[1:]
    out = Path(args[args.index("--out") + 1]) if "--out" in args else None
    runs = [Path(a).resolve() for a in args if not a.startswith("--") and (out is None or Path(a) != out or args.count(a) > 1)]
    if "--out" in args:
        i = args.index("--out"); runs = [Path(a).resolve() for j, a in enumerate(args) if j not in (i, i + 1)]
    main(runs, (out or runs[0].parent / "v4_all").resolve())
