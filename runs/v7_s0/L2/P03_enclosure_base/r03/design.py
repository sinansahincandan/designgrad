import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0  # Total height from z=0 to top of wall
wall_thickness = 2.0

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.0 # Hole goes from z=8 down to z=4

# 1. Create the Floor (R2)
# Spans z from 0 to 2
floor = cq.Workplane("XY").box(outer_x, outer_y, floor_thickness).translate((0, 0, floor_thickness / 2))

# 2. Create the Walls (R4)
# Outer dimensions 85x55, height extends from z=2 to z=31
# We create a solid block and hollow it out to ensure thin walls for R7
walls = (
    cq.Workplane("XY")
    .box(outer_x, outer_y, wall_height - floor_thickness)
    .faces("<Z").workplane()
    .rect(outer_x - 2 * wall_thickness, outer_y - 2 * wall_thickness)
    .cutThruAll()
).translate((0, 0, floor_thickness + (wall_height - floor_thickness) / 2))

# Combine Floor and Walls
main_body = floor.union(walls)

# 3. Add the Screw Bosses (R5)
# Bosses extend from z=2 to z=8
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder at the correct position
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2) # Start at top of floor
            .circle(boss_od / 2)
            .extrude(6)           # Extends to z=8
            .translate((bx, by, 0))
        )
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
# Hole is at least 4mm deep, starting from top of boss (z=8) downwards
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=8 - boss_hole_depth)
            .circle(boss_hole_d / 2)
            .extrude(boss_hole_depth)
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 5. Subtract Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We use a box that covers this exact volume.
cavity = cq.Workplane("XY").box(board_x, board_y, 32 - 8).translate((0, 0, 8 + (32 - 8) / 2))
main_body = main_body.cut(cavity)

# 6. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Opening: 9mm wide (Y), 3mm high (Z). 
# We use a box that spans from the outer face to the inner cavity to ensure it cuts through.
usb_cutout = cq.Workplane("XY").box(10, 9, 3).translate((-outer_x / 2, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body