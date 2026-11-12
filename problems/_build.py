"""Writes problems/Pxx_*/{spec.md, meta.json, hidden_tests.py, reference.py}. Run once; then freeze (hashes)."""
import json, textwrap
from pathlib import Path
ROOT = Path(__file__).parent
PLA = "PLA: density 1.24 g/cm3, Young's modulus E = 3500 MPa."
OUT = ("\n## Output\nWrite CadQuery (Python) code, units in millimetres. Assign the finished part (one single solid) "
       "to a variable named `result`.\n")
P = {}

# ---------------------------------------------------------------- P01
P["P01_shelf_bracket"] = dict(meta={"density": 1.24, "E": 3500, "split": "test"}, spec="""
# Shelf bracket
A wall-mounted bracket that carries the end of a shelf.

## Coordinate system
The wall is the plane x = 0; the bracket lies in x >= 0 and touches the wall. Z is up. Y is along the wall (horizontal).

## Requirements
- R1. One single, valid solid.
- R2. Envelope: the part fits inside 0 <= x <= 170, -20 <= y <= 20, 0 <= z <= 130 and touches the wall (minimum x = 0).
- R3. Two screw holes, diameter 5.5 mm, axis along X, through the part where it sits on the wall, centred at (y=0, z=20) and (y=0, z=60). A screwdriver must reach each screw head from the front: no material within 4 mm of either hole axis for x >= 10.
- R4. Shelf support: the shelf rests on a horizontal top surface at exactly z = 110 that reaches at least x = 150 (solid material directly below z = 110 between x = 140 and 150 around y = 0). Nothing of the bracket may be above z = 110 for x >= 8.
- R5. Strength: a downward load of 150 N acts at x = 150. Using cantilever beam theory on the cross-section cut by the plane x = 10, the bending stress M*c/I must be <= 20 MPa (M = 150 N x 140 mm).
- R6. Stiffness: estimated tip deflection F*L^3/(3*E*I) with L = 140 mm and I of the x = 10 section must be <= 2.0 mm.
- R7. Mass <= 90 g.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
plate = cq.Workplane("XY").box(6, 30, 110, centered=False).translate((0, -15, 0))
arm = cq.Workplane("XY").box(144, 10, 30, centered=False).translate((6, -5, 80))
result = plate.union(arm)
for z in (20, 60):
    result = result.cut(cq.Workplane("YZ").center(0, z).circle(2.75).extrude(10))
''')

# ---------------------------------------------------------------- P02
P["P02_phone_stand"] = dict(meta={"density": 1.24, "E": 3500, "split": "test"}, spec="""
# Desk phone stand
A one-piece desk stand that holds a phone leaning back for video calls.

## The phone (fixed, do not model it)
Phone: 160 x 75 x 9 mm, 200 g. Its bottom-back edge lies along the Y axis line at (x = 0, z = 8), from y = -37.5 to 37.5.
The phone leans back toward -X at 65 degrees from horizontal: its long axis is u = (-cos65, 0, sin65) and its screen faces
n = (sin65, 0, cos65). The phone occupies every point (0, y, 8) + a*u + b*n with 0 <= a <= 160, 0 <= b <= 9, |y| <= 37.5.
Its centre of mass is at (0, 0, 8) + 80*u + 4.5*n.

## Requirements
- R1. One single, valid solid.
- R2. Stands on the desk plane z = 0 (minimum z = 0). Footprint within 100 x 100 mm (x and y extents), height <= 120 mm.
- R3. The stand must not intersect the phone volume.
- R4. Back support: material directly behind the phone back (within 2 mm, -2 <= b <= 0) somewhere between a = 90 and a = 110 near the middle (|y| <= 15).
- R5. Seat and lip: material just below the phone's bottom edge (-4 <= a <= 0, 0 <= b <= 9, |y| <= 15) so it cannot slide down, and a front lip (0 <= a <= 8, 9 <= b <= 13, |y| <= 15) so the bottom cannot slide forward.
- R6. Stability: the combined centre of mass of stand + phone must project inside the stand's contact area on the desk with at least 5 mm margin.
- R7. Mass <= 60 g.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
def fbox(a0, a1, b0, b1, y0, y1):
    b = cq.Solid.makeBox(a1 - a0, y1 - y0, b1 - b0, cq.Vector(a0, y0, -b1))
    return b.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), -115).translate(cq.Vector(0, 0, 8))
