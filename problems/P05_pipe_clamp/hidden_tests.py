def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    bb = H.bbox(s)
    out.append(("R2", abs(bb.zmin) < 0.1 and 18 <= bb.ylen <= 22 and bb.xlen <= 80.1, [round(bb.xlen,1), round(bb.ylen,1)]))
    e, v = H.empty(s, H.cyl((0, -20, 12.5), (0, 1, 0), 12.6, 40)); out.append(("R3", e, v))
    cap = H.annulus((0, -8, 12.5), (0, 1, 0), 12.7, 15.5, 16).intersect(H.box(-7, -8, 20, 7, 8, 30))
    f, fr = H.filled(s, cap, 0.6); out.append(("R4", f, fr))
    r = [H.hole_ok(s, (x, 0, 0), (0, 0, 1), 6.6, 3)[0] for x in (-27, 27)]; out.append(("R5", all(r), r))
    r = [H.filled(s, H.box(a, -4, 0, b, 4, 3), 0.9)[0] for a, b in ((18.5, 23), (-23, -18.5))]; out.append(("R6", all(r), r))
    m = H.mass_g(s, meta["density"]); out.append(("R7", m <= 25, round(m, 1)))
    return out
