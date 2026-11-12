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
boss_height = 8.0  # From z=0 to z=8

usb_w = 9.0
usb_h = 3.0
usb_z = 14.0

# 1. Create the main block (Floor + Walls)
# Base block centered in XY, bottom at z=0
main_body = cq.Workplane("XY").box(outer_x, outer_y, total_height).translate((0, 0, total_height / 2))

# 2. Subtract the board space (R3)
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)
main_body = main_body.cut(cavity)

# 3. Create Screw Bosses (R5)
# Create the four cylinders as a single object first
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        b = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .circle(boss_od / 2)
            .extrude(boss_height)
            .translate((sx * boss_x, sy * boss_y, boss_height / 2))
        )
        if bosses.objects:
            bosses = bosses.union(b)
        else:
            bosses = b

# Subtract the pilot holes from the bosses (spanning full height z=0 to z=8)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bosses = (
            bosses.faces(">Z").workplane()
            .center(sx * boss_x, sy * boss_y)
            .hole(boss_hole_d, boss_height + 2) # Ensure it clears the bottom
        )

# Integrate bosses into main body
result = main_body.union(bosses)

# 4. USB-C Cutout (R6)
# Define a box that bridges the wall and the cavity
# Centered at (-42.5, 0, 14). Dimensions: width=10 (to ensure cut), height=9 (Y), depth=3 (Z)
# Note: The feedback suggests dimensions 10x9x3 for a clean cut.
cutout_box = (
    cq.Workplane("XY")
    .box(10.0, usb_w + 1.0, usb_h + 1.0) # Slightly larger to ensure clean intersection
    .translate((-42.5, 0, usb_z))
)

result = result.cut(cutout_box)

# Final assignment to 'result' as required