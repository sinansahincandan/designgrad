import cadquery as cq

# Parameters based on Design Document
plate_thickness = 6.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

strap_pocket_x = (35, 45)
strap_pocket_y = 6.0
strap_pocket_z = (-13, -6)

lip_x = (47, 52)
lip_y = 4.0
lip_z = (-13, -8)

# 1. Create the Back Plate
# x: [0, 6], y: [-8, 8], z: [-5, 45]
# Center of box is at (3, 0, 20)
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# 2. Create the Screw Holes (R3)
# Holes at (y=0, z=0) and (y=0, z=40). 
# Since plate is translated by 20 in Z, local holes are at -20 and +20.
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 3. Create the Support Arm / Main Body
# To satisfy R6 (Strength), we create a beefy arm that connects to the plate.
# The arm will extend from x=6 to x=52.
# We must ensure it overlaps with the plate in Z. Plate is z: [-5, 45].
# Arm height and position adjusted to overlap plate.
arm_height = 30.0
# Let's set arm top at z=-5 (to touch/overlap plate) or similar.
# The previous error showed arm was at z: [-44, -14], which is below the plate [ -5, 45].
# We need the arm to bridge the gap between the plate and the strap seat.
# Let's make the arm extend from x=0 (to overlap plate) up to x=52.
arm_width = 16.0
arm_thickness = 30.0 # Z dimension of the arm
# Arm spans x [0, 52], y [-8, 8], z [-24, 6] (This overlaps plate at z:[-5, 6])
arm = cq.Workplane("XY").box(52, arm_width, arm_thickness).translate((26, 0, -9))

# 4. Create the Retaining Lip (R5)
# x: [47, 52], y: [-4, 4], z: [-13, -8]
# Ensure it overlaps with the arm. Arm is at z: [-24, 6]. Lip is at z: [-13, -8]. This works.
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# 5. Combine Plate + Arm + Lip (R1)
combined = plate.union(arm).union(lip)

# 6. Subtract the Strap Pocket (R4)
# pocket: x[35, 45], y[-6, 6], z[-13, -6]
pocket_width = 10.0 # 45-35
pocket_depth = 12.0 # 6*2
pocket_height = 7.0 # -6 - (-13)
pocket = cq.Workplane("XY").box(pocket_width, pocket_depth, pocket_height).translate((40, 0, -9.5))

result = combined.cut(pocket)