base = cq.Solid.makeBox(100, 60, 3, cq.Vector(-75, -30, 0))
s = base.fuse(fbox(-12, 118, -3, 0, -20, 20)).fuse(fbox(-12, 0, 0, 13, -20, 20)).fuse(fbox(0, 8, 9, 13, -20, 20))
s = s.cut(cq.Solid.makeBox(300, 300, 50, cq.Vector(-150, -150, -50)))
result = cq.Workplane().add(s.clean())
''')

# ---------------------------------------------------------------- P03
P["P03_enclosure_base"] = dict(meta={"density": 1.24, "E": 3500, "split": "test"}, spec="""
# Electronics enclosure base
The bottom half of an enclosure for an 80 x 50 mm circuit board.

## Coordinate system
Centred on the origin in X and Y; the outside of the floor is the plane z = 0; Z is up. The board sits horizontally with its
underside at z = 8.

## Requirements
- R1. One single, valid solid.
- R2. Floor: solid floor at least 2 mm thick (z from 0 to 2) under the whole board area.
- R3. Board space: the region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be completely free of material.
- R4. Walls: outer size 85 x 55 mm (+-1.5 mm) in X and Y; wall top at z between 30 and 32.5; continuous side walls on all four sides (except the cutout in R6).
- R5. Four screw bosses that support the board at (x, y) = (+-35, +-20): solid round bosses (outer diameter >= 6 mm) from the floor up to z = 8, each with a 2.2 mm pilot hole open at its top (hole at least 4 mm deep).
- R6. USB-C cutout through the -X wall: opening at least 9 mm wide (Y) and 3 mm high (Z), centred at y = 0, z = 14.
- R7. Mass <= 70 g.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
result = cq.Workplane("XY").box(85, 55, 31, centered=(True, True, False))
result = result.cut(cq.Workplane("XY").box(81, 51, 30, centered=(True, True, False)).translate((0, 0, 2)))
for x in (-35, 35):
    for y in (-20, 20):
        result = result.union(cq.Workplane("XY").center(x, y).circle(3.2).extrude(6).translate((0, 0, 2)))
        result = result.cut(cq.Workplane("XY").center(x, y).circle(1.1).extrude(5).translate((0, 0, 3.01)))
result = result.cut(cq.Workplane("XY").box(4, 10, 4).translate((-42, 0, 14)))
''')

