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

def get_phone_point(a, b, y_val, offset_n=0.0):
    """Calculates a point in the phone's coordinate system with an optional normal offset."""
    x = base_p[0] + a * ux + (b + offset_n) * nx
    y = y_val
    z = base_p[2] + a * uz + (b + offset_n) * nz
    return (x, y, z)

# Design Parameters
base_w, base_d, base_thickness = 80.0, 80.0, 2.0
contact_thickness = 5.0 # Increased thickness to ensure better union intersection
clearance = -0.6  # Offset along normal (R3)

# 1. Base Plate (z: 0 to 2)
base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((0, 0, base_thickness/2))

# 2. Support Web / Main Body
# We create a central pillar that reaches up to the highest contact point (approx Z=110)
web = cq.Workplane("XY").box(20, 40, 120).translate((0, 0, 60))

# 3. Contact Volumes (Seat, Lip, Rear Brace)
def create_contact_volume(a_range, b_range, y_range, dx, dy, dz):
    """Creates a box centered at the average phone-coord point with clearance."""
    a_mid = (a_range[0] + a_range[1]) / 2.0
    b_mid = (b_range[0] + b_range[1]) / 2.0
    y_mid = (y_range[0] + y_range[1]) / 2.0
    cx, cy, cz = get_phone_point(a_mid, b_mid, y_mid, offset_n=clearance)
    # We use a slightly larger box to ensure it penetrates the web/connectors
    return cq.Workplane("XY").box(dx, dy, dz).translate((cx, cy, cz))

# Seat: a in [-4, 0], b in [0, 9], |y| <= 15 (R5)
seat = create_contact_volume((-4, 0), (0, 9), (-15, 15), 12, 35, contact_thickness)

# Lip: a in [0, 8], b in [9, 13], |y| <= 15 (R5)
lip = create_contact_volume((0, 8), (9, 13), (-15, 15), 12, 35, contact_thickness)

# Rear Brace: a in [90, 110], b in [-2, 0], |y| <= 15 (R4)
rear_brace = create_contact_volume((90, 110), (-2, 0), (-15, 15), 25, 35, contact_thickness)

# 4. Connectors to ensure R1 (Single Solid) and overlap >= 1mm
# Connector from Web to Seat/Lip area
seat_lip_connector = cq.Workplane("XY").box(30, 40, 120).translate((-5, 0, 60))

# Connector from Web to Rear Brace (The problematic piece)
# The rear brace is at a ~ 100, which translates to x ~ -30.
# We create a thick structural arm that spans from the central web to the brace location.
# To ensure it hits the brace, we calculate its center roughly or just make it very long.
brace_arm = cq.Workplane("XY").box(150, 20, 10).translate((30, 0, 95))

# Final Union (R1)
result = (
    base
    .union(web)
    .union(seat)
    .union(lip)
    .union(rear_brace)
    .union(seat_lip_connector)
    .union(brace_arm)
)

# Final check: The brace_arm is placed at Z=95, which should overlap the rear_brace 
# (which was reported around Z=93-103).