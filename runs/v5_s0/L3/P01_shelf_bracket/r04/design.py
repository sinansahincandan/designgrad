import cadquery as cq

# Parameters based on Design Document and Feedback
thickness_spine = 15.0  # x-dimension of spine (from x=0 to x=15)
width_spine = 20.0      # y-dimension of spine (-10 to 10)
height_wall = 110.0     # z-dimension of spine (0 to 110)

arm_thickness_z = 10.0  # thickness in Z direction
z_top = 110.0           # top surface at z=110
arm_start_x = 15.0      # arm starts where spine ends
arm_end_x = 150.0       # arm extends to x=150
arm_width = 20.0        # y-dimension of arm (-10 to 10)

screw_dia = 5.5
clearance_radius = 4.1  # slightly > 4mm for safety

# 1. Create the main body components
# Vertical spine: x from 0 to 15, y from -10 to 10, z from 0 to 110
spine = (
    cq.Workplane("XY")
    .box(thickness_spine, width_spine, height_wall, centered=(False, True, False))
)

# Shelf Arm: x from 15 to 150, y from -10 to 10, z from 100 to 110
arm = (
    cq.Workplane("XY")
    .box(arm_end_x - arm_start_x, arm_width, arm_thickness_z, centered=(False, True, False))
    .translate((arm_start_x, 0, z_top - arm_thickness_z))
)

# Combine spine and arm
bracket = spine.union(arm)

# 2. Subtract Screw Holes (R3)
# Holes are along X axis at y=0, z=20 and z=60
for z_pos in [20, 60]:
    # Hole cylinder: must go through the entire part from x=0 to x=150
    # We use a large extrusion and translate it to ensure coverage
    hole_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 10)
        .translate((-5, 0, 0)) 
    )
    bracket = bracket.cut(hole_cyl)

# 3. Subtract Screwdriver Clearance (R3)
# No material within 4 mm of either hole axis for x >= 10
for z_pos in [20, 60]:
    clearance_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(arm_end_x - 10 + 5) # Extrude from x=10 to end
        .translate((10, 0, 0))
    )
    bracket = bracket.cut(clearance_cyl)

# Final result assignment
result = bracket