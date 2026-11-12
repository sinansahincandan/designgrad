def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    bb = H.bbox(s)
    f, fr = H.filled(s, H.box(0, -8, -5, 2, 8, 45), 0.9); out.append(("R2", f and abs(bb.xmin) < 0.1, fr))
    r = [H.hole_ok(s, (0, 0, z), (1, 0, 0), 4.5, 4)[0] for z in (0, 40)]; out.append(("R3", all(r), r))
    f, fr = H.filled(s, H.box(34, -4, -17, 46, 4, -14), 0.8); e, v = H.empty(s, H.box(35, -6, -13, 45, 6, -6))
    out.append(("R4", f and e, {"bed": fr, "strap_space_mm3": v}))
    f, fr = H.filled(s, H.box(47, -4, -13, 52, 4, -8), 0.7); out.append(("R5", f, fr))
    c = H.cantilever(s, 8, 40, 50, meta["E"])
    out.append(("R6", c is not None and c["sigma_MPa"] <= 25 and c["deflection_mm"] <= 1.5, c))
    m = H.mass_g(s, meta["density"]); out.append(("R7", m <= 25 and bb.xlen <= 55.1, {"mass": round(m, 1), "xlen": round(bb.xlen, 1)}))
    return out
