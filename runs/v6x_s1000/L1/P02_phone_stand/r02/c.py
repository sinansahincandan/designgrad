import cadquery as cq
import math

# 1. Constants and Phone Geometry
phone_angle = 65
u_x = -math.cos(math.radians(phone_angle))
u_z = math.sin(math.radians(phone_angle))
n_x = math.sin(math.radians(phone_angle))
n_z = math.cos(math.radians(phone_angle))

# Phone base line: (0, y, 8)
# Point at a, b is: P = (0, y, 8) + a*u + b*n

def get_global_pos(a, b, y=0):
    """Helper to convert phone local coordinates (a, b, y) to global (x, y, z)."""
    x = a * u_x + b * n_x
    z = 8 + a * u_z + b * n_z
    return x, y, z

# 2. Design Dimensions & Requirements
base_w = 60.0  # x-extent: -40 to 20 (width 60)
base_d = 90.0  # y-extent: -45 to 45 (depth 90)
base_thickness = 3.0

# R4: Back Support at a=100, b=-1 (to be behind the phone)
a_back = 100.0
b_back = -1.0
back_support_x, back_support_y, back_support_z = get_global_pos(a_back, b_back, 0)

# R5: Seat (a in [-4, 0], b in [-2, 9])
a_seat, b_seat = -2.0, 3.5
seat_x, seat_y, seat_z = get_global_pos(a_seat, b_seat, 0)

# R5: Lip (a in [0, 8], b in [9, 13])
a_lip, b_lip = 4.0, 11.0
lip_x, lip_y, lip_z = get_global_pos(a_lip, b_lip, 0)

# 3. Construct Primitives

# Base Plate (R2: z=0 to 3, x=-40 to 20, y=-45 to 45)
stand_base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((-10, 0, base_thickness/2))

# Back Support (R4: width 30, thickness 3, height 60)
# We make it a pillar from z=0 up to back_support_z + some margin.
# To ensure connection to base, we extend it down into the base.
back_support = (
    cq.Workplane("XY")
    .box(30, 3, back_support_z + 10) 
    .translate((back_support_x, 0, (back_support_z + 10)/2 - 1)) # Subtracting 1 to ensure overlap with base
)

# Seat (R5: width 30, depth 15, height 4)
# To connect seat/lip to the main body, we add a vertical support pillar or extend them.
# Since they are floating in space relative to the base, let's create a connecting rib from the base to the seat.
seat = (
    cq.Workplane("XY")
    .box(30, 15, 4)
    .translate((seat_x, 0, seat_z))
)

# Connecting Rib for Seat
seat_rib = (
    cq.Workplane("XY")
    .box(5, 5, seat_z + 2) # Height from base to seat
    .translate((seat_x, 0, (seat_z + 2)/2))
)

# Lip (R5: width 30, depth 4, height 5)
lip = (
    cq.Workplane("XY")
    .box(30, 4, 5)
    .translate((lip_x, 0, lip_z))
)

# Connecting Rib for Lip (connects to seat or base)
lip_rib = (
    cq.Workplane("XY")
    .box(5, 5, lip_z + 2)
    .translate((lip_x, 0, (lip_z + 2)/2))
)

# 4. Final Assembly (R1: Single Solid)
result = (
    stand_base
    .union(back_support)
    .union(seat)
    .union(seat_rib)
    .union(lip)
    .union(lip_rib)
)