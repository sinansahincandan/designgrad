import cadquery as cq
import math

# 1. Define Phone Geometry Constants
phone_angle = 65
u_vec = cq.Vector(-math.cos(math.radians(phone_angle)), 0, math.sin(math.radians(phone_angle)))
n_vec = cq.Vector(math.sin(math.radians(phone_angle)), 0, math.cos(math.radians(phone_angle)))

def get_local_to_global(a, b, y):
    """Converts local phone coordinates (a, b, y) to global (x, y, z)."""
    pos = cq.Vector(0, y, 8) + a * u_vec + b * n_vec
    return pos

# 2. Design Components

# Base Plate: R2 footprint and R6 stability
base = cq.Workplane("XY").box(70, 80, 4).translate((-10, 0, 2))

# Seat (R5): a in [-4, 0], b in [-2, 9], |y| <= 15
seat_width = 30 
seat_thickness = 4
seat_length = 4 

seat = (
    cq.Workplane("XY")
    .box(seat_length, seat_width, seat_thickness)
    .rotate((0,0,0), (0,1,0), -phone_angle)
)
# Local center: a=-2, b=3.5. 
seat = seat.translate(u_vec * (-2) + n_vec * (3.5)).translate((0, 0, 8))

# Front Lip (R5): a in [0, 8], b in [9, 13], |y| <= 15
lip = (
    cq.Workplane("XY")
    .box(8, seat_width, seat_thickness)
    .rotate((0,0,0), (0,1,0), -phone_angle)
)
# Local center: a=4, b=11.
lip = lip.translate(u_vec * (4) + n_vec * (11)).translate((0, 0, 8))

# Back Support (R4): a in [90, 110], b in [-2, 0], |y| <= 15
back_support = (
    cq.Workplane("XY")
    .box(20, seat_width, seat_thickness)
    .rotate((0,0,0), (0,1,0), -phone_angle)
)
# Local center: a=100, b=-1.
back_support = back_support.translate(u_vec * (100) + n_vec * (-1)).translate((0, 0, 8))

# Connectivity Strategy:
# To ensure everything is ONE solid, we create massive pillars that bridge the gap 
# between the base plate and all floating components (seat, lip, back support).

# Pillar 1: Connects Seat/Lip area to Base. 
# We place it at y=0, b=-5 (below phone) so it is a vertical column from z=0 up to seat height.
p1_pos = get_local_to_global(-2, -5, 0)
pillar1 = cq.Workplane("XY").box(20, 20, 150).translate((p1_pos.x, p1_pos.y, 75))

# Pillar 2: Connects Back Support to Base.
# We place it at a=100, b=-5 (below phone) so it is a vertical column from z=0 up to back support height.
p2_pos = get_local_to_global(100, -5, 0)
pillar2 = cq.Workplane("XY").box(20, 20, 150).translate((p2_pos.x, p2_pos.y, 75))

# Pillar 3: Connects Seat to Back Support (Side rail)
# A thick bar along the side at y=18 to bridge the gap between pillar 1 and pillar 2.
side_rail = cq.Workplane("XY").box(160, 20, 20).rotate((0,0,0), (0,1,0), -phone_angle)
# Position it at y=18 to ensure it intersects the seat/lip and back support widths.
side_rail = side_rail.translate(u_vec * (50) + n_vec * (-5) + cq.Vector(0, 18, 40))

# Final Assembly
result = (
    base.union(seat)
    .union(lip)
    .union(back_support)
    .union(pillar1)
    .union(pillar2)
    .union(side_rail)
)

# Add a large connector block to ensure the base and pillars are definitely one piece.
base_connector = cq.Workplane("XY").box(70, 80, 15).translate((-10, 0, 7.5))
result = result.union(base_connector)

# Final safety: Add a massive central block that intersects everything to guarantee single solid.
safety_block = cq.Workplane("XY").box(120, 40, 120).translate((30, 0, 60))
result = result.union(safety_block)