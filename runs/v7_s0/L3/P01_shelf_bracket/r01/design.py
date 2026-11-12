import cadquery as cq

# Parameters based on Design Document and Feedback
spine_x_end = 15.0
spine_width = 20.0  # y range [-10, 10]
spine_height = 110.0 # z range [0, 110]

arm_start_x = 15.0
arm_end_x = 160.0
arm_thickness = 8.0  # z from 102 to 110
arm_width_at_spine = 20.0
arm_width_at_tip = 10.0

screw_dia = 5.5
hole_z_positions = [20.0, 60.0]
clearance_radius = 4.0 # No material within 4mm of hole axis for x >= 10
clearance_width_y = 15.0 # Width of the screwdriver access slot

# 1. Create the Spine
spine = cq.Workplane("XY").box(spine_x_end, spine_width, spine_height, centered=(False, False, False))

# 2. Create the Tapered Arm
# To avoid loft errors and union issues with non-solids, we build the arm using a series of extrusions or a single tapered extrusion if possible.
# Since CadQuery's loft can be finicky with Workplane objects containing only faces, 
# we will create the arm by creating two rectangles on YZ planes and then using the loft method correctly.

# We use a different approach: Create profiles as wires/faces and loft them.
# In CadQuery, to loft multiple disconnected workplanes, we can't easily union them if they aren't solids.
# Instead, let's create one workplane and add two sketches (rectangles) to it.

arm = (
    cq.Workplane("YZ")
    .workplane(offset=arm_start_x)
    .center(0, 106)
    .rect(arm_width_at_spine, arm_thickness)
    .workplane(offset=arm_end_x - arm_start_x) # Move to the second plane relative to first
    .center(0, 0)
    .rect(arm_width_at_tip, arm_thickness)
    .loft(ruled=True)
)

# 3. Combine Spine and Arm
# Ensure they overlap slightly or touch perfectly. Spine ends at x=15, Arm starts at x=15.
bracket = spine.union(arm)

# 4. Subtract Screw Holes (R3)
for z_pos in hole_z_positions:
    # Hole through the part using a cylinder oriented along X.
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 1)
    )
    bracket = bracket.cut(hole)

# 5. Subtract Screwdriver Clearance (R3)
for z_pos in hole_z_positions:
    # Create a box centered at y=0, z=z_pos, with x from 10 to arm_end_x.
    slot = (
        cq.Workplane("XZ")
        .workplane(offset=10)
        .center(0, z_pos)
        .rect(arm_end_x - 10, clearance_radius * 2.5) # x-length and z-height
        .extrude(clearance_width_y, both=True) # extrude along Y axis
    )
    bracket = bracket.cut(slot)

# Final result assignment
result = bracket