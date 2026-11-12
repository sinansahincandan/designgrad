import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
FACE_PLATE_WIDTH = 70.0  # x from -35 to 35
FACE_PLATE_HEIGHT = 55.0 # z from 0 to 55
BASE_PLATE_DEPTH = 25.0  # y from 0 to 25

# Motor Hole Coordinates (R4)
motor_holes = [
    (15.5, 45.5),
    (15.5, 14.5),
    (-15.5, 45.5),
    (-15.5, 14.5)
]

# Base Hole Coordinates (R6)
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body (R1)
# Face plate: x in [-35, 35], y in [0, 4], z in [0, 55]
# The previous error showed face_plate was translated incorrectly to Z=27.5..82.5
# We define it exactly as the design document specifies: x[-35,35], y[0,4], z[0,55]
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=(True, False, False))
    .translate((0, 0, 0)) # Min corner at (0,0,0) relative to center logic? No, box(centered=False) puts min corner at translate point.
)
# To match x in [-35, 35], y in [0, 4], z in [0, 55]:
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=False)
    .translate((-FACE_PLATE_WIDTH/2, 0, 0))
)

# Base plate: x in [-35, 35], y in [0, 25], z in [0, 5]
base_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-FACE_PLATE_WIDTH/2, 0, 0))
)

# Combine into a single solid
# They overlap at y in [0,4] and z in [0,5]
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis at (0, 30)
# The face plate is y in [0,4]. We drill along Y.
bracket = (
    bracket.faces("<Y").workplane()
    .center(0, 30)
    .hole(22.5)
)

# 3. Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    bracket = (
        bracket.faces("<Y").workplane()
        .center(x, z)
        .hole(3.4)
    )

# 4. Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# The pocket is on the negative Y side of the face plate.
pocket = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5), centered=False)
    .translate((-21.5, -48.0, 8.5))
)
bracket = bracket.cut(pocket)

# 5. Subtract Base Screw Holes (R6)
# Two vertical screw holes, diameter 5.5 mm, through the base plate thickness
bracket = (
    bracket.faces("<Z").workplane()
    .pushPoints([(25.0, 25.0), (-25.0, 25.0)])
    .hole(5.5)
)

result = bracket