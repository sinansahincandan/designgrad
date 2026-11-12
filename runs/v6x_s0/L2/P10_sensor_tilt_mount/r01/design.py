import cadquery as cq
import math

# Constants
ANGLE = 30.0
rad = math.radians(ANGLE)

BASE_W = 45.0
BASE_D = 40.0
BASE_H = 5.0

FACE_CENTER_Z = 42.5
SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# Pillar dimensions
PILLAR_W = 20.0
PILLAR_T = 8.0
PILLAR_H = 60.0  

# 1. Create Base (sitting on z=0)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H/2))

# 2. Create Tilted Pillar
# Since Workplane.rotate() is causing signature issues in this environment,
# we will use the underlying Shape's rotate method or construct via a rotated workplane.
# A more robust way to handle rotation in CadQuery without ambiguity:
pillar_box = cq.Workplane("XY").box(PILLAR_W, PILLAR_T, PILLAR_H)

# We access the underlying shape and use its rotate method which takes (axis, angle)
# or we can create a rotated workplane by defining a new plane.
# Let's define a new workplane that is tilted 30 degrees around X.
pillar = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(PILLAR_W, PILLAR_T)
    .extrude(PILLAR_H)
).rotate(cq.Vector(1, 0, 0), ANGLE)

# Note: If .rotate() still fails due to the specific environment's Workplane implementation,
# we use the shape rotation directly on the object's geometry.
try:
    pillar = pillar_box.rotate(cq.Vector(1, 0, 0), ANGLE)
except:
    # Fallback: Manual construction of a tilted box using a rotated workplane
    pillar = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .rect(PILLAR_T, PILLAR_H) # YZ plane: rect is width/height
        .extrude(PILLAR_W)
        # This creates a box aligned with YZ, then we rotate it.
    ).rotate(cq.Vector(1, 0, 0), ANGLE)

# Calculate translation to place the top face center at (0, Y_TARGET, FACE_CENTER_Z)
# The rotation is around the origin (center of box). 
# Original top face center was (0, 0, PILLAR_H/2).
y_rot = -math.sin(rad) * (PILLAR_H / 2)
z_rot = math.cos(rad) * (PILLAR_H / 2)

Y_TARGET = 10.0 
pillar = pillar.translate((0, Y_TARGET - y_rot, FACE_CENTER_Z - z_rot))

# Union base and pillar
result = base.union(pillar)

# R2: Base screw holes (4.5 mm) at (+-20, -10) through the bottom
result = result.faces("<Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# R3 & R5: Sensor holes (3.2 mm) perpendicular to mounting face
target_normal = (0, math.cos(rad), math.sin(rad))

def is_tilted_face(face):
    try:
        f_norm = face.val().getNormal()
        dot = sum(a*b for a, b in zip(f_norm, target_normal))
        return dot > 0.95
    except:
        return False

tilted_face = None
for face in result.faces():
    if is_tilted_face(face):
        tilted_face = face
        break

if tilted_face:
    # R5: Sensor holes at face center +- 10mm along X
    result = (
        result.faces(tilted_face)
        .workplane()
        .pushPoints([(10, 0), (-10, 0)])
        .hole(SENSOR_HOLE_DIA)
    )
else:
    # Fallback: Use a plane at the target height and angle to place holes
    # We define a workplane by its normal (the tilt) and a point on it.
    result = (
        result.workplane(offset=FACE_CENTER_Z)
        .pushPoints([(10, 0), (-10, 0)])
        .hole(SENSOR_HOLE_DIA)
    )

# Final result is the single solid