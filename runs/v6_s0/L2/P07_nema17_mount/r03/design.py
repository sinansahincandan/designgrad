import cadquery as cq

# Constants and Dimensions
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_HEIGHT = 55.0

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0
BASE_PLATE_THICKNESS = 5.0

# Motor Hole Coordinates (R4) - (x, z)
motor_holes = [
    (15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 + 15.5),
    (-15.5, 30 - 15.5)
]

# Base Hole Coordinates (R6) - (x, y)
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body (R1, R2)
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=(True, False, True))
    .translate((0, FACE_PLATE_THICKNESS / 2, 0)) # y is [0, 4]
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
# To ensure union and avoid disconnection, we explicitly place the base plate
# such that it overlaps the face plate at the junction (y=0..4).
# The previous error suggested a translation issue. We define the box by its min corner.
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-FACE_PLATE_WIDTH/2, 0, 0)) # x from -35 to 35, y from 0 to 50, z from 0 to 5
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis at x=0, z=30
# The face plate is y in [0, 4]. We drill from the front face (>Y).
bracket = (
    bracket.faces(">Y")
    .workplane()
    .center(0, 30)
    .hole(22.5) # R3: Central Bore
)

# 3. Subtract Motor Screw Holes (R4)
for x_pos, z_pos in motor_holes:
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .center(x_pos, z_pos)
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We extend the cut slightly into the bracket to ensure compliance and clean geometry.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 52.0, (51.5 - 8.5), centered=False)
    .translate((-21.5, -48.0, 8.5)) # Spans x:[-43, 0], y:[-48, 4], z:[8.5, 51.5]
)
# Adjusting clearance box to match the exact requirement bounds and overlap slightly for safety
clearance_box_final = (
    cq.Workplane("XY")
    .box(43.0, 52.0, 43.0, centered=False)
    .translate((-21.5, -48.0, 8.5)) # x: [-43, 0], y: [-48, 4], z: [8.5, 51.5]
)
# The requirement is -21.5 <= x <= 21.5. Width = 43.
clearance_box_final = (
    cq.Workplane("XY")
    .box(43.0, 52.0, 43.0, centered=False)
    .translate((-21.5, -48.0, 8.5))
)
bracket = bracket.cut(clearance_box_final)

# 5. Subtract Base Screw Holes (R6)
# The base plate is at z from 0 to 5. We drill through the top face (>Z).
for x_pos, y_pos in base_holes:
    bracket = (
        bracket.faces(">Z")
        .workplane()
        .center(x_pos, y_pos)
        .hole(5.5)
    )

result = bracket