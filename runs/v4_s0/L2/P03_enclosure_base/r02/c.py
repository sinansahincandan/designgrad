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

# Step A: Create the base block (Floor + Walls)
# The floor is from z=0 to z=2. The walls go up to wall_height.
# We create a solid block that covers the outer dimensions and height, 
# then we will subtract the cavity later.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# Step B: Create the 4 screw bosses and union them with the main body
# Bosses extend from z=2 to z=8.
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder at (bx, by) from z=2 to z=8
        # We use a workplane at offset 2 and extrude 6mm
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_od / 2)
            .extrude(6)
            .translate((bx, by, 0))
        )
        bosses = bosses.union(boss_cyl)

# Union the bosses into the main body to ensure a single solid (R1)
main_body = main_body.union(bosses)

# Step C: Subtract the board cavity (R3)
# Region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We create a box representing this volume and subtract it.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # Height is large enough to cover the range
    .translate((0, 0, 8 + (wall_height - 8) / 2)) # Center it so bottom is at z=8
)
# To be precise with R3: x in [-40, 40], y in [-25, 25], z in [8, 32]
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, 32 - 8)
    .translate((0, 0, 8 + (32 - 8) / 2))
)
main_body = main_body.cut(cavity)

# Step D: Subtract the 4 pilot holes (R5)
# Hole at least 4mm deep, starting from top (z=8) downwards.
# Target Z-range for hole: [4, 8]
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4) # Starts at z=4
            .circle(boss_hole_d / 2)
            .extrude(4) # Extends to z=8
            .translate((bx, by, 0))
        )
        main_body = main_body.cut(hole)

# Step E: Subtract the USB-C cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Use a slightly deeper box to ensure it cuts through the wall completely.
usb_cutout = (
    cq.Workplane("XY")
    .box(5, 9, 3) # width (Y)=9, height (Z)=3, depth (X)=5
    .translate((-outer_x/2 - 1, 0, 14)) # Move to -X face and slightly beyond
)
main_body = main_body.cut(usb_cutout)

result = main_body