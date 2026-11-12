import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
# R5: Hole from z=4 to z=8 (depth of 4mm)

# --- STEP 1: Build the additive components (Floor + Walls + Bosses) ---

# Create the main shell (Floor and Walls)
# We create a block that goes from z=0 up to wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# Add the bosses (cylinders from floor at z=2 up to z=8)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Boss goes from z=2 to z=8 (height of 6mm)
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_od / 2)
            .extrude(6)
            .translate((bx, by, 0))
        )
        main_body = main_body.union(boss_cyl)

# --- STEP 2: Build the subtractive components (Cavity + Holes + Cutout) ---

# R3: Board cavity (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32)
# The height is 32 - 8 = 24. Center Z is (8 + 32)/2 = 20.
cavity = cq.Workplane("XY").box(board_x, board_y, 24).translate((0, 0, 20))

# R6: USB-C cutout through the -X wall
# Centered at x=-42.5, y=0, z=14. Dimensions: X=5 (depth), Y=9 (width), Z=3 (height)
usb_cutout = cq.Workplane("XY").box(5, 9, 3).translate((-42.5, 0, 14))

# Apply all subtractions to the main body
main_body = main_body.cut(cavity)
main_body = main_body.cut(usb_cutout)

# R5: Boss pilot holes (from z=8 down to z=4)
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
        main_body = main_body.cut(hole)

result = main_body