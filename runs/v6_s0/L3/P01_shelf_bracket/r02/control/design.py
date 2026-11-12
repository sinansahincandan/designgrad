import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((0.0, -15.0, -55.0))
