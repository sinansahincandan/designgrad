import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0  # y direction: [-8, 8]
plate_height = 50.0 # z direction: [-5, 45]
screw_hole_dia = 4.5

strap_pocket_x = (35, 45)
strap_pocket_y = (-6, 6)
strap_pocket_z = (-13, -6)

lip_x = (47, 52)
lip_y = (-4, 4)
lip_z = (-13, -8)

# 1. Create the Back Plate (R2, R3)
# Center at x=1, y=0, z=20 to get x[0,2], y[-8,8], z[-5,45]
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((1, 0, 20))

# Add screw holes at (y=0, z=0) and (y=0, z=40)
# Since the plate is translated by 20 in Z, local coordinates are -20 and +20
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6, R7)
# To ensure R4 is possible, the arm must encompass the pocket Z-range [-13, -6]
# We'll create a tapered arm that connects the plate to the strap area.
# Base of arm at x=2, extending to x=50. 
# We use a larger block and then subtract/taper to keep mass low (R7).
arm_base = cq.Workplane("XY").box(48, 12, 20).translate((26, 0, -5))

# To ensure strength near the wall (R6), we add a beefy connection at the plate
connection = cq.Workplane("XY").box(8, 16, 25).translate((6, 0, 7.5))

# 3. Create the Retaining Lip (R5)
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# Combine Plate + Arm + Connection + Lip (R1)
combined = plate.union(arm_base).union(connection).union(lip)

# 4. Create the Strap Pocket (R4)
# The pocket must be empty: x[35,45], y[-6,6], z[-13,-6]
# We create a box representing this volume and subtract it from the combined solid.
pocket_vol = (
    cq.Workplane("XY")
    .box(strap_pocket_x[1] - strap_pocket_x[0], 
         strap_pocket_y[1] - strap_pocket_y[0], 
         strap_pocket_z[1] - strap_pocket_z[0])
    .translate(((strap_pocket_x[1] + strap_pocket_x[0])/2, 
                (strap_pocket_y[1] + strap_pocket_y[0])/2, 
                (strap_pocket_z[1] + strap_pocket_z[0])/2))
)

# Final Result: Subtract the pocket from the solid body
result = combined.cut(pocket_vol)

# Verification of R4 Bed:
# The pocket bottom is at z = -13. 
# The arm/body must exist below this to provide the "solid bed" at z = -14.
# Our arm_base center is z=-5, height 20 -> Z range [-15, 5].
# This provides material at z=-14 as required.