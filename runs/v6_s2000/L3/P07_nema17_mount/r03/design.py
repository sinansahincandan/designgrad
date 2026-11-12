import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 55.0

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0  # Y direction extension (from y=0 to y=50)
BASE_PLATE_THICKNESS = 10.0 # Z height (from z=0 to z=10)

# R4: Motor screw hole coordinates (x, z) relative to center of face plate
motor_screw_holes = [
    (15.5, 30 + 15.5), (-15.5, 30 + 15.5),
    (15.5, 30 - 15.5), (-15.5, 30 - 15.5)
]

# R6: Table screw hole coordinates (x, y)
table_screw_holes = [
    (25.0, 25.0), (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
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

# 2. Subtract R3: Central bore (diameter 22.5 through face plate along Y)
# We select the face at y=4 by looking for a face with normal in +Y direction
bracket = bracket.faces("<Y").workplane().center(0, 30).hole(22.5)

# 3. Subtract R4: Motor screw holes (diameter 3.4 through face plate along Y)
for sx, sz in motor_screw_holes:
    bracket = bracket.faces("<Y").workplane().center(sx, sz).hole(3.4)

# 4. Subtract R5: Motor clearance
# Clearance zone: x: +/- 21.5 (width 43), y: -48 to 0, z: 8.5 to 51.5
# The spec says the volume is in y < 0. Since our part starts at y=0, we subtract a box that overlaps.
clearance_cutout = (
    cq.Workplane("XY")
    .box(43, 48, 43, centered=False)
    .translate((-21.5, -48, 8.5)) 
)
bracket = bracket.cut(clearance_cutout)

# 5. Subtract R6: Table screw holes (diameter 5.5 through base plate along Z)
# The top of the base plate is at z=10. We select face with normal in +Z direction.
for tx, ty in table_screw_holes:
    bracket = bracket.faces("<Z").workplane().center(tx, ty).hole(5.5)

result = bracket