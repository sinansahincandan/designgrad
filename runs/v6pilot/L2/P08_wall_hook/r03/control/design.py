import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-2.0, -8.0, -18.0))
