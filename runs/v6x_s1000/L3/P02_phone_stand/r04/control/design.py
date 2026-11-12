import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-112.91, -40.0, -20.0))
