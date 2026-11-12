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
# To ensure it connects to the face plate (which is at y=0..4), 
# we make sure the base plate starts at y=0 and extends to y=50.
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, False))
    .translate((0, 0, BASE_PLATE_THICKNESS / 2))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis at (0, 30)
bracket = bracket.cut(
    cq.Workplane("XZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .circle(22.5 / 2)
    .extrude(10)
    .translate((0, 2, 0)) # Center in Y-space relative to face plate (y=0..4)
)

# 3. Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    hole_cyl = (
        cq.Workplane("XZ")
        .center(x, z)
        .circle(3.4 / 2)
        .extrude(10)
        .translate((0, 2, 0))
    )
    bracket = bracket.cut(hole_cyl)

# 4. Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We subtract a volume that overlaps the face plate at y=0 to create the pocket.
bracket = bracket.cut(
    cq.Workplane("XY")
    .box(43.0, 10.0, (51.5 - 8.5), centered=(True, False, True))
    .translate((0, 0, (51.5 + 8.5) / 2))
)

# 5. Subtract Base Screw Holes (R6)
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket