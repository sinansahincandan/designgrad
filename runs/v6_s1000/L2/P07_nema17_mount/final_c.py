import cadquery as cq

# Constants (Updated per feedback and design document)
FACE_PLATE_THICKNESS = 8.0
BASE_HEIGHT = 10.0
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
# Face plate: x [-35, 35], y [0, 8], z [0, 55]
face = (cq.Workplane("XY")
        .box(FACE_WIDTH, FACE_PLATE_THICKNESS, FACE_HEIGHT)
        .translate((0, FACE_PLATE_THICKNESS/2, FACE_HEIGHT/2)))

# Base plate: x [-35, 35], y [0, 50], z [0, 10]
base = (cq.Workplane("XY")
        .box(BASE_WIDTH, BASE_DEPTH, BASE_HEIGHT)
        .translate((0, BASE_DEPTH/2, BASE_HEIGHT/2)))

# Combine into one solid (R1)
bracket = base.union(face)

# 2. Subtract Holes
# Central bore (R3): through face plate along Y axis at (0, 30)
bracket = bracket.faces("<Y").workplane().center(0, 30).hole(CENTRAL_BORE_DIA)

# Motor screw holes (R4): through face plate along Y axis
for x_off, z_pos in MOTOR_HOLES:
    bracket = bracket.faces("<Y").workplane().center(x_off, z_pos).hole(MOTOR_HOLE_DIA)

# Base screw holes (R6): vertical through base at (x, y)
for x_off, y_off in BASE_SCREWS:
    bracket = bracket.faces("<Z").workplane().center(x_off, y_off).hole(BASE_SCREW_DIA)

# 3. Motor Clearance (R5)
# Forbidden zone: -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# Dimensions: width=43, depth=48, height=43. Center of box at (0, -24, 30)
clearance_box = cq.Workplane("XY").box(43, 48, 43).translate((0, -24, 30))
bracket = bracket.cut(clearance_box)

# 4. Mass Management (R7)
# To keep mass < 60g with increased thicknesses, hollow out the underside of the base plate.
# Subtract a block from the bottom of the base: x [-25, 25], y [5, 45], z [1, 9]
hollow_cut = (cq.Workplane("XY")
              .box(BASE_WIDTH - 20, BASE_DEPTH - 10, BASE_HEIGHT - 2)
              .translate((0, BASE_DEPTH/2, 1)))
bracket = bracket.cut(hollow_cut)

result = bracket