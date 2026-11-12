"""Deterministic geometry checks used ONLY by the hidden tests (never shown to the loop)."""
import math
import numpy as np
import cadquery as cq


def load(step_path):
    return cq.importers.importStep(str(step_path)).val()


def solids(shape):
    return shape.Solids()


def volume(shape):
    return sum(s.Volume() for s in shape.Solids())


def _inter_vol(shape, tool):
    try:
        r = shape.intersect(tool)
        return sum(s.Volume() for s in r.Solids())
    except Exception:
        return float("nan")


def box(x0, y0, z0, x1, y1, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, cq.Vector(x0, y0, z0))


def cyl(center, axis, r, h):
    """Cylinder of radius r, starting at `center`, length h along `axis`."""
    return cq.Solid.makeCylinder(r, h, cq.Vector(*center), cq.Vector(*axis))


def empty(shape, tool, tol=1.0):
    v = _inter_vol(shape, tool)
    return (v <= tol), round(v, 2)


def filled(shape, tool, frac):
    v = _inter_vol(shape, tool)
    tv = tool.Volume()
    return (v >= frac * tv), round(v / tv, 3)


def annulus(center, axis, r_in, r_out, h):
    return cyl(center, axis, r_out, h).cut(cyl(center, axis, r_in, h))


def hole_ok(shape, center, axis, d_nominal, depth, ring=2.0):
    """Hole of diameter d (±0.4) present: core empty, a ring of material around it."""
    core_empty, v = empty(shape, cyl(center, axis, d_nominal / 2 - 0.2, depth), tol=0.5)
    too_big, _ = empty(shape, annulus(center, axis, d_nominal / 2 + 0.4, d_nominal / 2 + 0.4 + ring, depth), tol=0.3)
    ring_ok, f = filled(shape, annulus(center, axis, d_nominal / 2 + 0.4, d_nominal / 2 + 0.4 + ring, depth), 0.6)
    return core_empty and ring_ok, {"core_material_mm3": v, "ring_fill": f}


def bbox(shape):
    return shape.BoundingBox()


def com(shape):
    c = cq.Shape.centerOfMass(cq.Compound.makeCompound(shape.Solids()))
    return np.array([c.x, c.y, c.z])


def support_polygon(shape, z_tol=0.3):
    """Convex hull (2D) of the part's contact with the plane z=zmin."""
    from scipy.spatial import ConvexHull
    import trimesh, tempfile, os
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "p.stl")
        cq.exporters.export(shape, p, tolerance=0.05, angularTolerance=0.2)
        m = trimesh.load(p)
    zmin = m.bounds[0][2]
    pts = m.vertices[m.vertices[:, 2] < zmin + z_tol][:, :2]
    if len(pts) < 3:
        return None
    return ConvexHull(pts)


def hull_margin(hull, xy):
    if hull is None:
        return -1e9
    eq = hull.equations
    return float(-(eq[:, :2] @ np.asarray(xy) + eq[:, 2]).max())


def section_props(shape, x0):
    """Section of the part by the plane x = x0. Returns area (mm2), centroid z, I_y (mm4, bending
    about the horizontal Y axis, i.e. vertical loads), and c = max |z - zc|."""
    import trimesh, tempfile, os
    with tempfile.TemporaryDirectory() as d:
        p = os.path.join(d, "p.stl")
        cq.exporters.export(shape, p, tolerance=0.02, angularTolerance=0.1)
        m = trimesh.load(p)
    sec = m.section(plane_origin=[x0, 0, 0], plane_normal=[1, 0, 0])
    if sec is None:
        return None
    planar, T = sec.to_planar(to_2D=None)
    polys = planar.polygons_full
    if not polys:
        return None
    A = Iz_sum = Iz2_sum = 0.0
    zs_all = []
    for poly in polys:
        rings = [(np.asarray(poly.exterior.coords), 1)] + [(np.asarray(r.coords), -1) for r in poly.interiors]
        for coords, sgn in rings:
            pts3 = trimesh.transform_points(np.c_[coords, np.zeros(len(coords))], T)
            y, z = pts3[:, 1], pts3[:, 2]
            zs_all.append(z)
            a = 0.5 * np.sum(y[:-1] * z[1:] - y[1:] * z[:-1])
            sz = np.sum((y[:-1] * z[1:] - y[1:] * z[:-1]) * (z[:-1] + z[1:])) / 6.0
            szz = np.sum((y[:-1] * z[1:] - y[1:] * z[:-1]) * (z[:-1] ** 2 + z[:-1] * z[1:] + z[1:] ** 2)) / 12.0
            o = sgn * (1.0 if a >= 0 else -1.0)
            A += o * a
            Iz_sum += o * sz
            Iz2_sum += o * szz
    if A <= 0:
        return None
    zc = Iz_sum / A
    I = Iz2_sum - A * zc ** 2
    zall = np.concatenate(zs_all)
    c = max(zall.max() - zc, zc - zall.min())
    return {"area": A, "zc": zc, "I": I, "c": c}


def cantilever(shape, x_sec, x_load, F, E):
    sp = section_props(shape, x_sec)
    if sp is None or sp["I"] <= 0:
        return None
    L = x_load - x_sec
    sigma = F * L * sp["c"] / sp["I"]
    delta = F * L ** 3 / (3 * E * sp["I"])
    return {"sigma_MPa": round(sigma, 2), "deflection_mm": round(delta, 3), "I_mm4": round(sp["I"], 1),
            "area_mm2": round(sp["area"], 1)}


def planar_faces_with_normal(shape, n, tol_deg=4.0):
    n = np.asarray(n, float); n /= np.linalg.norm(n)
    out = []
    for f in shape.Faces():
        if f.geomType() != "PLANE":
            continue
        v = f.normalAt()
        dn = np.array([v.x, v.y, v.z])
        if math.degrees(math.acos(np.clip(dn @ n, -1, 1))) <= tol_deg:
            out.append((f.Area(), f.Center()))
    return out


def single_valid(shape):
    n = len(shape.Solids())
    return (n == 1 and shape.isValid()), {"n_solids": n, "valid": bool(shape.isValid())}


def mass_g(shape, density):
    return volume(shape) * density / 1000.0


def stability(shape, density, extra_masses=()):
    """Combined CoM (part + point masses [(grams, xyz)]) inside the z-min support hull. Returns margin mm."""
    m0 = mass_g(shape, density)
    c = com(shape) * m0
    M = m0
    for g, p in extra_masses:
        c = c + g * np.asarray(p, float)
        M += g
    c = c / M
    return hull_margin(support_polygon(shape), c[:2]), c
