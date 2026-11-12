import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 32.0  # R4: Wall top at z=32
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.0

# 1. Create the main body (Floor + Walls)
# We create a solid block from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create the board cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We create a box that covers this range and subtract it.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height - 8)
    .translate((0, 0, 8 + (wall_height - 8) / 2))
)
main_body = main_body.cut(cavity)

# 3. Add the screw bosses (R5)
# Bosses are solid from floor (z=2) up to z=8.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder starting at z=2 and extruding 6mm to reach z=8
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_od / 2)
            .extrude(6)
            .translate((bx, by, 0))
        )
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
# Hole must be open at top (z=8) and at least 4mm deep (down to z=4).
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create a hole from z=4 to z=8
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4)
            .circle(boss_hole_d / 2)
            .extrude(4)
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Wall is at x = -outer_x/2 = -42.5.
# Box dimensions: X (penetration depth), Y (width 9mm), Z (height 3mm).
usb_cutout = (
    cq.Workplane("XY")
    .box(5, 9, 3) # x=5 ensures it goes through the wall thickness (~2.5mm)
    .translate((-outer_x / 2, 0, 14))
)
main_body = main_body.cut(usb_cutout)

result = main_body