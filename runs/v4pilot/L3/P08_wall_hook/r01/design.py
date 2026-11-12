import cadquery as cq

# Parameters
screw_hole_dia = 4.5
plate_thickness = 2.0
plate_width = 16.0 # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)

# 1. Create the Back Plate (R2, R3)
# x range [0, 2], y [-8, 8], z [-5, 45]
# Center of box is at (1, 0, 20)
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((1, 0, 20))

# Subtract Screw Holes (R3)
# Target the face at x=0 (the back of the plate relative to global origin)
# Since the box is centered at x=1, the faces are at x=0 and x=2.
# .faces("<X") selects the face with the minimum X coordinate.
# Local coordinates for holes on that face: 
# Plate center in Z is 20. Hole at z=0 -> local z = -20. Hole at z=40 -> local z = 20.
plate_with_holes = (
    plate.faces("<X")
    .workplane()
    .pushPoints([(0, -20), (0, 20)])
    .hole(screw_hole_dia)
)

# 2. Create the Support Arm (R6)
# The arm must be continuous and robust to handle bending stress.
# We'll create a large block that covers the range from x=2 up to the lip.
# To ensure R4 (bed at z=-14), the arm must extend down to at least z=-15.
# Arm dimensions: x [2, 50], y [-6, 6], z [-18, 5]
arm = cq.Workplane("XY").box(48, 12, 23).translate((26, 0, -6.5))

# 3. Create the Retaining Lip (R5)
# x [47, 52], y [-4, 4], z [-13, -8]
# Center: x = 49.5, y = 0, z = -10.5
# Box dimensions: width=5, height=8, depth=5
lip = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# 4. Combine parts via Union (R1)
combined_solid = plate_with_holes.union(arm).union(lip)

# 5. Subtract the Strap Pocket (R4)
# Requirement: space (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty.
# Box dimensions: width=10, height=12, depth=7
# Center: x = 40, y = 0, z = -9.5
pocket_vol = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# Final Result
result = combined_solid.cut(pocket_vol)

# Verification of R4:
# Pocket Z range: -9.5 +/- 3.5 -> [-13, -6]. Correct.
# The arm extends to z = -18 (bottom) and the pocket ends at z = -13.
# This leaves a solid bed at z = -14 (actually a surface from -14 to -13).