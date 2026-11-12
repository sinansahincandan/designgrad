import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0  # y direction (total width |y| <= 8)
plate_height = 50.0 # z direction (-5 to 45)
screw_hole_dia = 4.5

arm_length = 50.0
arm_width = 14.0    # y direction (covers |y| <= 6 for pocket)
arm_height = 24.0   # z direction to ensure coverage of pocket and seat
arm_x_start = 2.0

# R4: Pocket dimensions
pocket_x, pocket_y, pocket_z = 10.0, 12.0, 7.0
pocket_translate = (40.0, 0.0, -9.5) # Center of pocket [35-45, -6 to 6, -13 to -6]

# R5: Lip dimensions
lip_width = 5.0     # x direction (47 to 52)
lip_height = 8.0    # z direction (-13 to -5 approx)
lip_depth = 8.0     # y direction (|y| <= 4)

# 1. Create the Back Plate (R2, R3)
# Place plate from x=0 to x=2. Center at x=1, y=0, z=20.
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((1, 0, 20))

# Subtract screw holes (R3)
# Holes at (y=0, z=0) and (y=0, z=40). 
# Since plate is translated by 20 in Z, local hole coordinates are -20 and +20.
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Main Structural Body (R6)
# We need a beefy arm to satisfy R6.
# The arm starts at x=2 and goes to x=52.
# To ensure it covers the pocket [35,45] and seat [-13,-14], 
# we define a large block and subtract from it.
arm = (
    cq.Workplane("XY")
    .box(50, arm_width, arm_height)
    .translate((26, 0, -10)) # X range: [26-25, 26+25] = [1, 51]. Let's adjust to [2, 52]
)
# Adjusting translation for precise x-range [2, 52]
arm = cq.Workplane("XY").box(50, arm_width, arm_height).translate((27, 0, -10))

# 3. Create the Retaining Lip (R5)
# Solid material at 47 <= x <= 52, |y| <= 4, -13 <= z <= -8
lip = cq.Workplane("XY").box(lip_width, lip_depth, 5).translate((49.5, 0, -10.5))

# 4. Combine components (R1)
combined = plate.union(arm).union(lip)

# 5. Subtract the Strap Pocket (R4)
# R4: pocket is x[35,45], y[-6,6], z[-13,-6]
pocket_vol = cq.Workplane("XY").box(pocket_x, pocket_y, pocket_z).translate(pocket_translate)

# Final result
result = combined.cut(pocket_vol)

# Verification of R4: 
# Pocket center z=-9.5, height=7 -> range [-13, -6]. Correct.
# Pocket center x=40, width=10 -> range [35, 45]. Correct.
# Pocket center y=0, width=12 -> range [-6, 6]. Correct.