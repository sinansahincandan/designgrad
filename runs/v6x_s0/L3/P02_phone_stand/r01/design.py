import cadquery as cq
import math

# Constants and Phone Geometry
angle_deg = 65
angle_rad = math.radians(angle_deg)
cos_a = math.cos(angle_rad)
sin_a = math.sin(angle_rad)

# Phone bottom edge is at (0, y, 8). 
# Direction u = (-cos65, 0, sin65)
# Direction n = (sin65, 0, cos65)

def get_phone_pos(a, b, y):
    """Returns the (x, y, z) position for a given phone coordinate."""
    x = 0 + a * (-cos_a) + b * sin_a
    y_coord = y
    z = 8 + a * sin_a + b * cos_a
    return x, y_coord, z

# 1. Base Plate (R2: sits on z=0, R6: wide footprint for stability)
base_w = 90.0
base_d = 50.0
base_thickness = 3.0
base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((0, 0, base_thickness/2))

# 2. Seat and Lip (R5: a in [-4, 0] seat, [0, 8] lip; b in [9, 13])
# We create these as small blocks centered around the phone's bottom edge geometry.
# Since |y| <= 15 is required, we use y_width = 30.

# Seat: a=-2 (midpoint of -4 to 0), b=4.5 (midpoint of 0 to 9)
sx, sy, sz = get_phone_pos(-2, 4.5, 0)
seat = cq.Workplane("XY").box(15, 30, 4).translate((sx, sy, sz))

# Lip: a=4 (midpoint of 0 to 8), b=11 (midpoint of 9 to 13)
lx, ly, lz = get_phone_pos(4, 11, 0)
lip = cq.Workplane("XY").box(15, 30, 4).translate((lx, ly, lz))

# 3. Rear Brace (R4: a in [90, 110], b in [-2, 0])
# We place it at a=100, b=-1
rx, ry, rz = get_phone_pos(100, -1, 0)
rear_brace = cq.Workplane("XY").box(5, 30, 40).translate((rx, ry, rz))

# 4. Support Spine (R3: No interference, R7: Low mass)
# Instead of a massive block, we use thin struts to connect the components.
# Strut 1: Base to Seat/Lip area
s1_x, s1_y, s1_z = get_phone_pos(-2, 4.5, 0)
spine_strut_bottom = cq.Workplane("XY").box(5, 30, s1_z).translate((s1_x, s1_y, s1_z/2))

# Strut 2: Seat area to Rear Brace (the main structural spine)
# We'll use a thin rod following the phone's tilt direction u.
# The vector from seat center to brace center:
dx = rx - sx
dy = ry - sy
dz = rz - sz
dist = math.sqrt(dx**2 + dy**2 + dz**2)

spine_strut_main = (
    cq.Workplane("XY")
    .box(4, 30, dist)
    .rotate((0, 0, 0), (0, 1, 0), 0) # Placeholder for rotation logic
)
# To simplify and ensure R1/R3, we'll use a simple oriented box for the spine
# that connects seat to brace.
spine_strut_main = cq.Workplane("XY").box(4, 30, dist).translate((sx + dx/2, sy + dy/2, sz + dz/2))
# Rotate the strut to align with the vector (dx, dy, dz)
# Since dy is 0, we only rotate around Y axis.
angle_spine = math.degrees(math.atan2(dz, dx))
spine_strut_main = spine_strut_main.rotate((sx + dx/2, sy + dy/2, sz + dz/2), (0, 1, 0), -angle_spine)

# Strut 3: Rear Brace to Base
# Connect the bottom of the rear brace back to the base plate
rb_bottom_z = rz - 20 # approximate bottom of brace
brace_to_base = cq.Workplane("XY").box(5, 30, rb_bottom_z).translate((rx, ry, rb_bottom_z/2))

# Combine all parts (R1: Single Solid)
# We use union to ensure it's one piece.
result = (
    base
    .union(seat)
    .union(lip)
    .union(rear_brace)
    .union(spine_strut_bottom)
    .union(spine_strut_main)
    .union(brace_to_base)
)

# Final check: The spine/struts are thin (4mm-5mm), base is 3mm, total volume will be low.
# Volume estimation: Base(90*50*3=13500) + Seat(15*30*4=1800) + Lip(15*30*4=1800) 
# + Brace(5*30*40=6000) + Struts(~15000) < 48000 mm^3.