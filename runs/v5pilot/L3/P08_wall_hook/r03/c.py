import cadquery as cq

# Parameters
plate_thickness = 8.5
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
# Center at x=plate_thickness/2 to ensure it starts at x=0
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# Add screw holes at (y=0, z=0) and (y=0, z=40)
# The plate is translated by 20 in Z. Local coordinates -20 and +20 on the YZ plane 
# will result in absolute Z = 0 and Z = 40.
# We use faces("<X") to select the face at x=0 (or <X for the smallest X)
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6, R7)
# The arm starts from the edge of the plate (x=8.5) and extends to the strap area.
# We use a tapered/stepped approach for strength (R6) and mass optimization (R7).
arm_base = cq.Workplane("XY").box(42, 14, 18).translate((26, 0, -5))

# Beefy connection at the plate to handle bending moment (R6)
connection = cq.Workplane("XY").box(10, 16, 25).translate((9, 0, 7.5))

# 3. Create the Retaining Lip (R5)
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# Combine Plate + Arm + Connection + Lip (R1)
combined = plate.union(arm_base).union(connection).union(lip)

# 4. Create the Strap Pocket (R4)
# The pocket must be empty: x[35,45], y[-6,6], z[-13,-6]
pocket_vol = (
    cq.Workplane("XY")
    .box(strap_pocket_x[1] - strap_pocket_x[0], 
         strap_pocket_y[1] - strap_pocket_y[0], 
         strap_pocket_z[1] - strap_pocket_z[0])
    .translate(((strap_pocket_x[1] + strap_pocket_x[0])/2, 
                (strap_pocket_y[1] + strap_pocket_y[0])/2, 
                (strap_pocket_z[1] + strap_pocket_z[0])/2))
)

# Final Result: Subtract the pocket from the entire combined solid to ensure R4 is met.
result = combined.cut(pocket_vol)