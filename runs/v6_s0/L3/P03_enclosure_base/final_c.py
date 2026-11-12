import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 6.0  # From z=8 down to z=2

# 1. Create the main body (Floor + Walls)
# We create a solid block of outer dimensions and height, then subtract the board cavity.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We use a box that covers the required volume and subtract it.
cavity = cq.Workplane("XY").box(board_x, board_y, wall_height + 1).translate((0, 0, 8 + (wall_height + 1 - 8) / 2))
# To be precise with the R3 requirement: z from 8 to 32.
cavity = cq.Workplane("XY").box(board_x, board_y, 32 - 8).translate((0, 0, 8 + (32 - 8) / 2))
main_body = main_body.cut(cavity)

# 3. Add Screw Bosses (R5)
# Bosses are solid from floor (z=2) up to z=8.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder: OD 6mm, height 6mm (from z=2 to z=8)
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_od / 2)
            .extrude(6)
            .translate((bx, by, 0))
        )
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
# Hole diameter 2.2mm, depth at least 4mm. We'll go from z=8 down to z=2.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create a cylinder for the hole and subtract it
        # Positioned so top is at z=8: translate to (bx, by, 2) with height 6
        hole = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_hole_d / 2)
            .extrude(6)
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Opening at least 9mm wide (Y) and 3mm high (Z), centered at y=0, z=14 on the -X wall.
# We use a box that is deep enough to ensure it cuts through the wall completely.
usb_cutout = cq.Workplane("XY").box(10, 9, 3).translate((-outer_x / 2, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body