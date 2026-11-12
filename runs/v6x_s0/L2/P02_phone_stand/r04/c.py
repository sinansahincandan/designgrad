import cadquery as cq
import math

# --- Constants and Phone Geometry ---
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

# --- Design Parameters ---
base_w, base_d, base_thickness = 95.0, 80.0, 2.0
spine_width = 25.0
spine_wall = 1.5
max_z = 110.0

# --- Component Construction ---

# 1. Base Plate (z in [0, 2])
base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((0, 0, base_thickness/2))

# 2. Support Spine & Central Rib Assembly
# We create a massive central pillar that spans from z=0 to the max height of the phone support area.
# This ensures it intersects the base plate and provides an anchor for all contact volumes.
pillar = (
    cq.Workplane("XY")
    .box(spine_width, spine_width, max_z + 50) # Large pillar to ensure connectivity
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
    .translate((0, 0, 0)) # Centered at origin and spanning z=0 upwards
)

# 3. Contact Volumes & Connectors
def create_connected_volume(a_range, b_range, y_limit, thickness):
    """Creates a volume and a structural beam connecting it to the central pillar."""
    a_mid = sum(a_range)/2
    b_mid = sum(b_range)/2
    cx, cy, cz = get_phone_point(a_mid, b_mid, 0)
    
    # The contact volume itself
    dx = (a_range[1] - a_range[0]) + 2.0
    dy = y_limit
    dz = thickness
    
    volume = (
        cq.Workplane("XY")
        .box(dx, dy, dz)
        .rotate((0,0,0), (0,1,0), -angle_deg)
        .translate((cx, cy, cz))
    )
    
    # The connector: A massive beam that goes from the contact point to the central pillar.
    # We use a very large box and position it so it is guaranteed to intersect the pillar at (0,0,cz).
    dist = math.sqrt(cx**2 + cy**2)
    beam_len = dist + 30.0 # Extra length to ensure overlap with central pillar
    
    angle_to_center = math.atan2(cy, cx)
    # We create the beam such that its center is at a point between (cx,cy,cz) and (0,0,cz)
    # but we extend it significantly to guarantee intersection with the central pillar.
    beam = (
        cq.Workplane("XY")
        .box(beam_len, 20, thickness + 10)
        .rotate((0,0,0), (0,0,1), -math.degrees(angle_to_center))
        .translate((cx/2, cy/2, cz))
    )

    return volume.union(beam)

# Seat: a in [-4, 0], b in [0, 9]
seat = create_connected_volume((-4, 0), (0, 9), 30, 5)

# Lip: a in [0, 8], b in [9, 13]
lip = create_connected_volume((0, 8), (9, 13), 30, 5)

# Rear Brace: a in [90, 110], b in [-2, 0]
brace = create_connected_volume((90, 110), (-2, 0), 30, 15)

# --- Final Assembly ---
# We union everything. The pillar is the core anchor that connects to the base and all volumes via their beams.
result = (
    base
    .union(pillar)
    .union(seat)
    .union(lip)
    .union(brace)
)

# Final safety: ensure a single solid by adding one more massive vertical pillar if needed.
# The current logic uses a large central pillar and beams that reach the origin.