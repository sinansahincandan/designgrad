import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4) + Central Bore (R3)
# We combine all Y-axis holes into one list for a single subtraction operation
motor_holes_points = [(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]  # Central bore
for x in [-15.5, 15.5]:
    for z in [30 + 15.5, 30 - 15.5]:
        motor_holes_points.append((x, z))

# Base Hole Coordinates (R6)
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55 (R2)
# Using box with centered=(True, False, False) creates a block from y=0 to y=thickness.
# We translate by (0, 2, 0) so the face plate occupies y in [0, 4] if thickness is 4.
# Wait, if centered=(True, False, False), the Y-center is at 0. To get y from 0 to 4:
face_plate = cq.Workplane("XY").box(70, FACE_PLATE_THICKNESS, 55, centered=(True, False, False)).translate((0, FACE_PLATE_THICKNESS/2, 0))

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5 (R6)
# Set third parameter of centered to False so it sits on z=0.
base_plate = cq.Workplane("XY").box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, False))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2 & 3. Subtract Central Bore and Motor Screw Holes in one operation (R3, R4)
# We select the face at y=4 (the outer face of the plate) or y=0.
# Since we want to drill through the plate along Y, we use the face at y=4.
# The hole diameters are different, so we must handle them carefully. 
# However, CadQuery's .hole() uses one diameter. To support different diameters:
# We will create a single workplane and subtract the central bore then the small holes.

# First, the large central bore (R3)
bracket = bracket.faces(">Y").workplane().pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]).hole(22.5)

# Then, the four motor screw holes (R4)
for x, z in [(15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)]:
    bracket = bracket.faces(">Y").workplane().pushPoints([(x, z)]).hole(3.4)

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# The pocket is adjacent to the face plate on the -Y side.
pocket_z_min = 8.5
pocket_z_max = 51.5
pocket_y_start = -48.0
pocket_y_end = 0.0

clearance_box = (
    cq.Workplane("XY")
    .box(43.0, abs(pocket_y_start), (pocket_z_max - pocket_z_min), centered=(True, False, True))
    .translate((0, pocket_y_start/2, (pocket_z_max + pocket_z_min)/2))
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# These are vertical holes through the base plate at z=0.
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket