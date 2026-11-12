import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
BASE_HEIGHT = 8.0  # Adjusted to help meet mass requirement R7
MOTOR_SHAFT_Z = 30.0
CENTRAL_BORE_DIA = 22.5
MOTOR_HOLE_DIA = 3.4

# Base plate dimensions
BASE_X_WIDTH = 70.0
BASE_Y_DEPTH = 46.0  # Spans y from 4 to 50
BASE_Y_START = 4.0

# Envelope constraints (R7)
BASE_X_LIMIT = 35.0
MAX_Z = 55.0

# 1. Create the main L-shape body
# Face Plate: x [-35, 35], y [0, 4], z [0, 55]
face = (
    cq.Workplane("XY")
    .box(BASE_X_WIDTH, FACE_PLATE_THICKNESS, MAX_Z, centered=(True, True, False))
    .translate((0, FACE_PLATE_THICKNESS / 2, 0)) # y-center is 2, so spans 0 to 4
)

# Base Plate: x [-35, 35], y [4, 50], z [0, BASE_HEIGHT]
base = (
    cq.Workplane("XY")
    .box(BASE_X_WIDTH, BASE_Y_DEPTH, BASE_HEIGHT, centered=(True, True, False))
    .translate((0, BASE_Y_START + BASE_Y_DEPTH / 2, 0))
)

# Combine into one solid (R1)
bracket = face.union(base)

# 2. Subtract Holes
# R3: Central bore (drilled through face plate along Y axis)
# Select the face at y=4 to drill through towards y=0
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
clearance_box = (
    cq.Workplane("XY")
    .box(43, 48, 43) # width=43 (x: -21.5 to 21.5), depth=48 (y: -24 to 24... wait)
    # Precise translation for clearance box:
    # x range [-21.5, 21.5] -> center 0, width 43
    # y range [-48, 0]     -> center -24, depth 48
    # z range [8.5, 51.5]  -> center 30, height 43
    .translate((0, -24, 30))
)
bracket = bracket.cut(clearance_box)

# 4. Mass Reduction (R7)
# To ensure mass < 60g, we remove material from the center of the base plate.
# We cut a slot in the middle of the base plate area that doesn't hit R6 holes or face plate.
mass_reduction_cut = (
    cq.Workplane("XY")
    .workplane(offset=BASE_HEIGHT)
    .rect(40, 25) # x: [-20, 20], y: [center-12.5, center+12.5]
    # We want to cut in the base area (y > 4). Let's place it around y=30.
    .translate((0, 30, 0)) 
    .extrude(-BASE_HEIGHT) # Cut all the way through the base
)
bracket = bracket.cut(mass_reduction_cut)

result = bracket