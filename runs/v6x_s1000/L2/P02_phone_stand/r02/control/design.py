import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-68.53, -40.0, 0.0))
