import cadquery as cq
import math

# Constants and Phone Geometry
phone_angle = 65
u_x = -math.cos(math.radians(phone_angle))
u_z = math.sin(math.radians(phone_angle))
n_x = math.sin(math.radians(phone_angle))
n_z = math.cos(math.radians(phone_angle))

# 1. Base Plate (R2)
# Footprint: x in [-50, 20], y in [-45, 45] -> Width=70, Depth=90
# Center of box is at (-15, 0), thickness 4mm, z-min = 0
stand_base = cq.Workplane("XY").box(70, 90, 4).translate((-15, 0, 2))

# 2. Back Support (R4 & R3)
# Located at a=100, b in [-2, 0]
back_a = 100
back_x = back_a * u_x
back_z = 8 + back_a * u_z

# To ensure connection to base (z=0 to 4), we make sure the support extends down.
# The box is height 100, centered at z=50 -> spans z from 0 to 100.
# It overlaps with the base plate which is at z in [0, 4].
back_support = (
    cq.Workplane("XY")
    .box(2, 30, 100)
    .translate((back_x - 1 * n_x, 0, 50))
)

# 3. Seat (R5)
# a in [-4, 0], b in [-2, 0]
seat_a = -2
seat_b = -1
seat_x = 8 + seat_a * u_x + seat_b * n_x
seat_z = 8 + seat_a * u_z + seat_b * n_z

# To ensure connection, we extend the seat downwards to overlap with the base plate.
# Base is at z=0..4. Seat center is at seat_z. We make it tall enough to hit z=0.
seat_height = seat_z + 5 # Ensure it reaches below the base
seat = (
    cq.Workplane("XY")
    .box(10, 30, seat_height)
    .translate((seat_x, 0, seat_z - seat_height/2))
)

# 4. Lip (R5)
# a in [0, 8], b in [9, 13]
lip_a = 4
lip_b = 11
lip_x = 8 + lip_a * u_x + lip_b * n_x
lip_z = 8 + lip_a * u_z + lip_b * n_z

# To ensure connection, we extend the lip downwards to overlap with the base plate.
lip_height = lip_z + 5
lip = (
    cq.Workplane("XY")
    .box(5, 30, lip_height)
    .translate((lip_x, 0, lip_z - lip_height/2))
)

# Final assembly: Union all parts into one single solid (R1)
result = (
    stand_base
    .union(back_support)
    .union(seat)
    .union(lip)
)