import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-68.82, -25.0, -28.51))
