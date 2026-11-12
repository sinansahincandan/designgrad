import cadquery as cq

# Parameters based on Design Document
width = 40.0          # y range: -20 to 20
spine_x_end = 15.0    # x range of spine: 0 to 15
arm_x_end = 160.0     # total length x: up to 160
height_top = 110.0    # z top surface
screw_dia = 5.5       # R3 requirement
hole_z_coords = [20.0, 60.0]
wall_thickness = 4.0  # Thickness for spine shell

# 1. Create the Hollow Wall Spine (x: 0 to 15, y: -20 to 20, z: 0 to 110)
# To ensure it is a single connected solid with the arm, we make sure 
# the spine and arm overlap significantly in X.
spine = (
    cq.Workplane("XY")
    .box(spine_x_end + 2.0, width, height_top, centered=(False, True, False))
    .faces(">Z").shell(-wall_thickness)
)

# 2. Create the Shelf Arm (x: 15 to 160, y: -20 to 20)
# Profile in XZ plane: Top is flat at z=110. Bottom tapers from z=0 at x=15 to z=10 at x=160.
# We start the arm slightly before spine_x_end to ensure overlap for union.
arm_start_x = spine_x_end - 2.0 
arm_profile = (
    cq.Workplane("XZ")
    .moveTo(arm_start_x, 0)
    .lineTo(arm_x_end, 10) 
    .lineTo(arm_x_end, height_top)
    .lineTo(arm_start_x, height_top)
    .close()
)

# Extrude the arm along Y, centered at y=0 to satisfy R2 (-20 to 20)
arm = arm_profile.extrude(width).translate((0, -width/2, 0))

# 3. Create the Support Pillar (x: 140 to 150, y: -20 to 20, z: 0 to 110)
# This provides solid material directly below z=110 for x in [140, 150] as per R4.
pillar = (
    cq.Workplane("XY")
    .box(10, width, height_top, centered=(False, True, False))
    .translate((140, 0, 0))
)

# Combine Spine, Arm, and Pillar into one solid
bracket = spine.union(arm).union(pillar)

# 4. Subtract Screw Holes (R3) and Clearance Channels
for z_pos in hole_z_coords:
    # Hole: Cylinder along X axis centered at y=0, z=z_pos
    # We use a YZ plane extrusion to go through the spine
    hole_cyl = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(spine_x_end + 5.0) # Ensure it cuts through the wall and overlaps
    )
    bracket = bracket.cut(hole_cyl)

    # Clearance (R3): Rectangular channel for screwdriver access
    # "No material within 4mm of either hole axis for x >= 10"
    # We use a box centered at (y=0, z=z_pos) extending from x=10 to arm_x_end.
    clearance_channel = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(0, 0)
        .rect(arm_x_end - 10.0, width) # Rectangle in XY plane at height z_pos
        .extrude(8.0, both=True)       # Extrude 4mm up and 4mm down (total 8mm)
    ).translate((10, 0, 0))            # Move start to x=10

    bracket = bracket.cut(clearance_channel)

result = bracket