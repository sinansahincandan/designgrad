import cadquery as cq

# Parameters based on Design Document and Feedback Optimization
width = 15.0          # Reduced from 20.0 to satisfy R7 (Mass <= 90g)
height_wall = 110.0
thickness_arm = 10.0  # The top plate thickness (z=100 to z=110)
length_arm_ext = 160.0 # Total x-extent
spine_x_end = 15.0
screw_dia = 5.5

# 1. Create the main components
# Vertical spine: x from 0 to 15, y centered at 0 (-7.5 to 7.5), z from 0 to 110
spine = (
    cq.Workplane("XY")
    .box(spine_x_end, width, height_wall, centered=(False, False, False))
    .translate((0, -width/2, 0))
)

# Horizontal arm: x from 15 to 160, y centered at 0, z from 100 to 110 (R4 top surface)
arm = (
    cq.Workplane("XY")
    .box(length_arm_ext - spine_x_end, width, thickness_arm, centered=(False, False, False))
    .translate((spine_x_end, -width/2, height_wall - thickness_arm))
)

# Support Block: x from 140 to 150, y centered at 0, z from 0 to 100 (R4 solidity requirement)
support = (
    cq.Workplane("XY")
    .box(10, width, height_wall - thickness_arm, centered=(False, False, False))
    .translate((140, -width/2, 0))
)

# Combine all solid parts
bracket = spine.union(arm).union(support)

# 2. Subtract Screw Holes (R3)
# Holes are along X axis at y=0, z=20 and z=60. 
# We extrude through the whole part to ensure they pass through the spine.
hole_centers = [(20, 0), (60, 0)]
for z_pos, y_pos in hole_centers:
    bracket = bracket.cut(
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(0, y_pos)
        .circle(screw_dia / 2)
        .extrude(170) # Sufficiently long to clear the part
    )

# 3. Subtract Screwdriver Clearance (R3)
# Requirement: No material within 4mm of hole axis for x >= 10.
# Feedback Action: Use a rectangular cutout from x=10 to x=15 centered on hole axes.
for z_pos, y_pos in hole_centers:
    clearance = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(12.5, y_pos) # Center of the x=[10, 15] range
        .box(5, width + 2, 20, centered=(True, True, True)) 
    )
    bracket = bracket.cut(clearance)

# Final result assignment
result = bracket