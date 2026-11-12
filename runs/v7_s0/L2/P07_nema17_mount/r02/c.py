import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4)
motor_points = [
    (15.5, 45.5),
    (15.5, 14.5),
    (-15.5, 45.5),
    (-15.5, 14.5)
]

# Base Hole Coordinates (R6)
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: y from 0 to 4, centered vertically around z=30
face_plate_height = 50.0 # z range: 30 - 25 to 30 + 25 -> 5 to 55
face_plate = (
    cq.Workplane("XY")
    .box(70, FACE_PLATE_THICKNESS, face_plate_height)
    .translate((0, FACE_PLATE_THICKNESS/2, MOTOR_SHAFT_Z))
)

# Base plate: bottom at z=0, y from 0 to 50 (centered at y=25), x from -35 to 35
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS)
    .translate((0, 25, BASE_PLATE_THICKNESS/2))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Using XZ plane to create cylinder along Y axis
central_bore = (
    cq.Workplane("XZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .cylinder(FACE_PLATE_THICKNESS + 2, 22.5) # Extend slightly to ensure clean cut
    .translate((0, FACE_PLATE_THICKNESS/2, 0))
)

bracket = bracket.cut(central_bore)

# 3. Subtract Motor Screw Holes (R4)
motor_holes_combined = cq.Workplane("XZ")
for x, z in motor_points:
    motor_holes_combined = (
        motor_holes_combined
        .pushPoints([(x, z)])
        .cylinder(FACE_PLATE_THICKNESS + 2, 3.4)
    )

# Translate the combined holes to align with face plate Y position
motor_holes_combined = motor_holes_combined.translate((0, FACE_PLATE_THICKNESS/2, 0))
bracket = bracket.cut(motor_holes_combined)

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5)) 
    .translate((0, -24, (51.5 + 8.5)/2)) 
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
for x, y in base_holes:
    bracket = (
        bracket.faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket