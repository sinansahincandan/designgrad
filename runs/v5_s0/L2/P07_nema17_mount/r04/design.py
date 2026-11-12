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
# Face plate: y from 0 to 4, z from 0 to 55, x from -35 to 35
face_plate = (
    cq.Workplane("XY")
    .box(70, FACE_PLATE_THICKNESS, 55, centered=(True, False, True))
    .translate((0, FACE_PLATE_THICKNESS / 2, 27.5))
)

# Base plate: z from 0 to BASE_PLATE_THICKNESS, y from 0 to 50, x from -35 to 35
# Using centered=(True, False, False) ensures the bottom face is exactly at z=0
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, False))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis at (0, 30)
# Using .hole() on the <Y face (the one at y=0) to ensure precision
bracket = (
    bracket.faces("<Y")
    .workplane()
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .hole(22.5)
)

# 3. Subtract Motor Screw Holes (R4)
# Diameter 3.4 through the face plate along Y at specified coordinates
bracket = (
    bracket.faces("<Y")
    .workplane()
    .pushPoints(motor_holes)
    .hole(3.4)
)

# 4. Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We subtract a box that represents the motor body volume to ensure clearance.
# Since the bracket is on the +Y side and motor is in -Y, we cut into the face plate.
bracket = bracket.cut(
    cq.Workplane("XY")
    .box(43.0, 10.0, (51.5 - 8.5), centered=(True, False, True))
    .translate((0, -5.0, (51.5 + 8.5) / 2)) # Y center at -5 to overlap the y=0 plane
)

# 5. Subtract Base Screw Holes (R6)
# Vertical holes through the base plate at specified x, y coordinates
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket