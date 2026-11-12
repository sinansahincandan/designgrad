import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
FACE_PLATE_WIDTH = 70.0  # x from -35 to 35
FACE_PLATE_HEIGHT = 55.0 # z from 0 to 55
BASE_PLATE_DEPTH = 50.0  # y from 0 to 50

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
# We use centered=False and translate so that min corner is at (x,y,z)
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=False)
    .translate((-FACE_PLATE_WIDTH/2, 0, 0))
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
# To ensure it is a single solid, the base plate must overlap with the face plate.
# Face plate is at y in [0, 4]. Base plate should start at y=0 and go to y=50.
base_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-FACE_PLATE_WIDTH/2, 0, 0))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis. 
# The face plate is at y in [0, 4]. We drill from y=0 to y=4.
bracket = (
    bracket.faces("<Y")
    .workplane()
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .hole(22.5)
)

# 3. Subtract Motor Screw Holes (R4)
# Diameter 3.4 through the face plate along Y axis at specified (x, z)
for x, z in motor_holes:
    bracket = (
        bracket.faces("<Y")
        .workplane()
        .center(x, z)
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# Our face plate occupies y from 0 to 4. We must cut the part of the face plate that intersects this volume.
pocket_width = 21.5 * 2 # 43.0
pocket_depth = 4.0 + 1.0 # Extend slightly into the bracket to ensure clean cut at y=0
pocket_height = 51.5 - 8.5

bracket = bracket.cut(
    cq.Workplane("XY")
    .box(pocket_width, pocket_depth, pocket_height, centered=False)
    .translate((-pocket_width/2, -4.0, 8.5)) # y starts at -4 to cover the face plate up to y=0
)

# 5. Subtract Base Screw Holes (R6)
# Two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25), through base plate along Z.
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .center(x, y)
        .hole(5.5)
    )

result = bracket