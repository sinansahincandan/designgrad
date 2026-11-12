import cadquery as cq

# Dimensions based on Design Document and Feedback
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 7.0  # Updated per feedback and Design Document (R5)
boss_hole_d = 2.2
boss_hole_depth = 6.0 # From z=8 down to z=2

# 1. Create the main body (Floor + Walls)
# We create a solid block from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create the Board Cavity (R3)
# Region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # Height is large enough to clear top
    .translate((0, 0, 8 + wall_height / 2)) # Shift so bottom is at z=8
)
main_body = main_body.cut(cavity)

# 3. Create the Screw Bosses (R5)
# Per feedback: create all bosses first, then union to ensure a single solid (R1).
# Using direct translation for precise positioning as per feedback.
bosses_union = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Boss from z=2 to z=8 (6mm height)
        # Using cylinder(height, radius).translate((bx, by, z_center))
        # To get bottom at 2 and top at 8, center is at 5.
        boss_cyl = (
            cq.Workplane("XY")
            .cylinder(6, boss_od / 2)
            .translate((bx, by, 5))
        )
        bosses_union = bosses_union.union(boss_cyl)

# Union bosses with main body
main_body = main_body.union(bosses_union)

# 4. Subtract Pilot Holes (R5)
# Per feedback: subtract using a cylinder at correct global coordinates to avoid face-selection instability.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole from z=2 to z=8 (6mm depth)
        hole = (
            cq.Workplane("XY")
            .cylinder(6, boss_hole_d / 2)
            .translate((bx, by, 5))
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# x range: [-42.5, -39.5], y range: [-4.5, 4.5], z range: [12.5, 15.5]
usb_box = cq.Workplane("XY").box(5, 9, 3).translate((-outer_x/2, 0, 14))
main_body = main_body.cut(usb_box)

result = main_body