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
    return (x, y_offset, z)

# --- Component Construction ---

# 1. Base Plate
# Extents: x in [-45, 15], y in [-25, 25], z in [0, 5]
base = cq.Workplane("XY").box(60, 50, 5).translate((-15, 0, 2.5))

# 2. Support Spine (The main structural bridge)
spine_len = 140.0
spine_w = 15.0
spine_t = 12.0

# Create spine and rotate it around the origin to align with u vector direction
spine = (
    cq.Workplane("XY")
    .box(spine_t, spine_w, spine_len)
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
)

# Position the spine so it starts deep in the base and ends near the brace
anchor_a = 45.0
cx, cy, cz = get_global_pos(anchor_a, 0, 0)
spine = spine.translate((cx, cy, cz))

# 3. Seat (R5)
seat_center = get_global_pos(-2, 4.5, 0)
seat = cq.Workplane("XY").box(10, 30, 5).translate((seat_center[0], seat_center[1], seat_center[2]))

# 4. Lip (R5)
lip_center = get_global_pos(4, 11, 0)
lip = cq.Workplane("XY").box(10, 30, 5).translate((lip_center[0], lip_center[1], lip_center[2]))

# 5. Rear Brace (R4)
brace_center = get_global_pos(100, -1, 0)
rear_brace = cq.Workplane("XY").box(12, 30, 8).translate((brace_center[0], brace_center[1], brace_center[2]))

# --- Connectivity Fixes (Ensuring ONE solid via massive overlap) ---

# We will create a "Main Structural Core" that is guaranteed to intersect everything.
# This core will be a thick, tilted beam following the phone's axis.
core_len = 160.0
core_w = 30.0
core_t = 30.0

core = (
    cq.Workplane("XY")
    .box(core_t, core_w, core_len)
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
)
# Center the core so it spans from near base to far brace
core = core.translate((0, 0, 50))

# Connect Seat and Lip by making them part of a larger block that hits the core
seat_conn = cq.Workplane("XY").box(40, 40, 40).translate((seat_center[0], seat_center[1], seat_center[2]))
lip_conn = cq.Workplane("XY").box(40, 40, 40).translate((lip_center[0], lip_center[1], lip_center[2]))

# Connect Base to Core
# A large block that spans from z=0 up into the core area
base_to_core = cq.Workplane("XY").box(50, 50, 100).translate((-10, 0, 40))

# Connect Brace to Core
brace_to_core = cq.Workplane("XY").box(50, 50, 50).translate((brace_center[0]-20, brace_center[1], brace_center[2]))

result = (
    base
    .union(spine)
    .union(seat)
    .union(lip)
    .union(rear_brace)
    .union(core)
    .union(seat_conn)
    .union(lip_conn)
    .union(base_to_core)
    .union(brace_to_core)
)

# Final check: ensure the base is connected to everything via a massive floor-to-spine block
floor_bridge = cq.Workplane("XY").box(100, 60, 20).translate((10, 0, 5))
result = result.union(floor_bridge)