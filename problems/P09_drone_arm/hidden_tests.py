def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    bb = H.bbox(s)
    out.append(("R2", abs(bb.xmin) < 0.1 and bb.xmax <= 136.1 and bb.ymin >= -16.1 and bb.ymax <= 16.1 and abs(bb.zmin) < 0.1 and bb.zmax <= 20.1, [round(bb.xmax,1), round(bb.ymin,1), round(bb.ymax,1), round(bb.zmax,1)]))
    r = [H.hole_ok(s, (6, y, 0), (0, 0, 1), 3.2, 3)[0] for y in (-6, 6)]; out.append(("R3", all(r), r))
    r = [H.hole_ok(s, (120 + dx, y, 0), (0, 0, 1), 3.2, 3)[0] for dx in (-8, 8) for y in (-9.5, 9.5)]
    e, v = H.empty(s, H.cyl((120, 0, -1), (0, 0, 1), 2.8, 25), tol=0.5); out.append(("R4", all(r) and e, {"holes": r, "shaft_mm3": v}))
    c = H.cantilever(s, 20, 120, 12, meta["E"])
    out.append(("R5", c is not None and c["sigma_MPa"] <= 30, c)); out.append(("R6", c is not None and c["deflection_mm"] <= 1.0, c))
    m = H.mass_g(s, meta["density"]); out.append(("R7", m <= 20, round(m, 1)))
    return out
