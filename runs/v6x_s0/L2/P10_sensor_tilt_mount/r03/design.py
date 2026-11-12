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

# Target position for the mounting face center (R3, R4)
TARGET_Y = 10.0
TARGET_Z = FACE_CENTER_Z

# 1. Create Base (bottom surface at z=0 to satisfy R2)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H/2))

# Add base screw holes (R2)
# Holes are vertical and located at (+-20, -10)
base = base.faces(">Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# 2. Create Upright Pillar
pillar_width = 25.0
pillar_thickness = 10.0
pillar_height = 80.0 

rad = math.radians(ANGLE)

# The error "missing 1 required positional argument: 'angleDegrees'" in CadQuery's Workplane.rotate 
# often occurs because the method is actually a wrapper for rotating objects, and in some 
# environments/versions, it expects (axis, angle) but the signature check fails if not called on 
# an object or via a different path. We will use the underlying rotation logic by creating 
# the pillar and using rotate with explicit arguments.

pillar = cq.Workplane("XY").box(pillar_width, pillar_thickness, pillar_height)

# If .rotate(axis, angle) is failing due to signature issues in this specific environment,
# we use a different approach: create the box at an orientation using a plane or 
# simply rotate the objects via the underlying geometry if possible.
# However, let's try the most standard way for CadQuery 2.x which is .rotate(axis, angle).
# If that fails, it might be because 'angleDegrees' is a keyword-only argument in this version.
try:
    pillar = pillar.rotate(cq.Vector(1, 0, 0), ANGLE)
except TypeError:
    pillar = pillar.rotate(cq.Vector(1, 0, 0), angleDegrees=ANGLE)

# Calculate translation to place the center of the tilted face at (0, TARGET_Y, TARGET_Z)
# The unrotated box center is (0,0,0). The front face center was (0, thickness/2, 0).
# After rotation around X by ANGLE:
# y_new = (thickness/2)*cos(rad) - 0*sin(rad)
# z_new = (thickness/2)*sin(rad) + 0*cos(rad)
dy = TARGET_Y - (pillar_thickness / 2.0 * math.cos(rad))
dz = TARGET_Z - (pillar_thickness / 2.0 * math.sin(rad))

# Translate pillar to the target face position
pillar = pillar.translate((0, dy, dz))

# 3. Union Base and Pillar
# Ensure overlap: The pillar is tall enough that it will intersect the base at z=5.
result = base.union(pillar)

# 4. Add Sensor Holes (R5)
# Select the face with normal (0, cos30, sin30)
target_normal = cq.Vector(0, math.cos(rad), math.sin(rad))

# We use a small tolerance for selection and drill holes perpendicular to the face
result = result.faces(cq.selectors.NormalSelector(target_normal)).workplane().pushPoints([(10, 0), (-10, 0)]).hole(SENSOR_HOLE_DIA)