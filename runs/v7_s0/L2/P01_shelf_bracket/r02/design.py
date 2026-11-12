import cadquery as cq

# Parameters based on Design Document
width = 20.0
height_wall = 110.0
thickness_arm = 10.0
length_arm_start = 15.0
length_arm_end = 160.0
screw_dia = 5.5
screw_radius = screw_dia / 2

# 1. Create the main L-shape body
# Vertical spine: x from 0 to 15, y centered at 0 (-10 to 10), z from 0 to 110
spine = (
    cq.Workplane("XY")
    .box(15, width, height_wall, centered=(False, False, False))
)

# Horizontal arm: x from 15 to 160, y centered at 0 (-10 to 10), z from 100 to 110
arm = (
    cq.Workplane("XY")
    .box(length_arm_end - length_arm_start, width, thickness_arm, centered=(False, False, False))
    .translate((length_arm_start, 0, height_wall - thickness_arm))
)

# Combine spine and arm to form the base bracket
bracket = spine.union(arm)

# 2. Define Subtractions (Holes and Clearance)
subtractions = cq.Workplane("XY")

hole_z_positions = [20.0, 60.0]

for z_pos in hole_z_positions:
    # R3: Screw Holes - Cylinders along X axis
    # We create a cylinder and translate it so its axis is at (y=0, z=z_pos)
    # The cylinder height is 170 to ensure it passes through the entire part
    hole = (
        cq.Workplane("XY")
        .workplane(offset=z_pos) # This offset is actually on Z if we use a different plane, 
                                  # but let's be more explicit with translation.
        .cylinder(170, screw_radius)
        .translate((85, 0, z_pos - 0)) # Center the cylinder along X (from -85 to 85)
    )
    # To ensure absolute precision and avoid workplane confusion, we'll use a direct approach:
    # Create a cylinder on the YZ plane or just translate a cylinder.
    
    # Let's redefine hole more robustly:
    hole_cylinder = (
        cq.Workplane("XY")
        .cylinder(170, screw_radius)
        .translate((85, 0, z_pos)) # Center on X-axis at the specified Z and Y=0
    )
    # Note: cylinder() in CQ is along Z by default. We need it along X.
    # Correct way for X-axis hole:
    hole_x = (
        cq.Workplane("YZ")
        .center(0, z_pos) # Center on Y=0, Z=z_pos
        .circle(screw_radius)
        .extrude(170)
        .translate((85, 0, 0)) # Center the extrusion along X
    )
    subtractions = subtractions.union(hole_x)

    # R3: Clearance Cutouts - Rectangular prisms from x=10 to x=15
    # Dimensions: dx=5 (from 10 to 15), dy=8, dz=8
    # Centered at y=0, z=z_pos
    clearance = (
        cq.Workplane("XY")
        .box(5, 8, 8, centered=(False, False, False))
        .translate((10, 0, z_pos - 4)) # x starts at 10, y is centered at 0, z is centered at z_pos
    )
    subtractions = subtractions.union(clearance)

# 3. Perform the single boolean subtraction
result = bracket.cut(subtractions)