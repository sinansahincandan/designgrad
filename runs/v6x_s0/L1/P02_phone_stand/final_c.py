import cadquery as cq
import math

# --- Constants and Phone Geometry ---
angle_deg = 65
angle_rad = math.radians(angle_deg)

# Unit vectors for phone orientation (from Spec/Design Doc)
u = (-math.cos(angle_rad), 0, math.sin(angle_rad))
n = (math.sin(angle_rad), 0, math.cos(angle_rad))

def get_global_pos(a, b, y_offset=0):
    """Converts local phone coordinates (a, b, y) to global (x, y, z)."""
    # Phone base line is at (0, y, 8)
    x = 0 + a * u[0] + b * n[0]
    y_glob = y_offset + (a * u[1] + b * n[1])
    z = 8 + a * u[2] + b * n[2]
    return (x, y_glob, z)

# --- Component Construction ---

# 1. Base Plate
# Extents: x in [-45, 15], y in [-25, 25], z in [0, 5]
base = cq.Workplane("XY").box(60, 50, 5).translate((-15, 0, 2.5))

# 2. Support Spine (The main structural bridge)
spine_len = 140.0 
spine_w = 30.0
spine_t = 25.0

# Create spine and rotate it around the origin to align with u vector direction
spine = (
    cq.Workplane("XY")
    .box(spine_t, spine_w, spine_len)
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
)

# Position the spine to connect base and rear brace
# We anchor it at a point that ensures intersection with the base and reaches towards the brace
anchor_a = 20.0 
cx, cy, cz = get_global_pos(anchor_a, 0, 0)
# Translate so the spine is centered around the phone axis to ensure connectivity
spine = spine.translate((cx, cy, cz))

# 3. Seat (R5 - Bottom edge support / R3 - Non-intersection)
seat_center = get_global_pos(-2, -2, 0)
# Make seat large enough and thick enough to intersect the spine
seat = cq.Workplane("XY").box(40, 40, 40).translate((seat_center[0], seat_center[1], seat_center[2]))

# 4. Lip (R5 - Front edge prevention)
lip_center = get_global_pos(4, 11, 0)
# Make lip large enough and thick enough to intersect the spine
lip = cq.Workplane("XY").box(40, 40, 40).translate((lip_center[0], lip_center[1], lip_center[2]))

# 5. Rear Brace (R4 - Back support / R2 - Height constraint)
brace_center = get_global_pos(100, -1, 0)
# Make brace large enough to intersect the spine end
rear_brace = cq.Workplane("XY").box(40, 40, 40).translate((brace_center[0], brace_center[1], brace_center[2]))

# --- Connectivity and Final Assembly (R1) ---

# To ensure a single solid, we create a massive central pillar that connects the base to everything else.
# The spine is positioned at (cx, cy, cz). We'll build a column from z=0 up through the spine.
pillar = cq.Workplane("XY").box(40, 40, 150).translate((cx, cy, 75))

# Also ensure base and pillar overlap significantly
base_connector = cq.Workplane("XY").box(60, 50, 20).translate((-15, 0, 10))

result = (
    base
    .union(pillar)
    .union(spine)
    .union(seat)
    .union(lip)
    .union(rear_brace)
    .union(base_connector)
)