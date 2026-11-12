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
# Pilot hole depth: from z=8 down to z=4 (depth of 4mm)
boss_hole_depth = 4.0 

# 1. Create the main body (Outer block minus board cavity)
# The base block is centered on XY, so we translate it so floor starts at z=0
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# Subtract the board space (R3)
board_cavity = (cq.Workplane("XY")
                .box(board_x_max - board_x_min, 
                     board_y_max - board_y_min, 
                     board_z_top - board_z_bottom)
                .translate((0, 0, (board_z_bottom + board_z_top) / 2)))

main_body = base_block.cut(board_cavity)

# 2. Create the bosses with pilot holes (R5)
boss_positions = [
    (boss_x, boss_y), (boss_x, -boss_y),
    (-boss_x, boss_y), (-boss_x, -boss_y)
]

bosses_list = []
for px, py in boss_positions:
    # Create the solid boss cylinder from z=2 to z=8
    # Note: box() is centered, so we translate it. 
    # A cylinder from z=2 to z=8 has height 6 and center at z=5.
    boss_solid = (cq.Workplane("XY")
                  .cylinder(6.0, boss_od / 2)
                  .translate((px, py, 5.0)))
    
    # Create the pilot hole cylinder
    # The hole is open at z=8 and goes down to z=4 (depth 4)
    # Center of hole: z = 8 - (4/2) = 6
    hole_solid = (cq.Workplane("XY")
                  .cylinder(boss_hole_depth, boss_hole_d / 2)
                  .translate((px, py, 8.0 - (boss_hole_depth / 2))))
    
    # Subtract hole from boss before unioning to ensure topological integrity
    boss_with_hole = boss_solid.cut(hole_solid)
    bosses_list.append(boss_with_hole)

# Combine all bosses into one object
all_bosses = bosses_list[0]
for i in range(1, len(bosses_list)):
    all_bosses = all_bosses.union(bosses_list[i])

# 3. Union main body and bosses (R1)
result = main_body.union(all_bosses)

# 4. USB-C Cutout (R6)
# Centered at y=0, z=14. Width (Y) = 9mm, Height (Z) = 3mm.
# Spans from x=-42.5 to penetrate through the wall.
cutout_w = 9.0
cutout_h = 3.0
cutout_depth = 5.0 # Ensures it clears the wall thickness
cutout_box = (cq.Workplane("XY")
              .box(cutout_depth, cutout_w, cutout_h)
              .translate((-outer_x/2, 0, 14)))

result = result.cut(cutout_box)