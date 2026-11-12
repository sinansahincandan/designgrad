import cadquery as cq

# Dimensions
outer_x = 85.0
outer_y = 55.0
wall_height = 32.0
floor_thickness = 2.0

board_x_min, board_x_max = -40.0, 40.0
board_y_min, board_y_max = -25.0, 25.0
board_z_bottom = 8.0
board_z_top = 32.0

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 6.0  # From z=8 down to z=2

cutout_w_y = 9.0  # Width in Y direction
cutout_h_z = 3.0  # Height in Z direction

# 1. Create the main block (Floor + Walls)
# We create a solid block and then subtract the board cavity to form the shell
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height)
# Move so floor is at z=0 (center of box was at z=wall_height/2)
base_block = base_block.translate((0, 0, wall_height / 2))

# 2. Subtract the board space (R3)
board_cavity = (cq.Workplane("XY")
                .box(board_x_max - board_x_min, 
                     board_y_max - board_y_min, 
                     board_z_top - board_z_bottom)
                .translate((0, 0, (board_z_bottom + board_z_top) / 2)))

main_body = base_block.cut(board_cavity)

# 3. Create the bosses (R5)
# We create cylinders at the specific locations and union them to the main body
boss_positions = [
    (boss_x, boss_y), (boss_x, -boss_y),
    (-boss_x, boss_y), (-boss_x, -boss_y)
]

bosses = cq.Workplane("XY")
for px, py in boss_positions:
    # Create a cylinder from z=floor_thickness to z=board_z_bottom
    b = (cq.Workplane("XY")
         .workplane(offset=floor_thickness)
         .cylinder(boss_od / 2, board_z_bottom - floor_thickness)
         .translate((px, py, 0)))
    bosses = bosses.union(b)

# Combine main body and bosses
result = main_body.union(bosses)

# 4. Subtract the boss holes (R5)
# To ensure they are "open", we subtract them from the combined solid
for px, py in boss_positions:
    hole = (cq.Workplane("XY")
            .workplane(offset=board_z_bottom - boss_hole_depth)
            .cylinder(boss_hole_d / 2, boss_hole_depth)
            .translate((px, py, 0)))
    result = result.cut(hole)

# 5. USB-C Cutout (R6)
# Subtract a box that spans from the outer X boundary to the inner wall
# Outer X is -42.5, Inner X is -40.0. Center at y=0, z=14.
cutout_thickness = 3.0 # Ensures it clears the wall thickness
cutout = (cq.Workplane("XY")
          .box(cutout_thickness, cutout_w_y, cutout_h_z)
          .translate((-41.25, 0, 14)))

result = result.cut(cutout)