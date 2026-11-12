import cadquery as cq

# Parameters based on Design Document and Feedback
width = 30.0          # Y-dimension (-15 to 15)
spine_x = 15.0        # Thickness of the wall part
height_wall = 110.0   # Z-dimension (0 to 110)
arm_length = 160.0    # Total length along X
thickness_arm = 15.0  # Thickness of the arm in Z direction
screw_dia = 5.5       # Diameter of screw holes
hole_z_coords = [20.0, 60.0]

# 1. Create the main L-shape body
# Vertical spine: x from 0 to 15, y from -15 to 15, z from 0 to 110
spine = (
    cq.Workplane("XY")
    .box(spine_x, width, height_wall, centered=(False, False, False))
)

# Horizontal arm: x from 15 to 160, y from -15 to 15, z from (110-thickness) to 110
# To ensure top surface is exactly at z=110 and no part is above for x >= 8
arm = (
    cq.Workplane("XY")
    .box(arm_length - spine_x, width, thickness_arm, centered=(False, False, False))
    .translate((spine_x, 0, height_wall - thickness_arm))
)

# Combine spine and arm into one solid
bracket = spine.union(arm)

# 2. Subtract Screw Holes (R3)
# Holes must be along X-axis, centered at y=0, z=hole_z
for z_pos in hole_z_coords:
    # Create a cylinder along the X axis using YZ plane
    # We use a large enough length to ensure it cuts through the entire part
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(0, z_pos) # y=0 is center of width, z=z_pos
        .circle(screw_dia / 2)
        .extrude(arm_length + 10)
    )
    bracket = bracket.cut(hole)

# 3. Subtract Screwdriver Clearance (R3)
# Rectangular cutouts: 8mm wide (Y), 8mm high (Z), starting at x=10
for z_pos in hole_z_coords:
    # The feedback suggests a box centered at x=17.5, but the requirement is 
    # "no material within 4mm of axis for x >= 10".
    # We'll create a box that starts at x=10 and extends to the front face (x=160).
    # Dimensions: width(Y)=8, height(Z)=8.
    clearance = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(0, 0) # We will use translate to position it precisely
        .box(arm_length - 10, 8, 8, centered=(False, True, True)) 
    )
    # Translate the box so its left edge is at x=10
    clearance = clearance.translate((10, 0, 0))
    bracket = bracket.cut(clearance)

# Final result assignment
result = bracket