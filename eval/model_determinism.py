"""Does Gemma (Ollama, same model, temperature 0.3, same seed) give the same answer to the same prompt as in the recorded run?

python eval/model_determinism.py runs/v2_s0 [n_per_role] -> prints identical / different per resent call
Resends recorded calls exactly (system prompt, messages, seed = DG_SEED + call index - 1, the role's max_tokens) and compares the
answers character by character. Calls with images are skipped (the render is re-created, not stored byte-identical)."""
import json, random, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAXTOK = {"designer": 6000, "designer_regen": 6000, "update": 6000, "cad_agent": 6000, "sim_agent": 6000}
SEEDS = {"v2_s0": 0, "v2_s1000": 1000, "v2_s2000": 2000}


def resend(c, seed):
    msgs = [{"role": "user", "content": c["user"]}] if isinstance(c["user"], str) else \
        [{"role": "user" if i % 2 == 0 else "assistant", "content": t} for i, t in enumerate(c["user"])]
    body = {"model": "gemma4:26b", "stream": False, "think": False,
            "messages": [{"role": "system", "content": c["system"]}] + msgs,
            "options": {"temperature": 0.3, "seed": seed + c["i"] - 1, "num_ctx": 24576, "num_predict": MAXTOK.get(c["role"], 4096)}}
    req = urllib.request.Request("http://localhost:11434/api/chat", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=1800))["message"]["content"]


def main(run, n=2):
    seed = SEEDS[Path(run).name]
    calls = [json.loads(l) | {"_f": str(f)} for f in sorted((ROOT / run).glob("L*/*/calls.jsonl")) for l in f.read_text().splitlines()]
    calls = [c for c in calls if "output" in c and not c.get("n_images")]
    by = {}
    for c in calls:
        by.setdefault(c["role"], []).append(c)
    rng = random.Random(1)
    same = tot = 0
    for role, cs in sorted(by.items()):
        for c in rng.sample(cs, min(n, len(cs))):
            out = resend(c, seed)
            ok = out == c["output"]
            same += ok; tot += 1
            print(f"{role:<14} {Path(c['_f']).parent.parent.name}/{Path(c['_f']).parent.name} call {c['i']:>3}: "
                  f"{'IDENTICAL' if ok else 'DIFFERENT'} ({len(out)} vs {len(c['output'])} chars)", flush=True)
    print(f"{same}/{tot} resent calls gave the identical answer")


if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 2)
