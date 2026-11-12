import cadquery as cq

# Parameters
screw_hole_dia = 4.5
plate_thickness = 2.0
plate_width = 16.0  # y range [-8, 8]
plate_height = 50.0 # z range [-5, 45]

# R2: Back Plate (x in [0, 2], y in [-8, 8], z in [-5, 45])
# Center of plate is at x=1, y=0, z=20
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((1, 0, 20))

# R3: Screw Holes (y,z) = (0,0) and (0,40)
# Since the plate is translated by z=20, local coordinates for holes are -20 and +20
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# R6 & R7: Support Arm (Optimized for mass and strength)
# We create a large block that covers the arm area and then subtract the pocket.
# To satisfy R4/R5/R6, we define a structural body from x=2 to x=52.
# The seat top is at z=-14. Let's make the arm height from z=-18 to z=0.
arm_width = 10.0 # Reduced width for mass (R7)
arm_height = 18.0 
# Arm spans x from 2 to 52. Center of box at x=27, y=0, z=-9
arm_part = cq.Workplane("XY").box(50, arm_width, arm_height).translate((27, 0, -9))

# R5: Retaining Lip (x in [47, 52], |y| <= 4, z in [-13, -8])
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# Combine all additive parts (R1)
combined = plate.union(arm_part).union(lip)

# R4: Strap Pocket Subtraction
# The pocket must be empty: x in [35, 45], |y| <= 6, z in [-13, -6]
# We use a box centered to match these bounds.
# Width (y): 12 -> range [-6, 6]
# Height (z): 7 -> center at -9.5 -> range [-13, -6]
# Length (x): 10 -> center at 40 -> range [35, 45]
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# Final result: Subtract the pocket from the combined solid
result = combined.cut(pocket)

# Verification of R4 Seat Bed:
# The arm_part goes up to z=0 (center -9 + height/2 = 0).
# The pocket bottom is at z=-13. Therefore, a solid bed exists at z=-14? 
# Wait, the requirement says "top is at z=-14". 
# Let's adjust arm_part to ensure the seat top is exactly -14.
# If we want the pocket bottom to be -15 and top to be -6 (to leave a bed), 
# let's redefine the arm height/positioning more precisely.

# RE-CALIBRATING FOR R4 PRECISION:
plate = cq.Workplane("XY").box(2, 16, 50).translate((1, 0, 20))
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# Arm: x [2, 52], y [-5, 5], z [-18, -6] -> This puts the top at z=-6.
# To get a bed at z=-14, we need material below the pocket.
# Let's make the arm thicker in Z.
arm_part = cq.Workplane("XY").box(50, 10, 20).translate((27, 0, -14)) # z range [-24, -4]

# Pocket: x [35, 45], y [-6, 6], z [-13, -6]
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# Lip: x [47, 52], y [-4, 4], z [-13, -8]
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

combined_v2 = plate.union(arm_part).union(lip)
result = combined_v2.cut(pocket)

# Final check of R4:
# Pocket top is z=-6, bottom is z=-13.
# Arm goes from z=-24 to z=-4. 
# Below the pocket (z < -13), there is material (the arm).
# The "top" of the seat bed would be the surface at z = -13? 
# Requirement: "rests on a solid bed whose top is at z = -14".
# Let's shift the pocket so its bottom is at z=-14.
# Pocket height 7, so bottom -14 -> top -7. Center = -10.5.

pocket_v2 = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -10.5))
result = combined_v2.cut(pocket_v2)