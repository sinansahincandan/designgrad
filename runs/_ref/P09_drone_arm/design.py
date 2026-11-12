import cadquery as cq
arm = cq.Workplane("XY").box(120, 8, 12, centered=False).translate((0, -4, 0))
root = cq.Workplane("XY").box(12, 20, 4, centered=False).translate((0, -10, 0))
pad = cq.Workplane("XY").center(120, 0).circle(16).extrude(4)
s = arm.union(root).union(pad)
for y in (-6, 6):
    s = s.cut(cq.Workplane("XY").center(6, y).circle(1.6).extrude(20))
for dx in (-8, 8):
    for y in (-9.5, 9.5):
        s = s.cut(cq.Workplane("XY").center(120 + dx, y).circle(1.6).extrude(20))
s = s.cut(cq.Workplane("XY").center(120, 0).circle(3).extrude(20))
result = s
