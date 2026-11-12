import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4)
motor_holes = [
    (15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 + 15.5),
    (-15.5, 30 - 15.5)
]

# Base Hole Coordinates (R6)
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = cq.Workplane("XY").box(70, FACE_PLATE_THICKNESS, 55, centered=(True, False, True))

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
# Fix R6: Use centered=(True, False, False) so the bottom face is at z=0
base_plate = cq.Workplane("XY").box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, False))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Y-axis holes (Central Bore R3 and Motor Holes R4)
# We do this BEFORE the clearance pocket to ensure workplanes are stable on the original faces.
# Using .faces(">Y") selects the face at y=4.
bracket = bracket.faces(">Y").workplane()

# Subtract Central Bore (R3)
bracket = bracket.pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]).hole(22.5)

# Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    bracket = bracket.pushPoints([(x, z)]).hole(3.4)

# 3. Subtract Base Screw Holes (R6)
# Select the bottom face of the base plate at z=0
bracket = bracket.faces("<Z").workplane()
for x, y in base_holes:
    bracket = bracket.pushPoints([(x, y)]).hole(5.5)

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# Since the bracket is at y >= 0, we cut a notch into the face plate from the motor side (y=0).
pocket_z_min = 8.5
pocket_z_max = 51.5
pocket_y_start = -48.0
pocket_y_end = 0.0

# Define the clearance volume as a box and subtract it from the bracket
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, abs(pocket_y_start), (pocket_z_max - pocket_z_min), centered=(True, False, True))
    .translate((0, pocket_y_start / 2, (pocket_z_max + pocket_z_min) / 2))
)

# To ensure the pocket cuts into the face plate at y=0, we define a box that spans the required volume.
# The bracket exists for y > 0. We subtract the volume defined by R5.
bracket = bracket.cut(
    cq.Workplane("XY")
    .box(43.0, 48.0, (pocket_z_max - pocket_z_min), centered=(True, False, True))
    .translate((0, -24.0, (pocket_z_max + pocket_z_min) / 2))
)

result = bracket