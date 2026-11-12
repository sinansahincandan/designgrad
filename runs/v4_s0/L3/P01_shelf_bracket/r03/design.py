import cadquery as cq

# Parameters based on Design Document and Feedback
width_wall = 30.0      # Y dimension of spine
height_wall = 110.0    # Z dimension of spine
spine_thickness = 15.0 # X dimension of spine
arm_end_x = 160.0
top_z = 110.0

screw_dia = 5.5
hole_centers_yz = [(0, 20), (0, 60)]  # y, z coordinates

# 1. Create the Wall Spine (R2)
# Using rect + extrude to ensure bottom is at z=0 and top is at z=110
# centered=(False, True, False) for box would also work if translated, 
# but rect().extrude() is cleaner for building from z=0.
spine = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(spine_thickness, width_wall, centered=(False, True))
    .extrude(height_wall)
)

# 2. Create the Tapered Arm (R4)
# Profile at x = 15 (at the spine interface)
width_base = 30.0
thick_base = 10.0

# Profile at x = 160 (the tip)
width_tip = 10.0
thick_tip = 5.0

# To ensure R4: The top edge must be exactly at z=110.
# We calculate the center of each profile so that the top is always at top_z.
p1_center_z = top_z - thick_base / 2
p2_center_z = top_z - thick_tip / 2

# Create the arm loft starting from x=14 to ensure significant overlap with spine (x=0 to 15) for R1.
arm_loft = (
    cq.Workplane("YZ")
    .workplane(offset=14.0)
    .rect(width_base, thick_base).translate((0, 0, p1_center_z))
    .workplane(offset=arm_end_x - 14.0)
    .rect(width_tip, thick_tip).translate((0, 0, p2_center_z))
    .loft(combine=True)
)

# Combine spine and arm (R1)
bracket = spine.union(arm_loft)

# 3. Subtract Screw Holes and Clearance (R3)
for y_c, z_c in hole_centers_yz:
    # Hole: Cylinder along X axis through the part
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(y_c, z_c)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 1)
    )
    bracket = bracket.cut(hole)

    # Screwdriver Clearance: A box starting at x=10 and going to the end.
    # centered=(False, True, True) on YZ plane with offset 10 means:
    # X starts at 10, Y is centered on y_c, Z is centered on z_c.
    clearance = (
        cq.Workplane("YZ")
        .workplane(offset=10)
        .center(y_c, z_c)
        .box(arm_end_x, 8.5, 8.5, centered=(False, True, True))
    )
    bracket = bracket.cut(clearance)

result = bracket