import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-76.73, -40.0, -39.87))
