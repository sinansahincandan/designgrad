import cadquery as cq

# Parameters based on Design Document
width = 20.0
height_wall = 110.0
thickness_arm = 10.0
length_arm = 160.0 # Total x-extent is 15 + (160-15) = 160
screw_dia = 5.5

# 1. Create the main L-shape body
# Vertical spine: x from 0 to 15, y centered at 0 (-10 to 10), z from 0 to 110
spine = (
    cq.Workplane("XY")
    .box(15, width, height_wall, centered=(False, False, False))
    .translate((0, -width/2, 0))
)

# Horizontal arm: x from 15 to 160, y centered at 0 (-10 to 10), z from 100 to 110
arm = (
    cq.Workplane("XY")
    .box(length_arm - 15, width, thickness_arm, centered=(False, False, False))
    .translate((15, -width/2, height_wall - thickness_arm))
)

# Combine spine and arm
bracket = spine.union(arm)

# 2. Subtract Screw Holes (R3)
# Holes are along X axis at y=0, z=20 and z=60
hole_centers = [(20, 0), (60, 0)]
for z_pos, y_pos in hole_centers:
    bracket = bracket.cut(
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(0, y_pos)
        .circle(screw_dia / 2)
        .extrude(170) # Extrude through the whole part
    )

# 3. Subtract Screwdriver Clearance (R3)
# No material within 4mm of hole axis for x >= 10.
# We use a box centered at x=15 to cover the required clearance area.
for z_pos, y_pos in hole_centers:
    clearance = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(15, y_pos) # Center at x=15 to cover the region around x=10
        .box(20, width + 2, 20, centered=(True, True, True)) 
    )
    bracket = bracket.cut(clearance)

# Final result assignment
result = bracket