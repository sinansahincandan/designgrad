import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-76.38, -42.55, -22.43))
