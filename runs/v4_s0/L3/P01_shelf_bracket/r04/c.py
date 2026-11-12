import cadquery as cq

# Parameters based on Design Document and Feedback
width_wall = 30.0
height_wall = 110.0
spine_thickness = 15.0
arm_start_x = 15.0
arm_end_x = 160.0
top_z = 110.0

# Taper parameters for Arm (to satisfy R7 mass constraint)
width_base = 30.0
thick_base = 10.0  # Thickness of arm at spine interface
width_tip = 10.0
thick_tip = 5.0    # Thickness of arm at tip

screw_dia = 5.5
hole_centers_yz = [(0, 20), (0, 60)] # y, z coordinates

# 1. Create the Wall Spine (R2: starts at x=0, z=0)
# Using centered=(False, True, False) on XY plane makes origin the min X and min Z
spine = cq.Workplane("XY").box(spine_thickness, width_wall, height_wall, centered=(False, True, False))

# 2. Create the Tapered Arm (R4: top surface at z=110)
# Profile centers to ensure top edge is exactly at top_z
p1_center_z = top_z - thick_base / 2
p2_center_z = top_z - thick_tip / 2

# To ensure R1 (single solid), we start the loft with an overlap into the spine
arm_loft = (
    cq.Workplane("YZ")
    .workplane(offset=spine_thickness - 1.0) # Overlap spine by 1mm for a clean union
    .rect(width_base, thick_base).translate((0, 0, p1_center_z))
    .workplane(offset=arm_end_x - (spine_thickness - 1.0))
    .rect(width_tip, thick_tip).translate((0, 0, p2_center_z))
    .loft(combine=True)
)

# Combine spine and arm
bracket = spine.union(arm_loft)

# 3. Subtract Screw Holes (R3) and Screwdriver Clearance
for y_c, z_c in hole_centers_yz:
    # R3: Cylindrical screw holes along X axis
    hole_x = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(y_c, z_c)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 10)
    )
    bracket = bracket.cut(hole_x)

    # R3: Screwdriver Clearance (Feedback: 13.5mm x 13.5mm box starting at x=10)
    clearance_vol = (
        cq.Workplane("YZ")
        .workplane(offset=10) # Starts at x=10 as per feedback/spec
        .center(y_c, z_c)
        .box(arm_end_x + 10, 13.5, 13.5, centered=(True, True, True))
    )
    bracket = bracket.cut(clearance_vol)

result = bracket