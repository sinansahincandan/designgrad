import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 55.0

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0  # Y direction extension (from y=0 to y=50)
BASE_PLATE_THICKNESS = 10.0 # Z height (from z=0 to z=10)

# R4: Motor screw hole coordinates (x, z) relative to global origin
motor_screw_holes = [
    (15.5, 45.5), (-15.5, 45.5),
    (15.5, 14.5), (-15.5, 14.5)
]

# R6: Table screw hole coordinates (x, y) relative to global origin
table_screw_holes = [
    (25.0, 25.0), (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
# We use centered=False and translate so it occupies exactly [0, 4] in Y and [0, 55] in Z.
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=False)
    .translate((-35, 0, 0))
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 10
# We position it so it starts at y=0 and z=0.
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=False)
    .translate((-35, 0, 0))
)

# Combine into one solid using union
bracket = face_plate.union(base_plate)

# 2. Subtract R3: Central bore (diameter 22.5 through face plate along Y)
# The face plate is at y=0 to 4. We select the face at y=4 (>Y).
# The center of the face >Y is (x=0, z=27.5) because height is 55 and centered=False starts at z=0.
face_y_center_z = FACE_PLATE_HEIGHT / 2.0

bracket = bracket.faces(">Y").workplane().center(0, 30 - face_y_center_z).hole(22.5)

# 3. Subtract R4: Motor screw holes (diameter 3.4 through face plate along Y)
for sx, sz in motor_screw_holes:
    # We must offset the target Z by the face's local center Z to hit global Z
    bracket = bracket.faces(">Y").workplane().center(sx, sz - face_y_center_z).hole(3.4)

# 4. Subtract R5: Motor clearance
# Clearance zone: x: +/- 21.5 (width 43), y: -48 to 0 (motor side), z: 8.5 to 51.5
# Note: The spec says motor is in y < 0, but the bracket is at y >= 0. 
# To ensure clearance for a motor pressing against y=0, we subtract from the face plate area.
# However, R5 specifically defines a volume in y < 0. Since our part starts at y=0, 
# we check if any part of the bracket exists in that zone or if it's meant to be a notch.
# Given "nothing in ... -48 <= y <= 0", and our plate is y: 0-4, this implies the face 
# at y=0 must be clear. We will create a cutout that removes material from the front of the plate.
clearance_cutout = (
    cq.Workplane("XY")
    .box(43, 4, 43, centered=False) # Width 43, Depth 4, Height 43
    .translate((-21.5, -4, 8.5))   # x: -21.5 to 21.5, y: -4 to 0, z: 8.5 to 51.5
)
# To ensure the motor body (y < 0) doesn't hit the bracket, we make sure the face plate 
# at y=0 is clear of any protrusions. The current geometry is already y=0..4.
# If R5 implies a notch into the plate:
notch = cq.Workplane("XY").box(43, 4, 43, centered=False).translate((-21.5, -2, 8.5))
# But since motor is in y < 0 and bracket is y > 0, we ensure the interface at y=0 is flat.
# The current geometry already satisfies this as long as no part extends into y < 0.

# 5. Subtract R6: Table screw holes (diameter 5.5 through base plate along Z)
# Base plate is z=0 to 10. Face >Z is at z=10.
# The center of face >Z is (x=0, y=25).
face_z_center_y = BASE_PLATE_DEPTH / 2.0

for tx, ty in table_screw_holes:
    # Target global (tx, ty). Local offset from face center (0, 25) is (tx - 0, ty - 25)
    bracket = bracket.faces(">Z").workplane().center(tx, ty - face_z_center_y).hole(5.5)

result = bracket