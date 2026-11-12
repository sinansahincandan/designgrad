"""Run model-written code (CAD or simulation) in a separate process with a timeout."""
import json, re, subprocess, sys
from pathlib import Path

PY = sys.executable
HERE = Path(__file__).resolve().parent


def run_cad(code: str, outdir: Path, density: float, timeout: int = 120) -> dict:
    outdir = Path(outdir).resolve()
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "design.py").write_text(code)
    for f in ("metrics.json", "part.stl", "part.step"):
        (outdir / f).unlink(missing_ok=True)
    try:
        p = subprocess.run([PY, "-I", str(HERE / "cad_runner.py"), str(outdir / "design.py"), str(outdir), str(density)],
                           capture_output=True, text=True, timeout=timeout, cwd=outdir)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Timed out after {timeout}s."}
    mp = outdir / "metrics.json"
    if not mp.exists():
        return {"ok": False, "error": (p.stderr or p.stdout)[-1500:] or "runner crashed"}
    return json.loads(mp.read_text())


PART_FILES = ("part.step", "part.stl", "metrics.json")
_WRITE_CALLS = re.compile(r"\.export\w*\s*\(|exporters\.export|\.save\s*\(|\.to_file\s*\(")
_LOADS = re.compile(r"""importStep\s*\(\s*['"]part\.step|trimesh\.load(_mesh)?\s*\(\s*['"]part\.stl|metrics\.json""")


_PHYS_LOADS = re.compile(r"add_part\s*\(")


def sim_static_issues(code: str, phys: bool = False) -> str | None:
    """Problem-independent contract checks done before running: the script must measure the existing part, never write geometry."""
    issues = []
    if phys:
        if _WRITE_CALLS.search(code):
            issues.append("The script exports/saves files. Only set up scenes with physkit, run them and print the JSON report.")
        if "part_body.xml" not in code:
            issues.append("The script never loads the built part (read part_body.xml and part_assets.xml and put them in your MJCF). "
                          "Every scenario must simulate the built part.")
        if not re.search(r"^\s*(import[^\n]*\bmujoco\b|from mujoco\b)", code, re.M):
            issues.append("The script does not import mujoco. Write the scenes and the simulation with the mujoco Python bindings.")
        if re.search(r"class\s+\w*(Mock|Fake)\w*|\bmock\b|\bfake\b", code, re.I):
            issues.append("The script defines mock/fake physics. Never invent the outcome: run the real MuJoCo simulation.")
        return " ".join(issues) or None
    if _WRITE_CALLS.search(code):
        issues.append("The script exports/saves geometry (an export/save call). The part is already built: load part.step or "
                      "part.stl and measure it; never export, rebuild or overwrite part files.")
    if not _LOADS.search(code):
        issues.append("The script never loads the built part (cq.importers.importStep('part.step'), trimesh.load('part.stl') or "
                      "metrics.json). Every check must measure the existing part, not a copy you build yourself.")
    return " ".join(issues) or None


PHYS_FILES = ("part_body.xml", "part_assets.xml", "part_info.json")


def _ensure_mjpart(workdir: Path, density: float) -> str | None:
    """MuJoCo fragments of the built part (collision boxes, mass, inertia, visual mesh), cached next to the part."""
    out = workdir / "part_body.xml"
    if out.exists() and out.stat().st_mtime >= (workdir / "part.stl").stat().st_mtime:
        return None
    try:
        from .mjpart import build
        build(workdir, density)
        return None
    except Exception as e:
        return f"could not convert the part for MuJoCo: {e}"


