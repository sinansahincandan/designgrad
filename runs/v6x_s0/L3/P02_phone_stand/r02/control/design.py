import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-50.47, -50.0, 0.0))
