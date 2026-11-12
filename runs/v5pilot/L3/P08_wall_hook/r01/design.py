import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

strap_pocket_x_range = (35, 45)
strap_pocket_y_width = 12.0  # |y| <= 6 -> width 12
strap_pocket_z_range = (-13, -6)

lip_x_range = (47, 52)
lip_y_width = 8.0   # |y| <= 4 -> width 8
lip_z_range = (-13, -8)

# 1. Create the Back Plate (R2, R3)
# x: [0, 2], y: [-8, 8], z: [-5, 45]
# Center of plate is at x=1, y=0, z=20
p = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((1, 0, 20))

# R3: Two screw holes at (y=0, z=0) and (y=0, z=40)
# Since the plate is translated by +20 in Z, local Z offsets are -20 and +20.
# We use faces("<X") to select the face at x=0 for drilling through.
p = p.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R1, R6)
# To ensure R1 (single solid) and R6 (strength), we create a beefy arm that intersects the plate.
# The arm must cover the Z-range of the pocket (-13 to -6).
# We'll make it thick near the wall and taper towards the tip.
arm_part = (
    cq.Workplane("XY")
    .box(50, 16, 30) # Large structural block
    .translate((26, 0, -5)) # Center at x=26, y=0, z=-5. Z range: [-20, 10]
)

# 3. Create the Retaining Lip (R5)
# x: [47, 52], |y| <= 4, z: [-13, -8]
lip_part = (
    cq.Workplane("XY")
    .box(5, 8, 5)
    .translate((49.5, 0, -10.5)) # Center of x[47,52], y[-4,4], z[-13,-8]
)

# 4. Combine components (R1)
# We union the plate, arm, and lip. Because the arm starts at x=1 (center 26 - half-width 25),
# it overlaps with the plate (x: [0, 2]), ensuring a single solid.
combined = p.union(arm_part).union(lip_part)

# 5. Subtract the Strap Pocket (R4)
# R4: space (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty.
# The pocket volume is a box centered at x=40, y=0, z=-9.5
pocket_vol = (
    cq.Workplane("XY")
    .box(10, 12, 7) # width 10 (x), height 12 (y), depth 7 (z)
    .translate((40, 0, -9.5))
)

# Perform the cut to create the recessed seat
result = combined.cut(pocket_vol)

# Final verification of R4:
# Pocket Z range: -9.5 +/- 3.5 => [-13, -6]. Correct.
# Pocket X range: 40 +/- 5 => [35, 45]. Correct.
# Pocket Y range: 0 +/- 6 => [-6, 6]. Correct.