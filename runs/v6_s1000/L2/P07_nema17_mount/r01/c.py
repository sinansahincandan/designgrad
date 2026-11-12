import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
BASE_HEIGHT = 8.0  # Reduced from 15.0 to meet mass limit (R7)
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0
MOTOR_HOLE_OFFSET = 15.5
MOTOR_HOLE_DIA = 3.4
CENTRAL_BORE_DIA = 22.5

# Base plate dimensions (R7: Envelope -35 <= x <= 35)
BASE_X_HALF = 35.0
BASE_Y_MAX = 50.0

# 1. Create the main L-shape body
# Base Plate: x [-35, 35], y [0, 50], z [0, BASE_HEIGHT]
base = (
    cq.Workplane("XY")
    .box(BASE_X_HALF * 2, BASE_Y_MAX, BASE_HEIGHT, centered=(True, True, False))
)

# Face Plate: x [-35, 35], y [0, 4], z [0, 55]
# The previous error showed the face plate was being created at a high Z offset.
# We define it explicitly to ensure it starts from Z=0 and extends to Z=55.
# This ensures it overlaps with the base plate (Z: 0-8).
face_height = 55.0
face = (
    cq.Workplane("XY")
    .box(BASE_X_HALF * 2, FACE_PLATE_THICKNESS, face_height, centered=(True, True, False))
    # To get y in [0, 4], move by +2 in Y.
    # To get z in [0, 55], move by +27.5 in Z.
    .translate((0, FACE_PLATE_THICKNESS/2, face_height/2))
)

# Combine into one solid (R1)
bracket = base.union(face)

# 2. Subtract Holes

# R3: Central bore diameter 22.5 mm through the face plate along Y at (0, 30)
# We use faces(">Y") which is the plane at y=4 to drill through the thickness
bracket = bracket.faces(">Y").workplane().center(0, MOTOR_SHAFT_Z).hole(CENTRAL_BORE_DIA)

# R4: Four motor screw holes diameter 3.4 mm along Y at (+-15.5, 30 +- 15.5)
motor_holes = [
    (MOTOR_HOLE_OFFSET, MOTOR_SHAFT_Z + MOTOR_HOLE_OFFSET),
    (-MOTOR_HOLE_OFFSET, MOTOR_SHAFT_Z + MOTOR_HOLE_OFFSET),
    (MOTOR_HOLE_OFFSET, MOTOR_SHAFT_Z - MOTOR_HOLE_OFFSET),
    (-MOTOR_HOLE_OFFSET, MOTOR_SHAFT_Z - MOTOR_HOLE_OFFSET)
]

for x_off, z_pos in motor_holes:
    bracket = bracket.faces(">Y").workplane().center(x_off, z_pos).hole(MOTOR_HOLE_DIA)

# R6: Base screw holes diameter 5.5 mm vertical at (+-25, 25)
base_holes = [
    (25, 25),
    (-25, 25)
]

for x_off, y_off in base_holes:
    # Drill from bottom (z=0) upwards through the base plate
    bracket = bracket.faces("<Z").workplane().center(x_off, y_off).hole(5.5)

# 3. Motor Clearance (R5)
# Requirement: Nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
clearance_pocket = (
    cq.Workplane("XY")
    .box(43, 48, 43)
    .translate((0, -24, 30))
)
bracket = bracket.cut(clearance_pocket)

# Final Result
result = bracket