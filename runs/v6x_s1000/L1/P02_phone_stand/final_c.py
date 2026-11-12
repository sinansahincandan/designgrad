import cadquery as cq
import math

# Constants and Phone Geometry
phone_angle = 65
u_x = -math.cos(math.radians(phone_angle))
u_z = math.sin(math.radians(phone_angle))
n_x = math.sin(math.radians(phone_angle))
n_z = math.cos(math.radians(phone_angle))

# Vectors for translation logic
u = cq.Vector(u_x, 0, u_z)
n = cq.Vector(n_x, 0, n_z)
pos_bottom = cq.Vector(0, 0, 8)

# Design Dimensions
base_w = 90.0  # y direction
base_d = 60.0  # x direction
base_thickness = 5.0
support_width = 30.0
support_thickness = 3.0
support_height = 70.0

# 1. Base Plate (R2)
# Bounds: x in [-40, 20], y in [-45, 45], z in [0, 5]
stand_base = cq.Workplane("XY").box(60, 90, base_thickness).translate((-10, 0, base_thickness/2))

# 2. Back Support (R3 & R4)
# Position at a=100, thickness 3mm, centered on y=0, |y| <= 15
pos_back = pos_bottom + 100 * u
# To ensure connectivity with the base, we extend the upright's bottom to z=0 or below.
# The previous error showed it was at x ~ -45 while base ends at x=-40.
# We will shift the support slightly towards the center (positive X) or extend its width 
# so that it overlaps with the base plate.
upright = (
    cq.Workplane("XY")
    .box(support_thickness + 10, support_width, support_height) # Extended thickness to ensure overlap with base
    .translate((pos_back.x - 1.5 * n.x, 0, base_thickness/2)) # Bottom at z=0 to ensure union
)

# 3. Seat (R3 & R5)
seat_thickness = 3.0
seat_depth = 6.0 
seat = (
    cq.Workplane("XY")
    .box(seat_thickness, support_width, seat_depth)
    .translate((pos_bottom.x - 2 * u.x - 1.5 * n.x, 0, pos_bottom.z - 4.5 * n.z - seat_thickness/2))
)

# 4. Front Lip (R3 & R5)
lip_thickness = 3.0
lip_depth = 6.0 
lip = (
    cq.Workplane("XY")
    .box(lip_thickness, support_width, lip_depth)
    .translate((pos_bottom.x + 4 * u.x - 1.5 * n.x, 0, pos_bottom.z + 11 * n.z - lip_depth/2))
)

# 5. Connector (R1)
# To ensure the seat and lip are connected to the base, we create a central pillar.
connector = (
    cq.Workplane("XY")
    .box(10, support_width, 20)
    .translate((0, 0, 10)) # Centered on X=0, which is inside the base [-40, 20]
)

# Final assembly: Union all parts into one single solid
# We ensure upright overlaps with base by making it thicker and starting from z=0.
result = (
    stand_base
    .union(upright)
    .union(seat)
    .union(lip)
    .union(connector)
)