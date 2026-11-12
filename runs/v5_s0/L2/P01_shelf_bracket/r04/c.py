import cadquery as cq

# Parameters based on Design Document and Feedback
spine_thickness = 15.0
width = 14.0  # Y-range: -7 to 7 (R2)
height_wall = 110.0
arm_length_end = 160.0 # Extends to x=160 (R4)
shelf_z = 110.0
screw_dia = 5.5
hole_y = 0.0
hole_z_positions = [20.0, 60.0]

# R7: To keep mass < 90g (Volume < 72580 mm3), we use a tapered arm.
arm_thickness_start = 10.0
arm_thickness_end = 3.0

# 1. Create the Wall Spine (x: 0 to 15, y: -7 to 7, z: 0 to 110)
spine = cq.Workplane("XY").box(
    spine_thickness, width, height_wall, 
    centered=(False, True, False) # x starts at 0, y centered on 0, z starts at 0
)

# 2. Create the Tapered Arm (x: 15 to 160, y: -7 to 7, top surface z=110)
# We define a profile in the XZ plane that ensures the top edge is exactly at shelf_z.
arm = (
    cq.Workplane("XZ")
    .polyline([
        (spine_thickness, shelf_z), 
        (arm_length_end, shelf_z), 
        (arm_length_end, shelf_z - arm_thickness_end), 
        (spine_thickness, shelf_z - arm_thickness_start)
    ])
    .close()
    .extrude(width, both=True) # Extrude along Y, centered on 0
)

# Combine Spine and Arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3) and Clearance (R3)
for z_pos in hole_z_positions:
    # R3 Fix: Create the screw hole along the X-axis using a YZ workplane.
    # The cylinder spans from x=0 to x=spine_thickness (or more to ensure cut).
    bracket = bracket.cut(
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(hole_y, z_pos)
        .circle(screw_dia / 2)
        .extrude(spine_thickness + 1.0) # Ensure it cuts through the spine
    )

    # R3 Fix: Screwdriver clearance. No material within 4mm of axis for x >= 10.
    # Clearance zone: a box from x=10 to x=160, covering diameter + 8mm (4mm each side).
    # The feedback specifies width/height = 8.0 (which is diameter + clearance logic)
    # and length = 150 (from x=10 to x=160).
    clearance_length = 150.0 # From x=10 to x=160
    clearance_width = 8.0    # +/- 4mm in Y
    clearance_height = 8.0   # +/- 4mm in Z
    
    # Center of x=[10, 160] is (10+160)/2 = 85
    bracket = bracket.cut(
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(85, 0) 
        .box(clearance_length, clearance_width, clearance_height, centered=(True, True, True))
    )

# Final result assignment
result = bracket