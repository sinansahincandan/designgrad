import cadquery as cq

# Parameters based on Design Document and Feedback
spine_x_end = 15.0
spine_width = 20.0  # y range [-10, 10]
spine_height = 110.0 # z range [0, 110]

arm_start_x = 15.0
arm_end_x = 160.0
arm_thickness = 8.0  # z from 102 to 110
arm_z_center = 106.0 # (110 + 102) / 2
arm_width_at_spine = 20.0
arm_width_at_tip = 10.0

screw_dia = 5.5
hole_z_positions = [20.0, 60.0]
clearance_size = 8.0 # 8x8mm box for screwdriver access (R3)
clearance_width_y = 21.0 # Slightly wider than spine to ensure clean cut

# 1. Create the Spine
spine = cq.Workplane("XY").box(spine_x_end, spine_width, spine_height, centered=(False, False, False))

# 2. Create the Tapered Arm using Loft
# We create two profiles on YZ planes at x=15 and x=160
arm = (
    cq.Workplane("YZ")
    .workplane(offset=arm_start_x)
    .center(0, arm_z_center)
    .rect(arm_width_at_spine, arm_thickness)
    .workplane(offset=arm_end_x - arm_start_x)
    .center(0, 0)
    .rect(arm_width_at_tip, arm_thickness)
    .loft(ruled=True)
)

# 3. Combine Spine and Arm
bracket = spine.union(arm)

# 4. Subtract Screw Holes (R3) and Screwdriver Clearance
# We iterate through the hole positions to perform subtractions on the main bracket object
for z_pos in hole_z_positions:
    # Create the cylindrical screw hole (axis along X)
    # Using a cylinder centered at (y=0, z=z_pos) extending through the whole part
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=-1) # Start slightly before x=0 to ensure clean cut
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 2)
    )
    bracket = bracket.cut(hole)

    # Create the screwdriver clearance slot (R3)
    # Rectangular prism centered at (y=0, z=z_pos), x >= 10
    # The feedback suggests a box of 8x8mm to ensure no material within 4mm of axis
    slot = (
        cq.Workplane("XZ")
        .workplane(offset=10) # Start at x=10 as per R3
        .center(0, z_pos)
        .rect(arm_end_x - 10 + 1, clearance_size) # Length covers the rest of the arm
        .extrude(clearance_width_y, both=True) # Extrude along Y axis
    )
    bracket = bracket.cut(slot)

# Final result assignment
result = bracket