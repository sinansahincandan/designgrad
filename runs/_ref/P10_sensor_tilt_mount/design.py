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
