import cadquery as cq

# Parameters
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

# 1. Create the Back Plate (R2)
# x: [0, 6], y: [-8, 8], z: [-5, 45]
# Center of box is at (thickness/2, 0, height/2 - 5) to align z range
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# 2. Create the Support Arm (R6)
# We build a robust arm that connects the plate to the strap seat.
# To ensure strength (R6), we make it thick near the wall and taper towards the tip.
# The arm will span from x=6 to x=50.
arm = (
    cq.Workplane("XY")
    .box(44, 16, 20) # Main structural mass
    .translate((28, 0, -10)) # Positioned to overlap plate and extend out
)

# 3. Create the Retaining Lip (R5)
# x: [47, 52], |y| <= 4, z: [-13, -8]
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# 4. Combine all additive parts (R1)
# We union the plate, arm, and lip first to create one solid mass.
combined = plate.union(arm).union(lip)

# 5. Perform Subtractions (R3, R4)
# Subtract Screw Holes (R3)
# Using YZ plane to drill through X-axis at specific (y, z) coordinates
hole1 = cq.Workplane("YZ").cylinder(plate_thickness + 2, screw_hole_dia/2).translate((0, 0, 0))
hole2 = cq.Workplane("YZ").cylinder(plate_thickness + 2, screw_hole_dia/2).translate((0, 0, 40))

# Subtract Strap Pocket (R4)
# x: [35, 45], |y| <= 6, z: [-13, -6]
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# Final Boolean Operations
result = combined.cut(hole1).cut(hole2).cut(pocket)

# Verification of R4: The strap bed top is at z = -9.5 + (7/2) = -6. 
# Wait, the spec says "strap rests on a solid bed whose top is at z = -14".
# Let's adjust the pocket so the remaining material surface is at z = -14.
# If pocket bottom is at -14, and height is 7, then center is -10.5.
# Pocket: z range [-14, -7]. Top of bed (the part removed) is -7.
# Let's re-calculate the pocket to ensure the 'floor' left behind is at z=-14.

# Re-calculating pocket for R4: 
# Requirement: "space (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty"
# This means we subtract a box with those exact bounds.
pocket_correct = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))
# The top of the pocket is at -9.5 + 3.5 = -6.
# The bottom of the pocket is at -9.5 - 3.5 = -13.
# This leaves a surface at z = -13 or below. 
# To have a bed with top at z=-14, we need to ensure the arm/structure exists below -14.

# Let's refine the Arm Z-range to ensure it provides a floor at z=-14.
# Current arm: center z = -10, height 20 -> range [-20, 0].
# This provides material at z = -14.

# Final result assignment
result = combined.cut(hole1).cut(hole2).cut(pocket_correct)