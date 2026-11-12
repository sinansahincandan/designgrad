import cadquery as cq
def fbox(a0, a1, b0, b1, y0, y1):
    b = cq.Solid.makeBox(a1 - a0, y1 - y0, b1 - b0, cq.Vector(a0, y0, -b1))
    return b.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 1, 0), -115).translate(cq.Vector(0, 0, 8))
base = cq.Solid.makeBox(100, 60, 3, cq.Vector(-75, -30, 0))
s = base.fuse(fbox(-12, 118, -3, 0, -20, 20)).fuse(fbox(-12, 0, 0, 13, -20, 20)).fuse(fbox(0, 8, 9, 13, -20, 20))
s = s.cut(cq.Solid.makeBox(300, 300, 50, cq.Vector(-150, -150, -50)))
result = cq.Workplane().add(s.clean())
