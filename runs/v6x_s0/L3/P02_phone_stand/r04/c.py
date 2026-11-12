import cadquery as cq
import math

# Constants for Phone Geometry
angle_deg = 65
angle_rad = math.radians(angle_deg)
cos_a = math.cos(angle_rad)
sin_a = math.sin(angle_rad)

def get_phone_pos(a, b, y):
    """Returns the (x, y, z) position for a given phone coordinate."""
    # u = (-cos65, 0, sin65), n = (sin65, 0, cos65)
    x = 0 + a * (-cos_a) + b * sin_a
    y_coord = y
    z = 8 + a * sin_a + b * cos_a
    return x, y_coord, z

def get_phone_volume():
    """Generates the volume of the phone to be used for boolean subtraction."""
    com_x = 80 * (-cos_a) + 4.5 * sin_a
    com_y = 0
    com_z = 8 + 80 * sin_a + 4.5 * cos_a
    phone = cq.Workplane("XY").box(160, 75, 9).rotate((0,0,0), (0,1,0), 180 - angle_deg).translate((com_x, com_y, com_z))
    return phone

# 1. Base Plate
base_w = 80.0
base_d = 80.0
base_thickness = 3.0
base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((0, 0, base_thickness/2))

# 2. Components (Intended volumes)
# Seat: a in [-4, 0], b in [0, 9], |y| <= 15
s_a, s_b = -2, 4.5
sx, sy, sz = get_phone_pos(s_a, s_b, 0)
seat_vol = cq.Workplane("XY").box(30, 40, 20).translate((sx, sy, sz))

# Lip: a in [0, 8], b in [9, 13], |y| <= 15
l_a, l_b = 4, 11
lx, ly, lz = get_phone_pos(l_a, l_b, 0)
lip_vol = cq.Workplane("XY").box(30, 40, 20).translate((lx, ly, lz))

# Rear Brace: a in [90, 110], b in [-2, 0], |y| <= 15
r_a, r_b = 100, -1
rx, ry, rz = get_phone_pos(r_a, r_b, 0)
brace_vol = cq.Workplane("XY").box(40, 40, 80).translate((rx, ry, rz))

# Spine: Connects seat to brace and down to base
spine_vol = cq.Workplane("XY").box(30, 40, 150).translate((sx + (rx-sx)/2, sy, sz + (rz-sz)/2))
angle_spine = math.degrees(math.atan2(rz - sz, rx - sx))
spine_vol = spine_vol.rotate((sx + (rx-sx)/2, sy, sz + (rz-sz)/2), (0, 1, 0), -angle_spine)

# Connection to Base: Ensure the spine/brace structure reaches down into the base plate volume
base_conn = cq.Workplane("XY").box(50, 50, rz + 60).translate((rx, ry, (rz+60)/2))

# Central Support Pillar: To ensure everything is one single solid and connected to base
pillar = cq.Workplane("XY").box(40, 40, 150).translate((sx, sy, 75))

# 3. Subtract Phone Volume (R3)
v_phone = get_phone_volume()

seat = seat_vol.cut(v_phone)
lip = lip_vol.cut(v_phone)
brace = brace_vol.cut(v_phone)
spine = spine_vol.cut(v_phone).union(base_conn.cut(v_phone))

# 4. Final Union (R1)
# We union everything including the pillar to guarantee a single manifold solid.
result = base.union(seat).union(lip).union(brace).union(spine).union(pillar)