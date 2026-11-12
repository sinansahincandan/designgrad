import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-50.0, -15.5, -3.0))
