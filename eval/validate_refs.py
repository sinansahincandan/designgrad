"""Check every problem's hidden tests: the reference must pass all; a plain block must fail most."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "eval")); sys.path.insert(0, str(ROOT))
from designgrad.sandbox import run_cad
from hidden_eval import evaluate
for pd in sorted((ROOT / "problems").glob("P*")):
    if len(sys.argv) > 1 and not any(a in pd.name for a in sys.argv[1:]):
        continue
    meta = json.loads((pd / "meta.json").read_text())
    out = ROOT / "runs/_ref" / pd.name
    m = run_cad((pd / "reference.py").read_text(), out, meta["density"])
    if not m.get("ok"):
        print(pd.name, "REF FAIL", m.get("error", "")[-500:]); continue
    r = evaluate(pd, out / "part.step")
    fails = [(x["id"], x["value"]) for x in r["rows"] if not x["pass"]]
    mb = run_cad("import cadquery as cq\nresult = cq.Workplane().box(30, 20, 10)", ROOT / "runs/_ref" / (pd.name + "_block"), meta["density"])
    rb = evaluate(pd, ROOT / "runs/_ref" / (pd.name + "_block") / "part.step")
    print(f"{pd.name}: ref {r.get('n_pass')}/{r['n_req']} mass {m['mass_g']}g | block {rb.get('n_pass')}/{rb['n_req']} | FAILS {fails} {r.get('error','')}")
