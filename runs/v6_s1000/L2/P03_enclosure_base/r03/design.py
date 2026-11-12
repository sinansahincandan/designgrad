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
# Bosses extend from floor (z=2) up to board underside (z=8)
# Pilot hole extends from z=4 to z=8 as per design doc

# 1. Create the main block (Floor + Walls)
# We create a solid block and subtract the board cavity.
# The block starts at z=0 and goes to z=32.
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

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
    # Create the solid part of the boss (from z=2 to z=8)
    boss_cylinder = (cq.Workplane("XY")
                     .workplane(offset=floor_thickness)
                     .circle(boss_od / 2)
                     .extrude(board_z_bottom - floor_thickness)
                     .translate((px, py, 0)))
    
    # Create the pilot hole (from z=4 to z=8)
    # Note: translate is relative to XY plane, so we place it at z=4
    pilot_hole = (cq.Workplane("XY")
                  .workplane(offset=4.0)
                  .circle(boss_hole_d / 2)
                  .extrude(board_z_bottom - 4.0)
                  .translate((px, py, 0)))
    
    # Subtract hole from boss and add to collection
    single_boss = boss_cylinder.cut(pilot_hole)
    all_bosses = all_bosses.union(single_boss)

# Combine main body and bosses
result = main_body.union(all_bosses)

# 4. USB-C Cutout (R6)
# Defined by subtraction volume: -43 <= x <= -39, -4.5 <= y <= 4.5, 12.5 <= z <= 15.5
# Center of this box in X is -41, Y is 0, Z is 14.
# Dimensions: width (X) = 4, height (Y) = 9, depth (Z) = 3
cutout_volume = (cq.Workplane("XY")
                 .box(4, 9, 3)
                 .translate((-41, 0, 14)))

result = result.cut(cutout_volume)