import cadquery as cq
import math

# Constants
ANGLE = 30.0
BASE_W = 45.0
BASE_D = 40.0
BASE_H = 5.0
FACE_CENTER_Z = 42.5
SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# 1. Create Base
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H)

# 2. Create Upright Pillar
pillar_width = 20.0
pillar_thickness = 8.0
pillar_height = 100.0  # Large height to ensure intersection with base

# Build the pillar and sensor holes
# Sensor holes are at +/- 10mm along the tilted X-axis relative to face center
pillar = (
    cq.Workplane("XY")
    .box(pillar_width, pillar_thickness, pillar_height)
    .faces(">Y").workplane()
    .pushPoints([(10, 0), (-10, 0)])
    .hole(SENSOR_HOLE_DIA)
)

# The error "missing 1 required positional argument: 'angleDegrees'" in some CQ versions
# can occur if the signature is actually rotate(axis, angleDegrees).
# We will use a different approach to rotate by using a transformation matrix or 
# simply rotating the workplane itself.
# However, let's try the most robust way: rotate around an axis via a Workplane object.

# Define rotation axis and angle
axis = cq.Vector(1, 0, 0)
angle_rad = math.radians(-ANGLE)

# Instead of pillar.rotate(), we use the fact that we can create a new workplane 
# or apply a transformation. Since rotate() is failing, let's build the pillar 
# in its own coordinate system and then translate/rotate it using a single operation.

# Let's try to fix the call: some versions of CQ use .rotate(axis, angle) 
# but if that fails, we can manually construct the geometry or use rotateWithMatrix.
# Actually, let's use the Workplane.rotate method correctly by ensuring it's not a 
# confusion between axis (Vector) and direction.

# Let's try: pillar = pillar.rotate(axis, ANGLE) - wait, the error says angleDegrees is missing.
# This implies the signature might be rotate(self, axis, angleDegrees).
# If it still fails, we will use a different method to achieve rotation.

try:
    pillar = pillar.rotate(axis, -ANGLE)
except TypeError:
    # Fallback if rotate() is behaving unexpectedly in this environment
    # We'll create the pillar by extruding a profile that is already tilted.
    # Or more simply, we can use a rotation matrix via translation/rotation logic.
    # But let's try to define the pillar using an extrusion on a rotated plane.
    pillar = (
        cq.Workplane("XY")
        .workplane(offset=0)
        .transformed(rotate=(axis.x, axis.y, axis.z, -ANGLE)) # This is often more stable
        .box(pillar_width, pillar_thickness, pillar_height)
    )
    # Re-add holes to the transformed pillar
    pillar = (
        pillar.faces(">Y").workplane()
        .pushPoints([(10, 0), (-10, 0)])
        .hole(SENSOR_HOLE_DIA)
    )

# Calculate translation to place the mounting face center at (0, target_y, FACE_CENTER_Z)
t = pillar_thickness
# We need to find where the local face center is after rotation/transformation.
# Since we used transformed(), the pillar's local origin is now rotated.
# The face was at Y = t/2. After rotation around X by -30 deg:
# Y_new = (t/2) * cos(-30) = (t/2) * cos(30)
# Z_new = (t/2) * sin(-30) = -(t/2) * sin(30)
# Wait, the design says normal is (0, cos30, sin30). 
# A rotation of -30 around X makes Y -> Z and Z -> -Y.
# Let's use a more direct approach for the pillar to ensure R3/R4 are met.

# RE-DO PILLAR with explicit geometry to avoid rotate() issues
pillar_width = 20.0
pillar_thickness = 8.0
pillar_height = 100.0

# Create a box that is already tilted and positioned correctly
# We'll use the transformed method which is very reliable in CQ 2.x
target_y = 10.0
target_z = FACE_CENTER_Z

# The center of the face (before rotation) is (0, t/2, 0).
# After rotating by -30 degrees around X:
# Y_rot = (t/2)*cos(-30) = (t/2)*cos(30)
# Z_rot = (t/2)*sin(-30) = -(t/2)*sin(30)
# We want: 
# Final_Y = target_y => Local_Y + Y_rot = target_y => Local_Y = target_y - Y_rot
# Final_Z = target_z => Local_Z + Z_rot = target_z => Local_Z = target_z - Z_rot

rad = math.radians(-ANGLE)
y_rot = (pillar_thickness / 2.0) * math.cos(rad)
z_rot = (pillar_thickness / 2.0) * math.sin(rad)

local_y = target_y - y_rot
local_z = target_z - z_rot

# Build pillar using transformed to avoid the problematic .rotate() call
pillar = (
    cq.Workplane("XY")
    .transformed(rotate=(1, 0, 0, -ANGLE))
    .box(pillar_width, pillar_thickness, pillar_height)
)

# Add sensor holes to the transformed pillar
# The face is at local Y = t/2. Since it's a box centered at origin, we use ">Y"
pillar = (
    pillar.faces(">Y").workplane()
    .pushPoints([(10, 0), (-10, 0)])
    .hole(SENSOR_HOLE_DIA)
)

# Translate the whole pillar to the correct position
pillar = pillar.translate((0, local_y, local_z))

# 3. Combine Base and Pillar
result = base.union(pillar)

# 4. Add Base Screw Holes (Vertical)
result = (
    result.faces(">Z").workplane()
    .pushPoints([(20, -10), (-20, -10)])
    .hole(BASE_HOLE_DIA)
)