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
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = cq.Workplane("XY").box(70, FACE_PLATE_THICKNESS, 55, centered=(True, False, True))

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
base_plate = cq.Workplane("XY").box(70, 50, BASE_PLATE_THICKNESS, centered=(True, False, True))

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis. 
# We use faces("<Y") to ensure we are drilling from the motor side towards +Y.
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
# Since our bracket is at y >= 0, we must cut the portion of this volume that intersects the face plate (y=0 to 4).
# The pocket box: x range 43mm wide (+/-21.5), y range 4mm thick (centered at 2), z range 43mm high (8.5 to 51.5)
bracket = bracket.cut(
    cq.Workplane("XY")
    .box(43.0, 4.0, 43.0)
    .translate((0, 2, 30)) # Center Y at 2 (covers y=0 to 4), center Z at 30 (covers z=8.5 to 51.5)
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

# 6. Mass Verification (R7)
volume = result.val().Volume()
mass = volume * DENSITY_PLA
print(f"Volume: {volume:.2f} mm^3")
print(f"Mass: {mass:.2f} g")