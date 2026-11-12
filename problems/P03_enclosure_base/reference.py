import cadquery as cq
result = cq.Workplane("XY").box(85, 55, 31, centered=(True, True, False))
result = result.cut(cq.Workplane("XY").box(81, 51, 30, centered=(True, True, False)).translate((0, 0, 2)))
for x in (-35, 35):
    for y in (-20, 20):
        result = result.union(cq.Workplane("XY").center(x, y).circle(3.2).extrude(6).translate((0, 0, 2)))
        result = result.cut(cq.Workplane("XY").center(x, y).circle(1.1).extrude(5).translate((0, 0, 3.01)))
result = result.cut(cq.Workplane("XY").box(4, 10, 4).translate((-42, 0, 14)))
