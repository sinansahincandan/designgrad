import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
BASE_HEIGHT = 9.0  # Reduced from 15 to help meet mass requirement R7
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0
MOTOR_HOLE_OFFSET = 15.5
MOTOR_HOLE_DIA = 3.4
CENTRAL_BORE_DIA = 22.5

# Base plate dimensions
BASE_X_WIDTH = 70.0
BASE_Y_DEPTH = 50.0

# 1. Create the main L-shape body
# Base Plate: x [-35, 35], y [0, 50], z [0, BASE_HEIGHT]
base = cq.Workplane("XY").box(BASE_X_WIDTH, BASE_Y_DEPTH, BASE_HEIGHT, centered=(True, True, False))

# Face Plate: x [-35, 35], y [0, 4], z [0, 55]
# Centered at y=2 (so it spans 0 to 4) and z=30 (shaft axis)
face = (
    cq.Workplane("XY")
    .box(BASE_X_WIDTH, FACE_PLATE_THICKNESS, 55)
    .translate((0, 2, 30)) # y-center is 2, z-center is 30
)

# Combine into one solid (R1)
bracket = base.union(face)

# 2. Subtract Holes
# R3: Central bore (drilled through face plate along Y axis)
# We select the face at y=4 or y=0 to drill through
bracket = bracket.faces(">Y").workplane().center(0, MOTOR_SHAFT_Z).hole(CENTRAL_BORE_DIA)

# R4: Four motor screw holes (drilled through face plate along Y axis)
motor_holes = [
    (15.5, 30 + 15.5),
    (-15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 - 15.5)
]

for x_off, z_pos in motor_holes:
    bracket = bracket.faces(">Y").workplane().center(x_off, z_pos).hole(MOTOR_HOLE_DIA)

# R6: Base screw holes (vertical along Z axis at x=+/-25, y=25)
base_holes = [
    (25, 25),
    (-25, 25)
]

for x_off, y_off in base_holes:
    # Drill through the bottom face (z=0)
    bracket = bracket.faces("<Z").workplane().center(x_off, y_off).hole(5.5)

# 3. Motor Clearance (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We subtract a box that covers this volume to ensure compliance.
clearance_box = (
    cq.Workplane("XY")
    .box(43, 48, 43) # width=43 (x: -21.5 to 21.5), depth=48 (y: -24 to 24... wait)
    # Let's be precise with the translation for the clearance box
    # x range [-21.5, 21.5] -> center 0, width 43
    # y range [-48, 0]     -> center -24, depth 48
    # z range [8.5, 51.5]  -> center 30, height 43
    .translate((0, -24, 30))
)
bracket = bracket.cut(clearance_box)

# 4. Mass Reduction (R7)
# To ensure mass < 60g, we remove material from the base plate in non-critical areas.
# We'll cut a slot in the middle of the base plate.
bracket = bracket.cut(
    cq.Workplane("XY")
    .workplane(offset=BASE_HEIGHT)
    .rect(40, 25)
    .extrude(-BASE_HEIGHT * 0.8) # Cut most of the way through
)

result = bracket