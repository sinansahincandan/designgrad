import cadquery as cq

# Parameters based on Design Document and Feedback
width = 20.0
height_wall = 110.0
spine_thickness = 15.0
length_arm = 150.0
screw_dia = 5.5
clearance_width = 8.0

# 1. Create the Wall Spine (x: 0 to 15, y: -10 to 10, z: 0 to 110)
# We use centered=(False, False, False) and translate to ensure exact bounds
spine = cq.Workplane("XY").box(spine_thickness, width, height_wall, centered=(False, False, False)).translate((0, -width/2, 0))

# 2. Create the Tapered Shelf Arm using Loft
# Profiles are defined in YZ plane. Top edge must be at Z=110.
# p1 (at x=0 to overlap spine): spanning y [-10, 10], z [90, 110]
p1 = [(-width/2, 90), (width/2, 90), (width/2, 110), (-width/2, 110)]
# p2 (at x=length_arm): spanning y [-10, 10], z [105, 110]
p2 = [(-width/2, 105), (width/2, 105), (width/2, 110), (-width/2, 110)]

arm = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .polyline(p1).close()
    .workplane(offset=length_arm)
    .polyline(p2).close()
    .loft(ruled=True)
)

# Combine Spine and Arm to ensure a single solid
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
# Axis along X, centered at y=0, z=20 and z=60.
hole_centers = [(0, 20), (0, 60)] # (y, z)
for y_pos, z_pos in hole_centers:
    # Extrude through the entire length of the part
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
    # Create a box that clears the screw axis for x >= 10
    # Dimensions: length 15 (from x=10 to 25), width 8, height slightly larger than screw dia
    clearance_box = (
        cq.Workplane("XY")
        .box(15, clearance_width, screw_dia + 4, centered=(False, False, False))
        .translate((10, y_pos - clearance_width/2, z_pos - (screw_dia + 4)/2))
    )
    bracket = bracket.cut(clearance_box)

# Final result assignment
result = bracket