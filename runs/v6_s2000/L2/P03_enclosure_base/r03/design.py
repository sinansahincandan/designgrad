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
boss_height = 6.0  # From z=8 to z=14
boss_hole_depth = 6.0

usb_w = 9.0
usb_h = 3.0
usb_z = 14.0

# 1. Create the main block (Floor + Walls)
# We create a solid box and subtract the internal cavity.
# The base is placed such that its bottom face is at z=0.
base_block = cq.Workplane("XY").box(outer_x, outer_y, total_height).translate((0, 0, total_height / 2))

# 2. Define the Board Space Cavity (R3)
# The cavity is centered in X and Y, from z=8 to z=32.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)

# Subtract cavity from base to get the main body (Floor and Walls)
main_body = base_block.cut(cavity)

# 3. Create Screw Bosses (R5)
# Bosses extend from z=8 up to z=14.
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        # Create individual boss with hole
        b = (
            cq.Workplane("XY")
            .circle(boss_od / 2)
            .extrude(boss_height)
            .translate((sx * boss_x, sy * boss_y, board_z_start))
            .faces(">Z").workplane()
            .hole(boss_hole_d, boss_hole_depth)
        )
        # Union into the collection of bosses
        if bosses.objects:
            bosses = bosses.union(b)
        else:
            bosses = b

# 4. Combine Main Body and Bosses (R1)
result = main_body.union(bosses)

# 5. USB-C Cutout (R6)
# The cutout is on the -X wall, centered at y=0, z=14.
# We use a box that spans the thickness of the wall to ensure a clean cut.
cutout_box = (
    cq.Workplane("XY")
    .box(outer_x, usb_w, usb_h) # Large enough in X to ensure it cuts through
    .translate((-outer_x/2, 0, usb_z))
)

# Subtract the cutout from the result
result = result.cut(cutout_box)

# Final result is a single solid assigned to 'result'