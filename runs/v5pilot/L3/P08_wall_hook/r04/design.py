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
# Spans x: [0, 8.5], y: [-8, 8], z: [-5, 45]
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# Add screw holes at (y=0, z=0) and (y=0, z=40)
# Since the plate is translated by 20 in Z, local coordinates are -20 and +20
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6, R7)
# The arm must connect to the plate and reach the lip area.
# Plate ends at x=8.5. We start the arm from x=0 to ensure deep overlap with the plate.
# To reach the lip (which starts around x=47), we extend the arm to x=52.
arm_length = 52.0
arm_width = 16.0
arm_height = 25.0
# Center of arm in X: 52/2 = 26.
arm = cq.Workplane("XY").box(arm_length, arm_width, arm_height).translate((arm_length/2, 0, -5))

# Subtracting material from the top/bottom to create a taper (R7)
taper_cut = cq.Workplane("XY").box(arm_length, 12, 30).translate((arm_length/2, 0, -5))
arm = arm.cut(taper_cut)

# 3. Create the Retaining Lip (R5)
# The lip is at x [47, 52]. To ensure it fuses with the arm (which ends at x=52),
# we make sure the lip overlaps the arm by extending its start to x=46.
lip_width = 52 - 47 # 5
lip_start_x = 46 # Overlap with arm (arm ends at 52)
lip = cq.Workplane("XY").box(lip_width, 8, 5).translate((lip_start_x + lip_width/2, 0, -10.5))

# Combine Plate + Arm + Lip (R1)
# We use union on the objects. Since they overlap by > 1mm, they will form one solid.
combined = plate.union(arm).union(lip)

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

# Final Result: Subtract the pocket from the solid body
result = combined.cut(pocket_vol)