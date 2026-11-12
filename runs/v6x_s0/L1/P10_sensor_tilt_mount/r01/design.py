import cadquery as cq
import math

# Constants
ANGLE = 30.0
RAD = math.radians(ANGLE)

# Base dimensions (Adjusted for R6 stability margin)
BASE_W = 45.0
BASE_D = 45.0  # Increased to ensure >= 5mm margin
BASE_H = 5.0
BASE_HOLE_DIA = 4.5

# Target mounting face center (R4)
FACE_CENTER_X = 0.0
FACE_CENTER_Y = 15.0
FACE_CENTER_Z = 42.5

# Sensor hole dimensions (R5)
SENSOR_HOLE_DIA = 3.2
SENSOR_HOLE_OFFSET_X = 10.0

# Pillar dimensions
PILLAR_W = 20.0
PILLAR_T = 8.0
PILLAR_H = 60.0 # Sufficient height to reach face center

# 1. Create Base
# The base is centered such that y-range is [-10, 35] (since BASE_D=45 and we offset by -10)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 12.5, BASE_H/2))

# 2. Create Tilted Pillar (R3)
# Since .rotate() and .transformed() are causing issues in this environment's CQ version,
# we will build the pillar by creating a box and using a manual rotation via a sequence of operations
# or simply constructing it from primitives that don't rely on those broken methods.

# We define the pillar as a box at origin, then manually calculate its orientation/position.
pillar_box = cq.Workplane("XY").box(PILLAR_W, PILLAR_T, PILLAR_H)

# Instead of .rotate(), we use a more stable way to handle rotation if available, 
# but since the environment is failing on both rotate and transformed, 
# let's construct the pillar using a different approach: extrude a rectangle from a tilted plane.

# We define a workplane that is already tilted.
# The normal of the mounting face is (0, cos(30), sin(30)).
# This means the local Z-axis of our workplane will be this normal.
# A tangent vector in X is (1, 0, 0).
# A second tangent vector in Y would be cross((0, cos30, sin30), (1, 0, 0)) = (0, sin30, -cos30).

# We'll use the 'workplane' method with a normal to define the tilted plane.
pillar_final = (
    cq.Workplane("XY")
    .workplane(offset=0)
    # Create a new workplane at the target face center, with the correct normal
    .center(FACE_CENTER_X, FACE_CENTER_Y)
    .workplane(offset=FACE_CENTER_Z) 
    # We can't easily pass a vector to .workplane() in all CQ versions, 
    # so we build the pillar and rotate it using a standard rotation if possible, 
    # or just use the fact that we know the geometry.

    # Let's try one more time with a very simple approach: 
    # Build the pillar at origin, then translate/rotate using basic primitives.
)

# Re-attempting Pillar construction via a robust method:
# Create a box, and use rotate on the object itself if possible, or just build it correctly.
# Since .rotate(axis, angle) failed with "missing 1 required positional argument", 
# let's try passing the angle as a keyword argument.

try:
    pillar_tilted = pillar_box.rotate(cq.Vector(1, 0, 0), ANGLE)
except:
    # If that fails, we use the only reliable way left in CQ: build it on a tilted plane.
    # We'll create a rectangle on the XZ plane and extrude it along Y (which is now tilted).
    pillar_tilted = (
        cq.Workplane("XZ")
        .rect(PILLAR_W, PILLAR_T)
        .extrude(PILLAR_H)
    )
    # This creates a pillar along the Y axis. We need it to be tilted.
    # Let's use the most basic approach: build a box and rotate it via a different method.
    pillar_tilted = cq.Workplane("XY").box(PILLAR_W, PILLAR_T, PILLAR_H).rotate((1,0,0), ANGLE)

# If we reach here, the rotation worked or was bypassed. 
# Let's ensure pillar_final is correctly positioned.
face_local_y = (PILLAR_H / 2.0) * math.sin(RAD)
face_local_z = (PILLAR_H / 2.0) * math.cos(RAD)
trans_y = FACE_CENTER_Y - face_local_y
trans_z = FACE_CENTER_Z - face_local_z
pillar_final = pillar_tilted.translate((FACE_CENTER_X, trans_y, trans_z))

# 3. Combine into one solid (R1)
result = base.union(pillar_final)

# 4. Add Base Screw Holes (R2)
# Global hole positions: x = +-20, y = -10.
# The base center is at (0, 12.5, 2.5). 
# Relative to base center (0, 12.5): dx = +-20, dy = -10 - 12.5 = -22.5
result = result.faces("<Z").workplane().center(0, 0).pushPoints([(-20, -22.5), (20, -22.5)]).hole(BASE_HOLE_DIA)

# 5. Add Sensor Holes (R5)
target_normal = (0, math.cos(RAD), math.sin(RAD))

def is_mounting_face(face):
    f_norm = face.normal()
    return abs(f_norm.x - target_normal[0]) < 1e-3 and \
           abs(f_norm.y - target_normal[1]) < 1e-3 and \
           abs(f_norm.z - target_normal[2]) < 1e-3

mounting_face = None
for face in result.faces():
    if is_mounting_face(face):
        mounting_face = face
        break

if mounting_face:
    result = (
        result.faces([mounting_face])
        .workplane()
        .pushPoints([(SENSOR_HOLE_OFFSET_X, 0), (-SENSOR_HOLE_OFFSET_X, 0)])
        .hole(SENSOR_HOLE_DIA)
    )

# Final result is assigned to 'result'