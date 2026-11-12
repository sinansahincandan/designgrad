import cadquery as cq

# Parameters
width_spine = 30.0
thickness_spine = 15.0
height_wall = 110.0
length_arm = 150.0
thickness_arm = 12.0
screw_dia = 5.5
z_shelf = 110.0

# 1. Create the main L-shape body
# Vertical spine: x from 0 to 15, y from -15 to 15, z from 0 to 110
spine = (
    cq.Workplane("XY")
    .box(thickness_spine, width_spine, height_wall, centered=(False, False, False))
)

# Horizontal arm: x from 15 to 150, y from -15 to 15, z from (110-arm_thick) to 110
# Note: We start the arm at x=15 so it integrates with the spine.
arm = (
    cq.Workplane("XY")
    .box(length_arm - 15, width_spine, thickness_arm, centered=(False, False, False))
    .translate((15, 0, z_shelf - thickness_arm))
)

# Combine spine and arm
bracket = spine.union(arm)

# 2. Implement Tapered Profile (R7 - Mass Reduction)
# We want the width to be 30mm for x in [15, 40] and 20mm for x in [40, 150].
# Subtract two blocks from the sides of the arm starting at x=40.
side_cut_1 = (
    cq.Workplane("XY")
    .box(length_arm - 40, 5, thickness_arm, centered=(False, False, False))
    .translate((40, 10, z_shelf - thickness_arm))
)
side_cut_2 = (
    cq.Workplane("XY")
    .box(length_arm - 40, 5, thickness_arm, centered=(False, False, False))
    .translate((40, -15, z_shelf - thickness_arm))
)

bracket = bracket.cut(side_cut_1).cut(side_cut_2)

# 3. Subtract Screw Holes (R3)
# Holes are along X axis at y=0, z=20 and z=60
for z_pos in [20, 60]:
    hole_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos) # center is (y, z)
        .circle(screw_dia / 2)
        .extrude(length_arm + 10) # Extrudes along X
    )
    # The extrusion on YZ plane goes from x=0 to x=L. We need it to cover the spine too.
    # Since we used extrude(length, both=True) or similar, let's just translate.
    hole_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm + 20)
        .translate((-10, 0, 0)) # Ensure it covers x=0 to x=150
    )
    bracket = bracket.cut(hole_cyl)

# 4. Subtract Screwdriver Clearance (R3)
# No material within 4 mm of either hole axis for x >= 10.
for z_pos in [20, 60]:
    clearance_box = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(4.1) # Radius to clear the 4mm requirement
        .extrude(7) # Length from x=10 to x=17 (to cover 10-16)
        .translate((10, 0, 0))
    )
    bracket = bracket.cut(clearance_box)

# Final result assignment
result = bracket