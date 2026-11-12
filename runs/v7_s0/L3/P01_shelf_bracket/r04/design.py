import cadquery as cq

# Parameters based on Design Document and Feedback
spine_x_end = 15.0
spine_width = 20.0  # y range [-10, 10]
spine_height = 110.0 # z range [0, 110]

arm_start_x = 15.0
arm_end_x = 160.0
arm_thickness_z = 8.0  # z from 102 to 110
arm_width_at_spine = 20.0
arm_width_at_tip = 10.0

screw_dia = 5.5
hole_z_positions = [20.0, 60.0]
clearance_size = 8.0 # 8mm x 8mm square for screwdriver access

# 1. Create the Spine (centered on Y=0)
# Ensure top surface is exactly at z=110 by using centered=(False, False, False)
spine = (
    cq.Workplane("XY")
    .box(spine_x_end, spine_width, spine_height, centered=(False, False, False))
    .translate((0, -spine_width/2, 0))
)

# 2. Create the Tapered Arm (centered on Y=0)
# We use a loft on the YZ plane to create an arm extending along X.
# The profile is defined in YZ: width is Y, height is Z.
# To keep top surface at z=110 and thickness 8mm, we center the rectangle at z=106.
arm = (
    cq.Workplane("YZ")
    .workplane(offset=arm_start_x)
    .center(0, 106) # Center of Z-thickness [102, 110]
    .rect(arm_width_at_spine, arm_thickness_z) # rect(width/Y, height/Z)
    .workplane(offset=arm_end_x - arm_start_x)
    .center(0, 106)
    .rect(arm_width_at_tip, arm_thickness_z)
    .loft(ruled=True)
)

# 3. Combine Spine and Arm
bracket = spine.union(arm)

# 4. Subtract Screw Holes and Clearance Cutouts
for z_pos in hole_z_positions:
    # A. Cylindrical Hole (Diameter 5.5mm, axis along X)
    hole_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 10)
        .translate((-5, 0, 0)) # Ensure it passes through the whole part
    )
    bracket = bracket.cut(hole_cyl)

    # B. Screwdriver Clearance (8mm x 8mm square centered on hole axis)
    # Requirement: No material within 4mm of hole axis for x >= 10.
    slot_box = (
        cq.Workplane("XY")
        .box(arm_end_x + 20, clearance_size, clearance_size, centered=(False, False, False))
        .translate((10, -clearance_size/2, z_pos - clearance_size/2))
    )
    bracket = bracket.cut(slot_box)

result = bracket