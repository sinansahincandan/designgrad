import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 10.0  # y from 0 to 10
BASE_PLATE_THICKNESS = 5.0   # z from 0 to 5
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

# 1. Create the main L-shape body (R1)
# Face plate: x from -30 to 30, y from 0 to 10, z from 5 to 55
face_plate = (
    cq.Workplane("XY")
    .box(60, FACE_PLATE_THICKNESS, 50, centered=(True, False, False)) # x: -30 to 30, y: 0 to 10, z: 0 to 50
    .translate((0, 0, 5)) # Shift z up so it spans z=5 to 55
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, False)) # x: -35 to 35, y: 0 to 50, z: 0 to 5
)

# Combine into a single solid
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
# To ensure the pocket is cut into the face plate at the interface (y=0), 
# we define a box that overlaps the face plate from the negative Y side.
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, 43.0, centered=(True, False, True)) # x: -21.5 to 21.5, y: -24 to 24, z: 8.5 to 51.5
    # Note: Since the bracket is at y >= 0, this box cuts into the face plate from y=0 up to y=24.
    # However, R5 specifies the volume in y < 0. To satisfy the "recessed pocket" design doc,
    # we ensure the cut removes material from the face plate at the interface.
)
# We refine the clearance box to specifically target the motor body area intersecting the bracket
pocket_cut = (
    cq.Workplane("XY")
    .box(43.0, 18.5, 43.0, centered=(True, False, True)) # x: -21.5 to 21.5, y: -9.25 to 9.25, z: 8.5 to 51.5
    .translate((0, 0, 0)) 
)
# To strictly follow the Design Doc "recessed pocket cut from y=0 into face plate":
# We create a box that spans x[-21.5, 21.5], z[8.5, 51.5] and cuts from y=0 into the plate (y > 0)
pocket = (
    cq.Workplane("XY")
    .box(43.0, 10.0, 43.0, centered=(True, False, True)) # x: -21.5 to 21.5, y: -5 to 5, z: 8.5 to 51.5
    .translate((0, 5, 30)) # Center the Z at 30 and Y such that it cuts from y=0 into the plate
)
# Re-aligning pocket to match R5/Design Doc exactly:
# The motor is in y < 0. The bracket is in y > 0. A "recessed pocket" means removing material from the bracket at y=0.
pocket_volume = (
    cq.Workplane("XY")
    .box(43.0, 10.0, 43.0, centered=(True, False, True)) # x: -21.5 to 21.5, y: -5 to 5, z: 8.5 to 51.5
    .translate((0, 0, 30)) # Center Z at 30, Y center at 0 (so it covers y from -5 to 5)
)
bracket = bracket.cut(pocket_volume)

# 5. Subtract Base Screw Holes (R6)
# Drilled vertically through the base plate from top surface (>Z) down to z=0
for x, y in base_holes:
    bracket = (
        bracket.faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket