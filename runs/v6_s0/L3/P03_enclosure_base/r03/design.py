import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_start_z = 2.0
boss_end_z = 8.0

# 1. Create the main body (Floor + Walls)
# We create a solid block of outer dimensions and height, then subtract the board cavity.
# The box is centered on XY, so we translate it so the bottom is at z=0.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
cavity = cq.Workplane("XY").box(board_x, board_y, 32 - 8).translate((0, 0, 8 + (32 - 8) / 2))
main_body = main_body.cut(cavity)

# 3. Add Screw Bosses (R5) and Subtract Pilot Holes (R5)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        
        # Create cylinder: OD 6mm, height 6mm (from z=2 to z=8)
        # We use workplane(offset=2) and extrude to ensure it starts at the floor top.
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=boss_start_z)
            .circle(boss_od / 2)
            .extrude(boss_end_z - boss_start_z)
            .translate((bx, by, 0))
        )
        main_body = main_body.union(boss_cyl)

        # Subtract Pilot Hole: Diameter 2.2mm, from z=8 down to z=2
        hole = (
            cq.Workplane("XY")
            .workplane(offset=boss_start_z)
            .circle(boss_hole_d / 2)
            .extrude(boss_end_z - boss_start_z)
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 4. Subtract USB-C Cutout (R6)
# Opening spanning x from -43 to -39, y from -4.5 to 4.5, z from 12.5 to 15.5
# A box of width 4 centered at -41 spans from -43 to -39.
usb_cutout = cq.Workplane("XY").box(4, 9, 3).translate((-41, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body