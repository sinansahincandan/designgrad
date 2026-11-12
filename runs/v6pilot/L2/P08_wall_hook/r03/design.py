import cadquery as cq

# Parameters
plate_thickness = 4.0
plate_width = 16.0  # y direction
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

strap_pocket_x_min, strap_pocket_x_max = 35, 45
strap_pocket_y_half = 6
strap_pocket_z_min, strap_pocket_z_max = -13, -6

lip_x_min, lip_x_max = 47, 52
lip_y_half = 4
lip_z_min, lip_z_max = -13, -8

# 1. Create the Back Plate (R2, R3)
# Design Doc: x in [-2, 2], y in [-8, 8], z in [-5, 45]
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((0, 0, 20))

# Drill screw holes through the plate along X-axis (R3)
# Holes at (y=0, z=0) and (y=0, z=40)
# Since plate is translated by 20 in Z, local hole Z are -20 and +20
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Tapered Support Arm (R6, R7)
# Arm: x[2, 46], y[-7, 7], z[-18, 0] -> This provides a bed at z=-14 if pocket is cut correctly.
arm_body = cq.Workplane("XY").box(44, 14, 18).translate((24, 0, -9))

# 3. Create the Retaining Lip (R5)
# The previous lip was at x [46.5, 52.5], leaving a gap from 46 to 46.5.
# We extend it so it overlaps the arm (which ends at x=46).
# New lip: x in [45, 51] to ensure overlap with arm ending at 46.
lip = cq.Workplane("XY").box(6, 8, 5).translate((48, 0, -10.5))

# Combine Plate + Arm + Lip
combined = plate.union(arm_body).union(lip)

# 4. Subtract the Strap Pocket (R4)
# To get a bed top at z = -14, we need to cut from z = -14 up to some value.
# If arm bottom is at z = -18, and pocket starts at z = -14:
# Material remains in z range [-18, -14]. Top of material is -14.
# Pocket: x[35, 45], y[-6, 6], z[-14, -7] (height 7)
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -10.5))

result = combined.cut(pocket)