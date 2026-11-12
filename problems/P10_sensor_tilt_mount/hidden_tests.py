import math
def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    bb = H.bbox(s)
    r = [H.hole_ok(s, (x, -10, 0), (0, 0, 1), 4.5, 3)[0] for x in (-20, 20)]; out.append(("R2", all(r) and abs(bb.zmin) < 0.1, r))
    n = (0, math.cos(math.radians(30)), math.sin(math.radians(30)))
    faces = sorted(H.planar_faces_with_normal(s, n), key=lambda t: -t[0])
    if not faces:
        out += [("R3", False, "no face"), ("R4", False, None), ("R5", False, None), ("R6", False, None)]
    else:
        area, c = faces[0]
        out.append(("R3", area >= 900, round(area, 1)))
        out.append(("R4", 35 <= c.z <= 50, round(c.z, 1)))
        r = [H.hole_ok(s, (c.x + dx + n[0] * 0.5, c.y + n[1] * 0.5, c.z + n[2] * 0.5), (-n[0], -n[1], -n[2]), 3.2, 3.5)[0] for dx in (-10, 10)]
        out.append(("R5", all(r), r))
        p = (c.x + 15 * n[0], c.y + 15 * n[1], c.z + 15 * n[2])
        mg, _ = H.stability(s, meta["density"], [(50, p)]); out.append(("R6", mg >= 5, round(mg, 2)))
    m = H.mass_g(s, meta["density"]); out.append(("R7", m <= 35, round(m, 1)))
    return out
