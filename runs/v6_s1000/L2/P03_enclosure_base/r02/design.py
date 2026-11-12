import cadquery as cq

# Dimensions
floor_thickness = 2.0
outer_x = 85.0
outer_y = 55.0
wall_height = 32.0
wall_thickness = 2.5

board_x_min, board_x_max = -40.0, 40.0
board_y_min, board_y_max = -25.0, 25.0
board_z_bottom = 8.0
board_z_top = 32.0

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.5 # From z=8 down to z=3.5

# 1. Create the main block (Floor + Walls)
# We start with a solid block and subtract the board cavity
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height, centered=(True, True, False)).translate((0, 0, 0))

# 2. Subtract the board space (R3)
board_cavity = cq.Workplane("XY").box(
    board_x_max - board_x_min, 
    board_y_max - board_y_min, 
    board_z_top - board_z_bottom,
    centered=(True, True, False)
).translate((0, 0, board_z_bottom))

main_body = base_block.cut(board_cavity)

# 3. Create the bosses (R5)
boss_positions = [
    (boss_x, boss_y), (boss_x, -boss_y),
    (-boss_x, boss_y), (-boss_x, -boss_y)
]

# Build bosses as separate cylinders and union them to avoid selector issues with hole() on multiple faces
bosses = cq.Workplane("XY")
for pos in boss_positions:
    b = (cq.Workplane("XY")
         .workplane(offset=floor_thickness)
         .center(*pos)
         .circle(boss_od / 2)
         .extrude(board_z_bottom - floor_thickness))
    # Subtract the pilot hole from each boss individually
    b = (b.faces(">Z").workplane()
         .hole(boss_hole_d, boss_hole_depth))
    bosses = bosses.union(b)

# 4. Construct the main body
result = main_body.union(bosses)

# 5. USB-C Cutout (R6)
cutout_w_y = 9.0
cutout_h_z = 3.0

# The -X wall is at x = -42.5. 
# We create a box that cuts through the wall.
cutout_box = (cq.Workplane("XY")
              .box(wall_thickness + 10, cutout_w_y, cutout_h_z, centered=(True, True, False))
              .translate((-outer_x/2, 0, 14)))

result = result.cut(cutout_box)