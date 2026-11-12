import cadquery as cq
import math

# Constants from Design Document
ANGLE = 30.0
RAD = math.radians(ANGLE)

BASE_W = 45.0
BASE_D = 40.0
BASE_H = 10.0

PILLAR_W = 40.0
PILLAR_T = 30.0  # This is the width of the face (along X)
PILLAR_D = 8.0   # Thickness of the pillar
PILLAR_L = 60.0  # Length/Height of the pillar

TARGET_FACE_CENTER = (0.0, 25.98, 42.5)
SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# 1. Create Base (R2: bottom at z=0)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H / 2))

# 2. Create Pillar (R3: Tilted face)
pillar = cq.Workplane("XY").box(PILLAR_W, PILLAR_D, PILLAR_L)

# Rotate around X axis to tilt towards +Y (forward). 
# Using the correct rotate signature for CadQuery 2.x: rotate((axis), (direction), angle)
pillar = pillar.rotate((1, 0, 0), (0, 1, 0), -ANGLE)

# R4: Position the center of the top face to TARGET_FACE_CENTER
local_top_center_y = (PILLAR_L / 2.0) * math.sin(RAD)
local_top_center_z = (PILLAR_L / 2.0) * math.cos(RAD)

trans_y = TARGET_FACE_CENTER[1] - local_top_center_y
trans_z = TARGET_FACE_CENTER[2] - local_top_center_z
pillar = pillar.translate((0, trans_y, trans_z))

# 3. Combine into a single solid (R1)
result = base.union(pillar)

# 4. Add Base Screw Holes (R2: at +-20, -10)
result = result.faces(">Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# 5. Add Sensor Holes (R5: perpendicular to mounting face)
target_normal = cq.Vector(0, math.cos(RAD), math.sin(RAD))

# Find the mounting face by iterating through all faces and checking their center/normals
mounting_face = None
for f in result.faces():
    # In CadQuery 2.x, Face objects are part of the underlying OpenCASCADE geometry.
    # We can use the bounding box or centroid to find the face near TARGET_FACE_CENTER.
    # A robust way is checking the distance from the face's center (using Center() method)
    try:
        f_center = f.Center()
        if f_center.sub(cq.Vector(*TARGET_FACE_CENTER)).length < 1.0:
            mounting_face = f
            break
    except:
        continue

# If center check fails, try checking the normal of the face via its surface
if not mounting_face:
    for f in result.faces():
        try:
            # Get a point on the face and calculate normal
            # We use the bounding box center as a proxy for finding the right face
            bbox = f.BoundingBox()
            f_center = cq.Vector((bbox.xmin + bbox.xmax)/2, (bbox.ymin + bbox.ymax)/2, (bbox.zmin + bbox.zmax)/2)
            if f_center.sub(cq.Vector(*TARGET_FACE_CENTER)).length < 1.0:
                mounting_face = f
                break
        except:
            continue

if mounting_face:
    # Create holes on that specific tilted face
    result = mounting_face.workplane().pushPoints([(10, 0), (-10, 0)]).hole(SENSOR_HOLE_DIA)

result = result