import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
BASE_HEIGHT = 8.0  # Reduced from 15 to keep mass < 60g (R7)
CENTRAL_BORE_DIA = 22.5
MOTOR_HOLE_DIA = 3.4
BASE_SCREW_DIA = 5.5

# Dimensions
FACE_WIDTH = 70.0  # x: -35 to 35
FACE_HEIGHT = 55.0 # z: 0 to 55
BASE_WIDTH = 70.0  # x: -35 to 35
BASE_DEPTH = 50.0  # y: 0 to 50

# Motor mounting positions (x, z)
MOTOR_HOLES = [
    (15.5, 30 + 15.5),
    (-15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 - 15.5)
]

# Base screw positions (x, y)
BASE_SCREWS = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: x [-35, 35], y [0, 4], z [0, 55]
face = cq.Workplane("XY").box(FACE_WIDTH, FACE_PLATE_THICKNESS, FACE_HEIGHT, centered=(True, True, False))
# Note: box with centered=False at origin creates x from 0 to 70. 
# We need x from -35 to 35. Let's use translate.
face = cq.Workplane("XY").box(FACE_WIDTH, FACE_PLATE_THICKNESS, FACE_HEIGHT).translate((0, FACE_PLATE_THICKNESS/2, FACE_HEIGHT/2))
# To ensure z starts at 0 and y is [0,4]:
face = cq.Workplane("XY").box(FACE_WIDTH, FACE_PLATE_THICKNESS, FACE_HEIGHT).translate((0, FACE_PLATE_THICKNESS/2, FACE_HEIGHT/2))
# Wait, the simplest way to get x:[-35,35], y:[0,4], z:[0,55]:
face = cq.Workplane("XY").box(FACE_WIDTH, FACE_PLATE_THICKNESS, FACE_HEIGHT).translate((0, FACE_PLATE_THICKNESS/2, FACE_HEIGHT/2))
# Let's re-verify: center is (0, 2, 27.5). x range [-35, 35]. y range [0, 4]. z range [0, 55]. Correct.

# Base plate: x [-35, 35], y [0, 50], z [0, BASE_HEIGHT]
base = cq.Workplane("XY").box(BASE_WIDTH, BASE_DEPTH, BASE_HEIGHT).translate((0, BASE_DEPTH/2, BASE_HEIGHT/2))

# Combine into one solid (R1)
bracket = base.union(face)

# 2. Subtract Holes
# Central bore (R3): through face plate along Y axis at (0, 30)
# We use a cylinder to ensure it cuts through the thickness correctly
bracket = bracket.cut(cq.Workplane("YZ").center(0, 30).cylinder(FACE_PLATE_THICKNESS * 2, CENTRAL_BORE_DIA, centered=(True, True, True)).translate((0, 2, 30)))
# Actually, simpler: use the face at y=0 or y=4.
bracket = bracket.faces("<Y").workplane().center(0, 30).hole(CENTRAL_BORE_DIA)

# Motor screw holes (R4): through face plate along Y axis
for x_off, z_pos in MOTOR_HOLES:
    bracket = bracket.faces("<Y").workplane().center(x_off, z_pos).hole(MOTOR_HOLE_DIA)

# Base screw holes (R6): vertical through base at (x, y)
for x_off, y_off in BASE_SCREWS:
    bracket = bracket.faces("<Z").workplane().center(x_off, y_off).hole(BASE_SCREW_DIA)

# 3. Motor Clearance (R5)
# Forbidden zone: -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We create a box representing this volume and subtract it.
clearance_box = cq.Workplane("XY").box(43, 48, 43).translate((0, -24, 30))
bracket = bracket.cut(clearance_box)

result = bracket