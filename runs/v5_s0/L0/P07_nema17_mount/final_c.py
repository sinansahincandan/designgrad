import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4)
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

# 1. Create the main L-shape body
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = cq.Workplane("XY").box(70, FACE_PLATE_THICKNESS, 55, centered=(True, False, True))

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
base_plate = cq.Workplane("XY").box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, True))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis
bracket = bracket.faces(">Y").workplane().pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]).hole(22.5)

# 3. Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# Since our bracket is at y > 0, we cut a pocket into the face plate from the motor side (y=0)
clearance_pocket = (
    cq.Workplane("XY")
    .box(43.0, 48.0, 43.0, centered=(True, False, True)) # x: +/-21.5, y: -48 to 0, z: 8.5 to 51.5 (approx)
)
# Adjusting pocket Z to match requirement exactly
pocket_z_min = 8.5
pocket_z_max = 51.5
pocket_y_start = -48.0
pocket_y_end = 0.0

# We use a subtraction approach for the clearance volume
# The pocket is defined by its bounds relative to the coordinate system
bracket = bracket.cut(
    cq.Workplane("XY")
    .box(43.0, 48.0, (pocket_z_max - pocket_z_min), centered=(True, False, True))
    .translate((0, (pocket_y_start + pocket_y_end)/2, (pocket_z_max + pocket_z_min)/2))
)
# Re-aligning the pocket subtraction to be precise with R5
# The requirement says "nothing in [bounds]". We ensure the bracket doesn't exist there.
# Since our bracket is mostly y > 0, we only care about the part of the volume that intersects y > 0.
bracket = bracket.cut(
    cq.Workplane("XY")
    .rect(43.0, 50.0) # x range -21.5 to 21.5, y up to 50 (covers the face plate)
    .extrude(-48.0)   # extend in -y direction
    .translate((0, 0, 30)) # move to center of Z-range roughly
).cut(
    # This is a cleaner way: define the box and subtract it
    cq.Workplane("XY")
    .box(43.0, 50.0, (pocket_z_max - pocket_z_min), centered=(True, False, True))
    .translate((0, -24, (pocket_z_max + pocket_z_min)/2))
)

# Refined approach for R5: Subtract the specific volume box
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5), centered=(True, False, True))
    .translate((0, -24, (51.5 + 8.5)/2)) # y center is (-48+0)/2 = -24
)
# Actually, the requirement says "nothing in ... y <= 0". Our bracket starts at y=0.
# So we only need to ensure no part of the bracket protrudes into that volume for y > 0.
# But the face plate is at y=0 to 4. We must cut a notch in the face plate.
bracket = bracket.cut(
    cq.Workplane("XY")
    .box(43.0, 50.0, (51.5 - 8.5), centered=(True, False, True))
    .translate((0, -25, (51.5 + 8.5)/2))
)

# 5. Subtract Base Screw Holes (R6)
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket