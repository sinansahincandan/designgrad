import cadquery as cq

# Constants
FACE_PLATE_THICKNESS = 4.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 55.0

BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0  # Y direction extension (from y=0 to y=50)
BASE_PLATE_THICKNESS = 10.0 # z from 0 to 10

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
# Using XZ plane to drill through the thickness of the face plate (along Y)
bracket = bracket.cut(
    cq.Workplane("XZ")
    .center(0, 30)
    .circle(22.5 / 2)
    .extrude(4)
    .translate((0, 2, 0)) # Center of the 4mm plate is at y=2
)

# 3. Subtract R4: Motor screw holes (diameter 3.4 through face plate along Y)
for sx, sz in motor_screw_holes:
    bracket = bracket.cut(
        cq.Workplane("XZ")
        .center(sx, sz)
        .circle(3.4 / 2)
        .extrude(4)
        .translate((0, 2, 0)) # Center of the 4mm plate is at y=2
    )

# 4. Subtract R5: Motor clearance (redundant for y > 0, but following spec logic)
# Spec says nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# Since our part starts at y=0 and goes positive, we don't need to cut anything for R5 
# unless the motor body overlaps into the bracket material. 
# The spec says "nothing in ... -48 <= y <= 0". Our part is in y >= 0.

# 5. Subtract R6: Table screw holes (diameter 5.5 through base plate along Z)
for tx, ty in table_screw_holes:
    # Drill from z=0 to z=10 using XY plane
    bracket = bracket.cut(
        cq.Workplane("XY")
        .center(tx, ty)
        .circle(5.5 / 2)
        .extrude(10)
    )

# 6. Structural Strategy: Pocketing (to reduce mass as per Design Doc)
# Add shallow rectangular pockets in the base plate to optimize mass
pocket_width = 30.0
pocket_depth = 30.0
pocket_thickness = 4.0 # depth of pocket into the 10mm base

bracket = bracket.cut(
    cq.Workplane("XY")
    .center(0, 25)
    .rect(pocket_width, pocket_depth, centered=True)
    .extrude(pocket_thickness)
    .translate((-35, 0, 10)) # Move to base plate area (z=10 is top of base)
    # Note: We use a negative extrude or cut from the top. 
    # Let's re-orient for clarity:
)
# Redoing pocketing more cleanly:
pocket = (
    cq.Workplane("XY")
    .center(0, 25)
    .rect(30, 30)
    .extrude(4)
    .translate((-35, 0, 6)) # Cut from z=6 to z=10
)
bracket = bracket.cut(pocket)

result = bracket