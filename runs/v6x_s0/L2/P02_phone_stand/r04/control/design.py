import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-77.79, -40.0, -45.14))
