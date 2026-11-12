import math
def _frame_box(H, a0, a1, b0, b1, y0, y1):
    import cadquery as cq
    b = cq.Solid.makeBox(a1 - a0, y1 - y0, b1 - b0, cq.Vector(a0, y0, -b1))
    return b.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), -115).translate(cq.Vector(0, 0, 8))
def run(s, H, meta):
    out = []
    ok, v = H.single_valid(s); out.append(("R1", ok, v))
    bb = H.bbox(s)
    out.append(("R2", abs(bb.zmin) < 0.1 and bb.xlen <= 100.1 and bb.ylen <= 100.1 and bb.zmax <= 120.1, [round(bb.xlen,1), round(bb.ylen,1), round(bb.zmin,2), round(bb.zmax,1)]))
    e, v = H.empty(s, _frame_box(H, 0, 160, 0, 9, -37.5, 37.5), tol=1.0); out.append(("R3", e, v))
    f, fr = H.filled(s, _frame_box(H, 90, 110, -2, 0, -15, 15), 0.15); out.append(("R4", f, fr))
    f1, a = H.filled(s, _frame_box(H, -4, 0, 0, 9, -15, 15), 0.3)
    f2, b = H.filled(s, _frame_box(H, 0, 8, 9, 13, -15, 15), 0.3); out.append(("R5", f1 and f2, [a, b]))
    u = (-math.cos(math.radians(65)), 0, math.sin(math.radians(65))); n = (math.sin(math.radians(65)), 0, math.cos(math.radians(65)))
    pc = [80 * u[i] + 4.5 * n[i] for i in range(3)]; pc[2] += 8
    mg, c = H.stability(s, meta["density"], [(200, pc)]); out.append(("R6", mg >= 5, round(mg, 2)))
    m = H.mass_g(s, meta["density"]); out.append(("R7", m <= 60, round(m, 1)))
    return out
