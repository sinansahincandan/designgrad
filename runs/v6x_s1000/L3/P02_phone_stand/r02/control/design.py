import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-95.18, -40.0, 0.0))
