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
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height)

# Move the block so floor is at z=0
# box() centers on origin, so we shift it by wall_height/2
base_block = base_block.translate((0, 0, wall_height / 2))

# 2. Subtract the board space (R3)
board_cavity = cq.Workplane("XY").box(
    board_x_max - board_x_min, 
    board_y_max - board_y_min, 
    board_z_top - board_z_bottom
).translate((0, 0, (board_z_bottom + board_z_top) / 2))

# 3. Create the bosses (R5)
# Bosses sit on the floor (z=2) and go up to z=8
boss_positions = [
    (boss_x, boss_y), (boss_x, -boss_y),
    (-boss_x, boss_y), (-boss_x, -boss_y)
]

bosses = cq.Workplane("XY")
for px, py in boss_positions:
    # Create a cylinder for the boss
    b = (cq.Workplane("XY")
         .workplane(offset=floor_thickness)
         .circle(boss_od / 2)
         .extrude(board_z_bottom - floor_thickness)
         # Subtract pilot hole
         .faces(">Z").workplane()
         .hole(boss_hole_d, boss_hole_depth)
         .translate((px, py, 0)))
    bosses = bosses.union(b)

# 4. Construct the main body
# Start with the outer shell (floor + walls)
# To ensure a single solid and correct geometry, we build the floor and walls separately or subtract from a block
main_body = base_block.cut(board_cavity)

# Add bosses to the main body
result = main_body.union(bosses)

# 5. USB-C Cutout (R6)
# The -X wall is at x = -42.5. 
# We cut a hole through the wall.
cutout_w = 9.0
cutout_h = 3.0
result = (result.faces("<X").workplane()
          .center(0, 14 - floor_thickness) # Adjusting for local face coordinate if needed, 
                                          # but easier to use global coordinates via a large box cut
          .rect(cutout_w, cutout_h)
          .cutThruAll())

# Re-centering the cutout logic to be robust:
# A box at x=-42.5, y=0, z=14 with width 3 (to ensure it clears wall)
cutout_box = (cq.Workplane("XY")
              .box(wall_thickness + 2, cutout_w, cutout_h)
              .translate((-outer_x/2, 0, 14)))

result = result.cut(cutout_box)