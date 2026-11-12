import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-58.17, -50.0, -11.91))
