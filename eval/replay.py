"""Record-replay check: would the CURRENT code reproduce a recorded run?

python eval/replay.py runs/v2_s0 [L2 P01 ...]  -> runs/_replay/<run>/report.json (+ printed summary)

Gemma is replaced by the recorded answers of that run (calls.jsonl, in order). The current loop code runs for real: it builds every
prompt, runs the CAD and simulation code in the sandbox, renders, scores and keeps/rejects. The check passes when
  - every prompt the current code sends (role, system prompt, user message(s), number of images) equals the recorded one, in order;
  - every round's design, code, CAD metrics, simulation report and the run summary (kept round, scores) equal the recorded ones.
Together with a deterministic model (same prompt + seed -> same answer; see --model-check) this means a rerun gives the same results.
"""
import json, os, shutil, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import designgrad.loop as loop  # noqa: E402

_REC = {}


class ReplayLLM:
    def __init__(self, log_path, cap=None):
        self.log_path = Path(log_path); self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.cap = cap; self.calls = 0; self.tokens_in = self.tokens_out = 0; self.seconds = 0.0
        self.rec = [c for c in _REC["calls"] if "output" in c]
        self.k = 0; self.mismatch = []

    def remaining(self):
        return None if self.cap is None else self.cap - self.calls

    def __call__(self, role, system, user="", images=None, max_tokens=4096, messages=None, step=None):
        if self.cap is not None and self.calls >= self.cap:
            raise loop.BudgetExceeded(role) if hasattr(loop, "BudgetExceeded") else RuntimeError("cap")
        if messages is None:
            sent_user, n_img = user, len(images or [])
        else:
            sent_user = messages[-1]["content"] if len(messages) == 1 else [m["content"] for m in messages]
            n_img = sum(len(m.get("images", [])) for m in messages)
        if self.k >= len(self.rec):
            self.mismatch.append({"call": self.k + 1, "what": "extra call not in the recording", "role": role})
            raise RuntimeError("replay: more calls than recorded")
        c = self.rec[self.k]
        diffs = [f for f, a, b in (("role", role, c["role"]), ("system", system, c["system"]), ("user", sent_user, c["user"]),
                                   ("n_images", n_img, c["n_images"])) if a != b]
        if diffs:
            self.mismatch.append({"call": self.k + 1, "role": role, "fields": diffs})
        self.k += 1; self.calls += 1
        self.tokens_in += c.get("tok_in", 0); self.tokens_out += c.get("tok_out", 0); self.seconds += c.get("t", 0)
        with self.log_path.open("a") as f:
            f.write(json.dumps({"i": self.calls, "role": role, "replayed": True, "diff": diffs}) + "\n")
        return c["output"]

    def stats(self):
        return {"calls": self.calls, "tokens_in": self.tokens_in, "tokens_out": self.tokens_out, "seconds": round(self.seconds, 1)}


def _load(p):
    try:
        return json.loads(Path(p).read_text())
    except Exception:
        return None


def _sim_core(js):
    r = (js or {}).get("result") or {}
    return {k: (v.get("status"), json.dumps(v.get("value"), sort_keys=True), v.get("faithful")) for k, v in r.items()} if isinstance(r, dict) else r


def replay_unit(run_root: Path, level: str, problem: str, out_root: Path):
    rec_dir = run_root / level / problem
    _REC["calls"] = [json.loads(l) for l in (rec_dir / "calls.jsonl").read_text().splitlines()]
    out_root.mkdir(parents=True, exist_ok=True)
    if level != "L0":
        (out_root / "L0").mkdir(exist_ok=True)
        link = out_root / "L0" / problem
        if not link.exists():
            link.symlink_to((run_root / "L0" / problem).resolve())
    loop.LLM = ReplayLLM
    t0 = time.time()
    err = None
    try:
        r = loop.Run(ROOT / "problems" / problem, level, out_root, rounds=4, repair_steps=5, ladder=os.environ.get("DG_LADDER", "v2"))
        r.run()
        llm = r.llm
    except Exception as e:
        err = repr(e)[:300]
        llm = None
    new_dir = out_root / level / problem
    rep = {"unit": f"{level}/{problem}", "seconds": round(time.time() - t0, 1), "error": err,
           "calls_recorded": sum("output" in c for c in _REC["calls"]), "calls_replayed": llm.k if llm else None,
           "prompt_mismatches": llm.mismatch[:5] if llm else None, "n_prompt_mismatches": len(llm.mismatch) if llm else None}
    s_old, s_new = _load(rec_dir / "summary.json"), _load(new_dir / "summary.json")
    if s_old and s_new:
        rep["summary_same"] = (s_old["k"] == s_new["k"] and abs(s_old["proxy"] - s_new["proxy"]) < 1e-9 and
                               [round(t.get("score", 0), 9) for t in s_old["trace"]] == [round(t.get("score", 0), 9) for t in s_new["trace"]] and
                               [t.get("accepted") for t in s_old["trace"]] == [t.get("accepted") for t in s_new["trace"]])
        rep["kept_round"] = [s_old["k"], s_new["k"]]
    diffs = []
    for rd in sorted(rec_dir.glob("r0*")):
        nd = new_dir / rd.name
        for f in ("d.md", "c.py", "s.py", "loss.md"):
            if (rd / f).exists() and (not (nd / f).exists() or (rd / f).read_text() != (nd / f).read_text()):
                diffs.append(f"{rd.name}/{f}")
        mo, mn = _load(rd / "metrics.json"), _load(nd / "metrics.json")
        if mo is not None and mo != mn:
            keys = [k for k in set(mo) | set(mn or {}) if (mo or {}).get(k) != (mn or {}).get(k)]
            diffs.append(f"{rd.name}/metrics.json:{','.join(sorted(keys))[:120]}")
        so, sn = _load(rd / "sim.json"), _load(nd / "sim.json")
        if so is not None and _sim_core(so) != _sim_core(sn):
            diffs.append(f"{rd.name}/sim.json")
    rep["artifact_diffs"] = diffs
    rep["identical"] = bool(not err and rep.get("n_prompt_mismatches") == 0 and rep.get("summary_same") and not diffs
                            and rep["calls_replayed"] == rep["calls_recorded"])
    return rep


def main(argv):
    run_root = (ROOT / argv[0]).resolve()
    levels = [a for a in argv[1:] if a.startswith("L")] or ["L0", "L1", "L2", "L3", "L4"]
    probs = [a for a in argv[1:] if a.startswith("P")]
    out_base = ROOT / "runs" / "_replay" / run_root.name
    shutil.rmtree(out_base, ignore_errors=True)
    reports = []
    for lv in levels:
        for ud in sorted((run_root / lv).glob("P*")):
            if probs and not any(p in ud.name for p in probs):
                continue
            rep = replay_unit(run_root, lv, ud.name, out_base)
            reports.append(rep)
            print(f"{rep['unit']:<32} identical={rep['identical']}  prompts {rep['calls_replayed']}/{rep['calls_recorded']} "
                  f"mismatch={rep['n_prompt_mismatches']}  summary_same={rep.get('summary_same')}  diffs={rep['artifact_diffs'][:4]}  "
                  f"err={rep['error']}  {rep['seconds']}s", flush=True)
    (out_base / "report.json").write_text(json.dumps(reports, indent=1))
    print(f"{sum(r['identical'] for r in reports)}/{len(reports)} units identical")


if __name__ == "__main__":
    main(sys.argv[1:])
