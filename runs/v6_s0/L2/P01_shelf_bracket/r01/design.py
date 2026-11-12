import cadquery as cq

# Parameters based on Design Document
spine_width = 15.0
spine_height = 110.0
spine_y_range = 40.0 # -20 to 20
arm_length_end = 160.0
screw_dia = 5.5
clearance_radius = 4.0

# 1. Create the Wall Spine (x=0 to x=15)
# Positioned from x=0 to 15, y=-20 to 20, z=0 to 110
spine = (
    cq.Workplane("XY")
    .box(spine_width, spine_y_range, spine_height, centered=(False, False, False))
    .translate((0, -spine_y_range/2, 0))
)

# 2. Create the Tapered Shelf Arm (x=15 to x=160)
# The previous error showed the arm was offset in Y incorrectly.
# We need the arm to be centered at y=0 (spanning -20 to 20).
# Profile at x=15: thickness 20mm (z from 90 to 110), width 40mm
# Profile at x=160: thickness 10mm (z from 100 to 110), width 40mm

# We use a single Workplane and create two profiles on different planes.
# To ensure they union, we'll make the arm overlap the spine by 1mm.
arm = (
    cq.Workplane("XY")
    .workplane(offset=spine_width - 1.0) # Start at x=14 to overlap spine
    .center(0, 0)                       # Center in Y
    .rect(spine_y_range, 20)            # Width 40, Height 20
    .workplane(offset=arm_length_end - (spine_width - 1.0)) # Move to x=160-ish
    .center(0, -5)                      # Shift Z center: start was z=100 (90+10), end is z=105 (100+5)
    .rect(spine_y_range, 10)            # Width 40, Height 10
    .loft()
)

# Combine spine and arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
# Holes are along X axis at y=0, z=20 and z=60.
hole_centers = [(0, 20), (0, 60)] # (y, z)

for y_pos, z_pos in hole_centers:
    # Create a cylinder along X axis through the bracket
    # We use YZ plane and extrude along X.
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=-1) # Start slightly before x=0
        .center(y_pos, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_length_end + 5) 
    )
    bracket = bracket.cut(hole)

# 4. Subtract Screw Access Channels (R3)
# "no material within 4 mm of either hole axis for x >= 10"
for y_pos, z_pos in hole_centers:
    cyl_clearance = (
        cq.Workplane("YZ")
        .workplane(offset=10) # Start at x=10
        .center(y_pos, z_pos)
        .circle(4.0)
        .extrude(6) # Extends to x=16
    )
    bracket = bracket.cut(cyl_clearance)

# Final result assignment
result = bracket