import cadquery as cq
import math

# Constants and Phone Geometry
angle_deg = 65
angle_rad = math.radians(angle_deg)
cos_a = math.cos(angle_rad)
sin_a = math.sin(angle_rad)

# Phone geometry parameters
phone_l = 160
phone_w = 75
phone_t = 9

def get_phone_pos(a, b, y):
    """Returns the (x, y, z) position for a given phone coordinate."""
    # u = (-cos65, 0, sin65), n = (sin65, 0, cos65)
    x = 0 + a * (-cos_a) + b * sin_a
    y_coord = y
    z = 8 + a * sin_a + b * cos_a
    return x, y_coord, z

# Create the phone volume for Boolean subtraction (R3)
# The phone is centered at its own local origin before transformation.
# Local center of box: (0,0,0). We need to align it so bottom-back edge 
# (a=0, b=0, y=0) is at (0,0,8).
# In local coords, a=0, b=0 is the corner. So we translate by half dimensions.
phone_vol = (
    cq.Workplane("XY")
    .box(phone_l, phone_w, phone_t)
    .translate((phone_l/2, 0, phone_t/2)) # Move origin to bottom-back corner
    # Rotate around the edge line (x=0, z=8, y=y)
    # The rotation axis is the Y axis at the offset position.
    # However, it's easier to rotate first then translate.
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
    .translate((0, 0, 8))
)

# 1. Base Plate (R2: x in [-50, 50], y in [-50, 50], z=0)
base_w = 100.0
base_d = 100.0
base_thickness = 3.0
base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((0, 0, base_thickness/2))

# 2. Seat and Lip (R5: a in [-4, 0] seat, [0, 8] lip; b in [0, 13])
# We use small boxes and cut the phone volume to ensure R3.
# Seat center approx: a=-2, b=4.5, y=0
sx, sy, sz = get_phone_pos(-2, 4.5, 0)
seat = cq.Workplane("XY").box(15, 30, 6).translate((sx, sy, sz)).cut(phone_vol)

# Lip center approx: a=4, b=11, y=0
lx, ly, lz = get_phone_pos(4, 11, 0)
lip = cq.Workplane("XY").box(15, 30, 6).translate((lx, ly, lz)).cut(phone_vol)

# 3. Rear Brace (R4: a in [80, 95], b in [-2, 0])
rx, ry, rz = get_phone_pos(87, -1, 0)
rear_brace = cq.Workplane("XY").box(6, 30, 50).translate((rx, ry, rz))

# 4. Support Spine (R3: No interference, R7: Low mass)
# Connect seat to rear brace
dx = rx - sx
dy = ry - sy
dz = rz - sz
dist = math.sqrt(dx**2 + dy**2 + dz**2)

# Create a slim spine and cut the phone volume out of it
spine_strut_main = (
    cq.Workplane("XY")
    .box(4, 30, dist)
    .translate((sx + dx/2, sy + dy/2, sz + dz/2))
    .rotate((sx + dx/2, sy + dy/2, sz + dz/2), (0, 1, 0), -math.degrees(math.atan2(dz, dx)))
    .cut(phone_vol)
)

# Connect spine to base
spine_to_base = cq.Workplane("XY").box(4, 30, sz).translate((sx, sy, sz/2))

# Combine all parts (R1: Single Solid)
result = (
    base
    .union(seat)
    .union(lip)
    .union(rear_brace)
    .union(spine_strut_main)
    .union(spine_to_base)
)

# Verification of R2: 
# Base is [-50, 50]. Rear brace a=87 -> x approx 87 * -cos(65) = -36. 
# Total X range is roughly within [-50, 50].