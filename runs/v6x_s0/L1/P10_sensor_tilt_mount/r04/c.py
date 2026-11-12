import cadquery as cq
import math

# Constants
ANGLE = 30.0
BASE_W = 45.0
BASE_D = 60.0  # Updated for stability (R6)
BASE_H = 5.0
FACE_CENTER_Z = 42.5
SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# Pillar dimensions
PILLAR_W = 25.0
PILLAR_T = 10.0
PILLAR_H = 50.0  # Length of the pillar along its axis

# 1. Create Base
# Footprint: x in [-22.5, 22.5], y in [-20, 40]
base = (
    cq.Workplane("XY")
    .box(BASE_W, BASE_D, BASE_H)
    .translate((0, 10, BASE_H / 2)) # y center at 10 means range [-20, 40]
)

# Add base screw holes (R2)
base = base.faces(">Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# 2. Create Tilted Pillar
rad = math.radians(ANGLE)

# To avoid the "Workplane object must have at least one solid" error, 
# we ensure that when we call .box(), it actually puts a solid on the stack.
# In some CQ versions, transformations might clear the stack if not handled carefully.
# We'll build the pillar and then union it to the base using the underlying solids.

pillar_length = PILLAR_H + 50.0 # Ensure it reaches the base

# Create the pillar
pillar = (
    cq.Workplane("XY")
    .box(PILLAR_W, PILLAR_T, pillar_length)
    .transformed(rotate=(ANGLE, 0, 1))
)

# Calculate translation to place the "top" face center at (0, 0, FACE_CENTER_Z).
local_y = (PILLAR_T / 2) * math.cos(rad) - (pillar_length / 2) * math.sin(rad)
local_z = (PILLAR_T / 2) * math.sin(rad) + (pillar_length / 2) * math.cos(rad)

pillar = pillar.translate((0, -local_y, FACE_CENTER_Z - local_z))

# 3. Combine Base and Pillar (R1)
# If .union() fails due to stack issues, we use the solid directly.
# We extract the solids from both workplanes.
s1 = base.solids().pop()
s2 = pillar.solids().pop()
combined_solid = s1.union(s2)

# Re-wrap in a Workplane to continue operations
result = cq.Workplane("XY").add(combined_solid)

# 4. Add Sensor Holes (R5)
# We find the face with normal (0, cos30, sin30).
target_normal = (0, math.cos(rad), math.sin(rad))

# Select faces by direction and create holes on that plane.
result = (
    result.faces(cq.Direction(target_normal[0], target_normal[1], target_normal[2]))
    .workplane()
    .center(0, 0)
    .pushPoints([(10, 0), (-10, 0)])
    .hole(SENSOR_HOLE_DIA)
)