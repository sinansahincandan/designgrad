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
# We create a block that goes from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract the Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We use a box that covers the required Z range to ensure it clears any ceiling material.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, 32 - 8)
    .translate((0, 0, 8 + (32 - 8) / 2))
)
main_body = main_body.cut(cavity)

# 3. Add Screw Bosses (R5)
# Bosses are solid from floor (z=2) up to z=8.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Use .center(bx, by) as per feedback to avoid translation/offset confusion
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(6) # Extends from z=2 to z=8
        )
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole starts from top of boss (z=8) and goes down
        hole = (
            cq.Workplane("XY")
            .workplane(offset=8 - boss_hole_depth)
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(boss_hole_depth)
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# To ensure it penetrates the wall completely, we use a larger X dimension and center it at the outer face.
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # 10mm depth to ensure penetration through the ~2.5mm wall
    .translate((-outer_x / 2, 0, 14))
)
main_body = main_body.cut(usb_cutout)

result = main_body