# ---------------------------------------------------------------- P04
P["P04_test_tube_rack"] = dict(meta={"density": 1.24, "E": 3500, "split": "pilot"}, spec="""
# Test tube rack
A rack for ten 16 mm test tubes in two rows of five.

## Coordinate system
The rack stands on z = 0, Z up, centred on the origin in X and Y.

## Requirements
- R1. One single, valid solid.
- R2. Footprint within 140 x 80 mm; the top of the rack at z = 60 (+-2 mm).
- R3. Ten tube holes, diameter 17 mm, vertical, centred at x = -44, -22, 0, 22, 44 and y = -12.5, 12.5. Each hole must be clear from its top down to z = 10, with a ring of material around it at the top.
- R4. Each tube rests on a solid floor: material under every tube from z = 0 to 3 (within 4 mm of the hole axis).
- R5. Tipping: with all ten tubes in place (20 g each, centre of mass at z = 55 on each hole axis), the loaded rack must not tip before 20 degrees: atan(d / h) >= 20 deg, where d is the distance from the combined centre of mass to the nearest edge of the contact area and h its height.
- R6. Mass <= 150 g.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
pts = [(x, y) for x in (-44, -22, 0, 22, 44) for y in (-12.5, 12.5)]
top = cq.Workplane("XY").box(120, 50, 3, centered=(True, True, False)).translate((0, 0, 57)).faces(">Z").workplane().pushPoints(pts).hole(17)
bot = cq.Workplane("XY").box(120, 50, 3, centered=(True, True, False))
walls = cq.Workplane("XY").box(3, 50, 60, centered=(True, True, False)).translate((-58.5, 0, 0)).union(
        cq.Workplane("XY").box(3, 50, 60, centered=(True, True, False)).translate((58.5, 0, 0)))
result = bot.union(top).union(walls)
''')

# ---------------------------------------------------------------- P05
P["P05_pipe_clamp"] = dict(meta={"density": 1.24, "E": 3500, "split": "test"}, spec="""
# Pipe saddle clamp
A clamp that holds a 25 mm pipe against a flat surface, fixed with two screws.

## Coordinate system
The mounting surface is the plane z = 0; Z up. The pipe (outer diameter 25 mm) lies on that surface along the Y axis: its axis is the line x = 0, z = 12.5.

## Requirements
- R1. One single, valid solid.
- R2. Sits on z = 0; clamp width (Y extent) between 18 and 22 mm; total X extent <= 80 mm.
- R3. The pipe volume (radius 12.6 mm around its axis) must be free of material.
- R4. The clamp wraps over the top of the pipe: solid material in the band 12.7 to 15.5 mm from the pipe axis directly above the pipe (|x| <= 7).
- R5. Two screw holes, diameter 6.6 mm, vertical, centred at (x, y) = (+-27, 0), through flanges that lie on the surface.
- R6. Flanges at least 3 mm thick: solid from z = 0 to 3 for 18.5 <= |x| <= 23, |y| <= 4.
- R7. Mass <= 25 g.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
ring = cq.Workplane("XZ").center(0, 12.5).circle(16).extrude(-10, both=True)
body = ring.union(cq.Workplane("XY").box(32, 20, 12.5, centered=(True, True, False)))
flanges = cq.Workplane("XY").box(70, 20, 3, centered=(True, True, False))
s = body.union(flanges)
s = s.cut(cq.Workplane("XZ").center(0, 12.5).circle(12.75).extrude(-15, both=True))
s = s.cut(cq.Workplane("XY").box(25.5, 30, 12.5, centered=(True, True, False)))
for x in (-27, 27):
    s = s.cut(cq.Workplane("XY").center(x, 0).circle(3.3).extrude(5))
s = s.cut(cq.Workplane("XY").box(200, 200, 50, centered=(True, True, False)).translate((0, 0, -50)))
result = s
''')

# ---------------------------------------------------------------- P06
P["P06_heat_sink"] = dict(meta={"density": 2.70, "E": 69000, "split": "test"}, spec="""
# Passive heat sink
A finned aluminium heat sink for a 40 x 40 mm chip, cooled by natural convection.

## Coordinate system
The base's underside (chip contact) is the plane z = 0, centred on the origin in X and Y; Z up.

## Requirements
- R1. One single, valid solid.
- R2. Footprint exactly 40 x 40 mm (+-0.5), centred on the origin; total height <= 25 mm.
- R3. Solid base at least 3 mm thick (z = 0 to 3) over the whole footprint.
- R4. Thermal: natural-convection resistance estimate R = 1 / (h * A * eta) with h = 10 W/(m2 K), eta = 0.85 and A the total surface area of the part must be <= 9 K/W.
- R5. Two mounting holes, diameter 3.2 mm, vertical through the base at (x, y) = (+-15, 0). A screwdriver must reach each screw from above: no material within 3 mm of either hole axis above the base (z >= 3).
- R6. Mass <= 45 g.

## Material
Aluminium 6063: density 2.70 g/cm3.
""", tests='''
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
''', ref='''
import cadquery as cq
s = cq.Workplane("XY").box(40, 40, 3, centered=(True, True, False))
for x in (-19.25, -10.5, -5.5, 0, 5.5, 10.5, 19.25):
    s = s.union(cq.Workplane("XY").box(1.5, 40, 22, centered=(True, True, False)).translate((x, 0, 3)))
for x in (-15, 15):
    s = s.cut(cq.Workplane("XY").center(x, 0).circle(1.6).extrude(3))
result = s
''')

# ---------------------------------------------------------------- P07
P["P07_nema17_mount"] = dict(meta={"density": 1.24, "E": 3500, "split": "test"}, spec="""
# NEMA 17 motor mount
An L-shaped bracket that holds a NEMA 17 stepper motor against a vertical face plate and screws down to a table.

## Coordinate system
The table is z = 0, Z up. The motor's mounting face presses against the plane y = 0 from the -Y side; the motor body
(42.3 mm square, 48 mm long) lies in y < 0 with its shaft axis along Y through (x = 0, z = 30). The bracket is on the +Y side.

## Requirements
- R1. One single, valid solid.
- R2. Face plate at least 4 mm thick (y = 0 to 4) with solid material all around the central bore.
- R3. Central bore diameter 22.5 mm through the face plate, on the shaft axis.
- R4. Four motor screw holes, diameter 3.4 mm, through the face plate along Y at (x, z) = (+-15.5, 30 +- 15.5).
- R5. Motor clearance: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5.
- R6. Base on the table (minimum z = 0) with two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25).
- R7. Envelope -35 <= x <= 35, top <= 55 mm; mass <= 60 g.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
face = cq.Workplane("XY").box(50, 5, 55, centered=False).translate((-25, 0, 0))
base = cq.Workplane("XY").box(64, 40, 5, centered=False).translate((-32, 0, 0))
s = face.union(base)
def ycyl(x, z, r):
    return cq.Workplane("XZ").center(x, z).circle(r).extrude(-6)
s = s.cut(ycyl(0, 30, 11.25))
for x in (-15.5, 15.5):
    for z in (14.5, 45.5):
        s = s.cut(ycyl(x, z, 1.7))
for x in (-25, 25):
    s = s.cut(cq.Workplane("XY").center(x, 25).circle(2.75).extrude(6))
result = s
''')

