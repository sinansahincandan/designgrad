import cadquery as cq

# Dimensions from Design Document
outer_x, outer_y = 85.0, 55.0
floor_thickness = 2.0
wall_height_top = 31.0
board_cavity_z_start = 8.0

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_end_z = 8.0  # Bosses extend from z=0 to z=8

usb_width_y = 9.0
usb_height_z = 3.0
usb_center_z = 14.0
usb_cutout_x_start = -42.5
usb_cutout_x_end = -39.0

# 1. Create the Floor (R2)
floor = cq.Workplane("XY").box(outer_x, outer_y, floor_thickness).translate((0, 0, floor_thickness / 2))

# 2. Create the Walls (R4)
# We create a hollow shell. A simple way is to take a solid block and subtract a slightly smaller inner block.
# The walls start from z=floor_thickness up to wall_height_top.
wall_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height_top - floor_thickness).translate((0, 0, floor_thickness + (wall_height_top - floor_thickness) / 2))
inner_void = cq.Workplane("XY").box(outer_x - 5.0, outer_y - 5.0, wall_height_top).translate((0, 0, wall_height_top / 2))
walls = wall_block.cut(inner_void)

# 3. Create the Bosses (R5)
all_bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Boss cylinder from z=0 to z=8
        boss_cyl = (
            cq.Workplane("XY")
            .circle(boss_od / 2)
            .extrude(boss_end_z)
            .translate((bx, by, 0))
        )
        all_bosses = all_bosses.union(boss_cyl)

# Combine base components (R1)
base_structure = floor.union(walls).union(all_bosses)

# 4. Perform Subtractions
# R3: Board Cavity (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32)
board_cavity = (
    cq.Workplane("XY")
    .box(80.0, 50.0, 32.0 - board_cavity_z_start)
    .translate((0, 0, board_cavity_z_start + (32.0 - board_cavity_z_start) / 2))
)

# R5: Pilot Holes (2.2mm diameter through the bosses z=0 to z=8)
all_holes = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .circle(boss_hole_d / 2)
            .extrude(boss_end_z)
            .translate((bx, by, 0))
        )
        all_holes = all_holes.union(hole)

# R6: USB-C Cutout (x in [-42.5, -39], y in [-4.5, 4.5], z in [12.5, 15.5])
usb_cutout = (
    cq.Workplane("XY")
    .box(usb_cutout_x_end - usb_cutout_x_start, usb_width_y, usb_height_z)
    .translate(((usb_cutout_x_start + usb_cutout_x_end) / 2, 0, usb_center_z))
)

# Final assembly of subtractions
result = base_structure.cut(board_cavity).cut(all_holes).cut(usb_cutout)