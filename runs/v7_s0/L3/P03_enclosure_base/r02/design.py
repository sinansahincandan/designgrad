import cadquery as cq

# Dimensions from Design Document
outer_x, outer_y = 85.0, 55.0
floor_thickness = 2.0
wall_height = 31.0
wall_thickness = 2.5

board_x, board_y = 80.0, 50.0
cavity_z_start = 8.0
cavity_z_end = 32.0

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_z_start = 2.0
boss_z_end = 8.0

# USB-C Cutout (R6)
# x in [-44, -40], y in [-4.5, 4.5], z in [12.5, 15.5]
usb_x_min, usb_x_max = -44.0, -40.0
usb_y_min, usb_y_max = -4.5, 4.5
usb_z_min, usb_z_max = 12.5, 15.5

# --- STEP 1: Build Additive Components (Floor + Walls + Bosses) ---

# Create the Floor (R2)
floor = cq.Workplane("XY").box(outer_x, outer_y, floor_thickness).translate((0, 0, floor_thickness / 2))

# Create the Walls (R4)
# We create a hollow shell by taking a large block and subtracting a smaller inner block
wall_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, (floor_thickness + wall_height) / 2))
inner_void = cq.Workplane("XY").box(outer_x - 2*wall_thickness, outer_y - 2*wall_thickness, wall_height).translate((0, 0, (floor_thickness + wall_height) / 2))
walls = wall_block.cut(inner_void)

# Create the Bosses (R5)
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Each boss is a cylinder from z=2 to z=8
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=boss_z_start)
            .circle(boss_od / 2)
            .extrude(boss_z_end - boss_z_start)
            .translate((bx, by, 0))
        )
        bosses = bosses.union(boss_cyl)

# Combine additive parts (R1)
main_body = floor.union(walls).union(bosses)

# --- STEP 2: Build Subtractive Components (Cavity + Holes + Cutout) ---

# Board Cavity (R3)
# x in [-40, 40], y in [-25, 25], z in [8, 32]
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, cavity_z_end - cavity_z_start)
    .translate((0, 0, (cavity_z_start + cavity_z_end) / 2))
)

# Pilot Holes (R5)
pilot_holes = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=boss_z_start)
            .circle(boss_hole_d / 2)
            .extrude(boss_z_end - boss_z_start)
            .translate((bx, by, 0))
        )
        pilot_holes = pilot_holes.union(hole)

# USB-C Cutout (R6)
usb_cutout = (
    cq.Workplane("XY")
    .box(usb_x_max - usb_x_min, usb_y_max - usb_y_min, usb_z_max - usb_z_min)
    .translate(((usb_x_max + usb_x_min)/2, (usb_y_max + usb_y_min)/2, (usb_z_max + usb_z_min)/2))
)

# Apply all subtractions to the main body
result = main_body.cut(cavity).cut(pilot_holes).cut(usb_cutout)