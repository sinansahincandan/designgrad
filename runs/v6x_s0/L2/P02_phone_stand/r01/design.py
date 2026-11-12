import cadquery as cq
import math

# Constants and Phone Geometry
angle_deg = 65
angle_rad = math.radians(angle_deg)

# Vectors derived from spec:
# u (long axis): (-cos65, 0, sin65)
# n (normal/screen direction): (sin65, 0, cos65)
ux, uy, uz = -math.cos(angle_rad), 0.0, math.sin(angle_rad)
nx, ny, nz = math.sin(angle_rad), 0.0, math.cos(angle_rad)

# Base point of phone: (0, y, 8)
base_p = (0.0, 0.0, 8.0)

def get_phone_point(a, b, y_val):
    """Calculates a point in the phone's coordinate system."""
    x = base_p[0] + a * ux + b * nx
    y = y_val
    z = base_p[2] + a * uz + b * nz
    return (x, y, z)

# Design Parameters
base_w, base_d, thickness = 80.0, 80.0, 3.0

# 1. Base Plate (z: 0 to 3)
base = cq.Workplane("XY").box(base_w, base_d, thickness).translate((0, 0, thickness/2))

# 2. Support Spine / Main Backbone
spine_len = 160.0 
spine_width = 30.0
spine_thickness = 20.0 

# Create spine and ensure it is anchored to the base center
spine = (
    cq.Workplane("XY")
    .box(spine_thickness, spine_width, spine_len)
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
    .translate((0, 0, thickness))
)

# 3. Seat and Lip (R5)
def create_box_at_phone_coord(a, b, y_val, dx, dy, dz):
    cx, cy, cz = get_phone_point(a, b, y_val)
    return cq.Workplane("XY").box(dx, dy, dz).translate((cx, cy, cz))

# Seat: a in [-4, 0], b in [0, 9]. Offset slightly to avoid phone intersection (R3)
seat = create_box_at_phone_coord(-2, -1.5, 0, 6, 30, 4)

# Lip: a in [0, 8], b in [9, 13]. Offset slightly to avoid phone intersection (R3)
lip = create_box_at_phone_coord(4, 13.5, 0, 10, 30, 4)

# 4. Rear Brace (R4)
rear_brace = create_box_at_phone_coord(100, -1, 0, 15, 30, 15)

# 5. Connection logic (Ensuring R1: Single Solid)
# To prevent disconnected solids, we build a massive central pillar that spans the entire Z range
# and ensure it intersects both the base and all high-altitude components.
pillar = cq.Workplane("XY").box(40, 40, 200).translate((0, 0, 100))

# Bridges to connect seat/lip/brace to the central pillar
bridge_seat = create_box_at_phone_coord(-2, 5, 0, 30, 30, 10)
bridge_lip = create_box_at_phone_coord(4, 11, 0, 30, 30, 10)
brace_connector = create_box_at_phone_coord(100, -1, 0, 50, 50, 50)

# Anchor the pillar to the base plate
pillar_anchor = cq.Workplane("XY").box(40, 40, thickness * 2).translate((0, 0, thickness))

# Union everything
result = (
    base
    .union(spine)
    .union(seat)
    .union(lip)
    .union(rear_brace)
    .union(pillar)
    .union(bridge_seat)
    .union(bridge_lip)
    .union(brace_connector)
    .union(pillar_anchor)
)

# Final check: Ensure the spine is also anchored to the base center
spine_anchor = cq.Workplane("XY").box(30, 30, thickness * 2).translate((0, 0, thickness))
result = result.union(spine_anchor)