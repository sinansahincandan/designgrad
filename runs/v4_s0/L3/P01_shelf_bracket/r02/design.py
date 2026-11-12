import cadquery as cq

# Parameters based on Design Document and Feedback
width_wall = 30.0
height_wall = 110.0
spine_thickness = 15.0
arm_start_x = 15.0
arm_end_x = 160.0
top_z = 110.0

# Taper parameters for the arm (starting from x=15)
width_base = 30.0
thick_base = 10.0  # Z-thickness at spine interface
width_tip = 10.0
thick_tip = 5.0    # Minimum thickness to satisfy R4 and mass

screw_dia = 5.5
hole_centers_yz = [(0, 20), (0, 60)]  # y, z coordinates

# 1. Create the Wall Spine
# R2: x in [0, 15], y in [-15, 15], z in [0, 110]
# Feedback Fix: Ensure spine starts at z=0 by setting center_z to height/2
spine = (
    cq.Workplane("XY")
    .box(spine_thickness, width_wall, height_wall, centered=(False, True, height_wall / 2))
)

# 2. Create the Tapered Arm
# Feedback Fix: Ensure top surface is exactly at z=110 and no geometry above it.
p1_center_z = top_z - thick_base / 2
p2_center_z = top_z - thick_tip / 2

arm_loft = (
    cq.Workplane("YZ")
    .workplane(offset=arm_start_x)
    .rect(width_base, thick_base).translate((0, 0, p1_center_z))
    .workplane(offset=arm_end_x - arm_start_x)
    .rect(width_tip, thick_tip).translate((0, 0, p2_center_z))
    .loft(combine=True)
)

# Combine spine and arm into a single solid (R1)
bracket = spine.union(arm_loft)

# 3. Subtract Screw Holes and Screwdriver Clearance (R3)
for y_c, z_c in hole_centers_yz:
    # Create the screw hole cylinder along X axis
    # We make it long enough to pass through the entire part
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=-10) # Start before the spine for a clean cut
        .center(y_c, z_c)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 20)
    )
    bracket = bracket.cut(hole)

    # Feedback Fix: Screwdriver Clearance (R3)
    # No material within 4mm of hole axis for x >= 10.
    # A box with 8x8 cross-section centered on the axis.
    clearance_vol = (
        cq.Workplane("YZ")
        .workplane(offset=10) # Start exactly at x=10
        .center(y_c, z_c)
        .box(arm_end_x - 10, 8.0, 8.0, centered=(True, True, True))
    )
    bracket = bracket.cut(clearance_vol)

result = bracket