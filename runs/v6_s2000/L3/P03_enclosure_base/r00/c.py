import cadquery as cq

# Dimensions
outer_x = 85.0
outer_y = 55.0
wall_thickness = 2.5
floor_height = 8.0
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
# The cavity is centered in X and Y
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)

# 3. Create Screw Bosses (R5)
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        b = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .circle(boss_od / 2)
            .extrude(floor_height)
            .translate((sx * boss_x, sy * boss_y, 0))
        )
        bosses = bosses.union(b)

# Subtract holes from bosses
boss_holes = (
    cq.Workplane("XY")
    .workplane(offset=floor_height - boss_hole_depth)
    .center(boss_x, boss_y) # This is a simplified way; better to iterate
)
# Correct approach for holes: subtract from the bosses object
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bosses = (
            bosses.faces(">Z").workplane()
            .center(sx * boss_x, sy * boss_y)
            .hole(boss_hole_d, boss_hole_depth)
        )

# 4. USB-C Cutout (R6)
# The wall is at x = -42.5. We cut through the -X face.
usb_cutout = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(-outer_x/2, 0) # Move to X-wall center
    .rect(wall_thickness + 2, usb_w) # Ensure it cuts through
    # We'll use a different approach: create a box and subtract
)

# Constructing the final part using boolean operations
# Start with floor and walls
main_body = base_block.cut(cavity)

# Add bosses to main body
result = main_body.union(bosses)

# Subtract USB cutout (R6)
# Cutout is on the -X wall, centered at y=0, z=14
# We create a small box that intersects the wall and subtract it
cutout_box = (
    cq.Workplane("XY")
    .box(wall_thickness + 5, usb_w, usb_h)
    .translate((-outer_x/2, 0, usb_z))
)

result = result.cut(cutout_box)

# Final check: ensure the floor is solid under the board area (R2)
# The cavity starts at z=8, so the material from z=0 to z=8 is the floor.