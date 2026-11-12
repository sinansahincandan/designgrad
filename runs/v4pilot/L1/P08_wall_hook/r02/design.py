import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

arm_width = 18.0    # y direction
arm_height = 12.0   # z direction
# The arm must connect to the plate at x=2 and extend to cover the lip/seat areas.
# To ensure R6 (cross section at x=8 is 18x12), we define the arm length and position carefully.
arm_length = 50.0   # extends from x=2 to x=52
arm_start_x = 2.0

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
# x range: [0, 2]. Center of box is at x=1.0.
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# Add screw holes (R3)
# Holes at y=0, z=0 and y=0, z=40. 
# Since plate is translated by 20 in Z, local hole Z are -20 and +20.
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6)
# To ensure R6: at x=8, cross section is 18x12.
# The arm starts at x=2 and ends at x=52.
# We need to position it so that the strap seat/pocket logic works.
# Pocket bottom is z=-13. If we want a bed at z=-14, the arm must extend down there.
# Let's set the arm Z-center such that its top surface or middle accommodates the pocket.
# Based on R6 requirement and R4: The arm needs to be thick enough.
# We will use a large box for the arm and subtract the pocket later.
arm_z_center = -9.0 
arm_part = cq.Workplane("XY").box(arm_length, arm_width, arm_height).translate((arm_start_x + arm_length/2, 0, arm_z_center))

# 3. Create the Retaining Lip (R5)
lip_part = cq.Workplane("XY").box(lip_x_end - lip_x_start, lip_y_half * 2, lip_z_top - lip_z_bottom).translate((lip_x_start + (lip_x_end-lip_x_start)/2, 0, (lip_z_top + lip_z_bottom)/2))

# 4. Combine parts (R1)
# Union plate, arm, and lip to ensure a single solid.
combined = plate.union(arm_part).union(lip_part)

# 5. Subtract the Strap Pocket (R4)
# The pocket is a void in the arm/body.
pocket_vol = cq.Workplane("XY").box(pocket_x_end - pocket_x_start, pocket_y_half * 2, pocket_z_top - pocket_z_bottom).translate(((pocket_x_start + pocket_x_end)/2, 0, (pocket_z_top + pocket_z_bottom)/2))

result = combined.cut(pocket_vol)