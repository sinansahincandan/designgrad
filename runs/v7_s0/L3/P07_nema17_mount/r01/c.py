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
# Face plate: x from -35 to 35, z from 0 to 55, thickness in Y (y=0 to 4)
# Using XZ plane and centered=(True, False, True) puts it at y in [0, 4] if we extrude/box correctly.
# To get y from 0 to 4 with a box of thickness 4: center must be at y=2.
face_plate = cq.Workplane("XZ").box(70, 55, FACE_PLATE_THICKNESS).translate((0, FACE_PLATE_THICKNESS/2, 0))

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
# centered=(True, False, False) ensures it sits on the table (z=0)
base_plate = cq.Workplane("XY").box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, False))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis
bracket = bracket.faces(">Y").workplane().pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]).hole(22.5)

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
# We subtract a box representing this volume.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5), centered=(True, False, True))
    .translate((0, -24, (51.5 + 8.5)/2))
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket