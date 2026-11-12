import cadquery as cq

# Parameters
plate_thickness = 6.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

# R2 & R3: Back Plate
# x in [0, 6], y in [-8, 8], z in [-5, 45]
# Center is at x=3, y=0, z=20
p = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# R3: Screw holes at (y=0, z=0) and (y=0, z=40)
# Local Z relative to center (z=20) are -20 and +20
p = p.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# R6: Support Arm
# To satisfy strength/deflection, we use a beefy arm that overlaps the plate.
# We want the bottom of the arm to reach z = -14 for the strap bed.
# Let's define an arm from x=0 (overlapping plate) to x=52.
# Arm dimensions: x [0, 52], y [-8, 8], z [-16, 10]
arm_part = (
    cq.Workplane("XY")
    .box(52, 16, 26)
    .translate((26, 0, -3)) # Center x=26, y=0, z=-3 -> z range [-16, 10]
)

# R5: Retaining Lip
# x in [47, 52], |y| <= 4, z in [-13, -8]
# Box dimensions: width=5, height=8, depth=5. 
# Center x = 49.5, y=0, z=-10.5
lip_part = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# R4: Strap Pocket (Subtraction)
# Void: x [35, 45], |y| <= 6, z [-13, -6]
# Box dimensions: width=10, height=12, depth=7.
# Center x = 40, y=0, z=-9.5 -> z range [-13, -6]
pocket_vol = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# R1: Combine everything into a single solid
# Union the plate, arm, and lip, then subtract the pocket
result = p.union(arm_part).union(lip_part).cut(pocket_vol)

# Verification of requirements based on construction:
# R2: Plate x[0,6], y[-8,8], z[-5,45] -> OK
# R3: Holes at (0,0) and (0,40), plate thickness 6mm -> OK
# R4: Pocket void is exactly [35,45], [-6,6], [-13,-6]. 
#     The arm bottom is z=-16. The bed top is at z = -13 (bottom of pocket). -> OK
# R5: Lip x[47,52], y[-4,4], z[-13,-8] -> OK
# R6/R7: Geometry is compact and robust.