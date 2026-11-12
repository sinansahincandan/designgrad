def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    bb = H.bbox(s)
    ok = bb.xmin > -0.1 and bb.xmin < 0.1 and bb.xmax <= 170.1 and bb.ymin >= -20.1 and bb.ymax <= 20.1 and bb.zmin >= -0.1 and bb.zmax <= 130.1
    out.append(("R2", ok, [round(bb.xmin,2), round(bb.xmax,2), round(bb.ymin,2), round(bb.ymax,2), round(bb.zmin,2), round(bb.zmax,2)]))
    res = []
    for z in (20, 60):
        h, info = H.hole_ok(s, (0, 0, z), (1, 0, 0), 5.5, 3)
        acc, v = H.empty(s, H.cyl((10, 0, z), (1, 0, 0), 4, 160))
        res.append(h and acc); info["access_material_mm3"] = v
    out.append(("R3", all(res), res))
    f, fr = H.filled(s, H.box(140, -5, 107, 150, 5, 110), 0.9)
    e, v = H.empty(s, H.box(8, -20, 110.3, 170, 20, 131))
    out.append(("R4", f and e, {"support_fill": fr, "above_mm3": v}))
    c = H.cantilever(s, 10, 150, 150, meta["E"])
    out.append(("R5", c is not None and c["sigma_MPa"] <= 20, c))
    out.append(("R6", c is not None and c["deflection_mm"] <= 2.0, c))
    m = H.mass_g(s, meta["density"]); out.append(("R7", m <= 90, round(m, 1)))
    return out
