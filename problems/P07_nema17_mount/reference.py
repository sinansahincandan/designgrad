import cadquery as cq
face = cq.Workplane("XY").box(50, 5, 55, centered=False).translate((-25, 0, 0))
base = cq.Workplane("XY").box(64, 40, 5, centered=False).translate((-32, 0, 0))
s = face.union(base)
def ycyl(x, z, r):
    return cq.Workplane("XZ").center(x, z).circle(r).extrude(-6)
s = s.cut(ycyl(0, 30, 11.25))
for x in (-15.5, 15.5):
    for z in (14.5, 45.5):
        s = s.cut(ycyl(x, z, 1.7))
for x in (-25, 25):
    s = s.cut(cq.Workplane("XY").center(x, 25).circle(2.75).extrude(6))
result = s
