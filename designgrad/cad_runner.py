"""Child process: exec model-written CadQuery code, export STEP/STL, write metrics.json.

Usage: python cad_runner.py <code.py> <outdir> <density_g_cm3>
The code must assign the final part to a variable named `result`
(cq.Workplane, cq.Shape or cq.Assembly-free compound).
"""
import json, sys, traceback
from pathlib import Path

code_path, outdir, density = Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3])
outdir.mkdir(parents=True, exist_ok=True)
metrics = {"ok": False}
try:
    import cadquery as cq
    ns = {"__name__": "__designgrad__"}
    exec(compile(code_path.read_text(), "design.py", "exec"), ns)
    if "result" not in ns:
        raise RuntimeError("The code did not define a variable named `result`.")
    res = ns["result"]
    if isinstance(res, cq.Workplane):
        objs = [o for o in res.vals() if isinstance(o, cq.Shape)]
        if not objs:
            raise RuntimeError("`result` Workplane contains no solid.")
        shape = cq.Compound.makeCompound(objs) if len(objs) > 1 else objs[0]
    elif isinstance(res, cq.Shape):
        shape = res
    else:
        raise RuntimeError(f"`result` has unsupported type {type(res).__name__}.")
    solids = shape.Solids()
    if not solids:
        raise RuntimeError("`result` contains no solid body (only wires/faces?).")
    vol = sum(s.Volume() for s in solids)
    if vol <= 1e-6:
        raise RuntimeError("Solid has zero volume.")
    bb = shape.BoundingBox()
    com = cq.Shape.centerOfMass(cq.Compound.makeCompound(solids))
    holes = []
    for f in shape.Faces():
        if f.geomType() == "CYLINDER":
            try:
                cyl = f._geomAdaptor().Cylinder()
                ax = cyl.Axis().Direction()
                c = f.Center()
                holes.append({"r": round(cyl.Radius(), 3), "axis": [round(ax.X(), 3), round(ax.Y(), 3), round(ax.Z(), 3)],
                              "center": [round(c.x, 2), round(c.y, 2), round(c.z, 2)]})
            except Exception:
                pass
    cq.exporters.export(shape, str(outdir / "part.step"))
    cq.exporters.export(shape, str(outdir / "part.stl"), tolerance=0.05, angularTolerance=0.2)
    metrics.update({
        "ok": True,
        "n_solids": len(solids),
        "valid": bool(shape.isValid()),
        "bbox_min": [round(bb.xmin, 2), round(bb.ymin, 2), round(bb.zmin, 2)],
        "bbox_max": [round(bb.xmax, 2), round(bb.ymax, 2), round(bb.zmax, 2)],
        "size_mm": [round(bb.xlen, 2), round(bb.ylen, 2), round(bb.zlen, 2)],
        "volume_mm3": round(vol, 1),
        "mass_g": round(vol * density / 1000.0, 2),
        "center_of_mass": [round(com.x, 2), round(com.y, 2), round(com.z, 2)],
        "surface_area_mm2": round(sum(s.Area() for s in solids), 1),
        "cylindrical_faces": holes[:40],
        "n_cylindrical_faces": len(holes),
    })
    if len(solids) > 1:  # tell the agent WHICH pieces are separate, like a compiler pointing at a line
        def _sb(s):
            b = s.BoundingBox()
            return {"volume_mm3": round(s.Volume(), 1), "bbox_min": [round(b.xmin, 2), round(b.ymin, 2), round(b.zmin, 2)],
                    "bbox_max": [round(b.xmax, 2), round(b.ymax, 2), round(b.zmax, 2)]}
        metrics["solids"] = [_sb(s) for s in sorted(solids, key=lambda s: -s.Volume())[:8]]
    # resting stability on the lowest plane (gravity -Z)
    try:
        import numpy as np, trimesh
        from scipy.spatial import ConvexHull
        m = trimesh.load(outdir / "part.stl")
        v = m.vertices
        base = v[v[:, 2] < bb.zmin + 0.3][:, :2]
        cx, cy = com.x, com.y
        if len(base) >= 3:
            hull = ConvexHull(base)
            eq = hull.equations  # a x + b y + c <= 0 inside
            margin = float(-(eq[:, :2] @ np.array([cx, cy]) + eq[:, 2]).max())
            metrics["rest_stable"] = margin > 0
            metrics["rest_stability_margin_mm"] = round(margin, 2)
        else:
            metrics["rest_stable"] = False
            metrics["rest_stability_margin_mm"] = None
    except Exception as e:
        metrics["stability_error"] = str(e)[:200]
except Exception:
    tb = [l for l in traceback.format_exc().strip().splitlines()
          if "cad_runner.py" not in l and "exec(compile(code_path" not in l]
    metrics["error"] = "\n".join(tb[-10:])
(outdir / "metrics.json").write_text(json.dumps(metrics, indent=1))
