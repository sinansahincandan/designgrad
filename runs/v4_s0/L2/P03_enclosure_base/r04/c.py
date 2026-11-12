import cadquery as cq

# Dimensions
outer_x, outer_y = 85.0, 55.0
floor_thickness = 2.0
wall_height = 31.0
board_x, board_y = 80.0, 50.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 6.0  # From z=8 down to z=2

# 1. Create the Floor (z from 0 to 2)
floor = cq.Workplane("XY").box(outer_x, outer_y, floor_thickness).translate((0, 0, floor_thickness / 2))

# 2. Create the Walls (from z=2 up to wall_height)
# We create a hollow box by subtracting a smaller box from a larger one
walls = (
    cq.Workplane("XY")
    .workplane(offset=floor_thickness)
    .box(outer_x, outer_y, wall_height - floor_thickness)
    .cut(
        cq.Workplane("XY")
        .workplane(offset=floor_thickness)
        .box(outer_x - 5.0, outer_y - 5.0, wall_height) # Wall thickness approx 2.5mm
    )
    .translate((0, 0, (wall_height - floor_thickness) / 2))
)

# 3. Create the Bosses (cylinders at (+-35, +-20) from z=2 to z=8)
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create a single cylinder for each boss location
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=floor_thickness)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(6.0) # Extends from z=2 to z=8
        )
        bosses = bosses.union(boss_cyl)

# 4. Perform Boolean Union of Floor, Walls, and Bosses
main_body = floor.union(walls).union(bosses)

# 5. Subtract Board Cavity (R3: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32)
board_cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, 32.0 - 8.0)
    .translate((0, 0, 8.0 + (32.0 - 8.0) / 2))
)
main_body = main_body.cut(board_cavity)

# 6. Subtract USB-C Cutout (R6: centered at y=0, z=14 on the -X wall)
# X dimension is large enough to ensure it cuts through the wall into the cavity
usb_cutout = (
    cq.Workplane("XY")
    .box(10.0, 9.0, 3.0)
    .translate((-outer_x / 2, 0, 14.0))
)
main_body = main_body.cut(usb_cutout)

# 7. Subtract Pilot Holes (R5: 2.2mm diameter from z=8 down to z=2)
pilot_holes = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=floor_thickness)
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(6.0) # From z=2 to z=8
        )
        pilot_holes = pilot_holes.union(hole)

main_body = main_body.cut(pilot_holes)

result = main_body