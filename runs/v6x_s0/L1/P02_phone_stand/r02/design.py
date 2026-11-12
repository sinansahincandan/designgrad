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
# We need to ensure the spine spans from the base plate up to the rear brace.
spine_len = 180.0 # Increased length significantly to ensure it bridges everything
spine_w = 40.0  
spine_t = 30.0

# Create spine and rotate it to align with the phone's tilt (u vector direction)
spine = (
    cq.Workplane("XY")
    .box(spine_t, spine_w, spine_len)
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
)

# To ensure connectivity, we place the spine such that it passes through:
# - The Base Plate area (z ~ 2.5)
# - The Rear Brace area (z ~ 95)
# We'll use a very large anchor to make sure it spans the whole distance.
# Let's place the center of the spine at a point that is halfway between base and brace in 'a' space.
anchor_a = 40.0 
anchor_b = 0.0
cx, cy, cz = get_global_pos(anchor_a, anchor_b, 0)

# Translate spine so its center is at the calculated global position
spine = spine.translate((cx, cy, cz))

# 3. Seat (R5)
seat_a_mid = -2.0
seat_b_mid = 4.5
seat_size_a = 30.0 # Large to ensure intersection with spine
seat_size_b = 30.0
seat_size_y = 40.0

scx, scy, scz = get_global_pos(seat_a_mid, seat_b_mid, 0)
# Position seat such that it overlaps the spine and base
seat = cq.Workplane("XY").box(seat_size_a, seat_size_y, 30).translate((scx, scy, scz))

# 4. Lip (R5)
lip_a_mid = 4.0
lip_b_mid = 11.0
lip_size_a = 30.0 # Large to ensure intersection with spine
lip_size_b = 30.0
lip_size_y = 40.0

lcx, lcy, lcz = get_global_pos(lip_a_mid, lip_b_mid, 0)
# Position lip such that it overlaps the spine and base
lip = cq.Workplane("XY").box(lip_size_a, lip_size_y, 30).translate((lcx, lcy, lcz))

# 5. Rear Brace (R4)
brace_a_mid = 100.0
brace_b_mid = -1.0
brace_size_a = 40.0 # Large to ensure intersection with spine
brace_size_b = 40.0
brace_size_y = 40.0

bcx, bcy, bcz = get_global_pos(brace_a_mid, brace_b_mid, 0)
# Position brace such that it overlaps the spine
rear_brace = cq.Workplane("XY").box(brace_size_a, brace_size_y, 40).translate((bcx, bcy, bcz))

# --- Final Assembly (R1: Single Solid via Union) ---
# We also add a "connector" block to force the base and spine together if they are still separate.
# The spine is centered at anchor_a=40, which is high up. Let's add a vertical pillar from base to spine.
pillar = cq.Workplane("XY").box(30, 30, 150).translate((-15, 0, 75))

result = (
    base
    .union(spine)
    .union(seat)
    .union(lip)
    .union(rear_brace)
    .union(pillar)
)

# To ensure the pillar actually hits the base and spine:
# Base is at z=0..5. Pillar center is 75, so it spans 0..150. Hits base.
# Spine is centered at anchor_a=40 (z ~ 8 + 40*sin(65) ~ 44). Pillar hits spine.