import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-48.85, -45.0, 0.0))
