import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 10.0  # Increased thickness for stability/R6 compliance
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4) - x, z
motor_holes = [
    (15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 + 15.5),
    (-15.5, 30 - 15.5)
]

# Base Hole Coordinates (R6) - x, y
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body (R1)
# Face plate: parallel to XZ plane, thickness along Y axis (y in [0, 4]).
# Dimensions: x from -35 to 35 (width 70), z from 0 to 55 (height 55).
face_plate = (
    cq.Workplane("XZ")
    .box(70, 55, FACE_PLATE_THICKNESS)
    .translate((0, 2, 27.5)) # Center in XZ, move Y to [0, 4]
)

# Base plate: z in [0, BASE_PLATE_THICKNESS], y in [0, 50].
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS)
    .translate((0, 25, BASE_PLATE_THICKNESS/2)) # y center at 25, z from 0 to thickness
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis.
# We select the face at y=4 (>Y) and drill through.
bracket = bracket.faces(">Y").workplane().pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]).hole(22.5)

# 3. Subtract Motor Screw Holes (R4)
# Through the face plate along Y axis at (+-15.5, 30 +- 15.5)
for x, z in motor_holes:
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5))
    .translate((0, -24, (51.5 + 8.5)/2)) # Center in X and Z, Y offset to cover [-48, 0]
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# Using a robust subtraction method: create cylinders and cut them from the final solid.
for x, y in base_holes:
    hole_cyl = (
        cq.Workplane("XY")
        .pushPoints([(x, y)])
        .cylinder(BASE_PLATE_THICKNESS, 5.5/2)
        .translate((0, 0, BASE_PLATE_THICKNESS/2)) # Align cylinder with base plate volume
    )
    bracket = bracket.cut(hole_cyl)

result = bracket