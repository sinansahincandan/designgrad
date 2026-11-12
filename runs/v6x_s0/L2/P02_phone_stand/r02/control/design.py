import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-56.21, -40.0, 0.0))
