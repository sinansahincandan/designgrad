import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4) - Based on Design Doc: (+-15.5, 30 +- 15.5)
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

# 1. Create and process the Face Plate
# Face plate: y from 0 to 4, x from -35 to 35, z from 0 to 55 (approx)
# We use XZ plane for construction so thickness is in Y.
face_plate = (
    cq.Workplane("XZ")
    .box(70, 55, FACE_PLATE_THICKNESS)
    .translate((0, 27.5, 2)) # Center in X, Z center at 27.5, Y thickness [0,4]
)

# Subtract R3 (Central Bore) and R4 (Motor Screw Holes) from face_plate BEFORE union
face_plate = (
    face_plate.faces("<Y")
    .workplane()
    .pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)])
    .hole(22.5) # R3
)

for x, z in motor_holes:
    face_plate = (
        face_plate.faces("<Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4) # R4
    )

# 2. Create and process the Base Plate
# Base plate: z from 0 to 5, x from -35 to 35, y from 0 to 50
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS)
    .translate((0, 25, BASE_PLATE_THICKNESS / 2)) # Center in X, Y center at 25, Z [0,5]
)

# Subtract R6 (Base Screw Holes) from base_plate BEFORE union
# We use the top face of the base plate to drill down through Z
base_plate = (
    base_plate.faces(">Z")
    .workplane()
    .pushPoints(base_holes)
    .hole(5.5) # R6
)

# 3. Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We subtract a box that covers this volume from the combined bracket.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5)) # Width=43 (x), Depth=48 (y), Height=43 (z)
    .translate((0, -24, (51.5 + 8.5) / 2)) # y center is (-48+0)/2 = -24
)

# Subtract the clearance volume from the final bracket
result = bracket.cut(clearance_box)