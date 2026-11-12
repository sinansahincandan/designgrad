import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 8.0  # Updated per feedback to satisfy R2
BASE_HEIGHT = 8.0           # Height of the base plate (z from 0 to 8)
MOTOR_SHAFT_Z = 30.0
CENTRAL_BORE_DIA = 22.5
MOTOR_HOLE_DIA = 3.4

# Base plate dimensions
BASE_X_WIDTH = 70.0         # x from -35 to 35
BASE_Y_DEPTH = 42.0         # y from 8 to 50 (50-8=42)
BASE_Y_START = 8.0

# Envelope constraints (R7)
MAX_Z = 55.0

# 1. Create the main L-shape body
# Face Plate: x [-35, 35], y [0, 8], z [0, 55]
face = (
    cq.Workplane("XY")
    .box(BASE_X_WIDTH, FACE_PLATE_THICKNESS, MAX_Z, centered=(True, True, False))
    .translate((0, FACE_PLATE_THICKNESS / 2, 0)) # y-center is 4, so spans 0 to 8
)

# Base Plate: x [-35, 35], y [8, 50], z [0, 8]
base = (
    cq.Workplane("XY")
    .box(BASE_X_WIDTH, BASE_Y_DEPTH, BASE_HEIGHT, centered=(True, True, False))
    .translate((0, BASE_Y_START + BASE_Y_DEPTH / 2, BASE_HEIGHT / 2))
)

# Combine into one solid (R1)
bracket = face.union(base)

# 2. Subtract Holes
# R3: Central bore (drilled through face plate along Y axis)
# We use a cylinder to cut through the face plate thickness at y=0 to y=8
bracket = bracket.cut(
    cq.Workplane("XY")
    .workplane(offset=0) # Start from bottom
    .center(0, MOTOR_SHAFT_Z)
    .rect(CENTRAL_BORE_DIA, CENTRAL_BORE_DIA) # dummy for workplane context if needed
    .workplane(offset=FACE_PLATE_THICKNESS) 
    # Instead of hole(), we use a cylinder oriented along Y to ensure it cuts through the thickness correctly
    .cylinder(FACE_PLATE_THICKNESS, CENTRAL_BORE_DIA / 2)
    .rotate((0,0,0), (1,0,0), 90) # Rotate to align with Y axis
    .translate((0, FACE_PLATE_THICKNESS/2, MOTOR_SHAFT_Z)) # Adjusting for the cylinder orientation logic
)

# Re-implementing subtraction more robustly using cylinders along Y
# R3: Central bore
bracket = bracket.cut(
    cq.Workplane("YZ")
    .center(0, MOTOR_SHAFT_Z)
    .cylinder(FACE_PLATE_THICKNESS, CENTRAL_BORE_DIA / 2)
    .translate((0, FACE_PLATE_THICKNESS/2, 0)) # Center the cylinder on the face plate thickness
)

# R4: Four motor screw holes (drilled through face plate along Y axis)
motor_holes = [
    (15.5, 30 + 15.5),
    (-15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 - 15.5)
]

for x_off, z_pos in motor_holes:
    bracket = bracket.cut(
        cq.Workplane("YZ")
        .center(x_off, z_pos)
        .cylinder(FACE_PLATE_THICKNESS, MOTOR_HOLE_DIA / 2)
        .translate((0, FACE_PLATE_THICKNESS/2, 0))
    )

# R6: Base screw holes (vertical along Z axis at x=+/-25, y=25)
base_holes = [
    (25, 25),
    (-25, 25)
]

for x_off, y_off in base_holes:
    # Drill through the entire thickness of the base plate (z from 0 to 8)
    bracket = bracket.cut(
        cq.Workplane("XY")
        .workplane(offset=0)
        .center(x_off, y_off)
        .cylinder(BASE_HEIGHT + 2, 5.5 / 2) # +2 to ensure complete penetration
    )

# 3. Motor Clearance (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
clearance_box = (
    cq.Workplane("XY")
    .box(43, 48, 43) # width=43 (x: -21.5 to 21.5), depth=48 (y: -48 to 0), height=43 (z: 8.5 to 51.5)
    .translate((0, -24, 30)) # center x=0, y=-24, z=30
)
bracket = bracket.cut(clearance_box)

# 4. Mass Reduction (R7)
# To ensure mass < 60g (Volume < 48.38 cm^3), we remove material from the base plate.
mass_reduction_cut = (
    cq.Workplane("XY")
    .center(0, 29) # Center at y=29 to stay away from face plate and R6 holes
    .rect(50, 30) 
    .extrude(-BASE_HEIGHT) 
)
# We need to make sure the mass reduction cut is a solid we can subtract
bracket = bracket.cut(mass_reduction_cut)

result = bracket