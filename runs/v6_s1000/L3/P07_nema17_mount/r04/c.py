import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
BASE_HEIGHT = 5.0  # Reduced to help meet mass requirement R7
MOTOR_SHAFT_Z = 30.0
CENTRAL_BORE_DIA = 22.5
MOTOR_HOLE_DIA = 3.4

# Base plate dimensions
BASE_X_WIDTH = 70.0
BASE_Y_DEPTH = 46.0  # Spans y from 4 to 50
BASE_Y_START = 4.0

# Envelope constraints (R7)
MAX_Z = 55.0

# 1. Create the main L-shape body
# Face Plate: x [-35, 35], y [0, 4], z [0, 55]
face = (
    cq.Workplane("XY")
    .box(BASE_X_WIDTH, FACE_PLATE_THICKNESS, MAX_Z, centered=(True, True, False))
    .translate((0, FACE_PLATE_THICKNESS / 2, 0))
)

# Base Plate: x [-35, 35], y [4, 50], z [0, BASE_HEIGHT]
base = (
    cq.Workplane("XY")
    .box(BASE_X_WIDTH, BASE_Y_DEPTH, BASE_HEIGHT, centered=(True, True, False))
    .translate((0, BASE_Y_START + BASE_Y_DEPTH / 2, 0))
)

# Combine into one solid (R1)
bracket = face.union(base)

# R3 & R4: Holes in the face plate (along Y axis)
motor_holes_coords = [
    (0, MOTOR_SHAFT_Z),           # R3: Central bore
    (15.5, 30 + 15.5),            # R4: Motor screw 1
    (-15.5, 30 + 15.5),           # R4: Motor screw 2
    (15.5, 30 - 15.5),            # R4: Motor screw 3
    (-15.5, 30 - 15.5)            # R4: Motor screw 4
]

for x_pos, z_pos in motor_holes_coords:
    dia = CENTRAL_BORE_DIA if (x_pos == 0 and z_pos == MOTOR_SHAFT_Z) else MOTOR_HOLE_DIA
    # Create a cylinder along Y axis. In XZ plane, the normal is Y.
    # A cylinder(height, radius) on XZ plane extends along the Y direction.
    hole_cyl = (
        cq.Workplane("XZ")
        .center(x_pos, z_pos)
        .cylinder(FACE_PLATE_THICKNESS, dia/2)
    )
    # We must translate the cylinder to be centered in Y (at y=2)
    hole_cyl = hole_cyl.translate((0, 2.0, 0))
    bracket = bracket.cut(hole_cyl)

# R6: Base screw holes (vertical along Z axis at x=+/-25, y=25)
base_holes_coords = [(25, 25), (-25, 25)]
for x_off, y_off in base_holes_coords:
    hole_cyl = (
        cq.Workplane("XY")
        .center(x_off, y_off)
        .cylinder(BASE_HEIGHT + 2, 5.5/2, centered=(True, True, False))
    )
    # Translate to ensure it starts from z=0 and goes through base
    hole_cyl = hole_cyl.translate((0, 0, BASE_HEIGHT / 2))
    bracket = bracket.cut(hole_cyl)

# R5: Motor Clearance (nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5)
clearance_box = (
    cq.Workplane("XY")
    .box(43, 48, 43, centered=(True, True, False)) 
    .translate((0, -24, 30)) 
)
bracket = bracket.cut(clearance_box)

# R7: Mass Reduction (Aggressive pocketing in the base plate)
mass_reduction_cut = (
    cq.Workplane("XY")
    .rect(30, 35) # x: [-15, 15]
    .translate((0, 28, 0)) # y: [10.5, 45.5]
    .extrude(BASE_HEIGHT + 2)
)

bracket = bracket.cut(mass_reduction_cut)

result = bracket