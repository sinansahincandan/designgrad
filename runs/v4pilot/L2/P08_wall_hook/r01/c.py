import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0 # y direction (total width |y| <= 8)
plate_height = 50.0 # z direction (-5 to 45)
screw_hole_dia = 4.5

strap_width_pocket = 12.0 # |y| <= 6 for pocket
strap_bed_width = 8.0     # |y| <= 4 for bed/lip
arm_thickness = 20.0      # Thickness in Z to ensure R6 strength
arm_height = 30.0         # Total height of the arm block

# 1. Create Plate and Holes (R2, R3)
# We create it centered at origin first to make hole placement easy
p = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height)
# The faces are at x = -1 and x = 1. Use the face at x = -1 (the "<X" face).
# Since the box is centered at z=0, points (0, -20) and (0, 20) correspond to z=-20 and z=20.
p = p.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# Now translate the finished plate to its final position: x from 0 to 2, z from -5 to 45
p = p.translate((plate_thickness/2, 0, 20))

# 2. Create the Support Arm (R6)
# The arm needs to be beefy near the wall and connect to the strap seat.
# We'll create a block that spans from x=2 to x=52.
# To satisfy R4/R5, we position it so the top of the bed is at z = -14.
# Let's define the arm center Z such that its bottom is around -20 and top is around 10.
arm_part = (
    cq.Workplane("XY")
    .box(50, strap_bed_width + 4, arm_thickness) # Width |y| <= 6 approx
    .translate((27, 0, -10)) # x range [2, 52], z range [-10-10, -10+10] -> [-20, 0]
)

# To ensure the strap bed is at z = -14 (R4), we adjust the arm's Z position.
# If arm_thickness is 20, and center is -10, Z range is [-20, 0].
# The pocket subtraction will create the seat.

# 3. Create the Retaining Lip (R5)
# R5: solid material at 47 <= x <= 52, |y| <= 4, -13 <= z <= -8
lip_part = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# 4. Combine all additive parts (R1)
combined = p.union(arm_part).union(lip_part)

# 5. Subtract the Strap Pocket (R4)
# R4: pocket is x[35,45], y[-6,6], z[-13,-6]
pocket_vol = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# The subtraction ensures the space is empty and leaves a bed at z = -14
# (Pocket bottom: -9.5 - 3.5 = -13; Pocket top: -9.5 + 3.5 = -6)
result = combined.cut(pocket_vol)

# Final verification of constraints:
# R2: Plate x[0,2], y[-8,8], z[-5,45] -> Done via translate(1,0,20) on box(2,16,50)
# R3: Holes at (0,0) and (0,40) -> Done in local space then translated.
# R4: Pocket x[35,45], y[-6,6], z[-13,-6] -> Done via cut.
# R5: Lip x[47,52], y[-4,4], z[-13,-8] -> Done via union of lip_part.
# R7: X extent is 52mm (< 55mm).