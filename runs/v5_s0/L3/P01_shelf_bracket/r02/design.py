import cadquery as cq

# Parameters
width_spine = 40.0
thickness_spine = 15.0
height_wall = 110.0
length_arm_total = 150.0
thickness_arm = 20.0
z_shelf = 110.0
screw_dia = 5.5

# 1. Create the main body components
# Vertical spine: x from 0 to 15, y from -20 to 20, z from 0 to 110
spine = (
    cq.Workplane("XY")
    .box(thickness_spine, width_spine, height_wall, centered=(False, False, False))
)

# Arm Segment 1: Wide part (x from 15 to 60, y from -20 to 20)
arm_wide = (
    cq.Workplane("XY")
    .box(60 - 15, width_spine, thickness_arm, centered=(False, False, False))
    .translate((15, 0, z_shelf - thickness_arm))
)

# Arm Segment 2: Tapered part (x from 60 to 150, y from -10 to 10)
# Width is 20mm here
arm_narrow = (
    cq.Workplane("XY")
    .box(length_arm_total - 60, 20.0, thickness_arm, centered=(False, False, False))
    .translate((60, 0, z_shelf - thickness_arm))
)

# Combine spine and arm segments
bracket = spine.union(arm_wide).union(arm_narrow)

# 2. Subtract Screw Holes (R3)
# Holes are along X axis at y=0, z=20 and z=60
for z_pos in [20, 60]:
    # The hole must go through the entire part (x from 0 to 150)
    hole_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm_total + 10)
        .translate((-5, 0, 0)) # Ensure it covers x=0 to x=150
    )
    bracket = bracket.cut(hole_cyl)

# 3. Subtract Screwdriver Clearance (R3)
# No material within 4 mm of either hole axis for x >= 10
for z_pos in [20, 60]:
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(4.1) # Radius to clear the 4mm requirement
        .extrude(length_arm_total - 10) # Length from x=10 to end
        .translate((10, 0, 0))
    )
    bracket = bracket.cut(clearance_cyl)

# Final result assignment
result = bracket