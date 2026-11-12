import cadquery as cq
import math

# Constants
ANGLE = 30.0
RAD = math.radians(ANGLE)

BASE_W = 45.0
BASE_D = 40.0
BASE_H = 5.0

FACE_WIDTH = 40.0
FACE_LENGTH = 25.0  # Length along the tilt direction
FACE_CENTER_Z = 42.5

SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# 1. Create Base (Bottom surface at z=0)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H / 2))

# Add Base Screw Holes (R2)
base = base.faces(">Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# 2. Create Tilted Pillar/Mounting Face (R3, R4, R5)
pillar_thickness = 10.0
Y_target = 5.0 

# We use a transformed workplane to create the tilted slab.
# The transformation rotates the XY plane around X by ANGLE.
# This makes the Z-axis of the workplane point in direction (0, sin(A), cos(A)).
# Wait, if we rotate the PLANE around X, the new Z is (0, sin(A), cos(A)).
# The design wants normal (0, cos(30), sin(30)). 
# Let's use rotation = (ANGLE, 0, 0) which rotates the coordinate system.

pillar_slab = (
    cq.Workplane("XY")
    .transformed(rotate=(ANGLE, 0, 0))
    .rect(FACE_WIDTH, FACE_LENGTH)
    .extrude(pillar_thickness)
)

# The slab is currently centered at the origin of the transformed plane.
# We need to translate it so its top face center is at (0, Y_target, FACE_CENTER_Z).
# In the transformed space, the "top" face center was at (0, 0, FACE_LENGTH/2).
# Let's find where that point is in global coordinates.
half_l = FACE_LENGTH / 2.0
# Rotation matrix for X-axis rotation by ANGLE:
# x' = x
# y' = y*cos(A) - z*sin(A)
# z' = y*sin(A) + z*cos(A)
# For point (0, 0, half_l):
y_rot = -half_l * math.sin(RAD)
z_rot = half_l * math.cos(RAD)

# We want: (0, y_rot + trans_y, z_rot + trans_z) = (0, Y_target, FACE_CENTER_Z)
trans_y = Y_target - y_rot
trans_z = FACE_CENTER_Z - z_rot

pillar_slab = pillar_slab.translate((0, trans_y, trans_z))

# 3. Create a robust connector to ensure one single solid (R1)
# The slab is tilted. We'll create a thick vertical column that goes from the base up to the slab.
# To guarantee union, we make it overlap both by at least 1mm.
connector_h = FACE_CENTER_Z + 5.0 # Tall enough to reach top of slab
connector = (
    cq.Workplane("XY")
    .box(FACE_WIDTH * 0.6, pillar_thickness, connector_h)
    .translate((0, Y_target, connector_h / 2))
)

# Union the parts into one pillar structure
pillar_assembly = pillar_slab.union(connector)

# 4. Final Union (Base + Pillar Assembly)
result = base.union(pillar_assembly)

# 5. Sensor Holes (R5)
# The holes must be perpendicular to the mounting face.
# We use a transformed workplane at the target center.
# Since we used .transformed(rotate=(ANGLE, 0, 0)), the Z axis is now our normal.
hole_plane = (
    cq.Workplane("XY")
    .transformed(rotate=(ANGLE, 0, 0))
    .translate((0, Y_target, FACE_CENTER_Z))
)

# We create the holes by drilling through the assembly.
# To ensure they are drilled correctly, we'll use a cylinder and cut it from the result.
h1 = (
    cq.Workplane("XY")
    .cylinder(100, SENSOR_HOLE_DIA / 2)
    .transformed(rotate=(ANGLE, 0, 0))
    .translate((10, Y_target, FACE_CENTER_Z))
)

h2 = (
    cq.Workplane("XY")
    .cylinder(100, SENSOR_HOLE_DIA / 2)
    .transformed(rotate=(ANGLE, 0, 0))
    .translate((-10, Y_target, FACE_CENTER_Z))
)

result = result.cut(h1).cut(h2)