import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
FACE_PLATE_HEIGHT = 55.0
FACE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0

# Motor Hole Coordinates (R4) - relative to the face plate plane
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
face_plate = cq.Workplane("XY").box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=(True, False, True))

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
base_plate = cq.Workplane("XY").box(FACE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=(True, False, True))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# The bore is along the Y axis through the face plate. 
# We select the face at y=4 (the ">Y" face) and drill towards y=0.
# Since we are on a workplane at y=4, the hole center in XZ must be (0, 30).
bracket = bracket.faces(">Y").workplane().center(0, 30).hole(22.5)

# 3. Subtract Motor Screw Holes (R4)
# Using the same face (>Y) to drill through the thickness of the plate along Y.
for x_pos, z_pos in motor_holes:
    bracket = bracket.faces(">Y").workplane().center(x_pos, z_pos).hole(3.4)

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5.
# We define a box that represents this volume and subtract it from the bracket.
pocket_x_dim = 43.0  # 21.5 * 2
pocket_y_dim = 48.0
pocket_z_dim = 51.5 - 8.5

clearance_box = (
    cq.Workplane("XY")
    .box(pocket_x_dim, pocket_y_dim, pocket_z_dim, centered=(True, False, True))
    .translate((0, -24.0, (51.5 + 8.5) / 2.0)) # y center: (-48+0)/2 = -24; z center: (51.5+8.5)/2
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# The holes are vertical along Z. We select the bottom face (<Z) at z=0.
for x_pos, y_pos in base_holes:
    bracket = bracket.faces("<Z").workplane().pushPoints([(x_pos, y_pos)]).hole(5.5)

result = bracket