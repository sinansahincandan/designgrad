"""Tables and figures from results.json.  python eval/analyze.py runs/main [--split test]"""
import json, sys
from pathlib import Path
import numpy as np

LV = ["L0", "L1", "L2", "L3", "L4"]
NAMES = {"L0": "Single prompt", "L1": "+ TextGrad (text critic)", "L2": "+ CAD execution", "L3": "+ agent simulation", "L4": "+ render & gate (DesignGrad)"}


def boot_ci(x, n=10000, seed=0):
    x = np.asarray(x, float)
    if len(x) == 0:
        return (np.nan, np.nan)
    rng = np.random.default_rng(seed)
    m = rng.choice(x, (n, len(x))).mean(1)
    return float(np.percentile(m, 2.5)), float(np.percentile(m, 97.5))


def sign_test(d):
    from math import comb
    pos, neg = int((np.asarray(d) > 0).sum()), int((np.asarray(d) < 0).sum())
    n = pos + neg
    if n == 0:
        return 1.0
    k = min(pos, neg)
    return min(1.0, 2 * sum(comb(n, i) for i in range(k + 1)) / 2 ** n)


def main(root: Path, split="test"):
    rows = json.loads((root / "results.json").read_text())
    rows = [r for r in rows if split == "all" or r["split"] == split]
    probs = sorted({r["problem"] for r in rows})
    tab = {(r["level"], r["problem"]): r for r in rows}
    lv = [l for l in LV if any((l, p) in tab for p in probs)]
    out = [f"# Results ({split} split, n = {len(probs)} problem-seed units)\n",
           "| Level | Requirements met (mean) | 95% CI | All requirements met | Executes | Single solid | LLM calls | Tokens (in+out) | Wall time (min) |",
           "|---|---|---|---|---|---|---|---|---|"]
    for l in lv:
        rs = [tab[(l, p)] for p in probs if (l, p) in tab]
        pr = [r["pass_rate"] for r in rs]
        lo, hi = boot_ci(pr)
        out.append(f"| {l} {NAMES[l]} | {np.mean(pr):.3f} | [{lo:.2f}, {hi:.2f}] | {sum(r['all_pass'] for r in rs)}/{len(rs)} | "
                   f"{sum(r['executed'] for r in rs)}/{len(rs)} | {sum(r['single_solid'] for r in rs)}/{len(rs)} | {np.mean([r['calls'] for r in rs]):.1f} | "
                   f"{np.mean([r['tokens_in'] + r['tokens_out'] for r in rs]) / 1000:.0f}k | {np.mean([r['seconds'] for r in rs]) / 60:.1f} |")
    out += ["\n## What each added feature changed (paired by problem)\n",
            "| Step | Δ requirements met | 95% CI | wins / ties / losses | sign-test p | Cost per gain (extra tokens per +1 requirement) |", "|---|---|---|---|---|---|"]
    for a, b in zip(lv, lv[1:]):
        ps = [p for p in probs if (a, p) in tab and (b, p) in tab]
        d = np.array([tab[(b, p)]["pass_rate"] - tab[(a, p)]["pass_rate"] for p in ps])
        dn = np.array([tab[(b, p)]["n_pass"] - tab[(a, p)]["n_pass"] for p in ps])
        dt = np.array([(tab[(b, p)]["tokens_in"] + tab[(b, p)]["tokens_out"]) - (tab[(a, p)]["tokens_in"] + tab[(a, p)]["tokens_out"]) for p in ps])
        lo, hi = boot_ci(d)
        cpg = f"{dt.sum() / dn.sum() / 1000:.1f}k" if dn.sum() > 0 else "n/a (no gain)"
        out.append(f"| {a} → {b} | {d.mean():+.3f} | [{lo:+.2f}, {hi:+.2f}] | {(d > 0).sum()} / {(d == 0).sum()} / {(d < 0).sum()} | {sign_test(d):.3f} | {cpg} |")
    out += ["\n## Per problem: requirements met (n_pass / n_req)\n", "| Problem | " + " | ".join(lv) + " |", "|---|" + "---|" * len(lv)]
    for p in probs:
        out.append(f"| {p} | " + " | ".join(f"{tab[(l, p)]['n_pass']}/{tab[(l, p)]['n_req']}" if (l, p) in tab else "-" for l in lv) + " |")
    out += ["\n## Loop mechanics\n", "| Level | Rounds | Rejected updates | Sim rewrites | Gate: mismatch→c | Gate: systemic→d | Restarts from design | Reward-hacking events |", "|---|---|---|---|---|---|---|---|"]
    for l in lv:
        rs = [tab[(l, p)] for p in probs if (l, p) in tab]
        out.append(f"| {l} | {np.mean([r['rounds'] for r in rs]):.1f} | {sum(r['rejected_updates'] for r in rs)} | {sum(r['sim_updates'] for r in rs)} | "
                   f"{sum(r['gate_mismatch'] for r in rs)} | {sum(r['gate_systemic'] for r in rs)} | {sum(r['restarts'] for r in rs)} | {sum(r['reward_hacking_events'] for r in rs)} |")
    fails = {}
    for l in lv:
        for p in probs:
            if (l, p) in tab:
                for f in tab[(l, p)]["failed_reqs"]:
                    fails.setdefault(l, []).append(f"{p.split('_')[0]}:{f}")
    out += ["\n## Failed requirements by level\n"] + [f"- {l}: {', '.join(fails.get(l, [])) or 'none'}" for l in lv]
    (root / f"results_{split}.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))
    # figure: success by round
    try:
        import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
        fig, ax = plt.subplots(1, 2, figsize=(10, 3.6))
        cols = {"L0": "#888780", "L1": "#7F77DD", "L2": "#378ADD", "L3": "#1D9E75", "L4": "#D85A30"}
        means = [np.mean([tab[(l, p)]["pass_rate"] for p in probs if (l, p) in tab]) for l in lv]
        ax[0].bar(range(len(lv)), means, color=[cols[l] for l in lv]); ax[0].set_xticks(range(len(lv))); ax[0].set_xticklabels(lv)
        ax[0].set_ylim(0, 1); ax[0].set_ylabel("hidden requirements met"); ax[0].set_title("Final design")
        for l in lv[1:]:
            cs = [tab[(l, p)].get("curve_selected") or tab[(l, p)]["curve"] for p in probs if (l, p) in tab]
            L = max(len(c) for c in cs)
            m = [np.mean([c[min(i, len(c) - 1)] for c in cs]) for i in range(L)]
            ax[1].plot(range(L), m, marker="o", color=cols[l], label=l)
        ax[1].axhline(means[0], ls="--", color=cols["L0"], label="L0")
        ax[1].set_xticks(range(5)); ax[1].set_xlabel("round (design kept by keep-best, scored by hidden tests)")
        ax[1].set_ylim(0, 1); ax[1].legend(fontsize=8); ax[1].set_title("Success by round")
        fig.tight_layout(); fig.savefig(root / f"fig_results_{split}.png", dpi=150)
    except Exception as e:
        print("figure failed:", e)


if __name__ == "__main__":
    main(Path(sys.argv[1]), sys.argv[2] if len(sys.argv) > 2 else "test")
