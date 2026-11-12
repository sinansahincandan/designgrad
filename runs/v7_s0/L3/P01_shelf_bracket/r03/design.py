import cadquery as cq

# Parameters based on Design Document
spine_x_end = 15.0
spine_width = 20.0  # y range [-10, 10]
spine_height = 110.0 # z range [0, 110]

arm_start_x = 14.0  # Overlap with spine for single solid
arm_end_x = 160.0
arm_thickness = 8.0  # z from 102 to 110
arm_width_at_spine = 20.0
arm_width_at_tip = 10.0

screw_dia = 5.5
hole_z_positions = [20.0, 60.0]
clearance_radius = 4.0 

# 1. Create the Spine (centered on Y=0)
# Box at absolute position: min corner at (x0, y0, z0). 
# To get x in [0, 15], y in [-10, 10], z in [0, 110]:
spine = cq.Workplane("XY").box(spine_x_end, spine_width, spine_height, centered=False).translate((0, -spine_width/2, 0))

# 2. Create the Tapered Arm (centered on Y=0)
# The previous error showed solid 2 was offset in Y because of how loft() handles planes.
# We will create the arm by extruding a tapered profile along X to ensure it stays centered at y=0.
# A more robust way for a tapered width is to use a series of slices or a loft on XY/XZ with careful placement.

# Let's define profiles on the YZ plane and extrude along X. 
# But since we want tapering in Y, we should use the XZ plane as the profile plane and extrude along Y? No.
# We will create the arm using a loft of two rectangles on the YZ plane (at x=14 and x=160) 
# but that's not right for an X-extending arm.

# Correct approach: Create profiles in the YZ plane at different X positions? No, CQ loft works on parallel planes.
# We will use the XZ plane (normal is Y). The 'height' of the profile is Z, and 'width' is X. 
# This doesn't work for an arm extending along X.

# Let's use the XY plane to create a tapered width in Y as we move along X.
# We can achieve this by creating a polygon/path or using loft on two planes perpendicular to X (YZ planes).
arm = (
    cq.Workplane("YZ")
    .workplane(offset=arm_start_x)
    .center(0, 106) # Center of thickness [102, 110] is 106
    .rect(arm_thickness, arm_width_at_spine) # rect(width, height) in YZ: width=Y, height=Z
    .workplane(offset=arm_end_x - arm_start_x)
    .center(0, 0)
    .rect(arm_thickness, arm_width_at_tip) # rect(width, height) in YZ: width=Y, height=Z
    .loft(ruled=True)
)
# In the YZ plane, 'rect' uses the first param for Y and second for Z. 
# The loft will then extend along X (the normal of YZ).
# This arm is centered at x=arm_start_x, y=0, z=106.

# 3. Combine Spine and Arm
bracket = spine.union(arm)

# 4. Subtract Screw Holes (R3)
for z_pos in hole_z_positions:
    # Hole: Cylinder along X axis, centered at y=0, z=z_pos
    # We use YZ plane to create a cylinder whose axis is the X-axis.
    hole_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos) 
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 10) # Extends along X axis
    )
    # The extrusion starts at x=0 (the origin of the YZ plane).
    bracket = bracket.cut(hole_cyl.translate((-5, 0, 0)))

    # 5. Subtract Screwdriver Clearance (R3)
    # Slot: x >= 10, centered at y=0, z=z_pos, width 8mm in Z direction.
    slot_box = (
        cq.Workplane("XY")
        .box(arm_end_x + 20, spine_width * 3, clearance_radius * 2, centered=False)
        .translate((10, -spine_width * 1.5, z_pos - clearance_radius))
    )
    bracket = bracket.cut(slot_box)

result = bracket