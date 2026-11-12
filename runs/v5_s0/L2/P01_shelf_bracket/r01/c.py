import cadquery as cq

# Parameters based on Design Document and Requirements
spine_thickness = 15.0
width = 20.0  # Y-range: -10 to 10 (R2)
height_wall = 110.0
arm_length = 160.0 # Extends to x=160 (R4)
shelf_z = 110.0
screw_dia = 5.5
hole_y = 0.0
hole_z_positions = [20.0, 60.0]

# R7: To keep mass < 90g (Volume < 72580 mm3), we use a tapered arm.
arm_thickness_start = 15.0
arm_thickness_end = 6.0

# 1. Create the Wall Spine (x: 0 to 15, y: -10 to 10, z: 0 to 110)
spine = cq.Workplane("XY").box(
    spine_thickness, width, height_wall, 
    centered=(False, True, False) # x starts at 0, y centered on 0
)

# 2. Create the Tapered Arm (x: 15 to 160, y: -10 to 10, top surface z=110)
# We'll use a loft between two rectangles in the XZ plane.
# To ensure it is one solid, we make sure the arm overlaps with the spine slightly or touches exactly.
# The spine ends at x=15. The arm starts at x=15.

# Define profiles for lofting
# Profile 1: At x = 15
p1 = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .center(spine_thickness, shelf_z - arm_thickness_start/2)
    .rect(0.1, arm_thickness_start) # Use a tiny width to define the plane at x=15
)

# Actually, lofting in CadQuery is best done by providing a list of Workplanes or using specific geometry.
# Let's use a simpler approach: Create the arm as a single tapered block via extrusion with a taper angle 
# or by constructing it from a polygon.
# A more robust way for this specific shape (tapered in X):
arm_pts = []
num_steps = 10
for i in range(num_steps + 1):
    x = spine_thickness + (arm_length - spine_thickness) * (i / num_steps)
    # thickness at x: h(x) = start - (start-end)*(x-15)/(160-15)
    h_x = arm_thickness_start - (arm_thickness_start - arm_thickness_end) * ((x - spine_thickness) / (arm_length - spine_thickness))
    # Top surface is at z=110. Bottom surface is at z = 110 - h_x
    arm_pts.append((x, 110 - h_x))

# Create the arm using a polyline extrusion or similar. 
# Since it's a constant width (Y), we can create the XZ profile and extrude along Y.
arm = (
    cq.Workplane("XZ")
    .polyline([(spine_thickness, shelf_z), (arm_length, shelf_z), (arm_length, shelf_z - arm_thickness_end), (spine_thickness, shelf_z - arm_thickness_start)])
    .close()
    .extrude(width, both=True) # Extrude along Y, centered on 0
)

# Combine Spine and Arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3) and Clearance (R3)
for z_pos in hole_z_positions:
    # The screw hole itself (axis along X)
    # We extrude a cylinder through the part at the specified Z and Y=0
    bracket = bracket.cut(
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(spine_thickness/2, 0) # Center of spine for hole
        .circle(screw_dia / 2)
        .extrude(arm_length + spine_thickness) # Ensure it goes through everything
    )

    # R3: Screwdriver clearance. No material within 4mm of axis for x >= 10.
    # Clearance zone: a box from x=10 to x=25, covering diameter + 8mm (4mm each side).
    clearance_size = screw_dia + 8.0
    bracket = bracket.cut(
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(17.5, 0) # Center of [10, 25]
        .box(15, clearance_size, clearance_size, centered=(True, True, True))
    )

# Final check on R4: "Nothing of the bracket may be above z = 110 for x >= 8"
bracket = bracket.cut(
    cq.Workplane("XY")
    .workplane(offset=110)
    .center(8, 0)
    .box(arm_length + spine_thickness, width + 2, 50, centered=(False, True, False))
)

result = bracket