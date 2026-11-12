import cadquery as cq

# Constants
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_HEIGHT = 55.0

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 46.0  # From y=4 to y=50 (50-4=46)
BASE_PLATE_THICKNESS = 4.0

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

# Base plate: x from -35 to 35, y from 4 to 50, z from 0 to 4
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-35, 4, 0))
)

# Combine into one solid using union (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract R3: Central bore (diameter 22.5 through face plate along Y)
# Face plate is at y=0..4. We drill through the thickness.
bracket = bracket.faces(">Y").workplane().center(0, 30).hole(22.5)

# 3. Subtract R4: Motor screw holes (diameter 3.4 through face plate along Y)
for sx, sz in motor_screw_holes:
    bracket = bracket.faces(">Y").workplane().center(sx, sz).hole(3.4)

# 4. Subtract R5: Motor clearance
# Clearance zone: x: [-21.5, 21.5], y: [-48, 0], z: [8.5, 51.5]
# Since the bracket is on the +Y side (y >= 0), we subtract a volume that overlaps 
# with the face plate at the interface to ensure no protrusion into the motor space.
clearance_cutout = (
    cq.Workplane("XY")
    .box(43, 48, 43, centered=False)
    .translate((-21.5, -48, 8.5))
)
bracket = bracket.cut(clearance_cutout)

# 5. Subtract R6: Table screw holes (diameter 5.5 through base plate along Z)
for tx, ty in table_screw_holes:
    # Base plate is at z=0..4. Drill from top face (>Z).
    bracket = bracket.faces(">Z").workplane().center(tx, ty).hole(5.5)

# 6. R7: Mass Optimization (Pocketing the base plate)
# To keep mass < 60g, we remove material from the center of the base plate.
# Base plate is x:[-35,35], y:[4,50], z:[0,4].
# We create a pocket in the middle of the base (avoiding screw holes and face plate junction).
# Pocket: x: [-20, 20], y: [10, 45], z: [0, 4] (effectively reducing thickness)
# To maintain structural integrity, we'll make it a cutout from the top.
pocket = (
    cq.Workplane("XY")
    .box(40, 35, 2, centered=False)
    .translate((-20, 10, 2)) # Leaves 2mm thickness at bottom
)
bracket = bracket.cut(pocket)

result = bracket