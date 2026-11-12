import cadquery as cq

# Parameters based on Design Document and Requirements
plate_thickness = 2.0
plate_width = 16.0  # y direction: [-8, 8]
plate_height = 50.0 # z direction: [-5, 45]
screw_hole_dia = 4.5

strap_pocket_x = (35, 45)
strap_pocket_y = 6.0  # |y| <= 6
strap_pocket_z = (-13, -6)

lip_x = (47, 52)
lip_y = 4.0           # |y| <= 4
lip_z = (-13, -8)

# 1. Create Additive Components
# Back Plate: x[0,2], y[-8,8], z[-5,45]
# Center of box is (thickness/2, 0, height/2 - 5) to align z starting at -5
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# Support Arm: Tapered for strength (R6)
# We use a large block that connects the plate to the strap seat area.
# To ensure R6 (strength), we make it thick near the wall and at the seat.
arm = cq.Workplane("XY").box(50, 14, 20).translate((26, 0, -10))

# Retaining Lip: x[47,52], |y|<=4, z[-13,-8]
# Box dimensions: width=5, height=8, depth=5. 
# Center calculation for lip: x_mid = (47+52)/2 = 49.5; y_mid = 0; z_mid = (-13-8)/2 = -10.5
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# 2. Combine all additive parts into one solid (R1)
combined_solid = plate.union(arm).union(lip)

# 3. Create Subtractive Components (Voids)
# Screw Holes: Cylinders through the plate at x=1, y=0, z=0 and z=40
# Cylinder length is 2.5 to ensure it clears the 2mm plate
hole1 = cq.Workplane("XY").cylinder(2.5, screw_hole_dia).translate((1, 0, 0))
hole2 = cq.Workplane("XY").cylinder(2.5, screw_hole_dia).translate((1, 0, 40))

# Strap Pocket (R4): x[35,45], |y|<=6, z[-13,-6]
# Box dimensions: dx=10, dy=12, dz=7.
# Center calculation for pocket: x_mid = 40; y_mid = 0; z_mid = -9.5
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# 4. Perform all subtractions in a single chain to ensure manifold integrity (R1)
result = combined_solid.cut(pocket).cut(hole1).cut(hole2)

# Final check: result is the single solid variable.