def run_sim(code: str, workdir: Path, timeout: int = 180, phys: bool = False, density: float | None = None) -> dict:
    """Simulation script reads part.step / part.stl / metrics.json in cwd and prints a JSON object last.
    It runs in a fresh sub-folder holding READ-ONLY COPIES of the part files, so it can never alter the built part,
    and under sim_runner.py, which records the sim.py line of every exception the script catches."""
    import hashlib, os, shutil, stat
    workdir = Path(workdir).resolve()
    (workdir / "sim.py").write_text(code)
    bad = sim_static_issues(code, phys)
    if bad:
        return {"ok": False, "error": bad}
    if phys:
        err = _ensure_mjpart(workdir, density or 1.24)
        if err:
            return {"ok": False, "error": err}
    simdir = workdir / "simrun"
    if simdir.exists():
        for f in simdir.rglob("*"):
            f.chmod(stat.S_IRWXU if f.is_dir() else stat.S_IWUSR | stat.S_IRUSR)
        shutil.rmtree(simdir)
    simdir.mkdir()
    digest = {}
    for f in PART_FILES:
        if (workdir / f).exists():
            shutil.copy2(workdir / f, simdir / f)
            os.chmod(simdir / f, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            digest[f] = hashlib.sha256((simdir / f).read_bytes()).hexdigest()
    if phys:
        for f in PHYS_FILES:
            shutil.copy2(workdir / f, simdir / f)
            os.chmod(simdir / f, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
            digest[f] = hashlib.sha256((simdir / f).read_bytes()).hexdigest()
    (simdir / "sim.py").write_text(code)
    try:
        p = subprocess.run([PY, "-I", "-B", str(HERE / "sim_runner.py"), "sim.py"], capture_output=True, text=True,
                           timeout=timeout, cwd=simdir)
    except subprocess.TimeoutExpired:
        return {"ok": False, "error": f"Simulation timed out after {timeout}s."}
    changed = [f for f, h in digest.items() if not (simdir / f).exists()
               or hashlib.sha256((simdir / f).read_bytes()).hexdigest() != h]
    if changed:
        return {"ok": False, "error": f"The script modified or deleted {', '.join(changed)}. The part files are read-only: "
                                      "load and measure them, never write them."}
    motion = None
    if phys and (simdir / "media").exists():
        md = workdir / "phys_media"
        shutil.rmtree(md, ignore_errors=True)
        shutil.copytree(simdir / "media", md)
        try:
            motion = json.loads((md / "motion.json").read_text())
        except Exception:
            motion = None
    out = p.stdout.strip()
    if p.returncode != 0:
        tb = [l for l in p.stderr.strip().splitlines() if "frozen runpy" not in l and "sim_runner.py" not in l
              and "runpy.run_path" not in l]
        return {"ok": False, "error": (tb or ["?"])[-8:], "stdout": out[-800:]}
    try:
        handled = json.loads((simdir / "_handled.json").read_text())
    except Exception:
        handled = []
    from .llm import extract_json
    js = extract_json(out.splitlines()[-1] if out else "") or extract_json(out)
    if isinstance(js, dict):
        js = normalise_report(js, handled)
    return {"ok": isinstance(js, dict), "result": js, "stdout": out[-1500:], "stderr": p.stderr[-800:], **({"motion": motion} if motion else {}),
            **({} if isinstance(js, dict) else {"error": "Simulation did not print a JSON object on its last line."})}


_ERR_HINTS = ("Error", "error", "Exception", "not defined", "has no attribute", "ambiguous", "unsupported", "argument",
              "object is not", "index out of", "division by zero", "NaN", "nan")


def _where(note: str, handled: list) -> str:
    """Find the sim.py line where the exception quoted in `note` was raised (recorded by sim_runner)."""
    for h in handled:
        if h["msg"] and (h["msg"][:60] in note or note.strip() in h["msg"]):
            return f"line {h['line']}: {h['src']}  ->  {h['type']}"
    return ""


def normalise_report(js: dict, handled: list | None = None) -> dict:
    """Three-state per-requirement report. A check that crashed is `error`, never `fail`.
    Accepts the legacy {"pass": bool} form and the new {"status": pass|fail|error} form."""
    handled = handled or []
    out = {}
    for rid, v in js.items():
        if not isinstance(v, dict):
            out[rid] = {"status": "error", "value": None, "note": f"malformed entry: {str(v)[:80]}", "method": ""}
            continue
        st = str(v.get("status", "")).lower().strip()
        if st not in ("pass", "fail", "error"):
            st = "pass" if v.get("pass") is True else ("fail" if v.get("pass") is False else "error")
        note = str(v.get("note", ""))
        if st == "fail" and v.get("value") is None and any(h in note for h in _ERR_HINTS):
            st = "error"  # a crash reported as a failure
        out[rid] = {"status": st, "value": v.get("value"), "note": note[:300], "method": str(v.get("method", ""))[:300]}
        for k in ("scenario", "observation", "design_feedback"):
            if v.get(k):
                out[rid][k] = str(v[k])[:400]
        if isinstance(v.get("requirements"), list):
            out[rid]["requirements"] = [str(x) for x in v["requirements"]][:8]
        crit = v.get("criteria")
        if isinstance(crit, list):
            out[rid]["criteria"] = [{k: (str(c.get(k))[:120] if k == "condition" else c.get(k)) for k in ("condition", "measured", "ok")}
                                    for c in crit[:8] if isinstance(c, dict)]
        if st == "error":
            w = _where(note, handled)
            if w:
                out[rid]["where"] = w[:250]
    return out


def fmt_motion(simr):
    """The harness's own measurements of every simulation the scenario script ran (placement, motion, overlaps, blow-ups)."""
    mo = (simr or {}).get("motion") or []
    lines = []
    for e in mo:
        parts = [f"{n}: placed at {tuple(v.get('placed_at_mm', []))} mm, its local z axis tilted {v.get('placed_tilt_deg', '?')} deg from vertical "
                 f"(local x along {tuple(v.get('placed_axes', {}).get('x', []))}, local z along {tuple(v.get('placed_axes', {}).get('z', []))}); "
                 f"then moved {v['moved_mm']} mm, dropped {v['dropped_mm']} mm, rotated {v['rotated_deg']} deg" for n, v in e["bodies"].items()]
        extra = ""
        ov = {k: v for k, v in (e.get("start_overlap_mm") or {}).items() if "world" not in k}
        if ov:
            extra += " | AT THE START bodies interpenetrate: " + ", ".join(f"{k} by {v} mm" for k, v in ov.items()) + \
                     " (an object at its specified place overlapping the part = the part intrudes into its space)"
        if e.get("blew_up"):
            extra += " | the simulation blew up (bodies flew off), so its outcome is meaningless"
        lines.append(f"- simulation {e['simulation']} ({e.get('simulated_s', '?')} s): " + "; ".join(parts) + extra)
    return "\n".join(lines) or "(no motion log)"


def _contradictions(result: dict) -> list[str]:
    """Scenario verdicts checked against the harness's own measurements (one MuJoCo model per scenario, in order)."""
    rep, mo = result.get("result") or {}, result.get("motion") or []
    keys = list(rep)
    out = []
    if mo and len(mo) != len(keys):
        out.append(f"the report has {len(keys)} scenarios but the script built {len(mo)} MuJoCo models: build exactly ONE model per "
                   "scenario, in the same order (S1 = first model, ...), so each scenario's outcome can be checked")
        return out
    for k, e in zip(keys, mo):
        v = rep[k]
        ov = {n: d for n, d in (e.get("start_overlap_mm") or {}).items() if "world" not in n and d > 1.0}
        if ov and v["status"] != "fail":
            out.append(f"{k}: at the start {', '.join(f'{n} interpenetrate by {d} mm' for n, d in ov.items())}. An object at its specified "
                       "place overlapping the part means the part intrudes into its space: report this scenario as a design FAIL with the "
                       "depth and the intruding feature (or, if your placement is wrong, place the object where the specification says)")
        moved = {n: b for n, b in e["bodies"].items() if n != "part" and (b["moved_mm"] > 10 or b["rotated_deg"] > 10)}
        if v["status"] == "pass" and moved and not ov:
            out.append(f"{k}: reported PASS, but the harness measured " + "; ".join(f"{n} moved {b['moved_mm']} mm and rotated "
                       f"{b['rotated_deg']} deg" for n, b in moved.items()) + ". A scenario passes only if the objects stay where they "
                       "belong (start them 0.5-1 mm from their support so settling moves them only a little)")
        if e.get("blew_up") and v["status"] != "error":
            out.append(f"{k}: the simulation blew up (bodies flew off); fix the scene (overlaps, units, forces) before judging")
    return out


def phys_feedback(result: dict, min_scenarios: int = 3) -> str | None:
    """None when at least `min_scenarios` scenarios ran and each ended pass/fail; otherwise what is wrong."""
    if not result.get("ok"):
        err = result.get("error")
        err = "\n".join(err) if isinstance(err, list) else str(err)
        return "The script failed to run:\n" + err[-1500:] + ("\n\nstdout tail:\n" + result["stdout"][-500:] if result.get("stdout") else "")
    rep = result["result"]
    errs = [f"{k}: {v['note'] or 'error, no note'}" + (f"\n    raised at {v['where']}" if v.get("where") else "")
            for k, v in rep.items() if v["status"] == "error"]
    def _weak(t):
        t = str(t or "").strip()
        return not t or not re.search(r"\d", t) or re.search(r"\bif\b[^.]{0,20}\bfail", t, re.I)
    nofb = [k for k, v in rep.items() if v["status"] == "fail" and _weak(v.get("design_feedback"))]
    msg = ""
    con = _contradictions(result)
    if con:
        msg += "The harness's own measurements contradict or invalidate these scenarios:\n- " + "\n- ".join(con) + "\n"
    if nofb:
        msg += ("These scenarios failed but their design_feedback is missing, generic or written before the run: " + ", ".join(nofb) +
                ". Build design_feedback in your code AFTER the simulation from the measured values (f-string with the numbers): what "
                "moved and how far, which feature of the part causes it, and one concrete change with numbers. No 'If failed ...' text. "
                "If the failure comes from your scenario code, fix the code instead.\n")
    if len(rep) < min_scenarios:
        msg += f"The report has {len(rep)} scenario(s); write at least {min_scenarios} realistic scenarios.\n"
    if errs:
        msg += "These scenarios raised an error instead of running (status 'error'):\n- " + "\n- ".join(errs) + "\n"
    if msg and result.get("motion"):
        far = [f"{n} at {tuple(b.get('placed_at_mm', []))} mm" for e in result["motion"] for n, b in e["bodies"].items()
               if any(abs(x) > 2000 for x in b.get("placed_at_mm", []))]
        msg += "\nThe harness measured your simulations (positions in mm, as MuJoCo saw them):\n" + fmt_motion(result) + "\n"
        if far:
            msg += ("Some bodies start metres away from the part (" + "; ".join(sorted(set(far)))[:300] + "): MuJoCo positions and sizes "
                    "are in METRES, so a value in mm put there is 1000 times too large. Divide mm by 1000.\n")
    return (msg + "Every scenario must run and end with a judged outcome (status pass or fail) and failures must explain themselves.") if msg else None


def report_feedback(result: dict, req_ids: list[str]) -> str | None:
    """None when every requirement has a measured pass/fail; otherwise what is missing, for the agent loop."""
    if not result.get("ok"):
        err = result.get("error")
        err = "\n".join(err) if isinstance(err, list) else str(err)
        return "The script failed to run:\n" + err[-1500:] + ("\n\nstdout tail:\n" + result["stdout"][-500:] if result.get("stdout") else "")
    rep = result["result"]
    missing = [r for r in req_ids if r not in rep]
    errs = [f"{r}: {rep[r]['note'] or 'error, no note'}" + (f"\n    raised at {rep[r]['where']}" if rep[r].get("where") else "")
            for r in req_ids if r in rep and rep[r]["status"] == "error"]
    if not missing and not errs:
        return None
    msg = ""
    if missing:
        msg += "These requirements have no entry in the report: " + ", ".join(missing) + "\n"
    if errs:
        msg += "These checks raised an error instead of measuring (status 'error'):\n- " + "\n- ".join(errs) + "\n"
    return msg + "Every requirement must end with a real measurement (status pass or fail)."
