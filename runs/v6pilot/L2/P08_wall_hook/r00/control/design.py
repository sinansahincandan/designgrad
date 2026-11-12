import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((0.0, -8.0, -20.0))
