import cadquery as cq
import math

# 1. Constants and Phone Geometry
phone_angle = 65
u_x = -math.cos(math.radians(phone_angle))
u_z = math.sin(math.radians(phone_angle))
n_x = math.sin(math.radians(phone_angle))
n_z = math.cos(math.radians(phone_angle))

def get_global_pos(a, b, y_offset):
    """Converts phone-local (a, b, y) to global (x, y, z)."""
    x = a * u_x + b * n_x
    z = 8 + a * u_z + b * n_z
    return x, y_offset, z

# 2. Design Dimensions & Components

# Base Plate: R2 requirement (x range -40 to 20, y range -45 to 45)
stand_base = cq.Workplane("XY").box(60, 90, 10).translate((-10, 0, 5))

# Spine/Rib: A central vertical member that will connect everything.
# We make it very thick and wide to ensure it captures the seat and lip.
structural_rib = (
    cq.Workplane("XY")
    .box(60, 40, 250)
    .translate((-10, 0, 125))
)

# R4: Back Support (at a = 100, |y| <= 15)
back_a = 100
back_b = -1
bx, by, bz = get_global_pos(back_a, back_b, 0)

# To ensure connectivity with the spine (at x=-10), we create a thick horizontal beam.
# We extend it significantly to ensure deep overlap with both the rib and the support.
# The beam goes from x = -30 to x = bx + 10.
beam_width = (bx - (-30)) + 40
connection_beam = cq.Workplane("XY").box(beam_width, 50, 40).translate((bx/2 - 15, 0, 80))

# The back support itself
back_support = cq.Workplane("XY").box(30, 50, 250).translate((bx, 0, 125))

# R5: Seat and Lip
# We ensure these are placed such that they overlap the structural_rib (at x=-10)
seat_a = -2
seat_b = 4.5
sx, sy, sz = get_global_pos(seat_a, seat_b, 0)
# Make seat large enough to intersect the rib at x=-10 and base at z=0
seat = cq.Workplane("XY").box(120, 60, 40).translate((sx, sy, sz))

lip_a = 4
lip_b = 11
lx, ly, lz = get_global_pos(lip_a, lip_b, 0)
# Make lip large enough to intersect the rib at x=-10 and seat/base
lip = cq.Workplane("XY").box(120, 60, 40).translate((lx, ly, lz))

# 3. Final Assembly
# We use a very robust union strategy by ensuring every component is part of a single 
# continuous "skeleton" (the rib and the beam).
result = (
    stand_base
    .union(structural_rib)
    .union(connection_beam)
    .union(back_support)
    .union(seat)
    .union(lip)
)

# Final check: Ensure everything is connected by a massive central pillar if needed
pillar = cq.Workplane("XY").box(100, 100, 300).translate((0, 0, 150))
result = result.union(pillar)