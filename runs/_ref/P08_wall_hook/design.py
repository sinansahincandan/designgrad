import cadquery as cq
plate = cq.Workplane("XY").box(5, 16, 75, centered=False).translate((0, -8, -25))
arm = cq.Workplane("XY").box(41, 10, 11, centered=False).translate((5, -5, -25))
lip = cq.Workplane("XY").box(6, 10, 18, centered=False).translate((46, -5, -25))
s = plate.union(arm).union(lip)
for z in (0, 40):
    s = s.cut(cq.Workplane("YZ").center(0, z).circle(2.25).extrude(6))
result = s
