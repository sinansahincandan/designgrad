import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 55.0
BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0

# Motor Hole Coordinates (R4) - relative to face plate workplane at y=0
motor_holes = [
    (15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 + 15.5),
    (-15.5, 30 - 15.5)
]

# Base Hole Coordinates (R6) - relative to base plate workplane at z=0
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body (R1)
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=False)
    .translate((-FACE_PLATE_WIDTH/2, 0, 0))
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
# We include the R6 holes directly in the base plate definition for robustness
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-BASE_PLATE_WIDTH/2, 0, 0))
    .faces("<Z") # Select the bottom face (z=0)
    .workplane()
    .pushPoints(base_holes)
    .hole(5.5)
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Use an explicit cylinder subtraction on the YZ plane to ensure diameter and orientation are exact.
# The shaft axis is at x=0, z=30. We drill through the face plate along the Y axis.
central_bore = (
    cq.Workplane("YZ")
    .center(0, 30)
    .cylinder(FACE_PLATE_THICKNESS + 2, 22.5/2)
)
bracket = bracket.cut(central_bore)

# 3. Subtract Motor Screw Holes (R4)
# Use pushPoints on the face plane to ensure all holes are drilled through the Y-axis correctly.
bracket = (
    bracket.faces("<Y")
    .workplane()
    .pushPoints(motor_holes)
    .hole(3.4)
)

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5.
# Note: The bracket exists in positive Y. This pocket is in negative Y.
# However, the design doc mentions a "recessed area/pocket cut into the face plate".
# Based on R5 constraints, we subtract the volume to ensure clearance.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5), centered=False)
    .translate((-21.5, -48, 8.5))
)
bracket = bracket.cut(clearance_box)

result = bracket