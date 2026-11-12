"""Record SHA-256 of every problem spec, hidden test, check library and prompt file (run before the main run)."""
import hashlib, json, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
files = sorted([*ROOT.glob("problems/P*/*.md"), *ROOT.glob("problems/P*/hidden_tests.py"), *ROOT.glob("problems/P*/meta.json"),
                ROOT / "eval/checks.py", ROOT / "eval/hidden_eval.py", *ROOT.glob("designgrad/*.py")])
h = {str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
out = ROOT / "FROZEN.json"
if len(sys.argv) > 1 and sys.argv[1] == "--check":
    if len(sys.argv) > 2:                      # python eval/freeze.py --check FROZEN_v7.json
        out = ROOT / sys.argv[2]
    old = json.loads(out.read_text())["sha256"]
    bad = [k for k in old if h.get(k) != old[k]]
    print("OK, nothing changed" if not bad else f"CHANGED: {bad}")
else:
    out.write_text(json.dumps({"frozen_at": time.strftime("%Y-%m-%d %H:%M:%S"), "sha256": h}, indent=1))
    print(f"froze {len(h)} files")
