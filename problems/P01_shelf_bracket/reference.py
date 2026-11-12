import cadquery as cq
plate = cq.Workplane("XY").box(6, 30, 110, centered=False).translate((0, -15, 0))
arm = cq.Workplane("XY").box(144, 10, 30, centered=False).translate((6, -5, 80))
result = plate.union(arm)
for z in (20, 60):
    result = result.cut(cq.Workplane("YZ").center(0, z).circle(2.75).extrude(10))
