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
# The box is centered on origin, so we translate it so the bottom is at z=0
main_body = (
    cq.Workplane("XY")
    .box(outer_x, outer_y, wall_height)
    .translate((0, 0, wall_height / 2))
)

# 2. Subtract Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We create a box that covers this specific volume.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, 32 - 8) # Height is 24
    .translate((0, 0, 8 + (32 - 8) / 2)) # Center at z=20
)
main_body = main_body.cut(cavity)

# 3. Add Screw Bosses (R5)
# Bosses extend from the floor (z=0) up to z=8.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder from z=0 to z=8
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .circle(boss_od / 2)
            .extrude(8)
            .translate((bx, by, 0))
        )
        main_body = main_body.union(boss_cyl)

# 4. Subtract Pilot Holes (R5)
# Hole is at least 4mm deep, starting from the top of the boss (z=8) downwards.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=8) # Start at top of boss
            .circle(boss_hole_d / 2)
            .extrude(-boss_hole_depth) # Extrude downwards
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# To ensure it penetrates the entire wall thickness, we use a box that spans 
# from the outer face (-42.5) to well past the inner cavity boundary (-40).
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # X=10 ensures it cuts through the wall thickness (~2.5mm)
    .translate((-outer_x / 2 - 5, 0, 14)) # Center the box so it intersects the wall
)
main_body = main_body.cut(usb_cutout)

result = main_body