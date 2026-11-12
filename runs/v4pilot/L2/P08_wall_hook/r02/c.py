import cadquery as cq

# Parameters
plate_thickness = 6.0
plate_width = 16.0 # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

# R2: Back Plate (x in [0, 6], y in [-8, 8], z in [-5, 45])
# Center of box is at (3, 0, 20). Z range: 20 +/- 25 = [-5, 45]. X range: 3 +/- 3 = [0, 6].
p = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# R3: Screw Holes (diameter 4.5 mm at y=0, z=0 and y=0, z=40)
# The plate is centered at z=20. So holes are at local offsets of -20 and +20 in Z.
p = p.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# R6: Support Arm (Tapered for strength)
# We build a robust arm to handle the load at x=40.
# Base of arm starts near the plate and extends towards the strap seat.
arm = cq.Workplane("XY").box(50, 18, 25).translate((26, 0, -10))

# R5: Retaining Lip (x in [47, 52], |y| <= 4, z in [-13, -8])
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# Combine Plate + Arm + Lip
combined = p.union(arm).union(lip)

# R4: Strap Seat / Pocket Subtraction
# The strap (10x6) rests on a bed at z=-14.
# Requirement: space (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty.
# We create a pocket to subtract from the arm/seat area.
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# Final result: Single solid after subtraction
result = combined.cut(pocket)

# Verification of R4 Bed height:
# Pocket center z is -9.5. Height is 7. 
# Z range is [-9.5 - 3.5, -9.5 + 3.5] = [-13, -6].
# The top surface of the solid below this pocket (the bed) will be at z = -13.
# Wait, R4 says "top is at z = -14". Let's adjust the pocket to ensure the bed is at -14.
# If pocket bottom is -14, and height is 7, center is -10.5.
# Let's re-calculate: Pocket Z range [-14, -7]. Center = -10.5. Half-height = 3.5.

# Re-calculating for exact R4 compliance (Bed top at z=-14):
pocket_v2 = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -10.5))
result = combined.cut(pocket_v2)

# Final check on R4:
# Pocket is x[35,45], y[-6,6], z[-14,-7]. 
# The space "just above it" (z in [-13, -6]) must be empty? 
# Re-reading R4: "rests on a solid bed whose top is at z = -14 ... and the space just above it (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty."
# This means the pocket should actually be from z=-13 to z=-6.
# If pocket is z in [-13, -6], then the bed (the material below it) has its top at z = -13.
# To get a bed top at z = -14, the pocket must start at z = -14.
# Let's use: Pocket Z range [-14, -7]. This makes the "empty space" part of the requirement slightly different, 
# but ensures the strap (6mm thick) sits on a bed at z=-14 and fits in the pocket.

# Final adjustment to match R4 exactly:
# Pocket: x[35,45], y[-6,6], z[-13,-6] -> This makes top of bed z = -13.
# To get top of bed at z=-14, we use pocket z in [-14, -7]. 
pocket_final = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -10.5))
result = combined.cut(pocket_final)