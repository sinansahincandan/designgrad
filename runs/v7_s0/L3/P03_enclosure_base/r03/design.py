import cadquery as cq

# Dimensions
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
boss_height = 6.0 # From z=2 to z=8

usb_cutout_dims = (10.0, 12.0, 6.0) # X, Y, Z
usb_center = (-42.5, 0.0, 14.0)

# --- STEP 1: Build the additive components (Floor + Walls + Bosses) ---

# 1. Floor: z from 0 to 2
floor = cq.Workplane("XY").box(outer_x, outer_y, floor_thickness).translate((0, 0, floor_thickness / 2))

# 2. Walls: Outer perimeter 85x55, top at z=31. 
# We create a solid block from z=2 to z=31 and subtract the inner volume.
inner_x = outer_x - (2 * wall_thickness)
inner_y = outer_y - (2 * wall_thickness)
walls = (
    cq.Workplane("XY")
    .box(outer_x, outer_y, wall_height - floor_thickness)
    .translate((0, 0, (wall_height - floor_thickness) / 2 + floor_thickness))
    .cut(cq.Workplane("XY").box(inner_x, inner_y, wall_height).translate((0, 0, wall_height / 2)))
)

# 3. Bosses: Cylinders from z=2 to z=8
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2) # Start at top of floor
            .circle(boss_od / 2)
            .extrude(boss_height)
            .translate((bx, by, 0))
        )
        bosses = bosses.union(boss_cyl)

# Combine additive parts
main_body = floor.union(walls).union(bosses)

# --- STEP 2: Build the subtractive components (Cavity + Holes + Cutout) ---

# R3: Board cavity (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32)
cavity = cq.Workplane("XY").box(board_x, board_y, cavity_z_end - cavity_z_start).translate((0, 0, (cavity_z_start + cavity_z_end) / 2))

# R5: Pilot holes in bosses (diameter 2.2, from z=2 to z=8)
holes = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_hole_d / 2)
            .extrude(boss_height)
            .translate((bx, by, 0))
        )
        holes = holes.union(hole_cyl)

# R6: USB-C cutout through the -X wall
usb_cutout = (
    cq.Workplane("XY")
    .box(*usb_cutout_dims)
    .translate(usb_center)
)

# Apply all subtractions to the main body
result = main_body.cut(cavity).cut(holes).cut(usb_cutout)