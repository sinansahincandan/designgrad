import cadquery as cq
pts = [(x, y) for x in (-44, -22, 0, 22, 44) for y in (-12.5, 12.5)]
top = cq.Workplane("XY").box(120, 50, 3, centered=(True, True, False)).translate((0, 0, 57)).faces(">Z").workplane().pushPoints(pts).hole(17)
bot = cq.Workplane("XY").box(120, 50, 3, centered=(True, True, False))
walls = cq.Workplane("XY").box(3, 50, 60, centered=(True, True, False)).translate((-58.5, 0, 0)).union(
        cq.Workplane("XY").box(3, 50, 60, centered=(True, True, False)).translate((58.5, 0, 0)))
result = bot.union(top).union(walls)
