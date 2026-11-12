import cadquery as cq

# Constants based on Design Document and Specification
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 54.0  # Reduced to 54.0 for R7 safety margin

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0
BASE_PLATE_THICKNESS = 10.0

# Hole coordinates
motor_screw_holes = [
    (15.5, 45.5), (-15.5, 45.5),
    (15.5, 14.5), (-15.5, 14.5)
]

table_screw_holes = [
    (25.0, 25.0), (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 54
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=False)
    .translate((-35, 0, 0))
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 10
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-35, 0, 0))
)

# Combine into one solid using union
bracket = face_plate.union(base_plate)

# 2. Subtract R3 & R4: Y-axis holes (Central bore and Motor screws)
# We create a workplane on the outer face of the face plate (y=4)
# The face plate is at y=[0, 4], so faces(">Y") selects the plane at y=4.
bracket = bracket.faces(">Y").workplane()

# Drill central bore (R3)
bracket = bracket.center(0, 30).hole(22.5)

# Drill motor screw holes (R4)
# Note: .hole() in CadQuery relative to the workplane center. 
# Since we are already on the Y-max face, we push points for the remaining holes.
for sx, sz in motor_screw_holes:
    bracket = bracket.center(sx, sz).hole(3.4)

# 3. Subtract R5: Motor clearance
# Clearance zone: -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# To ensure it cuts the face plate (y=0..4), we extend the Y range slightly into the positive side.
clearance_cutout = (
    cq.Workplane("XY")
    .box(43, 4, 43, centered=False) # Width 43 (from -21.5 to 21.5), Height 43 (8.5 to 51.5)
    .translate((-21.5, -4, 8.5))    # Y starts at -4 to ensure overlap with face plate [0, 4]
)
bracket = bracket.cut(clearance_cutout)

# 4. Subtract R6: Table screw holes (diameter 5.5 through base plate along Z)
# The base plate top surface is at z=10. We select the face with max Z.
bracket = bracket.faces(">Z").workplane()
for tx, ty in table_screw_holes:
    bracket = bracket.center(tx, ty).hole(5.5)

result = bracket