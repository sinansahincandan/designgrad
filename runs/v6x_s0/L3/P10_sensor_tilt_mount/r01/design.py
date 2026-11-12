import cadquery as cq
import math

# Constants
ANGLE = 30.0
RAD = math.radians(ANGLE)

BASE_W = 45.0
BASE_D = 40.0
BASE_H = 5.0

FACE_CENTER_Z = 42.5
FACE_WIDTH = 30.0
FACE_HEIGHT = 35.0  # Area = 1050 mm^2 (>= 900)

SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# 1. Create Base
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H/2))

# 2. Create Pillar
pillar_thickness = 15.0 
pillar_width = FACE_WIDTH
pillar_height = 60.0 

# The error "missing 1 required positional argument: 'axisEndPoint'" indicates that 
# rotate() in this environment is actually the method for rotating an object around 
# a line defined by two points (start and end), not axis-angle.
# To rotate around X-axis, we use (0,0,0) to (1,0,0).

pillar = (
    cq.Workplane("XY")
    .box(pillar_width, pillar_thickness, pillar_height)
    .rotate((0, 0, 0), (1, 0, 0), ANGLE)
)

# Calculate translation needed to place the tilted face center at target height.
# The top face center in local coordinates (before rotation) is (0, 0, pillar_height/2).
# After rotation around X by ANGLE:
# y_new = 0 * cos(A) - (H/2) * sin(A)
# z_new = 0 * sin(A) + (H/2) * cos(A)
local_y_face = -(pillar_height / 2.0) * math.sin(RAD)
local_z_face = (pillar_height / 2.0) * math.cos(RAD)

trans_z = FACE_CENTER_Z - local_z_face
# Shift forward to ensure stability and intersection with base
trans_y = 15.0 

pillar = pillar.translate((0, trans_y, trans_z))

# 3. Combine into single solid (R1)
result = base.union(pillar)

# 4. Base Screw Holes (R2)
result = result.faces("<Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# 5. Sensor Holes (R5)
# The mounting face has normal n = (0, cos30, sin30).
target_normal = cq.Vector(0, math.cos(RAD), math.sin(RAD))

# Find the face that matches this direction and drill holes perpendicular to it.
result = result.faces(target_normal).workplane().pushPoints([(10, 0), (-10, 0)]).hole(SENSOR_HOLE_DIA)