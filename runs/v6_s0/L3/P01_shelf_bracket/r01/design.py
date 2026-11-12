import cadquery as cq

# Parameters based on Design Document
width = 40.0          # y range: -20 to 20
spine_x_end = 15.0    # x range of spine: 0 to 15
arm_x_end = 160.0     # total length x: up to 160
height_top = 110.0    # z top surface
screw_dia = 5.5       # R3 requirement
hole_z_coords = [20.0, 60.0]

# 1. Create the Wall Spine (x: 0 to 15, y: -20 to 20, z: 0 to 110)
# Using centered=False and translating ensures min corner is at (0, -20, 0)
spine = cq.Workplane("XY").box(spine_x_end, width, height_top, centered=(False, False, False)).translate((0, -width/2, 0))

# 2. Create the Shelf Arm (x: 15 to 160, y: -20 to 20)
# Define the arm profile in XZ plane:
# Top is always at z = height_top (110)
# Bottom rises from z=0 at x=spine_x_end to z=95 at x=arm_x_end (thickness 15mm)
arm_profile = (
    cq.Workplane("XZ")
    .moveTo(spine_x_end, 0)
    .lineTo(arm_x_end, 95) 
    .lineTo(arm_x_end, height_top)
    .lineTo(spine_x_end, height_top)
    .close()
)

# Extrude the profile along Y. 
# To ensure it connects to the spine and covers the correct y-range:
# The spine is at y = [-20, 20]. We extrude width=40 centered on y=0.
arm = arm_profile.extrude(width)
arm = arm.translate((0, -width/2, 0))

# Combine Spine and Arm
# To ensure they union correctly, we make the spine slightly wider in X to overlap with the arm profile start
spine_overlap = cq.Workplane("XY").box(spine_x_end + 1.0, width, height_top, centered=(False, False, False)).translate((0, -width/2, 0))
bracket = spine_overlap.union(arm)

# 3. Subtract Screw Holes (R3) and Clearance
for z_pos in hole_z_coords:
    # Hole: Cylinder along X axis centered at y=0, z=z_pos
    # In YZ plane, extrusion goes along X.
    hole_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_x_end + 10) # Extrudes from x=0 to arm_x_end+10
    )
    bracket = bracket.cut(hole_cyl)

    # Clearance (R3): No material within 4mm of hole axis for x >= 10.
    # We create a larger cylinder and translate it so it starts at x=10.
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2 + 4.0)
        .extrude(arm_x_end) # Extrudes from x=0 to arm_x_end
    )
    # Translate so the extrusion starts at x=10
    clearance_cyl = clearance_cyl.translate((10, 0, 0))
    bracket = bracket.cut(clearance_cyl)

# Final result assignment
result = bracket