import cadquery as cq

# Parameters based on Design Document and Feedback
width = 40.0
height_wall = 110.0
thickness_arm_base = 25.0  # Thickness at the start of the arm (x=15)
length_arm = 150.0         # Total x-reach
spine_thickness = 15.0
screw_dia = 5.5
clearance_width = 8.0      # Width for screwdriver access

# 1. Create the Wall Spine (x: 0 to 15, y: -20 to 20, z: 0 to 110)
# We use centered=(False, False, False) and translate to ensure exact bounds
spine = cq.Workplane("XY").box(spine_thickness, width, height_wall, centered=False).translate((0, -width/2, 0))

# 2. Create the Tapered Shelf Arm using Loft
# Profile 1 at x = spine_thickness (x=15)
# The arm must overlap the spine to ensure a single solid. 
# We'll start the profile slightly inside the spine or ensure the loft covers it.
p1 = [(-width/2, 110 - thickness_arm_base), (width/2, 110 - thickness_arm_base), (width/2, 110), (-width/2, 110)]
# Profile 2 at x = length_arm (x=150)
p2 = [(-width/2, 110 - 5), (width/2, 110 - 5), (width/2, 110), (-width/2, 110)]

# To ensure connection, we start the loft at x=0 instead of spine_thickness
arm = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .polyline(p1).close()
    .workplane(offset=length_arm)
    .polyline(p2).close()
    .loft(ruled=True)
)

# Combine Spine and Arm
# Since the arm now starts at x=0, it overlaps the spine (x: 0 to 15)
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
# Axis along X, centered at y=0, z=20 and z=60.
hole_centers = [(0, 20), (0, 60)] # (y, z)
for y_pos, z_pos in hole_centers:
    # The hole must go through the spine and into the arm area if it intersects.
    # We extrude along X from x=0 to x=150+
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(y_pos, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm + 10)
    )
    bracket = bracket.cut(hole)

# 4. Subtract Screwdriver Clearance (R3)
# Rectangular cutout from x=10 to x=25, width 8mm, centered on hole axis.
for y_pos, z_pos in hole_centers:
    # We use a box in 3D space for clearance to ensure it cuts through the spine correctly.
    clearance_box = (
        cq.Workplane("XY")
        .box(15, clearance_width, screw_dia + 10, centered=(False, False, False))
        .translate((10, y_pos - clearance_width/2, z_pos - (screw_dia+10)/2))
    )
    bracket = bracket.cut(clearance_box)

# Final result assignment
result = bracket