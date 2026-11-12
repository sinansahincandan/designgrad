import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
FACE_PLATE_WIDTH = 70.0
FACE_PLATE_HEIGHT = 55.0
BASE_PLATE_WIDTH = 70.0
BASE_PLATE_DEPTH = 50.0

# Motor Hole Coordinates (R4) + Central Bore (R3)
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0
CENTRAL_BORE_DIA = 22.5
MOTOR_SCREW_HOLE_DIA = 3.4

# Base Hole Coordinates (R6)
BASE_HOLES_XY = [(25.0, 25.0), (-25.0, 25.0)]
BASE_HOLE_DIA = 5.5

# 1. Create the main L-shape body (R1)
# Face plate: x from -35 to 35, y from 0 to 4, z from 0 to 55
face_plate = (
    cq.Workplane("XY")
    .box(FACE_PLATE_WIDTH, FACE_PLATE_THICKNESS, FACE_PLATE_HEIGHT, centered=(True, False, False))
    .translate((0, FACE_PLATE_THICKNESS / 2, 0))
)

# Base plate: x from -35 to 35, y from 0 to 50, z from 0 to 5
base_plate = (
    cq.Workplane("XY")
    .box(BASE_PLATE_WIDTH, BASE_PLATE_DEPTH, BASE_PLATE_THICKNESS, centered=(True, False, False))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore and Motor Screw Holes using cylinders to avoid face selection issues (R3, R4)
# We use a length of 10mm to ensure it fully clears the 4mm plate
bore_cylinder = (
    cq.Workplane("YZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .box(10, CENTRAL_BORE_DIA, 10, centered=(False, True, False)) # Using box/cylinder logic via cylinder
)
# More robust: create cylinders along Y axis
bore = cq.Workplane("XZ").workplane(offset=2).center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z).cylinder(10, CENTRAL_BORE_DIA/2)
bracket = bracket.cut(bore)

# Motor screw holes (R4)
motor_hole_coords = [
    (15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)
]
for x, z in motor_hole_coords:
    m_hole = cq.Workplane("XZ").workplane(offset=2).center(x, z).cylinder(10, MOTOR_SCREW_HOLE_DIA/2)
    bracket = bracket.cut(m_hole)

# 3. Create Motor Clearance Pocket (R5)
# Requirement: -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
# The pocket is adjacent to the face plate on the -Y side.
pocket_x_dim = 43.0  # 21.5 * 2
pocket_y_dim = 48.0
pocket_z_dim = (51.5 - 8.5)

clearance_box = (
    cq.Workplane("XY")
    .box(pocket_x_dim, pocket_y_dim, pocket_z_dim, centered=(True, False, True))
    .translate((0, -pocket_y_dim/2, (51.5 + 8.5)/2))
)
bracket = bracket.cut(clearance_box)

# 4. Subtract Base Screw Holes (R6)
# Vertical holes through the base plate at z=0
for x, y in BASE_HOLES_XY:
    # Create a cylinder centered at (x,y) extending from z=-1 to z=BASE_PLATE_THICKNESS+1
    base_hole = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .center(x, y)
        .cylinder(BASE_PLATE_THICKNESS + 2, BASE_HOLE_DIA/2)
    )
    bracket = bracket.cut(base_hole)

result = bracket