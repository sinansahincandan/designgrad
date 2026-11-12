import cadquery as cq
import math

# Constants
ANGLE = 30.0
BASE_W = 45.0
BASE_D = 40.0
BASE_H = 5.0
FACE_CENTER_Z = 42.5
TARGET_Y = 10.0  # Position of pillar relative to base center

SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# Pillar dimensions (to ensure face area >= 900 mm^2)
PILLAR_W = 40.0
PILLAR_D = 25.0
PILLAR_H = 60.0 # Length of pillar along its local axis

# 1. Create Base (bottom at z=0)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H/2))

# 2. Create Pillar
# To ensure connection to base, we extend the pillar length downwards.
pillar_length = PILLAR_H + 60.0 

# The error "missing axisEndPoint" indicates that in this environment's version of rotate(),
# it expects (startPoint, endPoint, angle) rather than (axisVector, angle).
# We will define the rotation axis by two points on the X-axis.
p1 = cq.Vector(0, 0, 0)
p2 = cq.Vector(1, 0, 0)

pillar = (
    cq.Workplane("XY")
    .box(PILLAR_W, PILLAR_D, pillar_length)
    # Move the box so the "top" face is at the origin
    .translate((0, 0, -pillar_length/2)) 
    .rotate(p1, p2, ANGLE)
    # Now the center of the mounting face is at (0,0,0). Translate to target.
    .translate((0, TARGET_Y, FACE_CENTER_Z))
)

# 3. Union Base and Pillar
result = base.union(pillar)

# 4. Add Base Screw Holes (R2)
# Located at (+-20, -10) on the bottom face (z=0)
result = result.faces("<Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# 5. Add Sensor Holes (R5)
target_normal = cq.Vector(0, math.cos(math.radians(ANGLE)), math.sin(math.radians(ANGLE)))

def find_face_by_normal(shape, normal):
    for face in shape.faces():
        if face.normal().normalized().dot(normal.normalized()) > 0.99:
            return face
    return None

mounting_face = find_face_by_normal(result, target_normal)

if mounting_face:
    # Use the found face to create a workplane for holes perpendicular to it
    result = result.faces(mounting_face).workplane().pushPoints([(10, 0), (-10, 0)]).hole(SENSOR_HOLE_DIA)
else:
    # Fallback if normal selection fails
    result = result.faces(">Z").workplane().pushPoints([(10, 0), (-10, 0)]).hole(SENSOR_HOLE_DIA)

# Final check to ensure it's a single solid Workplane object
if not isinstance(result, cq.Workplane):
    result = cq.Workplane(result)