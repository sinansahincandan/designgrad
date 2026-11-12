import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

arm_width = 18.0    # y direction
arm_height = 12.0   # z direction
arm_length = 51.0   # x direction (starts at x=1, ends at x=52)

# R4: Strap pocket requirements
# Pocket: 35 <= x <= 45, |y| <= 6, -14 <= z <= -7
pocket_x_start = 35.0
pocket_x_end = 45.0
pocket_y_half = 6.0
pocket_z_bottom = -14.0
pocket_z_top = -7.0

# R5: Retaining lip requirements
# Lip: 47 <= x <= 52, |y| <= 4, -13 <= z <= -8
lip_x_start = 47.0
lip_x_end = 52.0
lip_y_half = 4.0
lip_z_bottom = -13.0
lip_z_top = -8.0

# 1. Create the Back Plate (R2, R3)
# x in [0, 2], y in [-8, 8], z in [-5, 45]
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height, centered=False).translate((0, -8, -5))

# Add screw holes (R3) at (0,0) and (0,40) relative to the plate center
# Plate center is at x=1, y=0, z=20. 
# Holes are at (x=1, y=0, z=20-20) and (x=1, y=0, z=20+20)
plate = plate.faces("<X").workplane().pushPoints([(1, 0), (1, 40)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6)
# To ensure connection with the plate (x=2), we start the arm at x=1 and extend it to x=52.
# The design says cross section is 18x12 at x=8.
# We need the arm to overlap the plate in X and Z.
# Plate Z range: [-5, 45]. Arm Z center should be near -10.5 (from previous attempt) but must touch plate.
# Let's set arm Z range to cover the pocket (-14 to -7) and reach up to the plate at z=-5.
arm_start_x = 1.0
arm_end_x = 52.0
arm_len = arm_end_x - arm_start_x
# Arm Z range: [-16, -4]. This overlaps the plate (z starts at -5) and covers pocket (-14 to -7).
arm_z_min = -16.0
arm_height_val = 12.0
arm_part = cq.Workplane("XY").box(arm_len, arm_width, arm_height_val, centered=False).translate((arm_start_x, -arm_width/2, arm_z_min))

# 3. Create the Retaining Lip (R5)
# Lip: x in [47, 52], |y| <= 4, z in [-13, -8]
lip_w = lip_x_end - lip_x_start
lip_h = lip_z_top - lip_z_bottom
lip_part = cq.Workplane("XY").box(lip_w, lip_y_half * 2, lip_h, centered=False).translate((lip_x_start, -lip_y_half, lip_z_bottom))

# 4. Combine parts (R1)
# The arm starts at x=1 and the plate ends at x=2 -> Overlap in X.
# The arm Z range [-16, -4] overlaps the plate Z range [-5, 45] -> Overlap in Z.
combined = plate.union(arm_part).union(lip_part)

# 5. Subtract the Strap Pocket (R4)
# Pocket: 35 <= x <= 45, |y| <= 6, -14 <= z <= -7
pocket_w = pocket_x_end - pocket_x_start
pocket_d = pocket_y_half * 2
pocket_h = pocket_z_top - pocket_z_bottom
pocket_vol = cq.Workplane("XY").box(pocket_w, pocket_d, pocket_h, centered=False).translate((pocket_x_start, -pocket_y_half, pocket_z_bottom))

result = combined.cut(pocket_vol)