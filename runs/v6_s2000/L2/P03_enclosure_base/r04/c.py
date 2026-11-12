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

# 1. Create the main block (Floor + Walls)
# We start with a solid block and subtract the internal cavity
base_block = cq.Workplane("XY").box(outer_x, outer_y, total_height)
# Move base so bottom is at z=0
base_block = base_block.translate((0, 0, total_height / 2))

# 2. Subtract the board space (R3)
# The cavity is centered in X and Y, from z=8 to z=32
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)

main_body = base_block.cut(cavity)

# 3. Create Screw Bosses (R5)
# Define the bosses as cylinders from z=0 to z=8 and union them into main_body
boss_solids = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        boss_solids = boss_solids.union(
            cq.Workplane("XY").center(sx * boss_x, sy * boss_y)
            .circle(boss_od / 2).extrude(8.0)
        )

result = main_body.union(boss_solids)

# Subtract holes from bosses (R5)
# Holes are 2.2mm diameter and 6mm deep, starting at z=8 downwards
for sx in [-1, 1]:
    for sy in [-1, 1]:
        result = (
            result.faces(">Z").workplane()
            .center(sx * boss_x, sy * boss_y)
            .hole(boss_hole_d, boss_hole_depth)
        )

# 4. USB-C Cutout (R6)
# The cutout is on the -X wall, centered at y=0, z=14
# We create a box that intersects the wall and subtract it
cutout_box = (
    cq.Workplane("XY")
    .box(outer_x, usb_w, usb_h) # Large enough to ensure clean cut through width
    .translate((-outer_x/2, 0, usb_z))
)

# We use a specific box for the cutout to ensure it cuts through the -X face correctly
cutout_box = (
    cq.Workplane("XY")
    .box(10, usb_w, usb_h) # Width of cut through wall
    .translate((-outer_x/2, 0, usb_z))
)

result = result.cut(cutout_box)