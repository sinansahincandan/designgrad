import cadquery as cq

# Parameters based on Design Document and Feedback
spine_width = 20.0        # x: 0 to 15 (thickness), y: -10 to 10, z: 0 to 110
spine_x_end = 15.0
spine_height = 110.0
arm_start_x = 15.0
arm_end_x = 150.0
top_z = 110.0

# Arm taper parameters
arm_thickness_start = 20.0  # at x=15, bottom z = 110 - 20 = 90
arm_thickness_end = 5.0     # at x=150, bottom z = 110 - 5 = 105

screw_dia = 5.5
clearance_width = 8.0
clearance_x_start = 10.0
clearance_x_end = 25.0

# 1. Create the Wall Spine (x: 0 to 15, y: -10 to 10, z: 0 to 110)
spine = (
    cq.Workplane("XY")
    .box(spine_x_end, spine_width, spine_height, centered=(False, False, False))
)

# 2. Create the Tapered Shelf Arm using Loft
# Profile 1 at x=15: y in [-10, 10], z from (110-20) to 110
p1_bottom_z = top_z - arm_thickness_start
p1 = [(-spine_width/2, p1_bottom_z), (spine_width/2, p1_bottom_z), (spine_width/2, top_z), (-spine_width/2, top_z)]

# Profile 2 at x=150: y in [-10, 10], z from (110-5) to 110
p2_bottom_z = top_z - arm_thickness_end
p2 = [(-spine_width/2, p2_bottom_z), (spine_width/2, p2_bottom_z), (spine_width/2, top_z), (-spine_width/2, top_z)]

arm = (
    cq.Workplane("YZ")
    .workplane(offset=arm_start_x)
    .polyline(p1).close()
    .workplane(offset=arm_end_x - arm_start_x)
    .polyline(p2).close()
    .loft(ruled=True)
)

# Combine Spine and Arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
# Axis along X, centered at y=0, z=20 and z=60.
hole_centers = [(0, 20), (0, 60)] # (y, z)
for y_pos, z_pos in hole_centers:
    # Extrude through the entire length of the part (x=0 to x=150)
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(y_pos, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_end_x + 1) # Ensure it clears the end
    )
    bracket = bracket.cut(hole)

# 4. Subtract Screwdriver Clearance (R3)
# Rectangular cutout from x=10 to x=25, width 8mm, centered on hole axis.
for y_pos, z_pos in hole_centers:
    # Dimensions: length 15 (from x=10 to 25), width 8, height slightly larger than screw dia
    clearance_box = (
        cq.Workplane("XY")
        .box(clearance_x_end - clearance_x_start, clearance_width, screw_dia + 4, centered=(False, False, False))
        .translate((clearance_x_start, y_pos - clearance_width/2, z_pos - (screw_dia + 4)/2))
    )
    bracket = bracket.cut(clearance_box)

# Final result assignment
result = bracket