import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-27.0, -20.0, -3.0))
