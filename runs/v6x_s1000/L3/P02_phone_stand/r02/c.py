import cadquery as cq
import math

# 1. Constants and Phone Geometry
phone_angle = 65
u_x = -math.cos(math.radians(phone_angle))
u_z = math.sin(math.radians(phone_angle))
n_x = math.sin(math.radians(phone_angle))
n_z = math.cos(math.radians(phone_angle))

# 2. Design Dimensions (from Design Document)
base_w = 90.0  # x direction extent: -65 to 25
base_d = 80.0  # y direction extent: -40 to 40
base_thickness = 5.0
rib_thickness = 6.0
rib_width = 30.0 # width in Y direction for the spine

# 3. Base Plate (R2)
# x range [-65, 25], y range [-40, 40], z range [0, 5]
stand_base = cq.Workplane("XY").box(base_w, base_d, base_thickness).translate((-20, 0, base_thickness/2))

# 4. Continuous Spine Construction (R1, R4, R5)
# To ensure connectivity, we must make sure the spine overlaps with the base plate.
# The previous error showed solid 2 starts at z=5.5 while solid 1 ends at z=5.0.
# We will extend the spine downwards to overlap the base.

spine_length = 130 # Increased length to ensure it reaches down
spine_angle = math.radians(phone_angle)

# Create a box rotated to match the phone angle
# We translate it so that its bottom end penetrates the base plate (z < 5)
spine = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_width, spine_length)
    .rotate((0, 0, 0), (0, 1, 0), -phone_angle)
    # The translation is adjusted to ensure the spine intersects the base plate significantly.
    # We target a point near the seat/lip area and ensure it goes through z=5.
    .translate((-35, 0, 45)) 
)

# A. Seat & Lip (R5)
seat_pos = (0, 0, 8) + (-2 * u_x, 0, -1 * u_z)
seat = cq.Workplane("XY").box(rib_thickness, rib_width, 10).translate((seat_pos[0], 0, seat_pos[2]))

lip_pos = (0, 0, 8) + (4 * u_x, 0, 4 * u_z) + (10 * n_x, 0, 10 * n_z)
lip = cq.Workplane("XY").box(rib_thickness, rib_width, 10).translate((lip_pos[0], 0, lip_pos[2]))

# B. Back Support (R4)
back_a = 100.0
back_pos = (0, 0, 8) + (back_a * u_x - 1.5 * n_x, 0, back_a * u_z - 1.5 * n_z)
# Ensure back support overlaps with the spine
back_support = cq.Workplane("XY").box(rib_thickness, rib_width, 60).translate((back_pos[0], 0, back_pos[2] + 30))

# C. Connector to ensure base and spine are one solid
# We add a vertical pillar from the base up into the spine area if needed, 
# but adjusting the spine translation is more robust.
connector = cq.Workplane("XY").box(rib_thickness, rib_width, 20).translate((-35, 0, 10))

# Final Assembly: Union all parts into one single solid (R1)
result = (
    stand_base
    .union(spine)
    .union(seat)
    .union(lip)
    .union(back_support)
    .union(connector)
)