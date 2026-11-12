def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    f, fr = H.filled(s, H.annulus((0, 0, 30), (0, 1, 0), 11.7, 13.5, 4), 0.9); out.append(("R2", f, fr))
    h, i = H.hole_ok(s, (0, 0, 30), (0, 1, 0), 22.5, 4); out.append(("R3", h, i))
    r = [H.hole_ok(s, (x, 0, z), (0, 1, 0), 3.4, 4)[0] for x in (-15.5, 15.5) for z in (14.5, 45.5)]; out.append(("R4", all(r), r))
    e, v = H.empty(s, H.box(-21.5, -48, 8.5, 21.5, 0, 51.5)); out.append(("R5", e, v))
    bb = H.bbox(s)
    r = [H.hole_ok(s, (x, 25, 0), (0, 0, 1), 5.5, 3)[0] for x in (-25, 25)]; out.append(("R6", all(r) and abs(bb.zmin) < 0.1, r))
    m = H.mass_g(s, meta["density"])
    out.append(("R7", bb.xmin >= -35.1 and bb.xmax <= 35.1 and bb.zmax <= 55.1 and m <= 60, {"mass": round(m, 1), "x": [round(bb.xmin,1), round(bb.xmax,1)], "zmax": round(bb.zmax,1)}))
    return out
