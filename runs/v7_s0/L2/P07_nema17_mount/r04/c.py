import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Updated Motor Hole Coordinates (R4) per Feedback/Design Doc
motor_holes = [
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
# Face plate: y from 0 to 4, centered vertically around z=30 (z range: 30 +/- 25 -> 5 to 55)
face_plate_height = 50.0 
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

# 2. Subtract Central Bore (R3) via explicit cylinder cut
# Diameter 22.5 through the face plate along Y axis (y=0 to y=4)
cylinder_r3 = (
    cq.Workplane("XY")
    .cylinder(22.5, 10.0) # height 10 to ensure clearance of 4mm plate
    .rotate((0,0,0), (0,1,0), 90) # rotate to align with Y axis
    .translate((MOTOR_SHAFT_X, 2.0, MOTOR_SHAFT_Z)) # center at y=2
)
bracket = bracket.cut(cylinder_r3)

# 3. Subtract Motor Screw Holes (R4) via explicit cylinder cuts
for x, z in motor_holes:
    cylinder_r4 = (
        cq.Workplane("XY")
        .cylinder(3.4, 10.0) # height 10 to ensure clearance of 4mm plate
        .rotate((0,0,0), (0,1,0), 90) # rotate to align with Y axis
        .translate((x, 2.0, z)) # center at y=2
    )
    bracket = bracket.cut(cylinder_r4)

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5)) # width=43 (x), depth=48 (y), height=43 (z)
    .translate((0, -24, (51.5 + 8.5)/2)) # center y at -24, center z at 30
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6) via explicit cylinder cuts
for x, y in base_holes:
    cylinder_r6 = (
        cq.Workplane("XY")
        .cylinder(5.5, 10.0) # height 10 to ensure clearance of 5mm base
        .translate((x, y, 2.5)) # center at z=2.5
    )
    bracket = bracket.cut(cylinder_r6)

result = bracket