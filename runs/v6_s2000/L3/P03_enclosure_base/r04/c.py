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

usb_w = 9.0  # Y dimension (width)
usb_h = 3.0  # Z dimension (height)
usb_z = 14.0 # Center Z
usb_x_center = -41.25 # Midpoint of wall thickness (-42.5 to -40)

# 1. Create the main shell (Outer box minus internal cavity)
# We create a solid block and subtract the board space
main_shell = (
    cq.Workplane("XY")
    .box(outer_x, outer_y, total_height)
    .translate((0, 0, total_height / 2)) # Bottom at z=0
)

cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)

main_body = main_shell.cut(cavity)

# 2. Create Screw Bosses (R5)
# Each boss is a cylinder with a hole through its full height
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        x_pos = sx * boss_x
        y_pos = sy * boss_y
        
        # Create the solid cylinder for one boss
        single_boss = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .cylinder(boss_od / 2, boss_height)
            .translate((x_pos, y_pos, boss_height / 2))
        )
        
        # Subtract the hole from this specific boss
        single_boss_with_hole = (
            single_boss.faces(">Z").workplane()
            .center(0, 0)
            .hole(boss_hole_d, boss_height + 2) # Ensure it clears top/bottom
        )
        
        # Union this boss into the collection
        if sx == -1 and sy == -1:
            bosses = single_boss_with_hole
        else:
            bosses = bosses.union(single_boss_with_hole)

# Combine shell and bosses
result = main_body.union(bosses)

# 3. USB-C Cutout (R6)
# The cutout spans the wall thickness from x=-42.5 to x=-40
# Dimensions: X=2.5, Y=9, Z=3
cutout_box = (
    cq.Workplane("XY")
    .box(outer_x/2 - board_x/2 + 2, usb_w, usb_h) # Width covers wall thickness
    .translate((usb_x_center, 0, usb_z))
)

# Final subtraction for the cutout
result = result.cut(cutout_box)