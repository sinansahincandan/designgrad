import cadquery as cq

# Parameters based on Design Document and Feedback
spine_x_limit = 8.0
spine_width = 24.0  # y from -12 to 12
spine_height = 110.0
arm_start_x = spine_x_limit
arm_end_x = 160.0
arm_width = 24.0    # y from -12 to 12
top_z = 110.0

thickness_arm_start = 10.0  # at x=8 (z from 100 to 110)
thickness_arm_end = 6.0     # at x=160 (z from 104 to 110)

screw_dia = 5.5
clearance_radius = 4.0
hole_centers_z = [20, 60]

# 1. Create the Spine
# The spine is a block from x=0 to 8, y=-12 to 12, z=0 to 110
spine = (
    cq.Workplane("XY")
    .box(spine_x_limit, spine_width, spine_height, centered=(False, False, False))
)

# 2. Create the Tapered Arm
# To ensure a single solid via union, we extend the arm slightly into the spine (x from 7 to 160).
arm_start_overlap = 1.0 # overlap with spine
arm_profile = (
    cq.Workplane("XZ")
    .moveTo(spine_x_limit - arm_start_overlap, top_z)
    .lineTo(arm_end_x, top_z)
    .lineTo(arm_end_x, top_z - thickness_arm_end)
    .lineTo(spine_x_limit - arm_start_overlap, top_z - thickness_arm_start)
    .close()
)

# Extrude the profile along Y to create the arm. 
# The spine is y: -12 to 12.
# In XZ plane, extrusion goes along +Y. To get y from -12 to 12, we extrude 24 and translate by -12.
arm = (
    arm_profile.extrude(arm_width)
    .translate((0, -arm_width/2, 0))
)

# Combine spine and arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3) and Screwdriver Clearance
for z_pos in hole_centers_z:
    # The screw hole must penetrate the entire part along X axis (0 to 160)
    # We use a cylinder on YZ plane centered at (y=0, z=z_pos)
    screw_hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 1) # Ensure it goes through the whole part
    )
    bracket = bracket.cut(screw_hole)

    # Screwdriver clearance (R3): radius 4mm for x >= 10
    clearance_cyl = (
        cq.Workplane("YZ")
        .workplane(offset=10) # Start at x=10
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(arm_end_x + 1) 
    )
    bracket = bracket.cut(clearance_cyl)

# Final result assignment
result = bracket