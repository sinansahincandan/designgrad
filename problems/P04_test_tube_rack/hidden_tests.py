import math
XS = (-44, -22, 0, 22, 44); YS = (-12.5, 12.5)
def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    bb = H.bbox(s)
    out.append(("R2", bb.xlen <= 140.1 and bb.ylen <= 80.1 and 58 <= bb.zmax <= 62 and abs(bb.zmin) < 0.1, [round(bb.xlen,1), round(bb.ylen,1), round(bb.zmax,1)]))
    top = bb.zmax; r3 = []; r4 = []
    for x in XS:
        for y in YS:
            e, _ = H.empty(s, H.cyl((x, y, 10), (0, 0, 1), 8.3, max(top - 10, 1)), tol=1.0)
            ring, _ = H.filled(s, H.annulus((x, y, top - 3), (0, 0, 1), 9.0, 10.2, 3), 0.6)
            r3.append(e and ring)
            f, _ = H.filled(s, H.cyl((x, y, 0), (0, 0, 1), 4, 3), 0.8); r4.append(f)
    out.append(("R3", all(r3), r3)); out.append(("R4", all(r4), r4))
    mg, c = H.stability(s, meta["density"], [(20, (x, y, 55)) for x in XS for y in YS])
    ang = math.degrees(math.atan2(mg, c[2])) if mg > 0 else -1
    out.append(("R5", ang >= 20, round(ang, 1)))
    m = H.mass_g(s, meta["density"]); out.append(("R6", m <= 150, round(m, 1)))
    return out
