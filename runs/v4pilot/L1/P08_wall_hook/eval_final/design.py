import cadquery as cq

# Parameters
plate_thickness = 6.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

arm_width = 18.0    # y direction
arm_height = 12.0   # z direction
arm_length = 46.0   # x direction (starts at x=6, ends at x=52)

# R4: Strap pocket requirements
# Pocket: 35 <= x <= 45, |y| <= 6, -13 <= z <= -6
pocket_x_start = 35.0
pocket_x_end = 45.0
pocket_y_half = 6.0
pocket_z_bottom = -13.0
pocket_z_top = -6.0

# R5: Retaining lip requirements
# Lip: 47 <= x <= 52, |y| <= 4, -13 <= z <= -8
lip_x_start = 47.0
lip_x_end = 52.0
lip_y_half = 4.0
lip_z_bottom = -13.0
lip_z_top = -8.0

# 1. Create the Back Plate (R2, R3)
# To ensure x=0 is the back face, translate by thickness/2
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# Add screw holes (R3)
# Holes at y=0, z=0 and y=0, z=40. 
# Since plate is translated by 20 in Z, local hole Z are -20 and +20.
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6)
# We need an 18x12 cross section at x=8.
# If we place a box of length 46 starting at x=6, it covers x from 6 to 52.
# The center of this arm in Z: To get the pocket bottom at z=-13, 
# and knowing the pocket is subtracted from the arm, let's position the arm.
# Let's place the arm center such that its top surface or middle allows for the pocket.
# If arm_height = 12, and we want the pocket (z: -13 to -6) to be inside it:
# The arm Z-range should at least cover [-13, -6]. Let's center the arm around z=-9.5.
arm_z_center = -9.5 
arm_part = cq.Workplane("XY").box(arm_length, arm_width, arm_height).translate((6 + arm_length/2, 0, arm_z_center))

# 3. Create the Retaining Lip (R5)
lip_part = cq.Workplane("XY").box(lip_x_end - lip_x_start, lip_y_half * 2, lip_z_top - lip_z_bottom).translate((lip_x_start + (lip_x_end-lip_x_start)/2, 0, (lip_z_top + lip_z_bottom)/2))

# 4. Combine parts (R1)
combined = plate.union(arm_part).union(lip_part)

# 5. Subtract the Strap Pocket (R4)
# The pocket is a void in the arm.
pocket_vol = cq.Workplane("XY").box(pocket_x_end - pocket_x_start, pocket_y_half * 2, pocket_z_top - pocket_z_bottom).translate(((pocket_x_start + pocket_x_end)/2, 0, (pocket_z_top + pocket_z_bottom)/2))

result = combined.cut(pocket_vol)