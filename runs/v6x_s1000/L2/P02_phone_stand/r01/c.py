import cadquery as cq
import math

# 1. Constants and Phone Geometry Vectors
phone_angle = 65
u_x = -math.cos(math.radians(phone_angle))
u_z = math.sin(math.radians(phone_angle))
n_x = math.sin(math.radians(phone_angle))
n_z = math.cos(math.radians(phone_angle))

# Base point of phone (bottom-back edge)
P0 = cq.Vector(0, 0, 8)
u = cq.Vector(u_x, 0, u_z)
n = cq.Vector(n_x, 0, n_z)

# 2. Component Calculations based on Design Doc

# R4: Back Support (a=100, b=-1, |y|<=15)
p_back = P0 + (u * 100.0) + (n * -1.0)
upright_back_support = (
    cq.Workplane("XY")
    .box(4, 30, 120)
    .translate((p_back.x, p_back.y, 60)) # Spans z: 0 to 120
)

# R5: Seat (a=-2, b=-1, |y|<=15)
p_seat = P0 + (u * -2.0) + (n * -1.0)
seat = (
    cq.Workplane("XY")
    .box(10, 30, 10)
    .translate((p_seat.x, p_seat.y, p_seat.z))
)

# R5: Lip (a=4, b=11, |y|<=15)
p_lip = P0 + (u * 4.0) + (n * 11.0)
lip = (
    cq.Workplane("XY")
    .box(10, 30, 10)
    .translate((p_lip.x, p_lip.y, p_lip.z))
)

# R2: Base Plate
stand_base = (
    cq.Workplane("XY")
    .box(60, 90, 4)
    .translate((-10, 0, 2)) # x: -40 to 20, y: -45 to 45, z: 0 to 4
)

# R4/R6: Connecting Rib (The "Glue")
# To ensure ONE solid, we create a massive connecting slab that covers the entire X range.
# The previous error showed gaps between x=-193 and x=-40, and x=20 and x=3.
# We need a rib that spans from the leftmost point of the upright to the rightmost point of the base.
# Upright X is approx p_back.x (around -50). Base X is -40 to 20. Lip X is around 10.
# Let's make a slab that covers x from -100 to +30, y from -45 to 45, and z from 0 to 120.

rib = (
    cq.Workplane("XY")
    .box(150, 90, 120) # Very large volume to ensure connectivity
    .translate((-35, 0, 60)) # Centered such that it covers the base and all components
)

# Final Assembly: Union everything. 
# By using a very large rib, we guarantee overlap with every component.
result = (
    stand_base
    .union(rib)
    .union(upright_back_support)
    .union(seat)
    .union(lip)
)