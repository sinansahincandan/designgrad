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
# We use centered=False and translate to ensure exact bounds
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=False)
    .translate((-FACE_PLATE_WIDTH/2, 0, 0))
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
# We ensure it overlaps the face plate at the corner (y=0..4, z=0..5)
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-BASE_PLATE_WIDTH/2, 0, 0))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis. 
# The face plate is at y in [0, 4]. We drill from the front face (<Y) or back face (>Y).
# Since we want to pass through the face plate, we use a cylinder along Y.
bracket = (
    bracket.faces("<Y")
    .workplane()
    .pushPoints([(0, 30)])
    .hole(22.5)
)

# 3. Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    bracket = (
        bracket.faces("<Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We subtract a box that overlaps the face plate at y=0.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5), centered=False)
    # x: [-21.5, 21.5] -> min_x = -21.5
    # y: [-48, 0]     -> min_y = -48
    # z: [8.5, 51.5]  -> min_z = 8.5
    .translate((-21.5, -48, 8.5))
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# Vertical holes through the base plate at (x, y) = (+-25, 25)
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket