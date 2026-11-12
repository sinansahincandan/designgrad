import cadquery as cq

# Dimensions
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
floor_thickness = 2.0

board_x, board_y = 80.0, 50.0
cavity_z_start = 8.0
# Cavity goes up to wall top (31) or higher; we subtract the specified region
cavity_z_end = 32.0 

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.0 # From z=8 down to z=4

# USB-C Cutout (R6)
cutout_width_y = 9.0
cutout_height_z = 3.0
cutout_depth_x = 5.0 # Ensures it penetrates the wall

# 1. Create Main Body (Floor + Walls)
# We create a solid block from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create Bosses (R5)
# Bosses extend from z=0 to z=8
bosses_combined = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create a cylinder at the specific location
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(8.0)
        )
        bosses_combined = bosses_combined.union(boss_cyl)

# 3. Create Pilot Holes (R5)
# Holes are from z=4 to z=8 (open at top)
holes_combined = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4.0) # Start at z=4
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(4.0) # Extrude up to z=8
        )
        holes_combined = holes_combined.union(hole)

# 4. Create Board Cavity (R3)
# Region: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, cavity_z_end - cavity_z_start)
    .translate((0, 0, cavity_z_start + (cavity_z_end - cavity_z_start) / 2))
)

# 5. Create USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall (x = -42.5)
usb_cutout = (
    cq.Workplane("XY")
    .box(cutout_depth_x, cutout_width_y, cutout_height_z)
    .translate((-outer_x / 2, 0, 14))
)

# Final Boolean Assembly (R1)
# Combine main body and bosses, then subtract cavity, holes, and cutout
result = (main_body.union(bosses_combined)).cut(cavity).cut(holes_combined).cut(usb_cutout)