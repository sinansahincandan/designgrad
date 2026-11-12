import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-29.47, -20.0, -18.3))
