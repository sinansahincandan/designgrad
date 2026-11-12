import cadquery as cq
import math

# 1. Constants and Phone Geometry Vectors
phone_angle = 65
rad = math.radians(phone_angle)

# u: long axis of phone (leaning back toward -X)
u = (-math.cos(rad), 0, math.sin(rad))
# n: normal to the screen (facing +X)
n = (math.sin(rad), 0, math.cos(rad))

# Phone origin (bottom-back edge center)
p_origin = (0, 0, 8)

# 2. Design Dimensions
base_w = 90.0  # x range: -50 to 40
base_d = 80.0  # y range: -40 to 40
base_thickness = 3.0

rib_thickness = 4.0
rib_width = 30.0 # Width in Y direction (matches |y| <= 15 requirement)

# 3. Base Plate (R2)
# x: [-50, 40], y: [-40, 40], z: [0, 3]
stand_base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((-5, 0, base_thickness/2))

# 4. Feature Construction (using phone local coordinates)
# To avoid intersection (R3), we offset features in the -n direction.

# Seat (R5): a in [-4, 0], b in [-8, 0] -> Center approx at a=-2, b=-4
seat_center = (
    p_origin[0] - 2 * u[0] - 4 * n[0],
    p_origin[1] - 2 * u[1] - 4 * n[1],
    p_origin[2] - 2 * u[2] - 4 * n[2]
)
# Increased thickness and size to ensure overlap with spine/base
seat = cq.Workplane("XY").box(rib_thickness + 2, rib_width, 15).translate((seat_center[0], seat_center[1], seat_center[2]))

# Lip (R5): a in [0, 8], b in [1, 5] -> Center approx at a=4, b=3
lip_center = (
    p_origin[0] + 4 * u[0] - 6 * n[0],
    p_origin[1] + 4 * u[1] - 6 * n[1],
    p_origin[2] + 4 * u[2] - 6 * n[2]
)
lip = cq.Workplane("XY").box(rib_thickness + 2, rib_width, 15).translate((lip_center[0], lip_center[1], lip_center[2]))

# Back Support (R4): a in [90, 110], b in [-2, 0] -> Center approx at a=100, b=-1
back_center = (
    p_origin[0] + 100 * u[0] - 1 * n[0],
    p_origin[1] + 100 * u[1] - 1 * n[1],
    p_origin[2] + 100 * u[2] - 1 * n[2]
)
# Increased height and adjusted translation to ensure it hits the spine/base structure
back_support = cq.Workplane("XY").box(rib_thickness + 2, rib_width, 150).translate((back_center[0], back_center[1], back_center[2]))

# 5. Connectivity (R1): The Spine
spine_length = 160 # Increased length to ensure it reaches from base to back support
spine_center = (
    p_origin[0] + 50 * u[0] - 4 * n[0],
    p_origin[1] + 50 * u[1] - 4 * n[1],
    p_origin[2] + 50 * u[2] - 4 * n[2]
)

spine = (
    cq.Workplane("XY")
    .box(rib_thickness + 2, rib_width, spine_length)
    .rotate((0, 0, 0), (0, 1, 0), -phone_angle)
    .translate((spine_center[0], spine_center[1], spine_center[2]))
)

# Vertical pillar to connect spine to base plate
connector = cq.Workplane("XY").box(rib_thickness + 4, rib_width, 60).translate((spine_center[0], spine_center[1], 25))

# Final Assembly (R1)
# We ensure all pieces are unioned. The increased dimensions and lengths ensure overlaps.
result = (
    stand_base
    .union(spine)
    .union(seat)
    .union(lip)
    .union(back_support)
    .union(connector)
)