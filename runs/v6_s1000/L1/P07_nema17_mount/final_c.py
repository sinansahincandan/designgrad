import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
BASE_HEIGHT = 15.0
CENTRAL_BORE_DIA = 22.5
MOTOR_HOLE_DIA = 3.4
BASE_SCREW_DIA = 5.5

# Dimensions
BASE_X_WIDTH = 70.0  # x from -35 to 35
BASE_Y_DEPTH = 50.0  # y from 0 to 50
FACE_Z_HEIGHT = 55.0 # z from 0 to 55

# Motor mounting positions (x, z)
MOTOR_SHAFT_Z = 30.0
MOTOR_HOLE_OFFSET = 15.5
MOTOR_HOLES = [
    (15.5, MOTOR_SHAFT_Z + MOTOR_HOLE_OFFSET),
    (-15.5, MOTOR_SHAFT_Z + MOTOR_HOLE_OFFSET),
    (15.5, MOTOR_SHAFT_Z - MOTOR_HOLE_OFFSET),
    (-15.5, MOTOR_SHAFT_Z - MOTOR_HOLE_OFFSET)
]

# Base screw positions (x, y)
BASE_SCREW_X = 25.0
BASE_SCREW_Y = 25.0
BASE_HOLES = [
    (BASE_SCREW_X, BASE_SCREW_Y),
    (-BASE_SCREW_X, BASE_SCREW_Y)
]

# 1. Create the main L-shape body (R1)
# Base Plate: x [-35, 35], y [0, 50], z [0, 15]
base = cq.Workplane("XY").box(BASE_X_WIDTH, BASE_Y_DEPTH, BASE_HEIGHT, centered=(True, True, False))

# Face Plate: x [-35, 35], y [0, 4], z [0, 55]
# To ensure connection with the base (z=0 to 15), we make sure the face plate starts at z=0.
# The previous error showed a gap because of how translate/centered was used.
# We will define the face plate explicitly by its min corner.
face = (
    cq.Workplane("XY")
    .box(BASE_X_WIDTH, FACE_PLATE_THICKNESS, FACE_Z_HEIGHT, centered=(True, True, False))
    .translate((0, FACE_PLATE_THICKNESS/2, 0)) # Min corner at (x=-35, y=0, z=0)
)

# Combine into one single solid before subtractions (R1)
bracket = base.union(face)

# 2. Subtract Motor Clearance Pocket (R5)
# Requirement: x in [-21.5, 21.5], z in [8.5, 51.5], y in [0, 4]
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 4.0, 43.0, centered=(True, True, False)) # width 43 -> -21.5 to 21.5
    .translate((0, 2.0, 30.0)) # center z=30 (8.5 to 51.5), y=2 (0 to 4)
)
bracket = bracket.cut(clearance_box)

# 3. Subtract Holes
# Central bore (R3): diameter 22.5 through face plate on shaft axis (x=0, z=30)
# The face is at y=4.
bracket = bracket.faces(">Y").workplane().center(0, MOTOR_SHAFT_Z).hole(CENTRAL_BORE_DIA)

# Motor screw holes (R4): diameter 3.4 through face plate
for x_off, z_pos in MOTOR_HOLES:
    bracket = bracket.faces(">Y").workplane().center(x_off, z_pos).hole(MOTOR_HOLE_DIA)

# Base screw holes (R6): diameter 5.5 vertical through base plate at z=0
for x_off, y_off in BASE_HOLES:
    bracket = bracket.faces("<Z").workplane().center(x_off, y_off).hole(BASE_SCREW_DIA)

result = bracket