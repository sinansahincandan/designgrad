import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4)
motor_holes = [
    (15.5, 45.5),
    (-15.5, 45.5),
    (15.5, 14.5),
    (-15.5, 14.5)
]

# Base Hole Coordinates (R6)
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: y from 0 to 4, x from -35 to 35, z from 0 to 55
face_plate = (
    cq.Workplane("XZ")
    .box(70, 55, FACE_PLATE_THICKNESS)
    # Center in X: 0, thickness is in Y [0,4] -> center at y=2, Z center at 27.5
    .translate((0, 2, 27.5)) 
)

# Base plate: z from 0 to 5, x from -35 to 35, y from 0 to 50
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS)
    # Center in X: 0, Y center at 25, Z is [0,5] -> center at z=2.5
    .translate((0, 25, BASE_PLATE_THICKNESS / 2))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis.
# Target the front face of the face plate at y=4.
# Using a selector that finds faces with centroid y near 4.0
bracket = (
    bracket.faces("<Y")
    .workplane()
    .pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)])
    .hole(22.5)
)

# 3. Subtract Motor Screw Holes (R4)
# Target the front face of the face plate at y=4 and subtract all holes at once.
bracket = (
    bracket.faces("<Y")
    .workplane()
    .pushPoints(motor_holes)
    .hole(3.4)
)

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5)) # Width=43 (x), Depth=48 (y), Height=43 (z)
    .translate((0, -24, (51.5 + 8.5) / 2)) # y center is (-48+0)/2 = -24
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# Target the top face of the base plate at z=5 and drill downwards.
bracket = (
    bracket.faces("<Z")
    .workplane()
    .pushPoints(base_holes)
    .hole(5.5)
)

result = bracket