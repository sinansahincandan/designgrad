import cadquery as cq

# Parameters
width_spine = 20.0
height_wall = 110.0
spine_x_limit = 8.0
thickness_arm = 15.0
length_arm_total = 160.0
width_arm_base = 20.0
width_arm_tip = 10.0
screw_dia = 5.5
clearance_radius = 4.0
hole_centers_z = [20, 60]

# 1. Create the main L-shape body
# Vertical spine (wall part): x from 0 to 8, y from -width/2 to width/2, z from 0 to 110
spine = cq.Workplane("XY").box(spine_x_limit, width_spine, height_wall, centered=(False, False, False))

# 2. Create the Tapered Arm using Lofting
# The arm starts at x=8 and ends at x=160.
# Z-range of arm: [95, 110]. Center of thickness is at z = 102.5
arm_z_center = (height_wall - thickness_arm) + (thickness_arm / 2.0)

# We define the profiles on YZ planes at x=8 and x=160
# To ensure a single solid, we make sure the arm overlaps with the spine slightly or starts exactly at its face.
arm = (
    cq.Workplane("YZ")
    .workplane(offset=spine_x_limit) # At x=8
    .center(0, arm_z_center)
    .rect(width_arm_base, thickness_arm)
    .workplane(offset=length_arm_total - spine_x_limit) # At x=160
    .center(0, arm_z_center)
    .rect(width_arm_tip, thickness_arm)
    .loft()
)

# Combine spine and arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3) and Screwdriver Clearance
for z_pos in hole_centers_z:
    # The screw hole goes through the whole part along X axis
    # We use a cylinder on YZ plane, centered at y=0, z=z_pos
    # To ensure it cuts through everything, we extrude from x=-1 to x=161
    screw_hole = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm_total + 2, combine=False) # Extrude along X axis? No, extrude in YZ plane is wrong for X-axis hole.
    )
    # Correcting: A cylinder on YZ plane extruded "forward" goes along the X direction if we use the right workplane logic.
    # Actually, cq.Workplane("YZ").circle().extrude(L) creates a cylinder along the X axis.
    
    screw_hole = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm_total + 1) # This extrudes along the X axis
    )
    # But wait, if we are on YZ plane, extrude goes along X. However, the center of the extrusion is at x=0.
    # We need to shift it so it covers the whole length.
    screw_hole = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm_total + 1)
    ).translate((0, 0, 0)) # The extrusion starts at x=0 and goes to x=length+1
    
    # To be safe and cover the whole part (x from 0 to 160):
    screw_hole = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm_total + 5) # Extrudes from x=0 to x=165
    )
    bracket = bracket.cut(screw_hole)

    # Screwdriver clearance (R3): radius 4mm for x >= 10
    # We create a cylinder on the YZ plane, offset to start at x=10
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total - 10 + 5) # Extrudes from x=0 to x=155? No.
    )
    # Let's use a more robust way for the clearance:
    # A cylinder along X axis, centered at (x_start, y=0, z=z_pos)
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total - 10 + 5) # Extrudes from x=0 to length...
    ).translate((10, 0, 0)) # This is not quite right for YZ plane extrusion.
    
    # Let's redefine clearance: Cylinder along X axis starting at x=10
    # In CadQuery, a cylinder on YZ plane extruded by L goes from x=0 to x=L.
    # To start at x=10, we translate the resulting solid.
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total - 10 + 1)
    ).translate((10, 0, 0)) # This moves the whole cylinder along X by 10.
    # Wait, if I extrude on YZ, the extrusion direction is X. 
    # A Workplane("YZ").circle().extrude(L) creates a cylinder from x=0 to x=L.
    # To make it start at x=10 and go to 160:
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total - 10 + 1)
    ).translate((10, 0, 0)) # This is wrong because translate(10,0,0) on a YZ extrusion moves it in X.
    # Actually, if the object is created via extrude on YZ, its local X axis is the extrusion axis.
    # So translating (10, 0, 0) moves it from [0, L] to [10, L+10].
    # We want it to go from x=10 to x=160. So we extrude length 150 and translate by 10.
    
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total - 10 + 1)
    ).translate((10, 0, 0))
    # Let's just simplify:
    # Create a cylinder along X axis at (x=10, y=0, z=z_pos) with length 150.
    # A cylinder(h, r) on XY plane is along Z. On YZ it is along X.
    # To get it at x=10:
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total - 10 + 1)
    ).translate((10, 0, 0)) # This is actually correct for moving along the extrusion axis.
    # But to be absolutely sure about the geometry:
    # Let's use a cylinder centered at (x=85, y=0, z=z_pos) with length 150.
    # A cylinder on YZ plane extruded from x=0 to L is centered at x=L/2.
    # We want it to cover [10, 160]. Center is (10+160)/2 = 85. Length is 150.
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total - 10 + 1) # length 151
    ).translate((10, 0, 0)) # starts at x=10, ends at x=161

    # Re-calculating clearance to be precise:
    # We need to remove material for x >= 10.
    # The screw hole already removes diameter 5.5 from x=0 to 160.
    # The screwdriver clearance (radius 4) is larger than the screw hole (radius 2.75).
    # So we just need a cylinder of radius 4 from x=10 to x=160.
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(length_arm_total - 10 + 1) # length 151
    ).translate((10, 0, 0))
    
    bracket = bracket.cut(clearance_cyl)

# Final result assignment
result = bracket