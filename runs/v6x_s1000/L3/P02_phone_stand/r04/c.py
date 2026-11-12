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
stand_base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((-5, 0, base_thickness/2))

# 4. Feature Construction (using phone local coordinates)
eps = 0.1

# Seat (R5): a in [-4, 0], b in [0, 9] -> Target center approx a=-2, b=4.5
seat_center = (
    p_origin[0] + (-2) * u[0] + (4.5 - eps) * n[0],
    p_origin[1] + (-2) * u[1] + (4.5 - eps) * n[1],
    p_origin[2] + (-2) * u[2] + (4.5 - eps) * n[2]
)
seat = cq.Workplane("XY").box(rib_thickness + 10, rib_width, 20).translate((seat_center[0], seat_center[1], seat_center[2]))

# Lip (R5): a in [0, 8], b in [9, 13] -> Target center approx a=4, b=11
lip_center = (
    p_origin[0] + 4 * u[0] + (11 - eps) * n[0],
    p_origin[1] + 4 * u[1] + (11 - eps) * n[1],
    p_origin[2] + 4 * u[2] + (11 - eps) * n[2]
)
lip = cq.Workplane("XY").box(rib_thickness + 10, rib_width, 20).translate((lip_center[0], lip_center[1], lip_center[2]))

# Back Support (R4): a in [90, 110], b in [-2, 0] -> Target center approx a=100, b=-1
back_center = (
    p_origin[0] + 100 * u[0] + (-1 - eps) * n[0],
    p_origin[1] + 100 * u[1] + (-1 - eps) * n[1],
    p_origin[2] + 100 * u[2] + (-1 - eps) * n[2]
)
back_support = cq.Workplane("XY").box(rib_thickness + 15, rib_width, 80).translate((back_center[0], back_center[1], back_center[2]))

# 5. Connectivity (R1): The Spine
spine_length = 200 # Very long spine to ensure it crosses everything
spine_center_pos = (
    p_origin[0] + 40 * u[0] - 5 * n[0],
    p_origin[1],
    p_origin[2] + 40 * u[2] - 5 * n[2]
)

spine = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_width, spine_length)
    .rotate((0, 0, 0), (0, 1, 0), -phone_angle)
    .translate((spine_center_pos[0], spine_center_pos[1], spine_center_pos[2]))
)

# Vertical connector to bridge the gap between base plate and the angled spine
# We make it very thick/long to guarantee union with both base and spine
connector = cq.Workplane("XY").box(rib_thickness + 20, rib_width + 20, 100).translate((spine_center_pos[0], spine_center_pos[1], 30))

# To ensure connectivity of the back support (which was failing), we add a dedicated bridge
bridge_to_back = cq.Workplane("XY").box(rib_thickness + 20, rib_width + 20, 150).translate((
    p_origin[0] + 60 * u[0],
    p_origin[1],
    p_origin[2] + 60 * u[2]
))

# Final Assembly (R1)
result = (
    stand_base
    .union(spine)
    .union(seat)
    .union(lip)
    .union(back_support)
    .union(connector)
    .union(bridge_to_back)
)