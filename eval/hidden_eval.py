"""Run a problem's frozen hidden tests on a STEP file (in a child process).

Usage (child): python hidden_eval.py <problem_dir> <step_path>  -> prints JSON
"""
import importlib.util, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _child(problem_dir: Path, step: Path):
    sys.path.insert(0, str(HERE))
    import checks as H
    meta = json.loads((problem_dir / "meta.json").read_text())
    spec = importlib.util.spec_from_file_location("hidden_tests", problem_dir / "hidden_tests.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    shape = H.load(step)
    rows = []
    for rid, ok, val in mod.run(shape, H, meta):
        rows.append({"id": rid, "pass": bool(ok), "value": json.loads(json.dumps(val, default=lambda o: float(o) if hasattr(o, "__float__") else str(o)))})
    print(json.dumps(rows))


def evaluate(problem_dir, step, timeout=300) -> dict:
    """Returns {'ran': bool, 'rows': [...], 'pass_rate': float, 'n_req': int}."""
    problem_dir, step = Path(problem_dir), Path(step)
    n_req = sum(1 for l in (problem_dir / "spec.md").read_text().splitlines() if l.strip().startswith("- R"))
    if not step.exists():
        return {"ran": False, "rows": [], "pass_rate": 0.0, "n_req": n_req, "n_pass": 0}
    try:
        p = subprocess.run([sys.executable, "-I", str(HERE / "hidden_eval.py"), str(problem_dir), str(step)],
                           capture_output=True, text=True, timeout=timeout)
        rows = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception as e:
        err = (p.stderr[-600:] if 'p' in locals() else str(e))
        return {"ran": False, "rows": [], "pass_rate": 0.0, "n_req": n_req, "n_pass": 0, "error": err}
    n_pass = sum(r["pass"] for r in rows)
    return {"ran": True, "rows": rows, "n_req": n_req, "n_pass": n_pass, "pass_rate": n_pass / n_req}


if __name__ == "__main__":
    _child(Path(sys.argv[1]), Path(sys.argv[2]))
