import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 55.0

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0  # Y direction extension (from y=0 to y=50)
BASE_PLATE_THICKNESS = 10.0 # Z thickness (from z=0 to z=10)

# R4: Motor screw hole coordinates (x, z)
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
# We use centered=False and translate so that it occupies exactly [0, 4] in Y
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=False)
    .translate((-35, 0, 0))
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 10
# To ensure it is a single solid and overlaps the face plate (y=0..4),
# we position its center at Y = 25. Since depth is 50, range is [0, 50].
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-35, 0, 0))
)

# Combine into one solid using union
bracket = face_plate.union(base_plate)

# 2. Subtract R3: Central bore (diameter 22.5 through face plate along Y)
# We create a workplane at the mid-plane of the face plate (y=2) to drill along Y.
# The hole is centered at x=0, z=30.
bracket = bracket.workplane(offset=2).center(0, 30).hole(22.5)

# 3. Subtract R4: Motor screw holes (diameter 3.4 through face plate along Y)
# Using the same mid-plane workplane to ensure alignment with global XZ coordinates.
for sx, sz in motor_screw_holes:
    bracket = bracket.workplane(offset=2).center(sx, sz).hole(3.4)

# 4. Subtract R5: Motor clearance
# Clearance zone: x: +/- 21.5 (width 43), y: -48 to 0, z: 8.5 to 51.5
# Note: The spec says y is -48 to 0. Since the bracket starts at y=0, 
# this cutout effectively removes material from the face plate edge if it overlaps.
# However, R5 specifies a volume in the -Y region. We create a box that intersects 
# the face plate (y=0..4) to ensure no part of the motor body hits the bracket.
clearance_cutout = (
    cq.Workplane("XY")
    .box(43, 48, 43, centered=False) # Width 43 (x:-21.5 to 21.5), Depth 48 (y:-48 to 0), Height 43 (z:8.5 to 51.5)
    .translate((-21.5, -48, 8.5))
)
# To ensure the face plate is cleared where it meets the motor, we extend the cutout slightly into y > 0
clearance_cutout_extended = (
    cq.Workplane("XY")
    .box(43, 52, 43, centered=False) # Extend Y to cover the face plate thickness
    .translate((-21.5, -48, 8.5))
)
bracket = bracket.cut(clearance_cutout_extended)

# 5. Subtract R6: Table screw holes (diameter 5.5 through base plate along Z)
# The base plate top surface is at z=10.
for tx, ty in table_screw_holes:
    bracket = bracket.faces(">Z").workplane().center(tx, ty).hole(5.5)

result = bracket