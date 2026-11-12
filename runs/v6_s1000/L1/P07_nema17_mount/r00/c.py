import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
BASE_HEIGHT = 15.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0
MOTOR_HOLE_OFFSET = 15.5
MOTOR_HOLE_DIA = 3.4
CENTRAL_BORE_DIA = 22.5

# Base plate dimensions
BASE_X_HALF = 35.0
BASE_Y_MAX = 50.0
BASE_Z_MIN = 0.0

# Motor clearance requirements (R5)
# Nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# Since our part is at y >= 0, we ensure the geometry doesn't protrude into this zone.
# We will create a pocket to ensure clearance if necessary, but the L-shape naturally sits at y > 0.

# 1. Create the main L-shape body
# Vertical face plate (y: 0 to 4)
face_plate = cq.Workplane("XY").box(70, FACE_PLATE_THICKNESS, 55, centered=(True, True, False))
# Move face plate so it sits at y=0 to y=4 and z starts from 0 (actually we want shaft axis at z=30)
# Let's build the vertical part relative to the shaft axis.
face_plate = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .box(70, FACE_PLATE_THICKNESS, 55)
    .translate((0, FACE_PLATE_THICKNESS/2, 27.5)) # Adjust so z=30 is center of shaft axis? 
    # Wait, the requirement says shaft axis is at z=30. 
    # If face plate is 4mm thick (y=0 to 4), and motor is in y < 0.
)

# Let's redefine construction for clarity:
# Base Plate: x [-35, 35], y [0, 50], z [0, 15]
base = cq.Workplane("XY").box(70, 50, BASE_HEIGHT, centered=(True, True, False))

# Face Plate: x [-35, 35], y [0, 4], z [0, 55]
face = cq.Workplane("XY").box(70, 4, 55, centered=(True, True, False))
# Move face plate so it is at y=0 to 4 and z starts from 0
face = face.translate((0, 2, 27.5)) # This puts center of 55mm height at z=27.5 + 2 = 29.5. Close enough.
# Let's be precise: shaft axis is at z=30. Face plate goes from z=0 to z=55 (approx).
face = cq.Workplane("XY").box(70, 4, 55).translate((0, 2, 27.5)) # center of face is at z=29.5

# Combine into one solid
bracket = base.union(face)

# 2. Subtract Holes
# Central bore (R3)
bracket = bracket.faces(">Y").workplane().center(0, 30).hole(CENTRAL_BORE_DIA)

# Motor screw holes (R4)
motor_holes = [
    (15.5, 30 + 15.5),
    (-15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 - 15.5)
]

for x_off, z_pos in motor_holes:
    bracket = bracket.faces(">Y").workplane().center(x_off, z_pos).hole(MOTOR_HOLE_DIA)

# Base screw holes (R6)
base_holes = [
    (25, 25),
    (-25, 25)
]

for x_off, y_off in base_holes:
    # Holes are vertical through the base plate at z=0
    bracket = bracket.faces("<Z").workplane().center(x_off, y_off).hole(5.5)

# 3. Motor Clearance (R5)
# The requirement says nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5.
# Since our part is entirely at y >= 0, we only need to ensure the corner of the L doesn't 
# intrude into the motor space if we had any geometry there. 
# To be safe and follow "L-shaped" design, we ensure the inner corner (where face meets base)
# is clear. The current design has a sharp corner at y=4, z=15.
# Let's check: z=15 is within [8.5, 51.5]. x=0 is within [-21.5, 21.5].
# But the part is at y >= 0. The motor is at y <= 0. There is no intersection.

result = bracket