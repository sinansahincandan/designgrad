import cadquery as cq

# Dimensions
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0

board_x, board_y = 80.0, 50.0
cavity_z_start = 8.0

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.0  # From z=8 down to z=4

usb_width_y = 9.0
usb_height_z = 3.0
usb_center_z = 14.0

# 1. Create the main body (R4: Continuous walls and floor)
# A solid block from z=0 to z=31
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Add the Bosses (R5: Integrated into floor)
# We add them as cylinders from z=0 to z=8 before subtracting the cavity
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder from z=0 to z=8
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(8.0)
        )
        bosses = bosses.union(boss_cyl)

# Combine main body and bosses (R1: Single solid)
main_body = main_body.union(bosses)

# 3. Subtract the Board Cavity (R3)
# Region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# Since our wall top is at 31, we subtract from z=8 to z=31.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # height is arbitrary as long as it covers the range
    .translate((0, 0, 8 + (wall_height - 8) / 2)) # Center it so bottom is at z=8
)
# More precise cavity subtraction to ensure R3:
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height)
    .translate((0, 0, 8 + (wall_height - 8)/2))
)
# To be safe and precise with the Z range:
cavity = cq.Workplane("XY").box(board_x, board_y, wall_height).translate((0, 0, 8 + (wall_height-8)/2))
# Actually, let's just define a box that covers z=8 to z=31 exactly:
cavity = cq.Workplane("XY").box(board_x, board_y, wall_height).translate((0, 0, 8 + (wall_height-8)/2))
# Re-calculating cavity to be exact:
cavity = cq.Workplane("XY").workplane(offset=8).rect(board_x, board_y).extrude(wall_height - 8)
# Wait, rect is 2D. Let's use box for simplicity:
cavity = cq.Workplane("XY").box(board_x, board_y, wall_height).translate((0, 0, 8 + (wall_height-8)/2))

main_body = main_body.cut(cavity)

# 4. Subtract the USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# We extrude through the wall thickness.
usb_cutout = (
    cq.Workplane("XY")
    .workplane(offset=usb_center_z)
    .center(-outer_x/2, 0)
    .rect(usb_height_z, usb_width_y) # rect(width, height) -> x is width, y is height in local plane? 
    # In CadQuery .rect(w, h), w is along X, h is along Y.
    # We want Z=14 (offset), Y-width=9, Z-height=3. 
    # Since we are on the XY plane with offset Z, rect(3, 9) gives width 3 (along X) and height 9 (along Y).
    .extrude(10, both=True) # Extrude through the wall
)
# Let's refine the cutout to be exactly as requested: 9mm wide (Y), 3mm high (Z)
usb_cutout = (
    cq.Workplane("XY")
    .workplane(offset=usb_center_z)
    .center(-outer_x/2, 0)
    .rect(5, usb_width_y) # width 5 in X to ensure it cuts through the wall thickness
    # Wait, rect(w, h) -> w is along local X, h is along local Y.
    # We want height (Z) = 3, width (Y) = 9.
    # The workplane is XY at Z=14. So 'h' in rect is the Y dimension.
    # To get a 3mm height in Z, we can't use .rect() on an XY plane easily for Z-height.
    # Let's use a box instead.
)

usb_cutout = cq.Workplane("XY").box(10, usb_width_y, usb_height_z).translate((-outer_x/2, 0, usb_center_z))
main_body = main_body.cut(usb_cutout)

# 5. Subtract Pilot Holes (R5)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole at least 4mm deep, starting from top (z=8) downwards.
        # Top is z=8, depth 4 means hole goes from z=8 to z=4.
        hole = (
            cq.Workplane("XY")
            .workplane(offset=8 - boss_hole_depth)
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(boss_hole_depth)
        )
        main_body = main_body.cut(hole)

result = main_body