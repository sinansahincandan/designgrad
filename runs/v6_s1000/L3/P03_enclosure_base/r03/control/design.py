import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-42.5, -27.5, -1.0))
