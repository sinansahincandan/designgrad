import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2

# 1. Create the main body (Floor + Walls)
# We create a solid block of outer dimensions and height.
# The floor starts at z=0, so the box center is at wall_height/2.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract Board Cavity (R3)
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
        # Correct Boss Construction: Start at floor top (z=2), center at bx/by, extrude up to z=8.
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2) 
            .center(bx, by)      
            .circle(boss_od / 2) 
            .extrude(6)          
        )
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
# Hole diameter 2.2mm, depth 4mm (from z=8 down to z=4).
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Correct Pilot Hole: Start at z=4, extrude 4mm up to z=8.
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4) 
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(4)          
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Opening spans x in [-42.5, -37.5], y in [-4.5, 4.5], z in [12.5, 15.5].
# Center of X is (-42.5 + -37.5) / 2 = -40. Width (X-dim) is 5mm.
usb_cutout = cq.Workplane("XY").box(5, 9, 3).translate((-40, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body