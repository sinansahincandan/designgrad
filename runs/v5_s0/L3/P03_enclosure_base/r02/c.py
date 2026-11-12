import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_start_z = 2.0
boss_end_z = 8.0

# 1. Create the main body (Floor + Walls)
# We create a solid block from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Create the Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# We create a box representing this empty space and subtract it.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height) # Height covers the whole range to ensure clean cut
    .translate((0, 0, 8 + (wall_height - 8) / 2)) # Center it so bottom is at z=8
)
# Note: To strictly follow R3, we subtract a box that starts at z=8.
# Since our main body goes up to z=31, the cavity subtraction will work correctly.
main_body = main_body.cut(cavity)

# 3. Create the Screw Bosses (R5)
# We collect all boss cylinders and all pilot holes separately to perform single boolean operations.
all_bosses = cq.Workplane("XY")
all_holes = cq.Workplane("XY")

for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        
        # Create the solid cylinder for the boss (z=2 to z=8)
        boss_cyl = (
            cq.Workplane("XY")
            .circle(boss_od / 2)
            .extrude(boss_end_z - boss_start_z)
            .translate((bx, by, boss_start_z))
        )
        all_bosses = all_bosses.union(boss_cyl)
        
        # Create the pilot hole cylinder (z=2 to z=8)
        hole_cyl = (
            cq.Workplane("XY")
            .circle(boss_hole_d / 2)
            .extrude(boss_end_z - boss_start_z)
            .translate((bx, by, boss_start_z))
        )
        all_holes = all_holes.union(hole_cyl)

# Union bosses to the main body, then subtract holes from that unioned result
main_body = main_body.union(all_bosses)
main_body = main_body.cut(all_holes)

# 4. Create USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Width (Y) = 9mm, Height (Z) = 3mm. 
# We make it deep enough to ensure it cuts through the entire wall thickness.
usb_cutout = cq.Workplane("XY").box(10, 9, 3).translate((-outer_x/2, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body