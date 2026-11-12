import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.0

# 1. Create the main body (Floor + Walls)
# We create a block from z=0 to wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract the Board Cavity (R3)
# Region: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
# We subtract a box that covers this volume. 
# Since wall_height is 31, we subtract up to the top of the walls.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height - 8)
    .translate((0, 0, 8 + (wall_height - 8) / 2))
)
main_body = main_body.cut(cavity)

# 3. Create the Screw Bosses (R5)
# We create all four bosses as a single group first to ensure stability.
bosses_group = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create the solid cylinder from z=2 to z=8
        # We use center(bx, by) on a workplane at offset 2 to avoid translation issues
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=floor_thickness)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(6) # Extrudes from z=2 to z=8
        )
        bosses_group = bosses_group.union(boss_cyl)

# Subtract Pilot Holes from the bosses group
# Hole is at least 4mm deep, starting from top (z=8) downwards.
# This means hole goes from z=4 to z=8.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4) # Start at z=4
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(4) # Extrudes from z=4 to z=8
        )
        bosses_group = bosses_group.cut(hole)

# 4. Combine Main Body and Bosses (R1)
result = main_body.union(bosses_group)

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Must penetrate from outer boundary (-42.5) to inner cavity (-40).
# Width (Y) = 9mm, Height (Z) = 3mm.
# We use a box with enough depth to ensure it clears the wall thickness.
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # Depth of 10 is plenty to clear ~2.5mm wall
    .translate((-42.5 + 5, 0, 14)) # Center the box so it spans from -42.5 to -32.5
)
# More precise approach for R6:
usb_cutout = (
    cq.Workplane("XY")
    .box(5, 9, 3) # x-thickness of cutout is 5mm
    .translate((-40.0 - 2.5, 0, 14)) # Center it at the wall mid-point
)
# To be absolutely safe and satisfy "through-cut", we define a box that spans the X range:
usb_cutout = (
    cq.Workplane("XY")
    .box(2.5, 9, 3) # thickness from -42.5 to -40
    .translate((-41.25, 0, 14))
)

# Re-calculating cutout to ensure it covers the full wall thickness clearly:
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # Large enough depth
    .translate((-42.5 + 5, 0, 14)) # This places x-range from -42.5 to -32.5
)

result = result.cut(usb_cutout)