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
# Face plate: y from 0 to 4, centered vertically around z=30 (z range: 30 +/- 27.5 -> 2.5 to 57.5 is too high? 
# Let's follow feedback: translate(0, FACE_PLATE_THICKNESS/2, 30) for a box of height 55 means z goes from 30-27.5 to 30+27.5 = 2.5 to 57.5.
# Wait, R7 says top <= 55. Let's adjust the face plate height to 52.5 so it reaches exactly 55 (30 +/- 25).
face_plate_height = 50.0 # z range: 30 - 25 to 30 + 25 -> 5 to 55.
face_plate = (
    cq.Workplane("XY")
    .box(70, FACE_PLATE_THICKNESS, face_plate_height)
    .translate((0, FACE_PLATE_THICKNESS/2, MOTOR_SHAFT_Z))
)

# Base plate: bottom at z=0, y from 0 to 50 (centered at y=25), x from -35 to 35
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS)
    .translate((0, 25, BASE_PLATE_THICKNESS/2))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis
# Face plate is at y=0 to 4, so we select the face at y=4 or use a workplane on the side
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
    .box(43.0, 48.0, (51.5 - 8.5)) # width=43 (x), depth=48 (y), height=43 (z)
    .translate((0, -24, (51.5 + 8.5)/2)) # center y at -24, center z at 30
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
for x, y in base_holes:
    bracket = (
        bracket.faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket