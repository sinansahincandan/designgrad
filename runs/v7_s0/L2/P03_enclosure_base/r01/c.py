import cadquery as cq

# Dimensions
floor_thickness = 2.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
wall_thickness = 2.5

board_x, board_y = 80.0, 50.0
cavity_z_start = 8.0
cavity_z_end = 32.0 # Note: R4 says wall top is ~31, but R3 requires cavity up to 32. 
# To satisfy both, we ensure the walls reach at least 32 or the cavity is subtracted from what exists.

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.0

# 1. Create the Floor (R2)
floor = cq.Workplane("XY").box(outer_x, outer_y, floor_thickness).translate((0, 0, floor_thickness / 2))

# 2. Create the Walls (R4)
# We create a hollow shell by subtracting an inner box from an outer box
walls = (
    cq.Workplane("XY")
    .box(outer_x, outer_y, wall_height)
    .translate((0, 0, floor_thickness + wall_height / 2))
    .cut(
        cq.Workplane("XY")
        .box(outer_x - 2 * wall_thickness, outer_y - 2 * wall_thickness, wall_height)
        .translate((0, 0, floor_thickness + wall_height / 2))
    )
)

# 3. Create the Bosses (R5)
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Bosses from z=2 to z=8
        b = (
            cq.Workplane("XY")
            .workplane(offset=floor_thickness)
            .circle(boss_od / 2)
            .extrude(8 - floor_thickness)
            .translate((bx, by, 0))
        )
        bosses = bosses.union(b)

# Combine Floor, Walls, and Bosses (R1)
main_body = floor.union(walls).union(bosses)

# 4. Subtract Board Cavity (R3)
# Region: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
cavity = cq.Workplane("XY").box(board_x, board_y, cavity_z_end - cavity_z_start).translate((0, 0, cavity_z_start + (cavity_z_end - cavity_z_start) / 2))
main_body = main_body.cut(cavity)

# 5. Subtract Pilot Holes (R5)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole starts at top of boss (z=8) and goes down
        hole = (
            cq.Workplane("XY")
            .workplane(offset=cavity_z_start - boss_hole_depth)
            .circle(boss_hole_d / 2)
            .extrude(boss_hole_depth)
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 6. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14. Dimensions: 9mm wide (Y), 3mm high (Z).
# Through the -X wall. Wall is at x = -outer_x/2.
usb_cutout = (
    cq.Workplane("XY")
    .box(wall_thickness * 3, 9, 3) # Ensure it penetrates through the wall
    .translate((-outer_x / 2, 0, 14))
)
main_body = main_body.cut(usb_cutout)

result = main_body