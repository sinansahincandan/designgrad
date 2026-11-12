import cadquery as cq
s = cq.Workplane("XY").box(40, 40, 3, centered=(True, True, False))
for x in (-19.25, -10.5, -5.5, 0, 5.5, 10.5, 19.25):
    s = s.union(cq.Workplane("XY").box(1.5, 40, 22, centered=(True, True, False)).translate((x, 0, 3)))
for x in (-15, 15):
    s = s.cut(cq.Workplane("XY").center(x, 0).circle(1.6).extrude(3))
result = s
