import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0 # y direction
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5
strap_width = 10.0
strap_thickness = 6.0

# 1. Create the Back Plate
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height)
# Center plate at x=plate_thickness/2, y=0, z=20 (so z range is -5 to 45)
plate = plate.translate((plate_thickness/2, 0, 20))

# 2. Create the Screw Holes
# Hole 1 at (y=0, z=0), Hole 2 at (y=0, z=40)
# Note: Plate is translated by 20 in Z, so local Z for holes are -20 and +20
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 3. Create the Main Hook Arm (Structural Body)
# We build a tapered arm to connect the plate to the strap seat
# The arm starts near the plate and extends to the lip
arm = cq.Workplane("XY").box(50, 12, 15) # Rough block
# Refine arm: Tapered profile from x=2 to x=52
# We will use a union of primitives for better control over the single solid requirement
arm_body = (
    cq.Workplane("XY")
    .box(50, 14, 18) # Main structural mass
    .translate((25, 0, -10)) # Position it
)

# To ensure R6 (Strength), we make the connection at x=2 very beefy
connection = cq.Workplane("XY").box(10, 18, 30).translate((7, 0, 5))
arm_structure = arm_body.union(connection)

# 4. Create the Strap Seat and Lip
# The strap rests on a bed at z = -14. 
# Requirement R4: space (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty.
# We'll build the hook by starting with a solid and subtracting the strap pocket.

# Let's redefine the approach to ensure one single valid solid via additive construction
# Base block for the arm
base_arm = cq.Workplane("XY").box(50, 14, 25).translate((26, 0, -10))

# Combine Plate + Arm
hook_solid = plate.union(base_arm)

# Add the Retaining Lip (R5)
lip = cq.Workplane("XY").box(6, 8, 5).translate((49.5, 0, -10.5))
hook_solid = hook_solid.union(lip)

# Subtract the Strap Pocket (R4)
# The pocket is: 35 <= x <= 45, |y| <= 6, -13 <= z <= -6
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))
hook_solid = hook_solid.cut(pocket)

# Ensure the strap bed is at z = -14
# The current Z of the arm center is -10. With height 25, Z range is [-22.5, 0]
# We need a flat surface at z = -14 for the strap to rest on.
# Let's refine the geometry by creating a specific "seat" block and unioning it.

# RE-DESIGNING FOR PRECISION:
# Part A: Plate
p = cq.Workplane("XY").box(2, 16, 50).translate((1, 0, 20))
p = p.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# Part B: The Arm (Tapered for strength)
# We'll use a loft or a series of boxes to ensure R6
arm_part = (
    cq.Workplane("XY")
    .box(50, 14, 20).translate((27, 0, -10)) # Main body
)

# Part C: The Lip
lip_part = cq.Workplane("XY").box(6, 8, 5).translate((49.5, 0, -10.5))

# Combine A, B, C
combined = p.union(arm_part).union(lip_part)

# Part D: The Strap Pocket (Subtraction)
# R4: pocket is x[35,45], y[-6,6], z[-13,-6]
pocket_vol = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))
result = combined.cut(pocket_vol)

# Final check on Z-coordinates for the strap bed:
# The pocket bottom is at z = -9.5 - (7/2) = -13. 
# The pocket top is at z = -9.5 + (7/2) = -6.
# This matches R4 requirement exactly.