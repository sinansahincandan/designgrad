import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-43.0, -28.0, 0.0))
