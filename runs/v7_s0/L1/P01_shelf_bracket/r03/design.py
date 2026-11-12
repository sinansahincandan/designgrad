import cadquery as cq

# Parameters based on Design Document
spine_width = 30.0        # y from -15 to 15
spine_thickness = 15.0    # x from 0 to 15
spine_height = 110.0      # z from 0 to 110

arm_start_x = 15.0
arm_end_x = 160.0
arm_top_z = 110.0

thickness_at_wall = 20.0  # thickness at x=15
thickness_at_tip = 5.0    # thickness at x=160

screw_dia = 5.5
hole_centers = [(0, 20), (0, 60)] # (y, z)

# 1. Create the Wall Spine
spine = cq.Workplane("XY").box(spine_thickness, spine_width, spine_height, centered=(False, False, False))

# 2. Create the Tapered Arm
# We create the arm by lofting two rectangles at x=15 and x=160
# The top surface is at z=110.
# At x=15: bottom is at 110 - 20 = 90, top is at 110.
# At x=160: bottom is at 110 - 5 = 105, top is at 110.

arm_profile = (
    cq.Workplane("XZ")
    .workplane(offset=arm_start_x)
    .line(arm_end_x - arm_start_x, 0) # Move to x=160
    .workplane(offset=0)
    # We define the profile in the XZ plane: (x, z)
    # Start at x=0 (which is global x=15), z=thickness_at_wall
    # End at x=145 (which is global x=160), z=thickness_at_tip
    .rect(arm_end_x - arm_start_x, thickness_at_wall) # Placeholder to get a plane
)

# A more robust way for CadQuery: Create two faces and loft them
face_start = (
    cq.Workplane("XY")
    .workplane(offset=arm_start_x)
    .rect(spine_width, thickness_at_wall)
    .translate((0, 0, arm_top_z - thickness_at_wall))
)

# To use loft effectively for a tapered extrusion:
# We'll create the arm using a series of points or a wedge cut from a block.
# Let's use the "cut a wedge" approach for simplicity and reliability.
arm_block = (
    cq.Workplane("XY")
    .box(arm_end_x - arm_start_x, spine_width, thickness_at_wall, centered=(False, False, False))
    .translate((arm_start_x, 0, arm_top_z - thickness_at_wall))
)

# The wedge to cut: a triangle in the XZ plane
# Points of triangle in local XZ: (0, thickness), (length, thickness), (length, 0)
# This leaves a taper from thickness at x=15 to 0 at x=160.
# We want it to go from 20 to 5. So we cut a wedge that leaves 5mm.
wedge_cut = (
    cq.Workplane("XZ")
    .workplane(offset=arm_start_x)
    .center(0, arm_top_z) # Move to the top-left corner of the arm block
    # We want to cut from z = 110 - thickness_at_wall up to a sloped line
    # The slope: at x=15 (local 0), height is 20. At x=160 (local 145), height is 5.
    # Actually, it's easier to define the shape of the arm directly using a lofted profile.
)

# Let's use the Loft approach properly:
# Profile 1 at x=15: Rectangle [y:-15 to 15, z:90 to 110]
# Profile 2 at x=160: Rectangle [y:-15 to 15, z:105 to 110]

p1 = cq.Workplane("XY").workplane(offset=arm_start_x).rect(spine_width, thickness_at_wall).translate((0, 0, arm_top_z - thickness_at_wall))
# Note: rect is centered. We need to adjust it so top is at z=110.
p1 = cq.Workplane("XY").workplane(offset=arm_start_x).rect(spine_width, thickness_at_wall).translate((0, 0, arm_top_z - (thickness_at_wall/2)))

# Let's simplify: Create the arm as a block and cut it with a wedge.
# Block: x [15, 160], y [-15, 15], z [110-20, 110]
arm = cq.Workplane("XY").box(arm_end_x - arm_start_x, spine_width, thickness_at_wall, centered=(False, False, False)).translate((arm_start_x, 0, arm_top_z - thickness_at_wall))

# Wedge to remove: A triangle in XZ plane.
# At x=15 (local 0), we want z_bottom = 90.
# At x=160 (local 145), we want z_bottom = 105.
# The wedge starts at local x=0, z=90 and goes to local x=145, z=110? No.
# Let's define the wedge by its vertices in XZ plane: (0, 20), (145, 5), (145, 0), (0, 0) is NOT a triangle.
# The part to REMOVE is the area above the line connecting (0, 20) and (145, 5).
# Wait, the arm is at the TOP. So z=110 is the top surface.
# Bottom surface: Line from (x=15, z=90) to (x=160, z=105).
# The material to REMOVE is a triangle with vertices: (15, 110), (160, 110), (160, 105), (15, 90)? No.
# Let's use a simpler method: Create the arm as a loft between two rectangles.

