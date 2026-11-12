import cadquery as cq

# Parameters based on Design Document
width = 20.0
height_wall = 110.0
thickness_arm = 10.0
length_arm_start = 15.0
total_x_extent = 160.0
screw_dia = 5.5

# 1. Create the main L-shape body
# Vertical spine: x from 0 to 15, y centered at 0 (-10 to 10), z from 0 to 110
spine = (
    cq.Workplane("XY")
    .box(length_arm_start, width, height_wall, centered=(False, False, False))
)

# Horizontal arm: x from 15 to 160, y centered at 0 (-10 to 10), z from 100 to 110
arm = (
    cq.Workplane("XY")
    .box(total_x_extent - length_arm_start, width, thickness_arm, centered=(False, False, False))
    .translate((length_arm_start, 0, height_wall - thickness_arm))
)

# Combine spine and arm to ensure a single solid (R1)
bracket = spine.union(arm)

# 2. Subtract Screw Holes (R3)
# Requirement: Axis along X at (y=0, z=20) and (y=0, z=60).
hole_centers = [(0, 20), (0, 60)] # (y, z)

for y_pos, z_pos in hole_centers:
    # Create a cylinder on the YZ plane. 
    # To position it at x=80, we translate the workplane or the object.
    hole = (
        cq.Workplane("YZ")
        .center(y_pos, z_pos)
        .cylinder(total_x_extent + 20, screw_dia / 2)
        .translate((80, 0, 0))
    )
    bracket = bracket.cut(hole)

# 3. Subtract Screwdriver Clearance (R3)
for y_pos, z_pos in hole_centers:
    # Clearance box: centered on (y=0, z=z_pos), starting at x=10 and extending to end of part.
    # Dimensions: length = 150 (from x=10 to 160), width = 10 (y), height = 20 (z).
    # We use a box on the XY plane then translate it.
    clearance = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(85, y_pos) # Center at x=85 to cover [10, 160]
        .box(150, 10, 20, centered=(True, True, False))
    )
    bracket = bracket.cut(clearance)

# Final result assignment
result = bracket