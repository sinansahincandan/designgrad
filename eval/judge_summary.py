"""Unblind the judge's scores and summarise by level.

python eval/judge_summary.py runs/main runs/_keys/main_blind_key.json
-> runs/main/judge_summary.md, runs/main/judge_summary.json
"""
import json, sys
from pathlib import Path

import numpy as np
from scipy.stats import spearmanr

KEYS = ["soundness", "manufacturability", "fidelity", "novelty", "overall"]
LV = ["L0", "L1", "L2", "L3", "L4"]


def main(root: Path, keyfile: Path):
    key = json.loads(keyfile.read_text())
    res = {(r["level"], r["problem"]): r for r in json.loads((root / "results.json").read_text())}
    J = {}
    for f in sorted((root / "judgments").glob("judge_*.jsonl")):
        for line in f.read_text().splitlines():
            line = line.strip()
            if line.startswith("{"):
                j = json.loads(line)
                J[j["item"]] = j
    rows = []
    for iid, k in key.items():
        if iid in J:
            rows.append({**k, **{x: J[iid][x] for x in KEYS}, "hidden": res[(k["level"], k["problem"])]["pass_rate"]})
    md = [f"# Blind judge (Claude, {len(rows)} items)", "", "| Level | " + " | ".join(KEYS) + " |", "|---" * (len(KEYS) + 1) + "|"]
    summ = {}
    for lv in LV:
        rr = [r for r in rows if r["level"] == lv]
        summ[lv] = {x: float(np.mean([r[x] for r in rr])) for x in KEYS}
        md.append(f"| {lv} | " + " | ".join(f"{summ[lv][x]:.2f}" for x in KEYS) + " |")
    md += ["", "| Step | overall: wins / ties / losses |", "|---|---|"]
    by = {(r["level"], r["problem"]): r for r in rows}
    probs = sorted({r["problem"] for r in rows})
    pairs = {}
    for a, b in zip(LV, LV[1:]):
        w = t = l = 0
        for p in probs:
            if (a, p) in by and (b, p) in by:
                d = by[(b, p)]["overall"] - by[(a, p)]["overall"]
                w += d > 0; t += d == 0; l += d < 0
        pairs[f"{a}->{b}"] = [w, t, l]
        md.append(f"| {a} → {b} | {w} / {t} / {l} |")
    rho, p = spearmanr([r["overall"] for r in rows], [r["hidden"] for r in rows])
    md += ["", f"Spearman(judge overall, hidden pass rate) = {rho:.2f} (p = {p:.3g}, n = {len(rows)})"]
    (root / "judge_summary.md").write_text("\n".join(md) + "\n")
    (root / "judge_summary.json").write_text(json.dumps({"levels": summ, "pairs": pairs, "spearman": [rho, p], "n": len(rows)}, indent=1))
    print("\n".join(md))


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve())
