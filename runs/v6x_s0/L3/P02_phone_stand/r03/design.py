import cadquery as cq
import math

# Constants and Phone Geometry
angle_deg = 65
angle_rad = math.radians(angle_deg)
cos_a = math.cos(angle_rad)
sin_a = math.sin(angle_rad)

# Vectors for phone orientation
# u: long axis (tilt direction), n: normal to screen
u_vec = (-cos_a, 0, sin_a)
n_vec = (sin_a, 0, cos_a)

def get_phone_pos(a, b, y):
    """Returns the (x, y, z) position for a given phone coordinate."""
    x = 0 + a * u_vec[0] + b * n_vec[0]
    y_coord = y
    z = 8 + a * u_vec[2] + b * n_vec[2]
    return x, y_coord, z

# --- 1. Create the Phone Volume for Subtraction (R3) ---
# We model the phone as a box and rotate it to match the specification.
# The spec says: bottom-back edge is at (0, y, 8), length 160 along u, width 75 along y, thickness 9 along n.
phone_vol = (
    cq.Workplane("XY")
    .box(160, 75, 9)
    # Move center of box to the phone's center of mass position
    # CM is at (0, 0, 8) + 80*u + 4.5*n
    .translate((80 * u_vec[0] + 4.5 * n_vec[0], 0, 8 + 80 * u_vec[2] + 4.5 * n_vec[2]))
    # Rotate to align axes: local X -> u, local Y -> y, local Z -> n
    # We use a rotation matrix approach via multiple rotations or a single complex one.
    # Since it's a simple tilt around Y, we rotate by -65 degrees around Y.
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
)

# --- 2. Build the Stand Components ---

# Base Plate (R2: footprint [-50, 50], thickness 2mm)
base_w = 100.0
base_d = 90.0 # y in [-45, 45] to stay within 100x100 and provide stability
base_thickness = 2.0
base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((0, 0, base_thickness/2))

# Seat (R5: a in [-4, 0], b in [0, 9], |y| <= 15)
# We use a block that covers the range and let the subtraction handle precision.
sx, sy, sz = get_phone_pos(-2, 4.5, 0)
seat = cq.Workplane("XY").box(15, 30, 6).translate((sx, sy, sz))

# Lip (R5: a in [0, 8], b in [9, 13], |y| <= 15)
lx, ly, lz = get_phone_pos(4, 11, 0)
lip = cq.Workplane("XY").box(12, 30, 6).translate((lx, ly, lz))

# Rear Brace (R4: a in [70, 90], b in [-2, 0], |y| <= 15)
rx, ry, rz = get_phone_pos(80, -1, 0)
rear_brace = cq.Workplane("XY").box(4, 30, 60).translate((rx, ry, rz))

# Support Spine (R7: slimmed down to ~3mm thickness)
# Connects seat area to rear brace
s_start_x, s_start_y, s_start_z = get_phone_pos(-2, 4.5, 0)
s_end_x, s_end_y, s_end_z = get_phone_pos(80, -1, 0)

dx = s_end_x - s_start_x
dy = s_end_y - s_start_y
dz = s_end_z - s_start_z
dist = math.sqrt(dx**2 + dy**2 + dz**2)
mid_x, mid_y, mid_z = (s_start_x + dx/2), (s_start_y + dy/2), (s_start_z + dz/2)
angle_spine = math.degrees(math.atan2(dz, dx))

spine_strut_main = (
    cq.Workplane("XY")
    .box(3, 30, dist)
    .translate((mid_x, mid_y, mid_z))
    .rotate((mid_x, mid_y, mid_z), (0, 1, 0), -angle_spine)
)

# Connect Spine to Base
spine_to_base = cq.Workplane("XY").box(3, 30, s_start_z).translate((s_start_x, s_start_y, s_start_z/2))

# --- 3. Combine and Subtract (R1, R3) ---
# Union all parts first to create the stand geometry
stand_geometry = (
    base
    .union(seat)
    .union(lip)
    .union(rear_brace)
    .union(spine_strut_main)
    .union(spine_to_base)
)

# Subtract phone volume to ensure no intersection and create the cradle/hook shape
result = stand_geometry.cut(phone_vol)