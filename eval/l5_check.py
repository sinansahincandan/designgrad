"""Pre-registered L5 pilot criteria (PLAN_L5.md, step 1), checked from the run's records.

python eval/l5_check.py runs/l5_s0 [P02_phone_stand]
Needs hidden_rows.json in the round folders (eval/mechanics.py writes them).
1. scenario repair loops exhausted <= 15 %
2. every round: each object that is not the part is placed with a tilt that is not 0 deg when the spec tilts it
   (generic proxy: at least one non-part body placed with tilt > 5 deg in every simulation of every round)
3. no failed repair step whose only complaint is about a correct report (manual read: the feedback lines are printed)
4. every failed scenario has observation-based design_feedback (a number, no "if ... fail")
5. no scenario judged faithful AND pass while the harness motion log shows a non-part body moved > 10 mm or rotated > 10 deg
6. agent score vs hidden tests: pair agreement >= 0.8 over the run's rounds
"""
import itertools, json, re, sys
from pathlib import Path


def main(run, prob="P02_phone_stand"):
    d = Path(run) / "L5" / prob
    S = json.loads((d / "summary.json").read_text())
    loops = exh = 0
    tilt_ok = True
    fb_bad, contra, steps = [], [], []
    scores, hidden = [], []
    for t in S["trace"]:
        rd = d / f"r{t['k']:02d}"
        h = json.loads((rd / "hidden_rows.json").read_text()) if (rd / "hidden_rows.json").exists() else {}
        scores.append(t["score"]); hidden.append(sum(x is True for x in h.values()) / max(len(h), 1))
        if not (rd / "sim.json").exists():          # the part did not build: no scenarios this round
            steps.append(f"r{t['k']}: no simulation (part did not build)")
            continue
        A = json.loads((rd / "agent.json").read_text())
        loops += 1; exh += bool(A.get("sim_exhausted"))
        for h in A.get("sim_history", []):
            if not h["ok"]:
                steps.append(f"r{t['k']} step {h['step']}: {h['feedback'][:150]}".replace("\n", " | "))
        sim = json.loads((rd / "sim.json").read_text())
        mf = rd / "phys_media/motion.json"          # the harness log lives next to the recordings
        rep, mo = sim.get("result") or {}, sim.get("motion") or (json.loads(mf.read_text()) if mf.exists() else [])
        for e in mo:
            others = {n: b for n, b in e["bodies"].items() if n != "part"}
            if not others or not any(b.get("placed_tilt_deg", 0) > 5 for b in others.values()):
                tilt_ok = False                       # no non-part object in the model, or none placed tilted
        for k, v in rep.items():
            f = str(v.get("design_feedback") or "")
            if v.get("status") == "fail" and (not re.search(r"\d", f) or re.search(r"\bif\b[^.]{0,20}\bfail", f, re.I)):
                fb_bad.append(f"r{t['k']} {k}")
        for k, e in zip(rep, mo):
            v = rep[k]
            moved = [n for n, b in e["bodies"].items() if n != "part" and (b["moved_mm"] > 10 or b["rotated_deg"] > 10)]
            if v.get("status") == "pass" and v.get("faithful") is not False and moved:
                contra.append(f"r{t['k']} {k}")
    pairs = [(i, j) for i, j in itertools.combinations(range(len(scores)), 2) if hidden[i] != hidden[j] and scores[i] != scores[j]]
    agree = sum((scores[i] - scores[j]) * (hidden[i] - hidden[j]) > 0 for i, j in pairs) / len(pairs) if pairs else None
    res = {
        "1_exhausted_rate": (round(exh / loops, 2), exh / loops <= 0.15),
        "2_objects_tilted_as_placed": (tilt_ok, tilt_ok),
        "3_failed_steps_to_read": (len(steps), None),
        "4_feedback_observation_based": (fb_bad or "all", not fb_bad),
        "5_no_faithful_pass_contradicting_motion": (contra or "none", not contra),
        "6_score_hidden_pair_agreement": (None if agree is None else round(agree, 2), agree is None or agree >= 0.8),
    }
    for k, (v, ok) in res.items():
        print(f"{k:<44} {str(v):<40} {'PASS' if ok else ('READ' if ok is None else 'FAIL')}")
    print("\nfailed repair steps (criterion 3, read each):")
    for s in steps:
        print("  ", s)
    print("\nhidden per round:", [round(x, 2) for x in hidden], "kept round:", S["k"], "scores:", [round(x, 2) for x in scores])
    auto = all(ok for ok in [r[1] for r in res.values()] if ok is not None)
    print("\nAUTOMATIC CRITERIA:", "ALL PASS" if auto else "SOME FAIL")


if __name__ == "__main__":
    main(*sys.argv[1:])
