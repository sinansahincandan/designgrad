import cadquery as cq

# Parameters
spine_width = 15.0
spine_height = 110.0
spine_y_range = 30.0  # Total width (-15 to 15)

arm_start_x = 15.0
arm_end_x = 160.0
arm_top_z = 110.0
arm_start_thickness = 10.0
arm_end_thickness = 4.0
arm_width = 30.0

screw_dia = 5.5
hole_centers_z = [20, 60]
clearance_size = 10.0
clearance_x_start = 10.0
clearance_x_end = 25.0

# 1. Create the Wall Spine
# x: 0 to 15, y: -15 to 15, z: 0 to 110
spine = cq.Workplane("XY").box(spine_width, spine_y_range, spine_height, centered=(False, False, False))

# 2. Create the Tapered Shelf Arm
# To avoid lofting errors with complex Workplane objects, we use the standard pattern:
# Define two wires on different planes and loft them.
# We'll create a single workplane and add two separate sketches (wires) to it.

arm = (
    cq.Workplane("XY")
    # Profile 1 at x=15
    .workplane(offset=arm_start_x)
    .rect(arm_width, arm_start_thickness)
    .translate((0, 0, arm_top_z - arm_start_thickness/2))
    # Profile 2 at x=160
    .workplane(offset=arm_end_x - arm_start_x) # offset is relative to current workplane
    .rect(arm_width, arm_end_thickness)
    .translate((0, 0, arm_top_z - arm_end_thickness/2))
    .loft()
)

# Combine spine and arm
# Note: The lofted arm is created relative to the workplane offset. 
# We need to ensure it's positioned correctly in global space.
# Since we used .workplane(offset=arm_start_x), the first profile is at x=15.
# The second profile was offset by (arm_end_x - arm_start_x) from that, so it is at x=160.
bracket = spine.union(arm)

# 3. Subtract Screw Holes and Clearance
for z_pos in hole_centers_z:
    # Cylindrical holes along X axis (drilled through the spine)
    # The spine is from x=0 to x=15. We drill a cylinder centered at y=0, z=z_pos.
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=-1) # Start slightly before wall to ensure clean cut
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(spine_width + 5) 
    )
    bracket = bracket.cut(hole)

    # Rectangular clearance cutouts: 10x10 centered at (y=0, z=z_pos), x from 10 to 25
    # Center of box in X is (10+25)/2 = 17.5. Half-length is 7.5.
    # Center of box in Y is 0. Half-width is 5.
    # Center of box in Z is z_pos. Half-height is 5.
    clearance_box = (
        cq.Workplane("XY")
        .box(clearance_x_end - clearance_x_start, clearance_size, clearance_size)
        .translate(((clearance_x_start + clearance_x_end)/2, 0, z_pos))
    )
    bracket = bracket.cut(clearance_box)

# Final result assignment
result = bracket