"""Build blinded judge packages from a finished run.

python eval/blind_pack.py runs/main [--split test]
-> runs/main/blind/<item_id>/{spec.md, code.py, views.png (if it builds), facts.json}
-> runs/main/blind_key.json  (item_id -> level, problem)   <- never shown to the judge
Code comments are stripped (they can reveal iteration history). Item ids are random.
"""
import io, json, random, shutil, sys, tokenize
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from designgrad.render import render


def strip_comments(src: str) -> str:
    out, prev = [], None
    try:
        for tok in tokenize.generate_tokens(io.StringIO(src).readline):
            if tok.type == tokenize.COMMENT:
                continue
            out.append(tok)
        code = tokenize.untokenize(out)
    except Exception:
        code = "\n".join(l.split("#")[0].rstrip() for l in src.splitlines())
    return "\n".join(l for l in code.splitlines() if l.strip()) + "\n"


def main(root: Path, split="test", seed=7):
    rows = json.loads((root / "results.json").read_text())
    rows = [r for r in rows if split == "all" or r["split"] == split]
    rng = random.Random(seed)
    bd = root / "blind"
    if bd.exists():
        shutil.rmtree(bd)
    bd.mkdir()
    key = {}
    ids = rng.sample(range(1000, 9999), len(rows))
    for r, i in zip(rows, ids):
        iid = f"D{i}"
        src = root / r["level"] / r["problem"]
        d = bd / iid
        d.mkdir()
        (d / "spec.md").write_text((ROOT / "problems" / r["problem"].split("@")[0] / "spec.md").read_text())
        (d / "code.py").write_text(strip_comments((src / "final_c.py").read_text()))
        stl = src / "eval_final" / "part.stl"
        if stl.exists():
            render(stl, d / "views.png")
        m = src / "eval_final" / "metrics.json"
        facts = {"builds": r["executed"]}
        if m.exists():
            mm = json.loads(m.read_text())
            facts.update({k: mm.get(k) for k in ("n_solids", "size_mm", "mass_g") if k in mm})
            if not mm.get("ok"):
                facts["error"] = str(mm.get("error", ""))[-300:]
        (d / "facts.json").write_text(json.dumps(facts, indent=1))
        key[iid] = {"level": r["level"], "problem": r["problem"]}
    (root / "blind_key.json").write_text(json.dumps(key, indent=1))
    print(f"{len(key)} blinded items in {bd}")


if __name__ == "__main__":
    main(Path(sys.argv[1]).resolve(), sys.argv[2] if len(sys.argv) > 2 else "test")
