import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-20.0, -20.0, 0.0))
