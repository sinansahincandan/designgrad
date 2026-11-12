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
# We create a solid block from z=0 to wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create the screw bosses as a single object
all_bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Bosses span from z=2 to z=8 (height of 6)
        # We use center(bx, by) on a workplane offset to z=2
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=floor_thickness)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(6.0)
        )
        all_bosses = all_bosses.union(boss_cyl)

# Union bosses to the main body before subtracting cavities
main_body = main_body.union(all_bosses)

# 3. Subtract Board Cavity (R3)
# Region: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
# We use a box centered at the appropriate Z to represent the void
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # Height is large enough to clear top
    .translate((0, 0, 8 + (wall_height - 8) / 2))
)
main_body = main_body.cut(cavity)

# 4. Subtract Pilot Holes (R5)
# Hole at least 4mm deep, starting from top (z=8) downwards
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Workplane at z=8, center at boss location, extrude downwards
        hole = (
            cq.Workplane("XY")
            .workplane(offset=8)
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(-boss_hole_depth)
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# To ensure it pierces through, we make the box wider than the wall thickness.
# Wall is at x = -outer_x/2. We want the cutout to span from outside to inside.
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # Width=10 (X), Height=9 (Y), Depth=3 (Z) -> wait, rect/box params:
    # Let's use box(width_x, depth_y, height_z) for clarity
    # Requirement: 9mm wide (Y), 3mm high (Z).
    .box(10, 9, 3) 
    .translate((-outer_x/2 - 5, 0, 14)) # Move so it covers the wall and extends outside
)
# Re-defining cutout clearly to match R6: Y=9, Z=3, X spans through wall
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # x_dim=10, y_dim=9, z_dim=3
    .translate((-outer_x/2 - 5, 0, 14))
)
# Note: In CadQuery box(dx, dy, dz), dx is X, dy is Y, dz is Z.
# R6 says: 9mm wide (Y) and 3mm high (Z). 
# So we need: x_dim=large, y_dim=9, z_dim=3.
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # This creates a box with X-thickness 10, Y-width 9, Z-height 3
    .translate((-outer_x/2 - 5, 0, 14))
)

main_body = main_body.cut(usb_cutout)

result = main_body