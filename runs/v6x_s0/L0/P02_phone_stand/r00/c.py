import cadquery as cq
import math

# Constants and Phone Geometry
angle_deg = 65
angle_rad = math.radians(angle_deg)

# Design Parameters
base_w = 60.0
base_d = 50.0
thickness = 4.0

# 1. Base Plate (z: 0 to 4)
base = cq.Workplane("XY").box(base_w, base_d, thickness).translate((0, 0, thickness/2))

# 2. Main Support Spine
# We create a very long spine that starts from the center of the base and tilts back.
# By starting it at (0,0,0) and making it long, we ensure it hits the base.
spine_height = 150.0
spine_width = 25.0

long_spine = (
    cq.Workplane("XY")
    .box(thickness, spine_width, spine_height)
    .rotate((0, 0, 0), (0, 1, 0), -angle_deg)
    # Translate so the bottom of the tilted box is at or below z=4 and overlaps base center
    .translate((0, 0, 5)) 
)

# 3. Lip & Seat (R5)
# Requirement: a in [-4, 0] (seat), [0, 8] (lip). b in [9, 13].
# We'll create a vertical post that connects the base to the lip/seat.
lip_seat = cq.Workplane("XY").box(15, 20, thickness).translate((4, 11, 8))

# Connecting post for the Lip (from z=4 up to z=8)
lip_post = cq.Workplane("XY").box(5, 5, 10).translate((4, 11, 4))

# 4. Rear Brace (R4)
# Requirement: a ~ 100, b in [-2, 0].
rear_brace = cq.Workplane("XY").box(thickness, 15, 40).translate((-42, -1, 85))

# Connecting rod for the Rear Brace to reach the tilted spine.
# We need to find where the spine is at z=60-100 and bridge the gap.
# The spine center is (0,0,5) + rotation. 
# Let's just make a very large connecting block that bridges from the base/spine area up to the brace.
brace_connector = (
    cq.Workplane("XY")
    .box(40, 10, 80)
    .translate((-25, -5, 40)) # This spans z: 0 to 80 and x: -45 to -5
)

# To ensure the brace_connector actually hits the spine, we'll make it wider/longer.
brace_connector = (
    cq.Workplane("XY")
    .box(60, 15, 100)
    .translate((-35, -7, 50)) # Spans z: 0 to 100 and x: -65 to -5
)

# Combine all parts
# The long_spine starts at (0,0,5), so it is connected to the base.
# The lip_post connects the lip to the base.
# The brace_connector spans from z=0 up to 100, connecting the base/spine area to the rear_brace.
result = (
    base
    .union(long_spine)
    .union(lip_seat)
    .union(lip_post)
    .union(rear_brace)
    .union(brace_connector)
)