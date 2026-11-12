import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.0

# 1. Create the main body (Floor + Walls)
# We create a solid block representing the outer dimensions and height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create the screw bosses as separate solids to be unioned
bosses_collection = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Bosses are solid from z=2 to z=8 (height of 6)
        # We create them at the origin and translate them to their positions
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_od / 2)
            .extrude(6)
            .translate((bx, by, 0))
        )
        # To ensure we can union them properly later, we collect them
        # In CadQuery, it's often safer to build one object and union others
        if sx == -1 and sy == -1:
            bosses_collection = boss_cyl
        else:
            bosses_collection = bosses_collection.union(boss_cyl)

# 3. Combine Floor/Walls with Bosses (R1 compliance)
main_body = main_body.union(bosses_collection)

# 4. Subtract Board Cavity (R3)
# Region: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # Height covers the range needed
    .translate((0, 0, 8 + (wall_height - 8) / 2))
)
main_body = main_body.cut(cavity)

# 5. Subtract Pilot Holes from Bosses (R5)
# Hole at least 4mm deep, starting from top (z=8) downwards
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Subtract from z=4 up to z=8 (4mm deep)
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4)
            .circle(boss_hole_d / 2)
            .extrude(4)
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 6. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Using a larger X dimension to ensure it penetrates the entire wall thickness.
usb_cutout = cq.Workplane("XY").box(10, 9, 3).translate((-outer_x/2 - 2, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body