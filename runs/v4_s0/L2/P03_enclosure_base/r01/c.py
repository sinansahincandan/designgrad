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
# We create a solid block from z=0 to z=wall_height
# The box() function centers on origin, so we translate it by wall_height/2 to start at z=0
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract the Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We create a box for this cavity and subtract it.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # Height is large enough to clear the top
    .translate((0, 0, 8 + (wall_height - 8) / 2)) # Center it starting from z=8
)
main_body = main_body.cut(cavity)

# 3. Add Screw Bosses (R5)
# Bosses extend from the floor (z=2) up to the board underside (z=8).
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder starting at z=2 and extruding 6mm up to z=8
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(6)
        )
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
# Hole must be at least 4mm deep, starting from the top of the boss (z=8) downwards.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole from z=4 to z=8 (depth of 4mm)
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4)
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(4)
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Wall is at x = -outer_x/2 = -42.5.
# We use a box that spans through the wall thickness.
usb_cutout = cq.Workplane("XY").box(10, 9, 3).translate((-outer_x / 2, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body