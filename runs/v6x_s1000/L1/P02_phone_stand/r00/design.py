import cadquery as cq
import math

# Constants and Phone Geometry
phone_angle = 65
u_x = -math.cos(math.radians(phone_angle))
u_z = math.sin(math.radians(phone_angle))
n_x = math.sin(math.radians(phone_angle))
n_z = math.cos(math.radians(phone_angle))

# Design Dimensions
base_w = 90.0
base_d = 60.0  # x direction
base_thickness = 4.0
upright_thickness = 3.0

# 2. Calculate Back Support Position
back_a = 100.0
back_x = back_a * u_x
back_z = 8 + back_a * u_z

# Refined approach: Build from a single union of overlapping parts
# To avoid OCP errors with non-positive dimensions, we ensure lengths are positive.

# Base Plate (R2: x range -40 to 20, y range -45 to 45)
stand_base = cq.Workplane("XY").box(60, 90, 4).translate((-10, 0, 2))

# Upright support connecting base to back pillar (R4: near a=100)
# We ensure the upright is tall enough and overlaps with the base and rib/pillar
upright = (
    cq.Workplane("XY")
    .box(3, 30, 80)
    .translate((back_x, 0, 40))
)

# The cradle at the bottom (R5: intercept phone at a in [-4, 8])
cradle = (
    cq.Workplane("XY")
    .box(15, 30, 10)
    .translate((2, 0, 6))
)

# Structural rib to connect the cradle area to the upright/back support
# We use a positive length for the box and translate it to span the gap
rib_length = abs(back_x - 2) + 5
rib = (
    cq.Workplane("XY")
    .box(rib_length, 10, 4)
    .translate((back_x/2, 0, 6))
)

# Final assembly: Union all parts into one single solid
result = (
    stand_base
    .union(upright)
    .union(cradle)
    .union(rib)
)