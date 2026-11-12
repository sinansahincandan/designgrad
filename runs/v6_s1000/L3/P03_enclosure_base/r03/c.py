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
boss_hole_depth = 4.5 # From z=8 down to z=3.5

# 1. Build Base (Floor + Walls)
# Create a solid block representing the outer bounds and subtract the board cavity
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height)
# Move so floor is at z=0 (center of box was at z=wall_height/2)
base_block = base_block.translate((0, 0, wall_height / 2))

# 2. Subtract Board Space (R3)
board_cavity = (cq.Workplane("XY")
                .box(board_x_max - board_x_min, 
                     board_y_max - board_y_min, 
                     board_z_top - board_z_bottom)
                .translate((0, 0, (board_z_bottom + board_z_top) / 2)))

main_body = base_block.cut(board_cavity)

# 3. Build Bosses separately with holes (R5)
boss_positions = [
    (boss_x, boss_y), (boss_x, -boss_y),
    (-boss_x, boss_y), (-boss_x, -boss_y)
]

# We will create a single solid containing all four bosses and their holes
bosses_combined = cq.Workplane("XY")

for px, py in boss_positions:
    # Create the cylindrical pillar from floor (z=2) to board bottom (z=8)
    pillar = (cq.Workplane("XY")
              .workplane(offset=floor_thickness)
              .cylinder(board_z_bottom - floor_thickness, boss_od / 2)
              .translate((px, py, 0)))
    
    # Create the hole cylinder: starts at z=8 and goes down to z=3.5
    # We translate it so its center is at (px, py, 8 - depth/2)
    hole = (cq.Workplane("XY")
            .cylinder(boss_hole_depth, boss_hole_d / 2)
            .translate((px, py, board_z_bottom - boss_hole_depth / 2)))
    
    # Subtract hole from pillar and add to the collection
    bosses_combined = bosses_combined.union(pillar.cut(hole))

# 4. Combine Main Body and Bosses (R1)
result = main_body.union(bosses_combined)

# 5. USB-C Cutout (R6)
# Dimensions: 10mm (X) * 9mm (Y) * 3mm (Z)
# Positioned at x=-42.5, y=0, z=14
cutout_box = (cq.Workplane("XY")
              .box(10, 9, 3)
              .translate((-42.5, 0, 14)))

result = result.cut(cutout_box)