import cadquery as cq
import math

# Constants
ANGLE = 30.0
RAD = math.radians(ANGLE)

BASE_W = 45.0
BASE_D = 40.0
BASE_H = 10.0

FACE_CENTER_Z = 42.5
FACE_WIDTH = 40.0
FACE_HEIGHT = 30.0  # Area = 1200 mm^2 >= 900 mm^2

SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# 1. Create Base (Bottom surface at z=0)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H, centered=(False, False, False)).translate((0, 0, 0))

# 2. Create Tilted Pillar/Face
# We define the pillar such that it intersects the base.
pillar_thickness = 70.0 

# The face is at Z=42.5, tilted by ANGLE around X-axis.
# Extruding -70 along the normal (0, cos(30), sin(30)) ensures intersection with base.
pillar = (
    cq.Workplane("XY")
    .workplane(offset=FACE_CENTER_Z)
    .transformed(rotate=(ANGLE, 0, 0)) 
    .rect(FACE_WIDTH, FACE_HEIGHT)
    .extrude(-pillar_thickness)
)

# 3. Combine Base and Pillar
result = base.union(pillar)

# 4. Add Base Screw Holes (R2)
# Vertical holes at (+-20, -10) on the base top surface (Z=10)
result = result.faces(">Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# 5. Add Sensor Holes (R5)
# Perpendicular to the mounting face at +-10mm along X from center.
# We use a robust method: create cylinders oriented with the tilted normal and cut them.
# The rotation is around the X-axis at the FACE_CENTER_Z height.

for x_off in [10, -10]:
    # To place a cylinder correctly:
    # 1. Create cylinder at origin (0,0,0) along Z axis.
    # 2. Translate to local position on face (x_off, 0, FACE_CENTER_Z).
    # 3. Rotate around X-axis by ANGLE.
    # However, rotation in CQ 'transformed' is relative to the origin.
    # To rotate a cylinder at a specific point:
    # Translate to origin -> Rotate -> Translate back.
    
    cyl = (
        cq.Workplane("XY")
        .cylinder(100, SENSOR_HOLE_DIA / 2)
        .translate((x_off, 0, FACE_CENTER_Z))
        # To rotate around the point (x_off, 0, FACE_CENTER_Z):
        .transformed(rotate=(ANGLE, 0, 0), offset=(x_off, 0, FACE_CENTER_Z))
    )
    # The above 'transformed' with offset is actually a rotation around that offset point.
    # But in CQ, transformed(rotate, offset) rotates around the origin then translates.
    # Let's use the manual sequence for absolute certainty:
    
    cyl = (
        cq.Workplane("XY")
        .cylinder(100, SENSOR_HOLE_DIA / 2)
        .translate((-x_off, 0, -FACE_CENTER_Z)) # Move point to origin
        .transformed(rotate=(ANGLE, 0, 0))       # Rotate around origin
        .translate((x_off, 0, FACE_CENTER_Z))    # Move back
    )
    result = result.cut(cyl)