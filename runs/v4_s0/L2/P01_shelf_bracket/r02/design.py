import cadquery as cq

# Parameters based on New Design Document and Feedback
width = 20.0              # Y-dimension (from -10 to 10)
spine_thickness = 8.0     # X-dimension of the spine
height_wall = 110.0       # Z-dimension of the spine
length_arm = 150.0        # Total x-reach
thickness_arm_base = 30.0 # Z-height of arm at x=8 (z from 80 to 110)
tip_thickness = 5.0       # Z-height of arm at x=150 (z from 105 to 110)
screw_dia = 5.5           # Diameter of screw holes
clearance_width = 12.0    # Width for screwdriver access

# 1. Create the Wall Spine (x: 0 to 8, y: -10 to 10, z: 0 to 110)
spine = cq.Workplane("XY").box(spine_thickness, width, height_wall, centered=(False, False, False)).translate((0, -width/2, 0))

# 2. Create the Tapered Shelf Arm using Loft
# The arm starts at x=8 (the end of the spine) and goes to x=150.
# Profile 1 at x = 8: Rectangle with width 20, height 30, top at z=110.
# Points in YZ plane for profile 1: y from -10 to 10, z from (110-30) to 110.
p1 = [(-width/2, 110 - thickness_arm_base), (width/2, 110 - thickness_arm_base), (width/2, 110), (-width/2, 110)]

# Profile 2 at x = 150: Rectangle with width 20, height 5, top at z=110.
p2 = [(-width/2, 110 - tip_thickness), (width/2, 110 - tip_thickness), (width/2, 110), (-width/2, 110)]

# Loft the profiles along the X axis starting from x=8 to x=150
arm = (
    cq.Workplane("YZ")
    .workplane(offset=spine_thickness)
    .polyline(p1).close()
    .workplane(offset=length_arm - spine_thickness)
    .polyline(p2).close()
    .loft(ruled=True)
)

# Combine Spine and Arm to ensure a single solid
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
# Axis along X, centered at y=0, z=20 and z=60.
hole_centers = [(0, 20), (0, 60)] # (y, z)
for y_pos, z_pos in hole_centers:
    # Extrude a cylinder through the entire length of the part along X
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(y_pos, z_pos)
        .circle(screw_dia / 2)
        .extrude(length_arm + 10)
    )
    bracket = bracket.cut(hole)

# 4. Subtract Screwdriver Clearance (R3)
# Rectangular cutout from x=8 to x=25, width 12mm, centered on hole axis.
for y_pos, z_pos in hole_centers:
    # The clearance box must be wide enough (12mm) and positioned correctly.
    # We use a box in XY plane or just extrude from YZ to ensure it cuts through.
    clearance_box = (
        cq.Workplane("YZ")
        .workplane(offset=spine_thickness) # Start at x=8
        .center(y_pos, z_pos)
        # We create a rectangle in YZ and extrude it along X
        .rect(clearance_width, screw_dia + 10) # This is actually Z-height here? No, let's use box for clarity.
    )
    # Re-implementing clearance as a 3D box to be precise with the feedback
    cb = (
        cq.Workplane("XY")
        .box(25 - 8, clearance_width, screw_dia + 10, centered=(False, False, False))
        .translate((8, y_pos - clearance_width/2, z_pos - (screw_dia+10)/2))
    )
    bracket = bracket.cut(cb)

# Final result assignment
result = bracket