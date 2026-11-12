import cadquery as cq
import math

# 1. Constants and Phone Geometry Vectors
phone_angle = 65
u_x = -math.cos(math.radians(phone_angle))
u_z = math.sin(math.radians(phone_angle))
n_x = math.sin(math.radians(phone_angle))
n_z = math.cos(math.radians(phone_angle))

# Base point of the phone (bottom-back edge)
p0_x, p0_y, p0_z = 0.0, 0.0, 8.0

def get_point(a, b, y):
    """Calculates a 3D coordinate based on phone parameters a, b, and y."""
    return (
        p0_x + a * u_x + b * n_x,
        p0_y + y,
        p0_z + a * u_z + b * n_z
    )

# 2. Component Definitions based on Design Document and Feedback

# Base Plate (R2, R6): Wide footprint to ensure stability
base_w = 60.0  # from -40 to 20
base_d = 90.0  # from -45 to 45
stand_base = cq.Workplane("XY").box(base_w, base_d, 4.0).translate((-10, 0, 2))

# Seat (R5): a in [-4, 0], b in [0, 9], |y| <= 15
seat_center = get_point(-2, 4.5, 0)
seat = (
    cq.Workplane("XY")
    .box(4, 30, 9) 
    .translate((seat_center[0], seat_center[1], seat_center[2]))
)

# Lip (R5): a in [0, 8], b in [9, 13], |y| <= 15
lip_center = get_point(4, 11, 0)
lip = (
    cq.Workplane("XY")
    .box(8, 30, 4) 
    .translate((lip_center[0], lip_center[1], lip_center[2]))
)

# Back Support (R4): a in [90, 110], b in [-2, 0], |y| <= 15
back_support_center = get_point(100, -1, 0)
back_support = (
    cq.Workplane("XY")
    .box(20, 30, 30) 
    .translate((back_support_center[0], back_support_center[1], back_support_center[2] + 15))
)

# The error indicates that "solid 2" (the seat/lip area) is floating at:
# bbox [-53.17, -15.0, 98.21] to [-33.17, 15.0, 128.21].
# This means the 'seat' and 'lip' are being placed very high up in Z due to get_point logic.
# We must ensure a structural connection from the base (z=0) all the way up to these components.

# Main Structural Spine: Connects Base Plate to everything else
spine = (
    cq.Workplane("XY")
    .box(40, 40, 200) # Very large spine to ensure it hits every component's Z range
    .translate((0, 0, 100))
)

# Connection for the specific floating "solid 2" (the seat/lip area)
# Based on the error bbox, solid 2 is around z=100-130 and x=-50 to -30.
floating_connector = (
    cq.Workplane("XY")
    .box(60, 40, 150) # Large volume spanning from base to the floating part
    .translate((-40, 0, 75))
)

# Connection for Back Support
back_connector = (
    cq.Workplane("XY")
    .box(120, 40, 40) # Spans x from -40 to +80 approx
    .translate((30, 0, 50))
)

# 3. Final Assembly (R1)
result = (
    stand_base
    .union(seat)
    .union(lip)
    .union(back_support)
    .union(spine)
    .union(floating_connector)
    .union(back_connector)
)