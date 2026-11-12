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
floor_height = 8.0  # Bosses go from z=0 to z=8

usb_w = 9.0
usb_h = 3.0
usb_z = 14.0

# 1. Create the main block (Floor + Walls)
# A box centered at origin with height 32 spans -16 to 16.
# We translate it by total_height/2 so it spans 0 to 32.
base_block = cq.Workplane("XY").box(outer_x, outer_y, total_height).translate((0, 0, total_height / 2))

# 2. Subtract the board space (R3)
# The cavity is centered in X and Y, spanning z=8 to z=32.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)

# 3. Create Screw Bosses with holes (R5)
# We create each boss individually with its hole subtracted before unioning them.
boss_list = []
for sx in [-1, 1]:
    for sy in [-1, 1]:
        b = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .center(sx * boss_x, sy * boss_y)
            .circle(boss_od / 2)
            .extrude(floor_height)
            .faces(">Z").workplane()
            .hole(boss_hole_d, boss_hole_depth)
        )
        boss_list.append(b)

# Union all bosses into one object
bosses = boss_list[0]
for b in boss_list[1:]:
    bosses = bosses.union(b)

# 4. Construct the main body (Floor + Walls - Cavity + Bosses)
main_body = base_block.cut(cavity).union(bosses)

# 5. USB-C Cutout (R6)
# The cutout is on the -X wall. Outer X boundary is at -42.5.
# We use a box that extends slightly beyond the wall to ensure a clean cut.
cutout_box = (
    cq.Workplane("XY")
    .box(10.0, usb_w, usb_h) # Width 10 is enough to clear the wall thickness
    .translate((-outer_x/2, 0, usb_z))
)

# Final result: Subtract cutout from the main body
result = main_body.cut(cutout_box)