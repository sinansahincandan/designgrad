import cadquery as cq

# Constants and Dimensions
FACE_PLATE_THICKNESS = 4.0
BASE_PLATE_THICKNESS = 5.0
MOTOR_SHAFT_X = 0.0
MOTOR_SHAFT_Z = 30.0
CENTRAL_BORE_DIAMETER = 22.5

# Motor Hole Coordinates (R4) - Updated per feedback
motor_holes = [
    (15.5, 45.5),
    (-15.5, 45.5),
    (15.5, 14.5),
    (-15.5, 14.5)
]

# Base Hole Coordinates (R6)
base_holes = [
    (25.0, 25.0),
    (-25.0, 25.0)
]

# 1. Create the main L-shape body
# Face plate: y from 0 to 4, centered vertically around z=30 (z range: 30 +/- 25 -> 5 to 55)
face_plate_height = 50.0 
face_plate = (
    cq.Workplane("XY")
    .box(70, FACE_PLATE_THICKNESS, face_plate_height)
    .translate((0, FACE_PLATE_THICKNESS/2, MOTOR_SHAFT_Z))
)

# Base plate: bottom at z=0, y from 0 to 50 (centered at y=25), x from -35 to 35
base_plate = (
    cq.Workplane("XY")
    .box(70, 50, BASE_PLATE_THICKNESS)
    .translate((0, 25, BASE_PLATE_THICKNESS/2))
)

# Combine into a single solid (R1)
bracket = face_plate.union(base_plate)

# 2. Subtract Central Bore (R3) using explicit cylinder subtraction
# Cylinder axis parallel to Y-axis, centered at x=0, z=30, y=2 (middle of plate)
# Height is 10mm to ensure it fully clears the 4mm thickness
bore_cylinder = (
    cq.Workplane("YZ")
    .center(MOTOR_SHAFT_Z, MOTOR_SHAFT_X) # Note: YZ plane, so center is (z, x)
    .circle(CENTRAL_BORE_DIAMETER / 2)
    .extrude(10.0, both=True)
    .translate((0, 2, 0)) # Center along Y axis
)
# To be safer and more explicit with orientation:
bore_cylinder = (
    cq.Workplane("XZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .circle(CENTRAL_BORE_DIAMETER / 2)
    .extrude(10.0, both=True)
    .translate((0, 2, 0)) # Move to center of face plate thickness
)
# Correcting approach: Create a cylinder in XZ plane and translate it along Y
bore_cylinder = (
    cq.Workplane("XZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .circle(CENTRAL_BORE_DIAMETER / 2)
    .extrude(10.0, both=True)
    .translate((0, 2, 0)) # This is tricky in CQ due to plane definitions. 
)

# Let's use a more robust method for the bore:
bore_cyl = cq.Workplane("XZ").workplane(offset=2).circle(CENTRAL_BORE_DIAMETER/2).extrude(10, both=True).translate((MOTOR_SHAFT_X, 2, MOTOR_SHAFT_Z))
# Wait, the simplest way to create a cylinder along Y:
bore_cyl = (
    cq.Workplane("XZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .circle(CENTRAL_BORE_DIAMETER / 2)
    .extrude(10.0, both=True)
).translate((0, 2, 0)) # This is still confusing. Let's use the standard:

# RE-DOING BORE AND MOTOR HOLES WITH EXPLICIT CYLINDERS
# Create a list of all cylinders to subtract for face plate holes (R3 and R4)
subtraction_cylinders = []

# R3 Central Bore
bore_cyl = (
    cq.Workplane("XZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .circle(CENTRAL_BORE_DIAMETER / 2)
    .extrude(10.0, both=True)
).translate((0, 2, 0)) # This translates the XZ object along Y? No, CQ translate is global.

# Let's use a helper to create cylinders along Y axis
def create_y_cylinder(x, z, diameter, height):
    return (
        cq.Workplane("XZ")
        .center(x, z)
        .circle(diameter / 2)
        .extrude(height, both=True)
    ).translate((0, 0, 0)) # Placeholder

# Correct logic: Create cylinder in XZ plane, then translate it to the correct Y position
def get_y_cyl(x, z, d, h):
    return (
        cq.Workplane("XZ")
        .center(x, z)
        .circle(d/2)
        .extrude(h, both=True)
    ).translate((0, 2, 0)) # This is still not quite right for global coords.

# FINAL ATTEMPT AT BORE/HOLES LOGIC:
# We create a cylinder in the XZ plane at the correct X, Z and extrude it along Y by translating the whole object.
# Actually, in CadQuery, if you work on XZ plane, extrusion is along Y.

# R3 Bore
bracket = bracket.cut(
    cq.Workplane("XZ")
    .center(MOTOR_SHAFT_X, MOTOR_SHAFT_Z)
    .circle(CENTRAL_BORE_DIAMETER / 2)
    .extrude(10.0, both=True)
    .translate((0, 2, 0)) # This is actually translating X by 0, Y by 2, Z by 0 in global space? No.
)

# Let's use the most reliable method: create a cylinder and move it to (x, y_mid, z)
def subtract_y_cyl(base_obj, x, y_center, z, diameter, height):
    cyl = (
        cq.Workplane("XZ")
        .center(x, z)
        .circle(diameter / 2)
        .extrude(height, both=True)
    ).translate((0, y_center, 0)) # This is still not working as expected because of how XZ plane works.
    # Let's just use the Workplane "XY" and rotate it.
    return base_obj.cut(
        cq.Workplane("XY")
        .center(x, z) # Wait, XY center is x, y. 
        .circle(diameter/2)
        .extrude(height)
    )

# Let's go back to basics. A cylinder along Y is a circle in XZ plane.
# To place it at (x_target, y_target, z_target):
# 1. Create circle in XZ plane at (x_target, z_target)
# 2. Extrude along Y
# 3. Translate the result to have its center at y_target

def create_y_cyl_at(x, y, z, d, h):
    return (
        cq.Workplane("XZ")
        .center(x, z)
        .circle(d/2)
        .extrude(h, both=True)
    ).translate((0, y, 0)) # This is the key: XZ plane extrusion moves along Y.

# R3 Central Bore
bracket = bracket.cut(create_y_cyl_at(MOTOR_SHAFT_X, 2.0, MOTOR_SHAFT_Z, CENTRAL_BORE_DIAMETER, 10.0))

# R4 Motor Screw Holes
for mx, mz in motor_holes:
    bracket = bracket.cut(create_y_cyl_at(mx, 2.0, mz, 3.4, 10.0))

# 4. Create Motor Clearance Pocket (R5)
# Requirement: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5
clearance_box = (
    cq.Workplane("XY")
    .box(43.0, 48.0, (51.5 - 8.5))
    .translate((0, -24, (51.5 + 8.5)/2))
)
bracket = bracket.cut(clearance_box)

# 5. Subtract Base Screw Holes (R6)
for bx, by in base_holes:
    # These are vertical holes along Z. Use XY plane.
    bracket = bracket.cut(
        cq.Workplane("XY")
        .center(bx, by)
        .circle(5.5 / 2)
        .extrude(BASE_PLATE_THICKNESS + 2, both=True)
    )

result = bracket