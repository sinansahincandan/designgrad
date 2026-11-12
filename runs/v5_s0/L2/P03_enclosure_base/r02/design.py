import cadquery as cq

# Dimensions based on Design Document and Feedback
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.5  # R5: Outer diameter >= 6mm
boss_hole_d = 2.2 # R5: Pilot hole diameter
boss_hole_depth = 8.0 # R5: Hole from z=8 down to z=0

# 1. Create the main body (Floor + Walls)
# We create a solid block from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create the Board Cavity (R3)
# Region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # Large enough height to clear top
    .translate((0, 0, 8 + wall_height / 2)) # Shift so bottom is at z=8
)
main_body = main_body.cut(cavity)

# 3. Create the Screw Bosses (R5)
# Per feedback: bosses must extend from the floor (z=0) up to the board interface (z=8).
bosses_union = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Boss from z=0 to z=8 (8mm height)
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .circle(boss_od / 2)
            .extrude(8)
            .translate((bx, by, 0))
        )
        bosses_union = bosses_union.union(boss_cyl)

# Union bosses with main body (R1)
main_body = main_body.union(bosses_union)

# 4. Subtract Pilot Holes (R5)
# Per feedback: subtract from top (z=8) downwards using cutBlind to reach z=0.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        main_body = (
            main_body.faces("<Z").workplane(offset=8) # Move to top of boss at z=8
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .cutBlind(boss_hole_depth) # Cuts from z=8 down to z=0
        )

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Target volume: x range [-42.5, -39.5], y range [-4.5, 4.5], z range [12.5, 15.5]
usb_box = cq.Workplane("XY").box(5, 9, 3).translate((-outer_x/2, 0, 14))
main_body = main_body.cut(usb_box)

result = main_body