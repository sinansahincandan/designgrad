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
base_w, base_d, base_t = 90.0, 90.0, 2.0
wall_t = 1.5
plate_t = 2.0
y_limit = 15.0  # |y| <= 15

# 1. Base Plate (z: 0 to 2)
base = cq.Workplane("XY").box(base_w, base_d, base_t).translate((0, 0, base_t/2))

# 2. Support Spine (Hollow Shell)
spine_len = 105.0 # Increased to ensure it reaches high components
spine_width = 25.0
spine_thickness = 6.0 

# Create a hollow box for the spine
spine_outer = (
    cq.Workplane("XY")
    .box(spine_thickness, spine_width, spine_len)
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
    .translate((0, 0, spine_len/2)) 
)

spine_inner = (
    cq.Workplane("XY")
    .box(spine_thickness - 2*wall_t, spine_width - 2*wall_t, spine_len + 2)
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
    .translate((0, 0, spine_len/2))
)

spine = spine_outer.cut(spine_inner)
# Move spine so it starts at z=0 and extends upwards
# The rotation happens around (0,0,0). We translate to ensure overlap with base.
spine = spine.translate((0, 0, 2)) 

# 3. Seat, Lip, and Rear Brace (Thin Plates)
def create_thin_plate(a_range, b_range, y_range, thickness):
    """Creates a plate at specific phone coordinates with an offset."""
    a_mid = sum(a_range)/2
    b_mid = sum(b_range)/2
    y_mid = 0 
    
    cx, cy, cz = get_phone_point(a_mid, b_mid, y_mid)
    
    # Apply offset along -n to stay behind/under the phone
    offset_x = cx - 0.5 * nx
    offset_y = cy - 0.5 * ny
    offset_z = cz - 0.5 * nz
    
    dx = (a_range[1] - a_range[0]) + 2 
    dy = (y_range[1] - y_range[0])
    dz = thickness
    
    # To ensure union, we rotate the plate to match the phone's local plane (u, n)
    # and translate it. A box in XY rotated by angle_deg matches the u-axis direction.
    return (
        cq.Workplane("XY")
        .box(dx, dy, dz)
        .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
        .translate((offset_x, offset_y, offset_z))
    )

# Seat: a in [-4, 0], b in [0, 9], |y| <= 15
seat = create_thin_plate((-4, 0), (0, 9), (-y_limit, y_limit), plate_t)

# Lip: a in [0, 8], b in [9, 13], |y| <= 15
lip = create_thin_plate((0, 8), (9, 13), (-y_limit, y_limit), plate_t)

# Rear Brace: a in [75, 95], b in [-2, 0], |y| <= 15
rear_brace = create_thin_plate((75, 95), (-2, 0), (-y_limit, y_limit), plate_t)

# 4. Connection Logic (R1 & R6)
# We need a continuous structure. Let's build a central spine/pillar that connects everything.
# The spine is already angled. We add a thick vertical pillar at the base to connect to the spine.
connector_pillar = cq.Workplane("XY").box(20, 20, 100).translate((0, 0, 50))

# To ensure Seat/Lip/Brace are connected to the Spine:
# We'll create a "spine-extension" or simply make sure the spine is thick enough.
# Since the plates are offset by -0.5 along n, they should intersect the spine if the spine 
# follows the same tilt and covers the coordinate range.

# Final Union
result = (
    base
    .union(spine)
    .union(connector_pillar)
    .union(seat)
    .union(lip)
    .union(rear_brace)
)

# Ensure everything is one solid by adding a large structural block if needed, 
# but here we rely on the spine and pillar to bridge all parts.
# Let's add a rib that specifically bridges the gap between the base/pillar and the rear brace area.
rib = cq.Workplane("XY").box(40, 20, 10).translate((30, 0, 40))
result = result.union(rib)