import cadquery as cq

# Constants based on specification
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 55.0

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0  # Y direction extension (from y=0 to y=50)
BASE_PLATE_THICKNESS = 10.0

# R4: Motor screw hole coordinates (x, z)
motor_screw_holes = [
    (15.5, 30 + 15.5), (-15.5, 30 + 15.5),
    (15.5, 30 - 15.5), (-15.5, 30 - 15.5)
]

# R6: Table screw hole coordinates (x, y)
table_screw_holes = [
    (25.0, 25.0), (-25.0, 25.0)
]

# 1. Create the main L-shape body using centered=True to simplify coordinate management
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
# We create a box and translate it so its bottom face is at y=0 and base is at z=0
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=(True, False, True))
    .translate((0, 0, 0)) # Bottom face at z=0, center at x=0, y-range [0, 4]
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 10
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=(True, False, True))
    .translate((0, 0, 0)) # Bottom face at z=0, center at x=0, y-range [0, 50]
)

# Combine into one solid using union
bracket = face_plate.union(base_plate)

# 2. Subtract R3: Central bore (diameter 22.5 through face plate along Y)
# Using absolute cylinders to avoid workplane origin confusion as per feedback
central_bore = cq.Workplane("XY").cylinder(FACE_PLATE_THICKNESS, 22.5).translate((0, 2, 30))
# Note: The cylinder is created on XY plane (Z-axis), we need it along Y.
# Let's use XZ plane for the bore to align with the Y axis direction.
central_bore = cq.Workplane("XZ").cylinder(FACE_PLATE_THICKNESS, 22.5).translate((0, 30, 2))
bracket = bracket.cut(central_bore)

# 3. Subtract R4: Motor screw holes (diameter 3.4 through face plate along Y)
for sx, sz in motor_screw_holes:
    hole = cq.Workplane("XZ").cylinder(FACE_PLATE_THICKNESS, 3.4).translate((sx, sz, 2))
    bracket = bracket.cut(hole)

# 4. Subtract R5: Motor clearance
# Clearance zone: x: +/- 21.5 (width 43), y: -48 to 0, z: 8.5 to 51.5
# The spec says "nothing in ... -48 <= y <= 0". Since our bracket is at y >= 0, 
# this clearance primarily affects the interface or ensures no material exists where the motor body sits.
# However, R5 specifically defines a volume. We subtract the intersection of that volume with our part.
clearance_cutout = (
    cq.Workplane("XY")
    .box(43, 48, 43, centered=(True, True, True)) # Width 43, Depth 48, Height 43
    .translate((0, -24, 30)) # Center of Y is at -24 to cover up to y=0
)
# To strictly follow R5: x in [-21.5, 21.5], y in [-48, 0], z in [8.5, 51.5]
# We create a box representing this volume and subtract it from the bracket.
clearance_box = (
    cq.Workplane("XY")
    .box(43, 48, 43, centered=(True, True, True)) # This is a placeholder for logic
)
# Let's build the clearance box precisely:
c_x, c_y, c_z = 21.5, 0, 43 # half-widths/extents
# The volume is x: [-21.5, 21.5], y: [-48, 0], z: [8.5, 51.5]
# We create a box and translate it to the correct position.
# Center of X = 0, Center of Y = -24, Center of Z = (8.5 + 51.5)/2 = 30
clearance_box = (
    cq.Workplane("XY")
    .box(43, 48, 43) # width=43, depth=48, height=43
    .translate((0, -24, 30))
)
# Note: The box is centered on its own origin. To get z from 8.5 to 51.5 (height 43), 
# the center must be at 30.
bracket = bracket.cut(clearance_box)

# 5. Subtract R6: Table screw holes (diameter 5.5 through base plate along Z)
for tx, ty in table_screw_holes:
    # Drill through the base plate (z=0 to z=10) at (tx, ty)
    hole = cq.Workplane("XY").cylinder(BASE_PLATE_THICKNESS + 2, 5.5).translate((tx, ty, 0))
    bracket = bracket.cut(hole)

result = bracket