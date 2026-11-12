import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-22.5, -20.0, -57.5))
