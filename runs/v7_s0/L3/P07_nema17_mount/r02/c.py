import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4)
# Based on design doc: (+-15.5, 30), (+-15.5, 45.5), (+-15.5, 14.5)
# The feedback/doc implies a pattern around the shaft axis at z=30 +/- 15.5
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

# 1. Create the main L-shape body (R1)
# Base plate: z from 0 to 5, x from -35 to 35, y from 0 to 50
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, False))
)

# Face plate: y from 0 to 4, x from -35 to 35, z from 0 to 55
# We use XZ plane to define the vertical face and translate it into position
face_plate = (
    cq.Workplane("XZ")
    .box(70, 55, FACE_PLATE_THICKNESS, centered=(True, False, False))
    .translate((0, 2, 0)) # Center thickness at y=2 so it spans y=[0, 4]
)

# Combine into a single solid (R1)
bracket = base_plate.union(face_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis
# The face plate is at y in [0, 4]. We select the face with largest Y to drill through.
bracket = (
    bracket.faces(">Y")
    .workplane()
    .pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)])
    .hole(22.5)
)

# 3. Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5), centered=(True, False, True))
    .translate((0, -24, (51.5 + 8.5) / 2)) # y center: (-48+0)/2 = -24
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# Drilled from the top surface of the base plate (z=5)
for x, y in base_holes:
    bracket = (
        bracket.faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket