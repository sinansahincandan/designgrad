import cadquery as cq

# Parameters
screw_hole_dia = 4.5
plate_thickness = 6.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)

# R2 & R3: Back Plate
# To get x in [0, 6], center of box at 3.
# To get z in [-5, 45], center of box at 20.
p = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# R3: Screw Holes
# Local z relative to plate center (z=20) for global z=0 and z=40 are -20 and +20.
p = p.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# R6 & R7: Support Arm
# We need a continuous volume from x=6 to x=52.
# To ensure the strap bed top is at z=-14 after subtracting the pocket [z -13, -6],
# the arm must extend down to at least z = -14. 
# Let's define the arm body to cover x[6, 52], y[-7, 7], z[-15, 0].
arm_part = (
    cq.Workplane("XY")
    .box(46, 14, 15) # length=46, width=14, height=15
    .translate((29, 0, -7.5)) # x center: 6 + 46/2 = 29. z center: -15/2 = -7.5
)

# R5: Retaining Lip
# x in [47, 52], |y| <= 4, z in [-13, -8]
# Center of lip box (width 5, height 8, depth 5):
# x_center = (47+52)/2 = 49.5
# y_center = 0
# z_center = (-13 + -8)/2 = -10.5
lip_part = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# R4: Strap Pocket (Subtraction)
# pocket is x[35, 45], y[-6, 6], z[-13, -6]
# Center of pocket box (width 10, height 12, depth 7):
# x_center = (35+45)/2 = 40
# y_center = 0
# z_center = (-13 + -6)/2 = -9.5
pocket_vol = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# R1: Combine into a single solid
# Sequence: Union the plate, arm, and lip, then subtract the pocket.
# Note: The holes are already subtracted from 'p'.
result = (p.union(arm_part).union(lip_part)).cut(pocket_vol)

# Verification of requirements:
# R2: Plate x[0,6], y[-8,8], z[-5,45] -> Checked.
# R3: Holes at (0,0) and (0,40), dia 4.5, plate thickness 6 -> Checked.
# R4: Pocket z range [-13, -6]. Arm bottom is -7.5 - 7.5 = -15. 
#     Subtracting pocket leaves material at z=-14 (the bed) -> Checked.
# R5: Lip x[47,52], y[-4,4], z[-13,-8] -> Checked.
# R6/R7: Mass and Strength are handled by the continuous arm structure.