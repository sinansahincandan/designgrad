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
boss_height = 8.0

usb_w = 9.0  # Y dimension (width)
usb_h = 3.0  # Z dimension (height)
usb_z = 14.0 # Center Z

# 1. Create the main body (Floor + Walls)
# We create a solid block and then subtract the board space cavity.
# The base is from z=0 to z=32.
main_body = cq.Workplane("XY").box(outer_x, outer_y, total_height).translate((0, 0, total_height / 2))

# 2. Subtract the Board Space (R3)
# Cavity: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)

main_body = main_body.cut(cavity)

# 3. Create Screw Bosses (R5)
# Each boss is a cylinder from z=0 to z=8 with a hole through it.
boss_solids = []
for sx in [-1, 1]:
    for sy in [-1, 1]:
        cx = sx * boss_x
        cy = sy * boss_y
        # Create the solid cylinder for the boss
        b = (
            cq.Workplane("XY")
            .cylinder(boss_od / 2, boss_height)
            .translate((cx, cy, boss_height / 2))
        )
        # Subtract the hole from this specific boss
        h = (
            cq.Workplane("XY")
            .cylinder(boss_hole_d / 2, boss_height)
            .translate((cx, cy, boss_height / 2))
        )
        boss_solids.append(b.cut(h))

# Union all bosses into the main body
result = main_body
for b_solid in boss_solids:
    result = result.union(b_solid)

# 4. USB-C Cutout (R6)
# Opening at least 9mm wide (Y) and 3mm high (Z), centered at y=0, z=14.
# The cutout is on the -X wall. We use a box to subtract.
# Dimensions: width (along Y) = usb_w, height (along Z) = usb_h, depth (along X) = enough to clear wall
cutout_box = (
    cq.Workplane("XY")
    .box(outer_x + 2, usb_w, usb_h) # width here is actually the Y dimension in box() call
    .translate((-outer_x/2, 0, usb_z))
)

# Note: cq.Workplane.box(dx, dy, dz) -> dx is X, dy is Y, dz is Z.
# To get a cutout that is 9mm wide in Y and 3mm high in Z:
cutout_box = (
    cq.Workplane("XY")
    .box(outer_x + 2, usb_w, usb_h) # X=large, Y=9, Z=3
    .translate((-outer_x/2, 0, usb_z))
)

result = result.cut(cutout_box)

# Final check: The resulting object is a single solid.