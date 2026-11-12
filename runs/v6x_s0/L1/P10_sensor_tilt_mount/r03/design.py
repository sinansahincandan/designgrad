import cadquery as cq
import math

# Constants
ANGLE = 30.0
BASE_W = 45.0
BASE_D = 40.0
BASE_H = 5.0
FACE_CENTER_X = 0.0
FACE_CENTER_Y = 15.0
FACE_CENTER_Z = 42.5

SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

PILLAR_WIDTH = 35.0
PILLAR_THICKNESS = 30.0  # This is the dimension along the normal to create face area
PILLAR_HEIGHT = 60.0     # Length of the pillar block

# 1. Create Base (centered at origin, but we'll adjust Z so bottom is at z=0)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H / 2))

# 2. Create Pillar
# The error "missing 1 required positional argument: 'angleDegrees'" indicates that in this 
# specific environment's version of CadQuery, the rotate method might be expecting 
# different arguments or is being called on a Workplane object where the signature 
# differs from standard documentation. We will use the .rotate(axis, angle) pattern 
# but ensure we are calling it correctly. If rotate() fails, we can use rotation 
# matrices or build via extrusion/rotation if necessary.
# However, let's try passing the axis as a tuple and see if that satisfies the parser.

pillar = cq.Workplane("XY").box(PILLAR_WIDTH, PILLAR_THICKNESS, PILLAR_HEIGHT)

# Try to use rotate with explicit arguments. 
# If Workplane.rotate() is failing with "missing angleDegrees", it might be because 
# the environment expects a different signature or there's an internal mismatch.
# We will attempt to rotate using the axis and angle directly.
pillar = pillar.rotate(cq.Vector(1, 0, 0), ANGLE)

# Calculate translation to place the face center at target.
rad = math.radians(ANGLE)
# The box was centered at origin. After rotation around X:
# Local Y-axis becomes (0, cos(angle), sin(angle))
# Local Z-axis becomes (0, -sin(angle), cos(angle))
# The "front" face of the pillar is at local Y = PILLAR_THICKNESS/2.
face_local_center_y = (PILLAR_THICKNESS / 2) * math.cos(rad)
face_local_center_z = (PILLAR_THICKNESS / 2) * math.sin(rad)

trans_x = FACE_CENTER_X - 0
trans_y = FACE_CENTER_Y - face_local_center_y
trans_z = FACE_CENTER_Z - face_local_center_z

pillar = pillar.translate((trans_x, trans_y, trans_z))

# Ensure the pillar overlaps with the base to form a single solid.
# We add a connector (rib) from the base center to the pillar.
connector = cq.Workplane("XY").box(10, 10, 50).translate((0, 0, 25))

# Combine into one solid
result = base.union(pillar).union(connector)

# 3. Subtract Base Holes (R2)
# Holes at (+-20, -10), diameter 4.5, vertical (along Z)
result = result.faces(">Z").workplane().center(-20, -10).hole(BASE_HOLE_DIA)
result = result.faces(">Z").workplane().center(20, -10).hole(BASE_HOLE_DIA)

# 4. Subtract Sensor Holes (R5)
target_normal = cq.Vector(0, math.cos(rad), math.sin(rad))

def find_tilted_face(shape):
    for face in shape.faces():
        if face.normal().normalized().dot(target_normal) > 0.99:
            return face
    return None

tilted_face = find_tilted_face(result)

if tilted_face:
    # Create workplane on the tilted face and drill holes perpendicular to it
    result = (
        result.faces(tilted_face.surface())
        .workplane()
        .pushPoints([(10, 0), (-10, 0)])
        .hole(SENSOR_HOLE_DIA)
    )

# Final result is a single solid