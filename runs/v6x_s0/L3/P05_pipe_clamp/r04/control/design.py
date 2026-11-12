import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-15.5, -15.5, -27.5))
