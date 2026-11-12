import cadquery as cq

# Parameters based on Design Document and Feedback
width_spine = 30.0
height_spine = 110.0
thickness_spine = 15.0
screw_dia = 5.5
clearance_y_width = 14.0  # > 5.5 + 2*4 (R3)
hole_z_positions = [20.0, 60.0]

# 1. Create the Wall Spine
# Ensures bottom is at z=0 and top is at z=110 to satisfy R2/R4
spine = (
    cq.Workplane("XY")
    .box(thickness_spine, width_spine, height_spine)
    .translate((thickness_spine / 2, 0, height_spine / 2))
)

# 2. Create the Lofted Arm
# Profile at x=15: Width 30 (y:-15 to 15), Height 30 (z:80 to 110)
# Profile at x=160: Width 5 (y:-2.5 to 2.5), Height 5 (z:105 to 110)
# This ensures the top surface is flat at z=110 for all x >= 8 (R4)

arm = (
    cq.Workplane("YZ")
    # Profile 1 at x = thickness_spine
    .workplane(offset=thickness_spine)
    .center(0, 110 - 30/2)
    .rect(30, 30)
    # Profile 2 at x = 160
    .workplane(offset=160 - thickness_spine)
    .center(0, 110 - 5/2)
    .rect(5, 5)
    .loft()
)

# Combine Spine and Arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
# Axis along X, centered at y=0, z=z_pos
for z_pos in hole_z_positions:
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(thickness_spine * 2) # Ensure it cuts through the spine
    )
    # Translate hole to be centered on X-axis of the spine (x=7.5)
    bracket = bracket.cut(hole.translate((-thickness_spine/2, 0, 0)))

# 4. Subtract Screwdriver Clearance (R3)
# No material within 4mm of hole axis for x >= 10.
for z_pos in hole_z_positions:
    # Create a box centered at y=0, z=z_pos, spanning from x=10 to the end
    # Width is clearance_y_width (14mm), height covers the screw area
    clearance_box = (
        cq.Workplane("XY")
        .box(160, clearance_y_width, 20, centered=(False, True, True))
        .translate((10, 0, z_pos))
    )
    bracket = bracket.cut(clearance_box)

# Final result assignment
result = bracket