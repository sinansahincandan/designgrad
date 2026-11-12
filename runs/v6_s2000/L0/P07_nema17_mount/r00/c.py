import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 55.0

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0  # Y direction extension
BASE_PLATE_THICKNESS = 10.0

# R4: Motor screw hole coordinates (x, z) relative to center of face plate
motor_screw_holes = [
    (15.5, 45.5), (-15.5, 45.5),
    (15.5, 14.5), (-15.5, 14.5)
]

# R6: Table screw hole coordinates (x, y)
table_screw_holes = [
    (25.0, 25.0), (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = cq.Workplane("XY").box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=(True, False, True))

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 10
# To ensure it is a single solid and overlaps the face plate (y=0..4),
# we position its center at Y = 25. Since depth is 50, range is [0, 50].
# We translate it so that it starts from y=0 to overlap with the face plate.
base_plate = cq.Workplane("XY").box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=(True, False, True)).translate((0, 25, 5))

# Combine into one solid using union
bracket = face_plate.union(base_plate)

# 2. Subtract R3: Central bore (diameter 22.5 through face plate along Y)
# The face plate is at y=0 to 4. We drill through the thickness.
# Selecting faces with normal in +Y direction to drill through the plate.
bracket = bracket.faces(">Y").workplane().center(0, 30).hole(22.5)

# 3. Subtract R4: Motor screw holes (diameter 3.4 through face plate along Y)
for sx, sz in motor_screw_holes:
    bracket = bracket.faces(">Y").workplane().center(sx, sz).hole(3.4)

# 4. Subtract R5: Motor clearance
# Clearance zone: x: +/- 21.5 (width 43), y: 0 to 4, z: 8.5 to 51.5
# We create a box that intersects the face plate and subtract it.
clearance_cutout = cq.Workplane("XY").box(43, 4, 43, centered=(True, False, True)).translate((0, 2, 30))
bracket = bracket.cut(clearance_cutout)

# 5. Subtract R6: Table screw holes (diameter 5.5 through base plate along Z)
for tx, ty in table_screw_holes:
    # The base plate is from z=0 to z=10. We drill through the top face (>Z).
    bracket = bracket.faces(">Z").workplane().center(tx, ty).hole(5.5)

result = bracket