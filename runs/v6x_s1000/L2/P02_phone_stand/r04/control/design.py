import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-70.0, -45.0, 0.0))
