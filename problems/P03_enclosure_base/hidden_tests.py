def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    f, fr = H.filled(s, H.box(-38, -23, 0, 38, 23, 2), 0.95); out.append(("R2", f and abs(H.bbox(s).zmin) < 0.1, fr))
    e, v = H.empty(s, H.box(-40, -25, 8, 40, 25, 32)); out.append(("R3", e, v))
    bb = H.bbox(s)
    size_ok = 83.5 <= bb.xlen <= 86.5 and 53.5 <= bb.ylen <= 56.5 and 30 <= bb.zmax <= 32.5
    walls = [H.filled(s, H.box(-42.2, 10, 5, -40.8, 24, 28), 0.9)[0], H.filled(s, H.box(40.8, -20, 5, 42.2, 20, 28), 0.9)[0],
             H.filled(s, H.box(-30, -27.2, 5, 30, -25.8, 28), 0.9)[0], H.filled(s, H.box(-30, 25.8, 5, 30, 27.2, 28), 0.9)[0]]
    out.append(("R4", size_ok and all(walls), {"size": [round(bb.xlen,1), round(bb.ylen,1), round(bb.zmax,1)], "walls": walls}))
    res = []
    for x in (-35, 35):
        for y in (-20, 20):
            b, _ = H.filled(s, H.annulus((x, y, 2), (0, 0, 1), 1.6, 3.0, 6), 0.7)
            h, _ = H.empty(s, H.cyl((x, y, 4), (0, 0, 1), 0.9, 4), tol=0.3)
            res.append(b and h)
    out.append(("R5", all(res), res))
    e, v = H.empty(s, H.box(-43, -4.5, 12.5, -40.5, 4.5, 15.5), tol=0.3); out.append(("R6", e, v))
    m = H.mass_g(s, meta["density"]); out.append(("R7", m <= 70, round(m, 1)))
    return out
