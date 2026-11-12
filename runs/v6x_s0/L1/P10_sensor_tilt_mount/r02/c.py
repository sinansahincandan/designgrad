import cadquery as cq
import math

# Constants from Design Document
ANGLE = 30.0
BASE_W = 45.0
BASE_D = 40.0
BASE_H = 5.0
FACE_CENTER_X = 0.0
FACE_CENTER_Y = -5.0
FACE_CENTER_Z = 42.5

PILLAR_WIDTH = 40.0
PILLAR_HEIGHT = 60.0  # Sufficient height to reach target Z
PILLAR_THICKNESS = 15.0 # Thickness along the normal direction

SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# Calculate rotation in radians
rad = math.radians(ANGLE)

# 1. Create Base
# The base top surface should be at z=0 to sit on the desk.
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, -BASE_H/2))

# 2. Create Pillar
# We create a box centered at the origin first.
pillar = cq.Workplane("XY").box(PILLAR_WIDTH, PILLAR_THICKNESS, PILLAR_HEIGHT)

# The error "missing 1 required positional argument: 'angleDegrees'" in some CadQuery versions 
# happens when calling rotate with a single vector or tuple incorrectly. 
# In standard CQ 2.x, the signature is rotate(axis, angle). 
# If that fails, we use the underlying rotation method or ensure arguments are passed correctly.
pillar = pillar.rotate(cq.Vector(1, 0, 0), ANGLE)

# To position the face center at (FACE_CENTER_X, FACE_CENTER_Y, FACE_CENTER_Z):
# Local front face center: (0, -PILLAR_THICKNESS/2, 0)
# Rotated: x' = 0; y' = (-T/2)*cos(30); z' = (-T/2)*sin(30)
local_face_center_y = -(PILLAR_THICKNESS / 2.0) * math.cos(rad)
local_face_center_z = -(PILLAR_THICKNESS / 2.0) * math.sin(rad)

# Translation needed to move local_face_center to target FACE_CENTER
trans_y = FACE_CENTER_Y - local_face_center_y
trans_z = FACE_CENTER_Z - local_face_center_z

pillar = pillar.translate((FACE_CENTER_X, trans_y, trans_z))

# 3. Combine Base and Pillar (R1)
# Ensure they overlap to form a single solid.
result = base.union(pillar)

# 4. Add Sensor Holes (R5)
# We select the face with the specific normal vector to ensure perpendicularity.
target_normal = cq.Vector(0, math.cos(rad), math.sin(rad))

# Find the mounting face and drill holes
result = result.faces(cq.Plane(normal=target_normal)).workplane().center(0, 0).pushPoints([
    (10, 0), 
    (-10, 0)
]).hole(SENSOR_HOLE_DIA)

# 5. Add Base Screw Holes (R2)
result = result.faces(">Z").workplane().pushPoints([
    (20, -10), 
    (-20, -10)
]).hole(BASE_HOLE_DIA)