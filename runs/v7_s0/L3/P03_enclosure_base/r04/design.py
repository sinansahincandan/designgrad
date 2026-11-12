import cadquery as cq

# Dimensions
floor_thickness = 2.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0  # Total height from z=0 to z=31
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2

# Board cavity dimensions (R3)
board_x, board_y = 80.0, 50.0
cavity_z_start = 8.0
cavity_z_end = 32.0 # Note: Wall top is at 31, so this cuts through the top

# USB-C Cutout (R6) - Redefined per feedback and design doc
# x in [-43, -39.5], y in [-4.5, 4.5], z in [12.5, 15.5]
usb_width = 9.0
usb_height = 3.0
usb_depth = 3.5 # Spans from x=-43 to x=-39.5

# --- STEP 1: Build the additive components (Floor + Walls + Bosses) ---

# Create Floor (z=0 to z=2)
floor = cq.Workplane("XY").box(outer_x, outer_y, floor_thickness).translate((0, 0, floor_thickness / 2))

# Create Walls (from z=2 up to z=31)
# We build a hollow box by creating a large block and subtracting a slightly smaller inner block
wall_thickness = 2.5 # Derived from outer 85/55 and board 80/50
inner_x = outer_x - (2 * wall_thickness)
inner_y = outer_y - (2 * wall_thickness)
wall_height_val = wall_height - floor_thickness

walls = (
    cq.Workplane("XY")
    .workplane(offset=floor_thickness)
    .box(outer_x, outer_y, wall_height_val)
    .cut(cq.Workplane("XY").workplane(offset=floor_thickness).box(inner_x, inner_y, wall_height_val + 1))
)

# Create Bosses (z=2 to z=8)
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Extrude from top of floor (z=2) to z=8 (height 6)
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=floor_thickness)
            .circle(boss_od / 2)
            .extrude(6.0)
            .translate((bx, by, 0))
        )
        bosses = bosses.union(boss_cyl)

# Combine additive parts
main_body = floor.union(walls).union(bosses)

# --- STEP 2: Build the subtractive components (Cavity + USB Cutout + Pilot Holes) ---

# R3: Board cavity (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32)
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, cavity_z_end - cavity_z_start)
    .translate((0, 0, (cavity_z_end + cavity_z_start) / 2))
)

# R6: USB-C cutout through the -X wall
# Centered at y=0, z=14. Spans x from -43 to -39.5
usb_cutout = (
    cq.Workplane("XY")
    .box(usb_depth, usb_width, usb_height)
    .translate((-41.25, 0, 14)) # Center of x range [-43, -39.5] is -41.25
)

# R5: Boss pilot holes (from z=4 down to z=8)
pilot_holes = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole from z=4 to z=8 (depth of 4mm)
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4)
            .circle(boss_hole_d / 2)
            .extrude(4)
            .translate((bx, by, 0))
        )
        pilot_holes = pilot_holes.union(hole)

# Apply all subtractions to the main body
result = main_body.cut(cavity).cut(usb_cutout).cut(pilot_holes)