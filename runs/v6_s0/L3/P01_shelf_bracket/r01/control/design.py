import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((0.0, -60.0, 0.0))
