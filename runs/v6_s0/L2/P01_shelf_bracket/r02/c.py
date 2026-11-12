import cadquery as cq

# Parameters
spine_x = 15.0
spine_y_half = 20.0
spine_z_max = 110.0

arm_start_x = 15.0
arm_end_x = 160.0
arm_top_z = 110.0

# Taper parameters for the arm (at x=15 to x=160)
arm_thickness_start = 15.0
arm_thickness_end = 8.0

screw_dia = 5.5
clearance_dia = 8.0  # Satisfies R3 (4mm radius from axis)
hole_z_coords = [20.0, 60.0]

# 1. Create the Spine
# x: 0 to 15, y: -20 to 20, z: 0 to 110
spine = cq.Workplane("XY").box(spine_x, spine_y_half * 2, spine_z_max, centered=(False, True, False))

# 2. Create the Tapered Arm
# To create a loft in CadQuery reliably, we define two profiles on different workplanes 
# and use the loft method which expects multiple sketches/wires to be present in the history.
p1_z = arm_top_z - arm_thickness_start / 2
p2_z = arm_top_z - arm_thickness_end / 2

# Profile at x=15 (relative to origin)
arm_profile1 = (
    cq.Workplane("XZ")
    .workplane(offset=arm_start_x)
    .center(0, p1_z)
    .rect(spine_y_half * 2, arm_thickness_start)
)

# Profile at x=160 (relative to origin)
arm_profile2 = (
    cq.Workplane("XZ")
    .workplane(offset=arm_end_x)
    .center(0, p2_z)
    .rect(spine_y_half * 2, arm_thickness_end)
)

# Combine profiles and loft
# We use the 'add' method to bring both sketches into one Workplane object before calling loft
arm = arm_profile1.add(arm_profile2).loft(ruled=True)

# Combine spine and arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes and Clearance (R3)
for z_pos in hole_z_coords:
    # The screw hole (diameter 5.5) along X axis
    h = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(z_pos, 0)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 10)
    )
    
    # The clearance (diameter 8.0) starting from x=10
    c = (
        cq.Workplane("YZ")
        .workplane(offset=10)
        .center(z_pos, 0)
        .circle(clearance_dia / 2)
        .extrude(arm_end_x + 10)
    )
    
    bracket = bracket.cut(h).cut(c)

# Final result assignment
result = bracket