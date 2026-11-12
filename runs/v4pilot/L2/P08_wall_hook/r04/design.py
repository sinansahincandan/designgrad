import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

strap_pocket_x_min, strap_pocket_x_max = 35, 45
strap_pocket_y_min, strap_pocket_y_max = -6, 6
strap_pocket_z_min, strap_pocket_z_max = -13, -6

# 1. Create the Back Plate (R2)
# x: [0, 2], y: [-8, 8], z: [-5, 45]
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height)
plate = plate.translate((plate_thickness/2, 0, 20))

# 2. Create the Support Arm (R6)
# We create a beefy arm to handle bending stress and ensure it encompasses the pocket area.
# The arm needs to extend from the plate (x=2) to at least x=52.
# To satisfy R4, the arm must exist in the space where the pocket is subtracted.
arm_part = cq.Workplane("XY").box(50, 14, 25).translate((27, 0, -10))

# 3. Create the Retaining Lip (R5)
# x: [47, 52], y: [-4, 4], z: [-13, -8]
# Center of box at x=49.5, y=0, z=-10.5. Width=5, Height=8, Depth=5.
lip_part = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# 4. Combine all additive parts (R1)
total_additions = plate.union(arm_part).union(lip_part)

# 5. Create Subtractions (R3 & R4)

# Screw Holes (R3): Cylinders at (0,0,0) and (0,0,40) passing through the plate
# We use a height of 10 to ensure they clear the 2mm plate easily.
hole1 = cq.Workplane("XY").cylinder(10, screw_hole_dia).translate((0, 0, 0))
hole2 = cq.Workplane("XY").cylinder(10, screw_hole_dia).translate((0, 0, 40))

# Strap Pocket (R4): x[35, 45], y[-6, 6], z[-13, -6]
# Box dimensions: dx=10, dy=12, dz=7. Center: x=40, y=0, z=-9.5
pocket_vol = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# 6. Final Boolean Subtraction
result = total_additions.cut(hole1).cut(hole2).cut(pocket_vol)

# Verification of R4:
# Pocket Z range: -9.5 +/- 3.5 -> [-13, -6]. Correct.
# Pocket X range: 40 +/- 5 -> [35, 45]. Correct.
# Pocket Y range: 0 +/- 6 -> [-6, 6]. Correct.

# Verification of R5:
# Lip X range: 49.5 +/- 2.5 -> [47, 52]. Correct.
# Lip Z range: -10.5 +/- 2.5 -> [-13, -8]. Correct.