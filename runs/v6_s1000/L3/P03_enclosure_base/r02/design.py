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

cutout_w = 9.0  # Y direction
cutout_h = 3.0  # Z direction

# 1. Create the main block (Floor + Walls)
# We start with a solid block of the full outer dimensions and height.
# The floor is part of this block from z=0 to z=2.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract the board space (R3)
# The cavity is from z=8 to z=32.
board_cavity = (cq.Workplane("XY")
                .box(board_x_max - board_x_min, 
                     board_y_max - board_y_min, 
                     board_z_top - board_z_bottom)
                .translate((0, 0, (board_z_bottom + board_z_top) / 2)))

main_body = main_body.cut(board_cavity)

# 3. Create the bosses and pilot holes (R5)
boss_positions = [
    (boss_x, boss_y), (boss_x, -boss_y),
    (-boss_x, boss_y), (-boss_x, -boss_y)
]

# We build all bosses as a single object first to avoid topological errors during union
bosses = cq.Workplane("XY")
for px, py in boss_positions:
    # Create the cylinder for the boss (from z=2 to z=8)
    b = (cq.Workplane("XY")
         .workplane(offset=floor_thickness)
         .circle(boss_od / 2)
         .extrude(board_z_bottom - floor_thickness)
         .translate((px, py, 0)))
    bosses = bosses.union(b)

# Subtract the pilot holes from the combined boss object before joining to main body
# The hole is at the top of the boss (z=8) and goes down 4mm (to z=4)
for px, py in boss_positions:
    bosses = (bosses.faces(">Z").workplane()
              .center(px, py)
              .hole(boss_hole_d, boss_hole_depth))

# Join bosses to the main body
result = main_body.union(bosses)

# 4. USB-C Cutout (R6)
# The wall is at x = -42.5. We use a box that clears the wall thickness.
# Centered at y=0, z=14.
cutout_box = (cq.Workplane("XY")
              .box(5.0, cutout_w, cutout_h)
              .translate((-outer_x/2, 0, 14)))

result = result.cut(cutout_box)