"""Child process wrapper for model-written simulation scripts.

Usage (cwd = the isolated simrun folder):  python -I sim_runner.py sim.py
- Runs sim.py as __main__.
- Records every exception the script CATCHES (its per-check try/except) together with the line of sim.py where it was raised,
  so the agent gets compiler-like feedback ("line 138: min_y, max_y, ... = path2d.bounds -> ValueError ...") instead of only
  the exception text. Written to _handled.json next to the script.
"""
import json, linecache, runpy, sys
from pathlib import Path

script = str(Path(sys.argv[1]).resolve())
try:  # deterministic randomness: agent scripts that sample (e.g. trimesh mesh.sample) give the same numbers on every rerun
    import random as _random, numpy as _npr
    _random.seed(0); _npr.random.seed(0)
    _orig_rng = _npr.random.default_rng
    _npr.random.default_rng = lambda seed=None, *a, **k: _orig_rng(0 if seed is None else seed, *a, **k)
except Exception:
    pass

_REC = {}
if Path("part_body.xml").exists():  # physics-scenario mode: record what the agent's own MuJoCo simulation does (for the humans)
    try:
        import mujoco, numpy as _np
        _info = json.loads(Path("part_info.json").read_text())
        _ext = max(_np.array(_info["bbox_max_mm"]) - _np.array(_info["bbox_min_mm"])) * 1e-3
        _orig_step = mujoco.mj_step

        def _step(m, d, nstep=1):
            _orig_step(m, d, nstep)
            r = _REC.get(id(m))
            if r is None:
                if len(_REC) >= 8:
                    return
                cam = mujoco.MjvCamera(); cam.azimuth, cam.elevation = -125, -12
                pid = mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, "part")
                cam.lookat[:] = d.xpos[pid] if pid >= 0 else d.xpos[1:].mean(0)
                cam.distance = _ext * 3.2
                m.vis.headlight.ambient[:] = 0.45; m.vis.headlight.diffuse[:] = 0.6; m.vis.headlight.specular[:] = 0.2   # viewing only
                r = _REC[id(m)] = {"ren": mujoco.Renderer(m, 360, 480), "cam": cam, "n": 0, "frames": [], "dt": m.opt.timestep,
                                   "every": max(1, int(round(1 / (30 * m.opt.timestep))))}
            r["d"] = d
            if "start" not in r:   # independent motion log: where every free body starts and ends
                r["start"] = {}
                for b in range(1, m.nbody):
                    j = m.body_jntadr[b]
                    if j >= 0 and m.jnt_type[j] == mujoco.mjtJoint.mjJNT_FREE:
                        r["start"][mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_BODY, b) or f"body{b}"] = (b, d.xpos[b].copy(), d.xquat[b].copy())
                ov = {}
                for i in range(d.ncon):   # bodies interpenetrating at the start (deeper than 1 mm)
                    c = d.contact[i]
                    if c.dist < -0.001:
                        n1 = mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_BODY, m.geom_bodyid[c.geom1]) or "world"
                        n2 = mujoco.mj_id2name(m, mujoco.mjtObj.mjOBJ_BODY, m.geom_bodyid[c.geom2]) or "world"
                        k = "-".join(sorted((n1, n2)))
                        ov[k] = max(ov.get(k, 0.0), round(-c.dist * 1000, 1))
                r["overlap"] = ov
            r["n"] += nstep
            if r["n"] >= r["every"] * len(r["frames"]) and len(r["frames"]) < 300:
                r["ren"].update_scene(d, r["cam"]); r["frames"].append(r["ren"].render().copy())
        mujoco.mj_step = _step
    except Exception:
        pass


def _save_media():
    if not _REC:
        return
    from PIL import Image
    Path("media").mkdir(exist_ok=True)
    log = []
    for i, r in enumerate(_REC.values()):
        d, entry = r.get("d"), {"simulation": i + 1, "simulated_s": round(r["n"] * r.get("dt", 0), 2), "bodies": {}}
        for name, (b, p0, q0) in (r.get("start") or {}).items():
            dq = _np.zeros(3); mujoco.mju_subQuat(dq, d.xquat[b], q0)
            R0 = _np.zeros(9); mujoco.mju_quat2Mat(R0, q0); R0 = R0.reshape(3, 3)
            tilt0 = float(_np.degrees(_np.arccos(_np.clip(R0[2, 2], -1.0, 1.0))))   # angle of the body's local z from vertical
            entry["bodies"][name] = {"moved_mm": round(float(_np.linalg.norm(d.xpos[b] - p0)) * 1000, 1),
                                     "dropped_mm": round(float(p0[2] - d.xpos[b][2]) * 1000, 1),
                                     "rotated_deg": round(float(_np.degrees(_np.linalg.norm(dq))), 1),
                                     "placed_at_mm": [round(float(x) * 1000, 1) for x in p0],
                                     "placed_tilt_deg": round(tilt0, 1),
                                     "placed_axes": {"x": [round(float(x), 2) for x in R0[:, 0]], "z": [round(float(x), 2) for x in R0[:, 2]]}}
        entry["start_overlap_mm"] = r.get("overlap", {})
        entry["blew_up"] = any(v["moved_mm"] > 1000 for v in entry["bodies"].values())
        log.append(entry)
    Path("media/motion.json").write_text(json.dumps(log))
    for i, r in enumerate(_REC.values()):
        if len(r["frames"]) > 2:
            ims = [Image.fromarray(f).convert("P", palette=Image.ADAPTIVE, colors=96) for f in r["frames"]]
            ims[0].save(f"media/scenario_{i + 1}.gif", save_all=True, append_images=ims[1:], duration=33, loop=0)
handled = []


def _on_handled(code, offset, exc):
    if code.co_filename != script or len(handled) >= 50:
        return
    tb, line = exc.__traceback__, None
    while tb is not None:  # deepest frame that belongs to the agent's own script
        if tb.tb_frame.f_code.co_filename == script:
            line = tb.tb_lineno
        tb = tb.tb_next
    if line is not None:
        handled.append({"type": type(exc).__name__, "msg": str(exc)[:200], "line": line,
                        "src": linecache.getline(script, line).strip()[:160]})


try:
    mon = sys.monitoring
    TOOL = mon.DEBUGGER_ID
    mon.use_tool_id(TOOL, "designgrad")
    mon.register_callback(TOOL, mon.events.EXCEPTION_HANDLED, _on_handled)
    mon.set_events(TOOL, mon.events.EXCEPTION_HANDLED)
except Exception:  # older Python: run without line capture
    pass

try:
    runpy.run_path(script, run_name="__main__")
finally:
    try:
        Path("_handled.json").write_text(json.dumps(handled))
    except Exception:
        pass
    try:
        _save_media()
    except Exception:
        pass
