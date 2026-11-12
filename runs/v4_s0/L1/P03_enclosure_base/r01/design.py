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
# We create a solid block that covers the outer dimensions and height.
# The floor is z=0 to z=2, walls go up to wall_height.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create the board cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We subtract this volume from the main body.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height)
    .translate((0, 0, 8 + wall_height / 2)) # Center the cavity vertically starting at z=8
)
# To ensure we only subtract from z=8 upwards:
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height - 8)
    .translate((0, 0, 8 + (wall_height - 8) / 2))
)
main_body = main_body.cut(cavity)

# 3. Create the screw bosses (R5)
# We create all four boss cylinders first to ensure a clean union.
bosses_list = []
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Bosses from z=0 up to z=8
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .circle(boss_od / 2)
            .extrude(8)
            .translate((bx, by, 0))
        )
        bosses_list.append(boss_cyl)

# Combine all bosses into one object and union with main body
all_bosses = bosses_list[0]
for i in range(1, len(bosses_list)):
    all_bosses = all_bosses.union(bosses_list[i])

main_body = main_body.union(all_bosses)

# 4. Subtract Pilot Holes from bosses (R5)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole starts at z=8 and goes down to z=4 (depth of 4mm)
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4) # Start extrusion from z=4
            .circle(boss_hole_d / 2)
            .extrude(4)           # Extrude up to z=8
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Through-cut: width in X should be enough to clear the wall thickness.
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # x=10 (depth), y=9 (width), z=3 (height)
    .translate((-outer_x / 2, 0, 14))
)
main_body = main_body.cut(usb_cutout)

result = main_body