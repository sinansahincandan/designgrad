import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0
DENSITY_PLA = 1.24e-6  # g/mm^3 (equivalent to 1.24 g/cm^3)

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
# Face plate: x from -30 to 30, y from 0 to 4, z from 0 to 55
face_plate = cq.Workplane("XY").box(60, FACE_PLATE_THICKNESS, 55, centered=(True, False, True))

# Base plate: x from -30 to 30, y from 0 to 30, z from 0 to 5
base_plate = cq.Workplane("XY").box(60, 30, BASE_PLATE_THICKNESS, centered=(True, False, True))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis. 
# The face plate is at y in [0, 4]. The "minimum Y" face is at y=0.
bracket = bracket.faces("<Y").workplane().pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]).hole(22.5)

# 3. Subtract Motor Screw Holes (R4)
for x, z in motor_holes:
    bracket = (
        bracket.faces("<Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5.
# The pocket box dimensions: width=43, depth=48, height=43.
# To center it at y = -24 (so it spans -48 to 0), we translate the box.
pocket_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, 43.0)
    .translate((0, -24, 30)) # Center Y at -24, center Z at 30
)
bracket = bracket.cut(pocket_box)

# 5. Subtract Base Screw Holes (R6)
for x, y in base_holes:
    bracket = (
        bracket.faces("<Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket

# 6. Mass Verification (R7)
volume = result.val().Volume()
mass = volume * DENSITY_PLA
print(f"Volume: {volume:.2f} mm^3")
print(f"Mass: {mass:.2f} g")