import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 7.0  # From z=8 down to z=1

# 1. Create the main body (Floor + Walls)
# We create a solid block and then subtract the board cavity.
# The floor is at z=0 to z=2. The walls go up to wall_height.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Define the Board Cavity (R3)
# Region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We subtract a box that covers this volume.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # height is large enough to cover the range
    .translate((0, 0, 8 + (wall_height - 8) / 2)) # center it so bottom is at z=8
)

# 3. Create and Add Bosses (R5)
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Bosses extend from floor (z=2) up to z=8
        boss_cyl = (
            cq.Workplane("XY")
            .cylinder(6.0, boss_od / 2) # height 6, radius od/2
            .translate((bx, by, 5))      # center at z=5 (so bottom is at 5-3=2 and top at 5+3=8)
        )
        bosses = bosses.union(boss_cyl)

# Combine main body and bosses
result_solid = main_body.union(bosses)

# 4. Perform all subtractions (R3, R5 holes, R6 cutout)
# Subtract Board Cavity
result_solid = result_solid.cut(cavity)

# Subtract Pilot Holes (R5)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole starts at z=1 and extends to z=8 (depth 7mm)
        hole = cq.Workplane("XY").cylinder(boss_hole_depth, boss_hole_d / 2).translate((bx, by, 1 + boss_hole_depth / 2))
        result_solid = result_solid.cut(hole)

# Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Increased X-dimension to 10mm to ensure clean penetration of the wall.
usb_cutout = cq.Workplane("XY").box(10, 9, 3).translate((-outer_x / 2, 0, 14))
result_solid = result_solid.cut(usb_cutout)

result = result_solid