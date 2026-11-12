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
boss_hole_depth = 6.0 # Extends from z=8 down to z=2

usb_w = 9.0  # Y dimension
usb_h = 3.0  # Z dimension
usb_z = 14.0 # Center of cutout in Z

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

# 3. Create Screw Bosses (R5)
boss_solids = []
for sx in [-1, 1]:
    for sy in [-1, 1]:
        # Create a single boss with its hole already subtracted
        # Extrude from z=0 to z=8
        b = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .center(sx * boss_x, sy * boss_y)
            .circle(boss_od / 2)
            .extrude(8.0) 
            .faces(">Z").workplane()
            .hole(boss_hole_d, boss_hole_depth)
        )
        boss_solids.append(b)

# Combine all bosses into one object
bosses = boss_solids[0]
for i in range(1, len(boss_solids)):
    bosses = bosses.union(boss_solids[i])

# 4. USB-C Cutout (R6)
# Create a box that spans from outside the wall to inside the cavity
# Wall is at x = -42.5, Cavity edge is at x = -40.
# We use a width of 10mm in X to ensure it cuts through completely.
cutout_box = (
    cq.Workplane("XY")
    .box(10.0, usb_w, usb_h) 
    .translate((-outer_x/2, 0, usb_z))
)

# Constructing the final part using boolean operations
# Start with main body (Floor + Walls - Cavity)
main_body = base_block.cut(cavity)

# Add bosses to main body and then subtract the USB cutout
result = (main_body.union(bosses)).cut(cutout_box)