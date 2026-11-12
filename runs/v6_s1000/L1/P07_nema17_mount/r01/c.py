import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
BASE_HEIGHT = 12.0
SHAFT_AXIS_Z = 30.0
CENTRAL_BORE_DIA = 22.5

# Motor screw holes (R4)
MOTOR_HOLE_DIA = 3.4
MOTOR_HOLES = [
    (15.5, SHAFT_AXIS_Z + 15.5),
    (-15.5, SHAFT_AXIS_Z + 15.5),
    (15.5, SHAFT_AXIS_Z - 15.5),
    (-15.5, SHAFT_AXIS_Z - 15.5)
]

# Base screw holes (R6)
BASE_HOLE_DIA = 5.5
BASE_HOLES = [
    (25, 25),
    (-25, 25)
]

# 1. Create the Base Plate (Optimized for R7 mass < 60g)
# x: [-30, 30], y: [0, 35], z: [0, 12]
base = cq.Workplane("XY").box(60, 35, BASE_HEIGHT, centered=(True, True, False))

# 2. Create the Face Plate (R2, R3, R4)
# To ensure it is a single solid and connects to the base, we must overlap them.
# The base spans z: [0, 12]. We will make the face plate span z: [0, 55].
# This ensures they share the volume from z=0 to z=12.
face_height = 55.0
face = (
    cq.Workplane("XY")
    .box(70, FACE_PLATE_THICKNESS, face_height, centered=(True, True, False))
    # Translate so the bottom of the face plate is at z=0 and its y-range is [0, 4]
    # The box command with centered=False places min corner at (0,0,0).
    # We want x: [-35, 35], y: [0, 4], z: [0, 55].
    .translate((-35, 0, 0))
)

# 3. Combine into one solid (R1)
bracket = base.union(face)

# 4. Subtract Holes from the combined solid
# Central bore (R3) - through the face plate at z=30
# The face plate is located at y=[0, 4]. We use faces(">Y") to find the outer surface.
bracket = bracket.faces(">Y").workplane().center(0, SHAFT_AXIS_Z).hole(CENTRAL_BORE_DIA)

# Motor screw holes (R4) - through the face plate
for x_off, z_pos in MOTOR_HOLES:
    bracket = bracket.faces(">Y").workplane().center(x_off, z_pos).hole(MOTOR_HOLE_DIA)

# Base screw holes (R6) - vertical through the base at z=0
for x_off, y_off in BASE_HOLES:
    bracket = bracket.faces("<Z").workplane().center(x_off, y_off).hole(BASE_HOLE_DIA)

# 5. Motor Clearance Pocket (R5)
# Requirement: x in [-21.5, 21.5], y < 0, z in [8.5, 51.5]
# We subtract a volume that covers the motor body area to ensure clearance.
# The pocket is defined for y < 0. Our part exists at y >= 0.
# To satisfy R5 and avoid interference, we cut a notch into the junction.
bracket = bracket.cut(
    cq.Workplane("XY")
    .box(43, 10, 43) # x: [-21.5, 21.5], y: [-5, 5], z: [8.5, 51.5] (approximate center)
    .translate((0, -5, 30)) 
)

result = bracket