# ---------------------------------------------------------------- P08
P["P08_wall_hook"] = dict(meta={"density": 1.24, "E": 3500, "split": "pilot"}, spec="""
# Wall hook for a bag strap
A screw-on wall hook that holds a bag by a 10 mm wide strap.

## Coordinate system
The wall is the plane x = 0; the hook is in x >= 0. Z up, Y horizontal along the wall.

## Requirements
- R1. One single, valid solid.
- R2. A flat back plate on the wall: solid material at 0 <= x <= 2 over |y| <= 8, -5 <= z <= 45; minimum x = 0.
- R3. Two screw holes, diameter 4.5 mm, along X through the back plate at (y, z) = (0, 0) and (0, 40); plate at least 4 mm thick around them.
- R4. Strap seat: the strap (10 mm wide, 6 mm thick) rests on a solid bed whose top is at z = -14 under 34 <= x <= 46, |y| <= 4, and the space just above it (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty.
- R5. Retaining lip: solid material at 47 <= x <= 52, |y| <= 4, -13 <= z <= -8 so the strap cannot slide off.
- R6. Strength: 50 N downward at x = 40. Using beam theory on the section cut by the plane x = 8: bending stress <= 25 MPa and tip deflection estimate F*L^3/(3*E*I) with L = 32 mm <= 1.5 mm.
- R7. Mass <= 25 g; X extent <= 55 mm.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
plate = cq.Workplane("XY").box(5, 16, 75, centered=False).translate((0, -8, -25))
arm = cq.Workplane("XY").box(41, 10, 11, centered=False).translate((5, -5, -25))
lip = cq.Workplane("XY").box(6, 10, 18, centered=False).translate((46, -5, -25))
s = plate.union(arm).union(lip)
for z in (0, 40):
    s = s.cut(cq.Workplane("YZ").center(0, z).circle(2.25).extrude(6))
result = s
''')

# ---------------------------------------------------------------- P09
P["P09_drone_arm"] = dict(meta={"density": 1.24, "E": 3500, "split": "test"}, spec="""
# Drone arm
A printed arm that connects a small quadcopter frame to one motor.

## Coordinate system
The arm lies along +X starting at x = 0 (frame side). Its underside is the plane z = 0; Z up. The motor sits on top at (x, y) = (120, 0).

## Requirements
- R1. One single, valid solid.
- R2. Envelope: minimum x = 0, maximum x <= 136, |y| <= 16, minimum z = 0, height <= 20 mm.
- R3. Frame attachment: two vertical holes, diameter 3.2 mm, at (x, y) = (6, +-6).
- R4. Motor mount: four vertical holes, diameter 3.2 mm, at (x, y) = (120 +- 8, +-9.5), and a 6 mm vertical clearance hole for the shaft at (120, 0) through the whole part.
- R5. Strength: motor thrust 12 N upward at x = 120. Using beam theory on the section cut by the plane x = 20 the bending stress must be <= 30 MPa.
- R6. Stiffness: tip deflection estimate F*L^3/(3*E*I) with L = 100 mm and I of the x = 20 section <= 1.0 mm.
- R7. Mass <= 20 g.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
arm = cq.Workplane("XY").box(120, 8, 12, centered=False).translate((0, -4, 0))
root = cq.Workplane("XY").box(12, 20, 4, centered=False).translate((0, -10, 0))
pad = cq.Workplane("XY").center(120, 0).circle(16).extrude(4)
s = arm.union(root).union(pad)
for y in (-6, 6):
    s = s.cut(cq.Workplane("XY").center(6, y).circle(1.6).extrude(20))
for dx in (-8, 8):
    for y in (-9.5, 9.5):
        s = s.cut(cq.Workplane("XY").center(120 + dx, y).circle(1.6).extrude(20))
s = s.cut(cq.Workplane("XY").center(120, 0).circle(3).extrude(20))
result = s
''')

# ---------------------------------------------------------------- P10
P["P10_sensor_tilt_mount"] = dict(meta={"density": 1.24, "E": 3500, "split": "test"}, spec="""
# Tilted sensor mount
A desk mount that holds a 50 g sensor board facing forward and tilted up by 30 degrees.

## Coordinate system
The desk is z = 0, Z up. "Forward" is +Y.

## Requirements
- R1. One single, valid solid.
- R2. Base on the desk (minimum z = 0) with two vertical screw holes, diameter 4.5 mm, at (x, y) = (+-20, -10).
- R3. Mounting face: one flat face of at least 900 mm2 whose outward normal is n = (0, cos30, sin30) (facing forward, tilted up 30 deg).
- R4. The centre of that face is at a height between 35 and 50 mm.
- R5. Two sensor screw holes, diameter 3.2 mm, perpendicular to the mounting face, at the face centre +- 10 mm along X.
- R6. Stability: with the 50 g sensor (its centre of mass 15 mm in front of the face centre, along n) the combined centre of mass must lie inside the contact area with >= 5 mm margin.
- R7. Mass <= 35 g.

## Material
""" + PLA, tests='''
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
''', ref='''
import cadquery as cq
base = cq.Solid.makeBox(56, 50, 4, cq.Vector(-28, -20, 0))
plate = cq.Solid.makeBox(36, 4, 40, cq.Vector(-18, -4, -20)).rotate(cq.Vector(0, 0, 0), cq.Vector(1, 0, 0), 30).translate(cq.Vector(0, 5, 42))
web = cq.Solid.makeBox(8, 16, 38, cq.Vector(-4, -10, 0))
s = base.fuse(plate).fuse(web).clean()
w = cq.Workplane().add(s)
for x in (-20, 20):
    w = w.cut(cq.Workplane("XY").center(x, -10).circle(2.25).extrude(5))
import math
n = cq.Vector(0, math.cos(math.radians(30)), math.sin(math.radians(30)))
for dx in (-10, 10):
    c = cq.Vector(dx, 5, 42) + n * 1
    w = w.cut(cq.Workplane().add(cq.Solid.makeCylinder(1.6, 8, c, -n)))
result = w
''')

for name, d in P.items():
    pd = ROOT / name
    pd.mkdir(exist_ok=True)
    (pd / "spec.md").write_text(d["spec"].strip() + "\n" + OUT)
    (pd / "meta.json").write_text(json.dumps(d["meta"], indent=1))
    (pd / "hidden_tests.py").write_text(textwrap.dedent(d["tests"]).strip() + "\n")
    (pd / "reference.py").write_text(textwrap.dedent(d["ref"]).strip() + "\n")
print("wrote", len(P))
