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
boss_hole_depth = 4.0  # From z=8 down to z=4

# 1. Create the main block (Floor + Walls)
# We create a solid block and subtract the board cavity
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height)
# Move so floor is at z=0 (center of box is at z=wall_height/2)
base_block = base_block.translate((0, 0, wall_height / 2))

# 2. Subtract the board space (R3)
board_cavity = (cq.Workplane("XY")
                .box(board_x_max - board_x_min, 
                     board_y_max - board_y_min, 
                     board_z_top - board_z_bottom)
                .translate((0, 0, (board_z_bottom + board_z_top) / 2)))

main_body = base_block.cut(board_cavity)

# 3. Create the bosses (R5)
boss_positions = [
    (boss_x, boss_y), (boss_x, -boss_y),
    (-boss_x, boss_y), (-boss_x, -boss_y)
]

all_bosses = cq.Workplane("XY")
for px, py in boss_positions:
    # Create the solid cylinder for the boss (z=0 to z=8)
    boss_cyl = (cq.Workplane("XY")
                .cylinder(boss_od / 2, 8.0)
                .translate((px, py, 4.0))) # center at z=4 so bottom is at 0 and top at 8
    
    # Create the hole cylinder (z=4 to z=8)
    hole_cyl = (cq.Workplane("XY")
                .cylinder(boss_hole_d / 2, boss_hole_depth)
                .translate((px, py, 8.0 - (boss_hole_depth / 2))))
    
    # Subtract hole from boss
    single_boss = boss_cyl.cut(hole_cyl)
    all_bosses = all_bosses.union(single_boss)

# 4. Combine main body and bosses
result = main_body.union(all_bosses)

# 5. USB-C Cutout (R6)
# Opening at least 9mm wide (Y) and 3mm high (Z), centered at y=0, z=14.
# The -X wall is located at x = -outer_x/2 = -42.5
cutout_w_y = 9.0
cutout_h_z = 3.0

# We use a box to cut through the wall for robustness
cutout_box = (cq.Workplane("XY")
              .box(10.0, cutout_w_y, cutout_h_z)
              .translate((-outer_x/2 - 5.0, 0, 14.0)))

result = result.cut(cutout_box)