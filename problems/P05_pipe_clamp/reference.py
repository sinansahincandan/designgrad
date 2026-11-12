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
