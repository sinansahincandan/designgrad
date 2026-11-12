import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-2.5, -12.0, -1.0))
