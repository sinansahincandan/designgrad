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

boss_positions = [(35.0, 20.0), (35.0, -20.0), (-35.0, 20.0), (-35.0, -20.0)]
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.5  # Ensures hole is at least 4mm deep

# 1. Create the main block (Floor + Walls)
# We create a solid block and subtract the board cavity to ensure R1/R2/R3/R4
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height)
# Shift so floor is at z=0 (box() centers on origin)
base_block = base_block.translate((0, 0, wall_height / 2))

# 2. Subtract the board space (R3)
board_cavity = (cq.Workplane("XY")
                .box(board_x_max - board_x_min, 
                     board_y_max - board_y_min, 
                     board_z_top - board_z_bottom)
                .translate((0, 0, (board_z_bottom + board_z_top) / 2)))

main_body = base_block.cut(board_cavity)

# 3. Create the bosses with holes (R5)
# We create the cylinders first, then subtract the holes from them as a single operation
bosses = (cq.Workplane("XY")
          .pushPoints(boss_positions)
          .circle(boss_od / 2)
          .extrude(board_z_bottom - floor_thickness) # Extrudes from z=2 to z=8
          .faces(">Z").workplane()
          .pushPoints(boss_positions) # Re-select centers for the holes
          .hole(boss_hole_d, boss_hole_depth))

# 4. Combine main body and bosses (R1)
result = main_body.union(bosses)

# 5. USB-C Cutout (R6)
# Opening at least 9mm wide (Y) and 3mm high (Z), centered at y=0, z=14 on the -X wall.
cutout_w = 9.0 # Y dimension
cutout_h = 3.0 # Z dimension
# A box to cut through the -X wall. 
# The wall is at x = -outer_x/2 = -42.5.
cutout_box = (cq.Workplane("XY")
              .box(wall_thickness + 2, cutout_w, cutout_h)
              .translate((-outer_x/2, 0, 14)))

result = result.cut(cutout_box)