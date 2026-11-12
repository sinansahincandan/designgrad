def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    bb = H.bbox(s); cx, cy = (bb.xmin + bb.xmax) / 2, (bb.ymin + bb.ymax) / 2
    out.append(("R2", 39.5 <= bb.xlen <= 40.5 and 39.5 <= bb.ylen <= 40.5 and abs(cx) < 0.5 and abs(cy) < 0.5 and abs(bb.zmin) < 0.1 and bb.zmax <= 25.1, [round(bb.xlen,2), round(bb.ylen,2), round(bb.zmax,2)]))
    f, fr = H.filled(s, H.box(-19.5, -19.5, 0, 19.5, 19.5, 3), 0.95); out.append(("R3", f, fr))
    A = sum(x.Area() for x in s.Solids()) * 1e-6
    R = 1 / (10 * A * 0.85) if A > 0 else 1e9; out.append(("R4", R <= 9, round(R, 2)))
    r = []
    for x in (-15, 15):
        h, _ = H.hole_ok(s, (x, 0, 0), (0, 0, 1), 3.2, 3)
        e, _ = H.empty(s, H.cyl((x, 0, 3.05), (0, 0, 1), 3.0, 25), tol=0.5)
        r.append(h and e)
    out.append(("R5", all(r), r))
    m = H.mass_g(s, meta["density"]); out.append(("R6", m <= 45, round(m, 1)))
    return out
