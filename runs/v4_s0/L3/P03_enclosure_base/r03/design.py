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
# The block goes from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Add the Bosses (Union)
# Bosses extend from z=2 to z=8
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create a cylinder at the correct position and height
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_od / 2)
            .extrude(6)  # Extends from z=2 to z=8
            .translate((bx, by, 0))
        )
        main_body = main_body.union(boss_cyl)

# 3. Subtract Board Cavity (R3)
# Region: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
# A box of 80x50x24 centered at z=20 covers z from 8 to 32.
cavity = cq.Workplane("XY").box(board_x, board_y, 24).translate((0, 0, 20))
main_body = main_body.cut(cavity)

# 4. Subtract Pilot Holes (R5)
# Holes are 2.2mm diameter, 4mm deep, starting from top of boss (z=8) downwards to z=4
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4) # Starts at z=4
            .circle(boss_hole_d / 2)
            .extrude(4)          # Extends to z=8
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Opening at least 9mm wide (Y) and 3mm high (Z), centered at y=0, z=14 on the -X wall.
# We use a box that penetrates from the outer face into the cavity.
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # Depth X=10, Width Y=9, Height Z=3
    .translate((-outer_x / 2, 0, 14))
)
main_body = main_body.cut(usb_cutout)

result = main_body