import cadquery as cq

# Dimensions
outer_x = 85.0
outer_y = 55.0
total_height = 32.0

board_x = 80.0
board_y = 50.0
board_z_start = 8.0
board_z_end = 32.0

boss_x, boss_y = 35.0, 20.0
boss_od = 7.0
boss_hole_d = 2.2
boss_hole_depth = 6.0

usb_w = 9.0
usb_h = 3.0
usb_z = 14.0

# 1. Create the main body (Floor + Walls)
# We create a block and subtract the internal cavity (R3)
# The base block is centered on XY, with bottom at z=0
main_body = (
    cq.Workplane("XY")
    .box(outer_x, outer_y, total_height)
    .translate((0, 0, total_height / 2))
)

# Subtract the board space cavity (R3)
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)

main_body = main_body.cut(cavity)

# 2. Create Screw Bosses (R5)
# Use pushPoints to create all four cylinders at once from z=0 to z=8
boss_points = [
    (boss_x, boss_y),
    (boss_x, -boss_y),
    (-boss_x, boss_y),
    (-boss_x, -boss_y)
]

bosses = (
    cq.Workplane("XY")
    .pushPoints(boss_points)
    .circle(boss_od / 2)
    .extrude(8.0) # Extends from z=0 to z=8
)

# Subtract the pilot holes from the bosses
# Holes are open at the top (z=8) and go down 6mm
bosses = (
    bosses.faces(">Z")
    .workplane()
    .pushPoints(boss_points)
    .hole(boss_hole_d, boss_hole_depth)
)

# 3. Combine Main Body and Bosses (R1)
result = main_body.union(bosses)

# 4. USB-C Cutout (R6)
# The cutout is on the -X wall, centered at y=0, z=14
# We create a box that intersects the wall and subtract it
cutout_box = (
    cq.Workplane("XY")
    .box(outer_x, usb_w, usb_h) # Width covers X dimension to ensure clean cut
    .translate((-outer_x/2, 0, usb_z))
)

# To ensure the cutout is specifically on the -X face and doesn't eat the whole part:
# We use a box that starts at the outer edge and goes inward
cutout_box = (
    cq.Workplane("XY")
    .box(10.0, usb_w, usb_h) 
    .translate((-outer_x/2, 0, usb_z))
)

result = result.cut(cutout_box)