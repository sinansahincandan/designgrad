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

# 1. Create the main L-shape body (R1)
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = cq.Workplane("XY").box(
    FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, 
    centered=(True, False, False)
).translate((0, 2.0, 0)) # Spans y: [0, 4]

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
# To ensure it is one solid and overlaps the face plate (y=0..4), 
# we make sure the base plate starts at y=0.
base_plate = cq.Workplane("XY").box(
    FACE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, 
    centered=(True, False, False)
).translate((0, 0, 0)) # Spans y: [0, 50], z: [0, 5]

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis at (0, 30)
bracket = bracket.cut(
    cq.Workplane("XZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .cylinder(FACE_PLATE_THICKNESS * 2, 22.5, centered=(True, True, True))
    .translate((0, 2.0, 0)) # Align with face plate Y-center (y=2)
)

# 3. Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    bracket = bracket.cut(
        cq.Workplane("XZ")
        .center(x, z)
        .cylinder(FACE_PLATE_THICKNESS * 2, 3.4, centered=(True, True, True))
        .translate((0, 2.0, 0)) # Align with face plate Y-center (y=2)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
pocket_x_dim = 43.0  # 21.5 * 2
pocket_y_dim = 48.0
pocket_z_dim = (51.5 - 8.5)

clearance_box = (
    cq.Workplane("XY")
    .box(pocket_x_dim, pocket_y_dim, pocket_z_dim, centered=True)
    .translate((0, -24.0, (51.5 + 8.5) / 2)) # y center: (-48+0)/2 = -24; z center: (51.5+8.5)/2
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# Vertical holes at (x, y) through the base plate (z=0 to 5)
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .center(x, y)
        .hole(5.5)
    )

result = bracket