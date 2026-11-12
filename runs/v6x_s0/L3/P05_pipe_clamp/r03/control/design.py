import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-27.0, -15.5, -17.5))
