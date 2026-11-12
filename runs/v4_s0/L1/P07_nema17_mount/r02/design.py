import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
FACE_PLATE_HEIGHT = 55.0
BASE_PLATE_DEPTH = 55.0  # y from 0 to 55
ENVELOPE_WIDTH = 50.0    # x from -25 to 25 (Updated per feedback)

# Motor Hole Coordinates (R4)
motor_holes = [
    (15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 + 15.5),
    (-15.5, 30 - 15.5)
]

# Base Hole Coordinates (R6)
# Located at x = +-25, which is the edge of the new ENVELOPE_WIDTH
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body (R1)
# Face plate: x from -25 to 25, y from 0 to 4, z from 0 to 55
face_plate = cq.Workplane("XY").box(ENVELOPE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=(True, False, True))

# Base plate: x from -25 to 25, y from 0 to 55, z from 0 to 5
base_plate = cq.Workplane("XY").box(ENVELOPE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=(True, False, True))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis at (0, 30)
bracket = bracket.faces(">Y").workplane().pushPoints([(0, 30)]).hole(22.5)

# 3. Subtract Motor Screw Holes (R4)
# Four holes diameter 3.4 through the face plate along Y axis
for x, z in motor_holes:
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We create a box representing this volume and subtract it from the bracket.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5)) # width=43 (x), depth=48 (y), height=(z_max-z_min)
    .translate((0, -24.0, (51.5 + 8.5) / 2.0)) # center y at (-48+0)/2, center z at (51.5+8.5)/2
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# Two vertical holes diameter 5.5 at (x, y) = (+-25, 25) through the base plate
for x, y in base_holes:
    bracket = (
        bracket.faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket