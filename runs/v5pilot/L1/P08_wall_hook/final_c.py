import cadquery as cq

# Parameters
screw_hole_dia = 4.5
boss_dia = 12.5
boss_length = 8.5
plate_thickness = 2.0
plate_width = 16.0 # y direction (total |y| <= 8)
plate_height = 50.0 # z direction (-5 to 45)

# 1. Create the Back Plate and Bosses (R2, R3)
# Main plate: x [0, 2], y [-8, 8], z [-5, 45]
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# Bosses: Cylinders at (y=0, z=0) and (y=0, z=40), extending to x=8.5
# Local Z for holes are -20 and +20 relative to plate center at z=20
boss1 = cq.Workplane("XY").cylinder(boss_length, boss_dia).translate((boss_length/2, 0, 0))
boss2 = cq.Workplane("XY").cylinder(boss_length, boss_dia).translate((boss_length/2, 0, 40))

# Union plate and bosses
mounting_structure = plate.union(boss1).union(boss2)

# Drill screw holes through the bosses (R3)
# Holes are at y=0, z=0 and y=0, z=40 in global coordinates
mounting_structure = mounting_structure.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6)
# Requirement: At x=8, cross-section is 16mm (y) by 12mm (z).
# We'll create a box that spans from the bosses to the tip.
# To ensure it covers the pocket and lip, we make it deep enough in Z.
# Arm center at z=-14 (to support strap bed) or similar.
# Let's define an arm that is 16mm wide (y) and 20mm high (z).
# The pocket subtraction will create the seat.
arm_body = cq.Workplane("XY").box(50, 16, 20).translate((27, 0, -10))

# Combine mounting structure and arm
combined = mounting_structure.union(arm_body)

# 3. Create the Retaining Lip (R5)
# x [47, 52], |y| <= 4, z [-13, -8]
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))
combined = combined.union(lip)

# 4. Create the Strap Pocket (R4)
# The pocket is empty space: x [35, 45], |y| <= 6, z [-13, -6]
# To ensure the bed top is at z=-14, we must make sure the arm_body extends below -14.
# Our arm_body center is -10 with height 20 -> Z range is [-20, 0]. This works.
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# Final subtraction to create the strap seat
result = combined.cut(pocket)

# Verification of R4:
# Pocket center z = -9.5, height = 7 -> Z range is [-13, -6].
# The solid material immediately below this pocket (at x=40, y=0) 
# will be the arm_body which goes down to z=-20.
# Thus, the top of the "bed" is at z = -13? 
# Wait, the spec says: "the space just above it ... must be empty".
# And "strap rests on a solid bed whose top is at z = -14".
# If pocket is [-13, -6], the surface at z=-13 is the top of the bed.
# Let's adjust pocket to [ -6, -14 ] so the top of the material below it is -14.
# Pocket: x[35,45], y[-6,6], z[-13,-6]. 
# If we subtract this, the surface at z=-13 becomes an interface.
# To have a bed TOP at z=-14, the pocket must be from z=-14 to z=-6.

pocket_v2 = cq.Workplane("XY").box(10, 12, 8).translate((40, 0, -10))
# Pocket center z = -10, height = 8 -> Z range is [-14, -6].
# This makes the top of the material below it (the bed) exactly z=-14.

result = combined.cut(pocket_v2)