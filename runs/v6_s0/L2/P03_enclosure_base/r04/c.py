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
        # Use absolute cylinder and translate to position correctly: 
        # center at z=(2+8)/2 = 5
        boss_cyl = cq.Workplane("XY").cylinder(boss_od, 6).translate((bx, by, 5))
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole starts from top of boss (z=8) and goes down to z=4.
        # Center at z=(8+4)/2 = 6
        hole = cq.Workplane("XY").cylinder(boss_hole_d, boss_hole_depth).translate((bx, by, 6))
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# x from -45 to -38 (7mm wide), y width 9, z height 3.
# Centered at y=0, z=14. Center of X is (-45 + -38)/2 = -41.5
usb_cutout = (
    cq.Workplane("XY")
    .box(7, 9, 3)
    .translate((-41.5, 0, 14))
)
main_body = main_body.cut(usb_cutout)

result = main_body