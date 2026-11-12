import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0

# Motor Hole Coordinates (R4) - x, z
motor_holes = [
    (15.5, 30 + 15.5),
    (15.5, 30 - 15.5),
    (-15.5, 30 + 15.5),
    (-15.5, 30 - 15.5)
]

# Base Hole Coordinates (R6) - x, y
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body (R1)
# Face plate: parallel to YZ plane, thickness along X axis. 
# To get y in [0, 4], we center a box of width 4 at x=2 and translate it.
# However, the spec says face plate is y in [0, 4]. Let's align with feedback:
# Face plate occupies y in [0, 4]. We use YZ plane for construction.
face_plate = (
    cq.Workplane("YZ")
    .box(FACE_PLATE_THICKNESS, 70, 55, centered=(True, True, True))
    .translate((2, 0, 27.5)) # This places x in [0, 4]. Wait, feedback says y in [0, 4].
)
# Re-interpreting feedback: "Face plate must be parallel to the YZ plane (y in [0, 4])"
# If it is parallel to YZ, its thickness is along X. 
# If the requirement is y in [0, 4], then the face plate is in the XZ plane.
# Let's follow the feedback instruction exactly: "Face plate... parallel to YZ plane (y in [0, 4])"
# This implies thickness is along X. But if it says "y in [0, 4]", that's a contradiction in terms of axes.
# Looking at R5: motor body lies in y < 0. Bracket is on +Y side. 
# Therefore, the face plate must be in the XZ plane (thickness along Y).

# Corrected approach based on Spec and Feedback:
# Face plate thickness is along Y axis (y=0 to 4).
face_plate = (
    cq.Workplane("XZ")
    .box(70, 55, FACE_PLATE_THICKNESS, centered=(True, True, True))
    .translate((0, 2, 27.5)) # y is [0, 4], z is [0, 55]
)

# Base plate: z in [0, 5], y in [0, 50].
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS)
    .translate((0, 25, BASE_PLATE_THICKNESS/2)) # bottom at z=0, y center at 25
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3)
# Diameter 22.5 through the face plate along Y axis.
# Face plate is in XZ plane, so we drill along Y (normal to XZ).
bracket = bracket.faces(">Y").workplane().pushPoints([(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)]).hole(22.5)

# 3. Subtract Motor Screw Holes (R4)
# Through the face plate along Y axis at (+-15.5, 30 +- 15.5)
for x, z in motor_holes:
    bracket = (
        bracket.faces(">Y")
        .workplane()
        .pushPoints([(x, z)])
        .hole(3.4)
    )

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5))
    .translate((0, -24, (51.5 + 8.5)/2))
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
# Two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25).
for x, y in base_holes:
    bracket = (
        bracket.faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .hole(5.5)
    )

result = bracket