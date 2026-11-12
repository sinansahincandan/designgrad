import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
# Bosses extend from z=2 to z=8 (height 6)

# 1. Create the main body (Floor + Walls)
# We create a solid block of outer dimensions and height, then subtract the board cavity.
# The floor starts at z=0, so the box goes from z=0 to z=wall_height.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
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
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(6)
        )
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
# Hole diameter 2.2mm, depth 6mm. We'll go from z=8 down to z=2.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create a cylinder for the hole and subtract it
        # Positioned so top is at z=8: workplane at offset 2, extrude 6 downwards? 
        # Actually, to match the feedback: workplane(offset=2).center(bx, by).circle(...).extrude(6) 
        # creates a cylinder from z=2 up to z=8. To subtract it, we use the same geometry.
        hole = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(6)
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# x range is 7.5mm wide (from -45 to -37.5), y is 9mm, z is 3mm.
# Center of X [-45, -37.5] is -41.25.
usb_cutout = cq.Workplane("XY").box(7.5, 9, 3).translate((-41.25, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body