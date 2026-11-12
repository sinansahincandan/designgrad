import cadquery as cq

# Parameters based on Design Document
spine_x_start = 0.0
spine_x_end = 15.0
spine_y_half_width = 7.5  # Total width 15mm
spine_z_height = 110.0

arm_x_start = 15.0
arm_x_end = 150.0
arm_z_top = 110.0
arm_thickness = 10.0
arm_z_bottom = arm_z_top - arm_thickness

# Tapered width parameters (Y-dimension)
y_width_at_spine = 15.0  # at x=15
y_width_at_tip = 8.0     # at x=150

screw_dia = 5.5
clearance_radius = 4.1
screw_z_positions = [20, 60]

# 1. Create the Spine
# Positioned from x=0 to 15, y=-7.5 to 7.5, z=0 to 110
spine = (
    cq.Workplane("XY")
    .box(spine_x_end - spine_x_start, spine_y_half_width * 2, spine_z_height, centered=(False, True, False))
)

# 2. Create the Tapered Arm using Loft
# To ensure connection and correct positioning:
# We define profiles on planes perpendicular to X (YZ planes).
# Profile at x = 15
p1 = cq.Workplane("YZ").workplane(offset=arm_x_start).rect(y_width_at_spine, arm_thickness, centered=(True, True))
# Profile at x = 150
p2 = cq.Workplane("YZ").workplane(offset=arm_x_end).rect(y_width_at_tip, arm_thickness, centered=(True, True))

# Lofting between the two profiles. 
# We must ensure the Z-center of these rectangles is at (arm_z_top - arm_thickness/2)
# so that the top surface is exactly at z=110.
arm = (
    cq.Workplane("YZ")
    .workplane(offset=arm_x_start)
    .rect(y_width_at_spine, arm_thickness)
    .workplane(offset=arm_x_end - arm_x_start)
    .rect(y_width_at_tip, arm_thickness)
    .loft()
)

# The lofted object is currently centered at Z=0 because rect() was centered on the workplane.
# We need to move it so its top surface (z = thickness/2) is at z=110.
# Target center Z = 110 - (10/2) = 105.
arm = arm.translate((0, 0, 105))

# To ensure a robust union, we extend the arm slightly into the spine or vice versa.
# The spine ends at x=15 and the arm starts at x=15. They touch but might not overlap perfectly due to precision.
# We'll extend the arm start back to x=14.
arm = arm.translate((-1, 0, 0))

# Combine spine and arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes and Clearance
for z_pos in screw_z_positions:
    # Screw Hole (Diameter 5.5mm)
    # Axis along X, centered at y=0, z=z_pos
    hole = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_x_end + 20) # Extends through the whole part
    )
    bracket = bracket.cut(hole)

    # Screwdriver Clearance (Radius 4.1mm)
    # No material within 4mm for x >= 10
    clearance = (
        cq.Workplane("YZ")
        .center(10, z_pos)
        .circle(clearance_radius)
        .extrude(arm_x_end + 20) # Extends from x=10 to the end
    )
    bracket = bracket.cut(clearance)

# Final result assignment
result = bracket