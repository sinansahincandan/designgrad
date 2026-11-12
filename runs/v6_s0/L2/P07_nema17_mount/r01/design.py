import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4)
motor_holes = [
    (15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 + 15.5),
    (-15.5, 30 - 15.5)
]

# Base Hole Coordinates (R6)
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body (R1, R2)
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = cq.Workplane("XY").box(70, FACE_PLATE_THICKNESS, 55, centered=(True, False, True)).translate((0, 2, 27.5))

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
base_plate = cq.Workplane("XY").box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, True))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis (y=0 to y=4)
# Using cylinder cut as per feedback to ensure precision and avoid workplane issues
bracket = bracket.cut(
    cq.Workplane("XZ").center(0, 30).cylinder(11.25, 4)
)

# 3. Subtract Motor Screw Holes (R4)
# Four motor screw holes, diameter 3.4 mm, through the face plate along Y at (x, z) = (+-15.5, 30 +- 15.5)
for x, z in motor_holes:
    bracket = bracket.cut(
        cq.Workplane("XZ").center(x, z).cylinder(1.7, 4)
    )

# 4. Motor Clearance (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# Since our bracket is defined for y >= 0, we ensure the face plate doesn't protrude into y < 0.
# The current definition of face_plate (y=0 to 4) already satisfies this. 
# No additional cut is strictly required unless the geometry was overlapping y < 0.

# 5. Subtract Base Screw Holes (R6)
# Two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25), through base plate from z=0
for x, y in base_holes:
    bracket = bracket.cut(
        cq.Workplane("XY").center(x, y).cylinder(2.75, 6)
    )

result = bracket