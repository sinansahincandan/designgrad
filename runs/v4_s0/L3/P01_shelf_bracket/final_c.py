import cadquery as cq

# Parameters based on Design Document
width_wall = 30.0
height_wall = 110.0
spine_thickness = 15.0
arm_start_x = 15.0
arm_end_x = 160.0
top_z = 110.0
arm_thickness_base = 10.0

screw_dia = 5.5
hole_centers_yz = [(0, 20), (0, 60)] # y, z coordinates

# 1. Create the Wall Spine
# R2: x in [0, 15], y in [-15, 15], z in [0, 110]
spine = cq.Workplane("XY").box(spine_thickness, width_wall, height_wall, centered=(False, True, False))

# 2. Create the Tapered Arm
# Profile at x = 15 (at the spine interface)
width_base = 30.0
thick_base = 10.0

# Profile at x = 160 (the tip)
width_tip = 10.0
thick_tip = 5.0

# To ensure a single solid, we create the arm starting from x=14 to overlap with spine (x=15)
arm_loft = (
    cq.Workplane("YZ")
    .workplane(offset=14.0) # Overlap spine by 1mm
    .rect(width_base, thick_base)
    .workplane(offset=arm_end_x - 14.0)
    .rect(width_tip, thick_tip)
    .loft(combine=True)
)

# The loft is centered on the YZ plane by default in rect/loft logic if not careful.
# We must ensure the arm's Z-top matches top_z = 110.
# The loft creates a shape where the center of the profiles are at (y,z).
# Let's define profiles with explicit centers to match the design requirement: Top surface at z=110.
p1_center_z = top_z - thick_base / 2
p2_center_z = top_z - thick_tip / 2

arm_loft = (
    cq.Workplane("YZ")
    .workplane(offset=14.0)
    .rect(width_base, thick_base).translate((0, 0, p1_center_z))
    .workplane(offset=arm_end_x - 14.0)
    .rect(width_tip, thick_tip).translate((0, 0, p2_center_z))
    .loft(combine=True)
)

# Combine spine and arm
bracket = spine.union(arm_loft)

# 3. Subtract Screw Holes (R3)
for y_c, z_c in hole_centers_yz:
    # Create a cylinder along X axis by extruding on YZ plane
    # We make it long enough to clear the whole object
    hole_x = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(y_c, z_c)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 10)
    )
    bracket = bracket.cut(hole_x)

    # 4. Screwdriver Clearance (R3)
    # No material within 4mm of hole axis for x >= 10.
    # A box on YZ plane with offset=10 extrudes along X.
    clearance_vol = (
        cq.Workplane("YZ")
        .workplane(offset=10)
        .center(y_c, z_c)
        .box(arm_end_x + 10, 8.5, 8.5, centered=(True, True, True))
    )
    bracket = bracket.cut(clearance_vol)

result = bracket