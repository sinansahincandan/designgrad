import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0
FACE_PLATE_Z_CENTER = 27.5

# Motor Hole Coordinates (R4) - Global X, Z
motor_holes = [
    (15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 + 15.5),
    (-15.5, 30 - 15.5)
]

# Base Hole Coordinates (R6) - Global X, Y
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: y from 0 to 4, x from -35 to 35, z from 0 to 55
# We use XZ plane and translate so thickness is in Y [0, 4] and Z center at 27.5
face_plate = (
    cq.Workplane("XZ")
    .box(70, 55, FACE_PLATE_THICKNESS)
    .translate((0, 2, 27.5)) # Center in X, Y thickness is [0,4], Z center at 27.5
)

# Base plate: z from 0 to 5, x from -35 to 35, y from 0 to 50
# We use XY plane and translate so thickness is in Z [0, 5]
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS)
    .translate((0, 25, BASE_PLATE_THICKNESS / 2)) # Center in X, Y center at 25, Z is [0,5]
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis. 
# We select the face at y=4 to create a workplane.
# The local origin of the workplane is the center of the face (0, 27.5).
bracket = (
    bracket.faces(">Y")
    .workplane()
    .pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z - FACE_PLATE_Z_CENTER)])
    .hole(22.5)
)

# 3. Subtract Motor Screw Holes (R4)
# Use the same face at y=4. Adjust Z to be relative to the workplane origin.
for x, z in motor_holes:
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .pushPoints([(x, z - FACE_PLATE_Z_CENTER)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5.
# Since the bracket is at y >= 0, we subtract a box that covers this volume.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5)) # Width=43 (x), Depth=48 (y), Height=43 (z)
    .translate((0, -24, (51.5 + 8.5) / 2)) # y center is (-48+0)/2 = -24
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# Select the bottom face (z=0). The local origin of this workplane is at (x=0, y=25).
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints([(x, y - 25)])
        .hole(5.5)
    )

result = bracket