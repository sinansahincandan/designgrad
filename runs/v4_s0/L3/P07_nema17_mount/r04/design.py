import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 6.0  # Reduced for mass compliance (R7)
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4) - x, z (using absolute values as per feedback)
motor_holes = [
    (15.5, 45.5),
    (15.5, 14.5),
    (-15.5, 45.5),
    (-15.5, 14.5)
]

# Base Hole Coordinates (R6) - x, y
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body (R1)
# Face plate: y in [0, 4]. Dimensions: x from -35 to 35 (width 70), z from 0 to 55 (height 55).
face_plate = (
    cq.Workplane("XZ")
    .box(70, 55, FACE_PLATE_THICKNESS)
    .translate((0, 2, 27.5)) # Centers thickness so y is [0, 4]
)

# Base plate: z from 0 to 6. x in [-30, 30], y in [0, 50].
base_plate = (
    cq.Workplane("XY")
    .box(60, 50, BASE_PLATE_THICKNESS)
    .translate((0, 25, BASE_PLATE_THICKNESS/2)) # y center at 25, z from 0 to thickness
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis.
bracket = bracket.faces(">Y").workplane().pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]).hole(22.5)

# 3. Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# We use a subtraction on the XZ plane to ensure precise rectangular bounds.
clearance_box = (
    cq.Workplane("XZ")
    .rect(43.0, 43.0) # width 43 (from -21.5 to 21.5), height 43 (from 8.5 to 51.5)
    .translate((0, 30)) # center of rect at x=0, z=(8.5+51.5)/2 = 30
    .extrude(-48) # Extrude in -Y direction to cover y < 0
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
for x, y in base_holes:
    hole_cyl = (
        cq.Workplane("XY")
        .pushPoints([(x, y)])
        .cylinder(BASE_PLATE_THICKNESS, 5.5/2)
        .translate((0, 0, BASE_PLATE_THICKNESS/2)) # Align with base plate volume
    )
    bracket = bracket.cut(hole_cyl)

# 6. Implement Weight Reduction Pockets (R7)
# Pocket in the center of the Base Plate: x in [-20, 20], y in [10, 40]
base_pocket = (
    cq.Workplane("XY")
    .rect(40, 30) # width 40, height 30
    .translate((0, 25)) # center at y=25
    .extrude(BASE_PLATE_THICKNESS)
    .translate((0, 0, -BASE_PLATE_THICKNESS/2)) # Center it in the base thickness
)
# We cut a pocket that goes through the base plate but doesn't hit the face plate junction (y=0)
bracket = bracket.cut(base_pocket)

result = bracket