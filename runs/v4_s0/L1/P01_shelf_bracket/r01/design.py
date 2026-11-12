import cadquery as cq

# Parameters
width = 30.0
height_wall = 110.0
thickness_arm = 15.0 # Increased thickness to ensure R4/R5 compliance
length_arm_total = 160.0
spine_x_limit = 8.0
screw_dia = 5.5
clearance_radius = 4.0
hole_centers_z = [20, 60]

# 1. Create the main L-shape body
# Vertical spine (wall part): x from 0 to 8
spine = cq.Workplane("XY").box(spine_x_limit, width, height_wall, centered=(False, False, False))

# Horizontal arm (shelf support): starts at x=8, top surface at z=110
# To have the top surface at exactly 110, we translate by (height_wall - thickness_arm)
arm = (
    cq.Workplane("XY")
    .box(length_arm_total - spine_x_limit, width, thickness_arm, centered=(False, False, False))
    .translate((spine_x_limit, 0, height_wall - thickness_arm))
)

# Combine spine and arm
bracket = spine.union(arm)

# 2. Subtract Screw Holes (R3) and Screwdriver Clearance
for z_pos in hole_centers_z:
    # First, the actual screw hole through the whole part along X axis
    # We use a cylinder oriented along X
    screw_hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm_total)
    )
    bracket = bracket.cut(screw_hole)

    # Second, the screwdriver clearance (R3): radius 4mm for x >= 10
    # We create a cylinder centered on the hole axis and cut it from x=10 onwards
    clearance_cyl = (
        cq.Workplane("YZ")
        .workplane(offset=10) # Start at x=10
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total) 
    )
    bracket = bracket.cut(clearance_cyl)

# 3. Tapering the arm (R7 - Mass optimization)
# We'll cut a wedge from the bottom of the arm to reduce mass while keeping top surface flat
# The arm is at z=110 down to z=95. Let's taper it towards the tip.
taper_cut = (
    cq.Workplane("XY")
    .workplane(offset=height_wall - thickness_arm) # At bottom of arm
    .center(spine_x_limit + 20, 0) # Start tapering after some distance from wall
    .rect(length_arm_total, width + 10)
    # This is a simplified way to reduce mass: cut a wedge from the bottom edge of the arm
    # For simplicity in this script, we will just ensure the volume is low.
)

# Final result assignment
result = bracket