rect_start = cq.Workplane("XY").workplane(offset=arm_start_x).rect(spine_width, thickness_at_wall).translate((0, 0, arm_top_z - thickness_at_wall/2))
# To make the top surface exactly z=110:
rect_start = cq.Workplane("XY").workplane(offset=arm_start_x).rect(spine_width, thickness_at_wall).translate((0, 0, arm_top_z - thickness_at_wall))
# Correcting rect_start to be centered on Y and have top at z=110:
# Center of rect is (arm_start_x + length/2, 0, 110 - thickness/2)
rect_start = cq.Workplane("XY").workplane(offset=arm_start_x).rect(spine_width, thickness_at_wall).translate((0, 0, arm_top_z - thickness_at_wall))
# Actually, CadQuery's rect is centered. Let's build it manually to be sure.

def create_rect_face(x_pos, width, height, top_z):
    return (
        cq.Workplane("XY")
        .workplane(offset=x_pos)
        .rect(width, height)
        .translate((0, 0, top_z - height/2))
    )

# We'll use a simpler approach: A single block and cut the bottom with a wedge.
arm = cq.Workplane("XY").box(arm_end_x - arm_start_x, spine_width, thickness_at_wall, centered=(False, False, False)).translate((arm_start_x, 0, arm_top_z - thickness_at_wall))

# Wedge to cut: The volume below the taper line.
# Taper line in XZ plane (local x): z = 20 - (15/145)*x  <-- this is height from bottom
# We want top at Z=110. Bottom at Z = 110 - (20 - (15/145)*x)
# Let's just cut a wedge that leaves the desired thickness.
# The part to remove is a triangle in XZ: (0, 20), (145, 5), (145, 0), (0, 0)? No.
# Let's define the shape of the arm as a lofted profile between two rectangles.
# Profile 1 (at x=15): y in [-15, 15], z in [90, 110]
# Profile 2 (at x=160): y in [-15, 15], z in [105, 110]

# We use a Workplane on XZ to draw the profile and extrude it.
arm = (
    cq.Workplane("XZ")
    .workplane(offset=arm_start_x)
    .polyline([(0, 90), (arm_end_x - arm_start_x, 105), (arm_end_x - arm_start_x, 110), (0, 110)])
    .close()
    .extrude(spine_width, both=True) # This extrudes along Y. centered=True makes it y in [-15, 15]
).translate((0, 0, 0))

# Combine spine and arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
for y_pos, z_pos in [(0, 20), (0, 60)]:
    # The hole itself (axis along X)
    hole = cq.Workplane("XY").workplane(offset=z_pos).center(y_pos, 0).circle(screw_dia/2).extrude(170) # Long enough to clear everything
    # Wait, the circle is in XY plane, so it's a hole along Z. We need axis along X.
    # To get axis along X: use Workplane "YZ" or rotate.
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0) # x=0 is the wall
        .center(y_pos, z_pos)
        .circle(screw_dia/2)
        .extrude(170)
    )
    bracket = bracket.cut(hole)

# 4. Subtract Screwdriver Clearance (R3)
# "no material within 4 mm of either hole axis for x >= 10"
# Requirement: 10mm x 10mm rectangular cutout centered on hole axes, from x=10 to x=25.
for y_pos, z_pos in [(0, 20), (0, 60)]:
    clearance = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(y_pos, 0) # Center on hole axis
        # We need a box that is x from 10 to 25.
        # In the XY plane at z_pos, the center of the hole is (x, y) = (any, 0).
        # The requirement says "no material within 4mm of axis for x >= 10".
        # A 10x10 box centered on the axis (y=0, z=z_pos) covering x from 10 to 25.
        # In CadQuery's XY plane at offset z_pos:
        # The hole axis is the line y=0.
        # We want a cutout: x in [10, 25], y in [-5, 5], z in [z_pos-5, z_pos+5]
    )
    # Let's use a box and translate it.
    # A box of size (dx=15, dy=10, dz=10) centered at its own center.
    # We want x to be 10 to 25 -> center_x = 17.5
    # y to be -5 to 5 -> center_y = 0
    # z to be z_pos-5 to z_pos+5 -> center_z = z_pos
    clearance_box = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(17.5, 0) # This is relative to the workplane origin? No, center() is relative to WP.
        # Let's be explicit:
    )
    # Correct approach for clearance:
    clearance_box = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(17.5, 0) # This is relative to the workplane origin (x=0, y=0)
        # But we want x=10 to 25. Since our WP is at z_pos, and center() moves the origin...
        # Let's just use a box and translate it to the absolute position.
    )
    
    # Absolute positioning for clearance:
    # Box: width(x)=15, height(y)=10, depth(z)=10
    # Center at x=17.5, y=0, z=z_pos
    clearance_box = (
        cq.Workplane("XY")
        .box(15, 10, 10, centered=(False, True, True)) # corner is at (x,y,z) = (10, 0, z_pos-5)? No.
    )
    # Let's use the most reliable way:
    clearance_box = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(17.5, 0) # Now origin is at x=17.5, y=0
        .box(15, 10, 10, centered=(True, True, True)) # This covers x: [10, 25], y: [-5, 5], z_local: [-5, 5]
    )
    # Wait, the workplane offset is z. So center(17.5, 0) moves the origin to (17.5, 0, z_pos).
    # Then box(15, 10, 10) centered at that origin covers x: [10, 25], y: [-5, 5], z: [z_pos-5, z_pos+5].
    # This is perfect.
    bracket = bracket.cut(clearance_box)

result = bracket