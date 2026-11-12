import cadquery as cq
result = cq.Workplane("XY").box(1, 1, 1, centered=False).translate((-30.0, -10.0, -37.5))
