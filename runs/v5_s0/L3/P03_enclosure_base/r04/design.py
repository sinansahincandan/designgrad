import cadquery as cq

# Dimensions
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
floor_thickness = 2.0

board_x, board_y = 80.0, 50.0
board_z_start = 8.0
board_z_end = 32.0

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_start_z = 2.0
boss_end_z = 8.0

# 1. Create the Main Body (Floor + Walls)
# We create a solid block from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create the Screw Bosses (R5)
# We create the bosses as separate solids to union them with the main body first
all_bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder from z=2 to z=8
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=boss_start_z)
            .circle(boss_od / 2)
            .extrude(boss_end_z - boss_start_z)
            .translate((bx, by, 0))
        )
        all_bosses = all_bosses.union(boss_cyl)

# Union Floor/Walls and Bosses (R1 compliance strategy)
combined_solid = main_body.union(all_bosses)

# 3. Subtract the Board Cavity (R3)
# Region: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, board_z_start + (board_z_end - board_z_start) / 2))
)
combined_solid = combined_solid.cut(cavity)

# 4. Subtract the Pilot Holes (R5)
# Holes are 2.2mm diameter from z=2 to z=8
all_holes = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole_cyl = (
            cq.Workplane("XY")
            .workplane(offset=boss_start_z)
            .circle(boss_hole_d / 2)
            .extrude(boss_end_z - boss_start_z)
            .translate((bx, by, 0))
        )
        all_holes = all_holes.union(hole_cyl)

combined_solid = combined_solid.cut(all_holes)

# 5. Subtract USB-C Cutout (R6)
# x range: [-42.5, -39], y range: [-4.5, 4.5] (9mm wide), z range: [12.5, 15.5] (3mm high centered at 14)
# We use a box and translate it to the correct position.
# Box dimensions: width_x = 3.5, width_y = 9, height_z = 3
usb_cutout = (
    cq.Workplane("XY")
    .box(3.5, 9.0, 3.0)
    .translate((-40.75, 0, 14.0)) # Center of [-42.5, -39] is -40.75
)
result = combined_solid.cut(usb_cutout)