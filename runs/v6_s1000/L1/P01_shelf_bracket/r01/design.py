import cadquery as cq

def build_bracket():
    # Dimensions based on Design Document and Feedback
    width = 40.0          # y-span: -20 to 20
    wall_thickness = 15.0 # x: 0 to 15
    shelf_length = 150.0  # total length in x
    height_at_root = 120.0 # z max for wall plate
    top_z = 110.0         # shelf surface height
    hole_dia = 5.5
    
    # 1. Create the Wall Plate (x: 0-15, y: -20 to 20, z: 0-120)
    # Using centered=(True, True, False) for Y and X/Z alignment
    wall_plate = (
        cq.Workplane("XY")
        .box(wall_thickness, width, height_at_root, centered=(False, True, False))
    )

    # 2. Create the Tapered Shelf Support (x: 15-150)
    # To satisfy R4/R5/R6/R7, we create a tapered arm.
    # We'll use a series of boxes to approximate a taper or a loft.
    # Let's use a simple approach: a main block and then subtract a wedge for tapering.
    # The shelf must be solid at x=140-150, z=110.
    
    # Base horizontal arm (x from 15 to 150)
    # We'll make it thick enough at the root and taper it towards the tip.
    arm_length = shelf_length - wall_thickness
    arm_height_root = 35.0 # Height of the arm section at x=15
    arm_height_tip = 15.0  # Height of the arm section at x=150
    
    # Create a block for the arm
    arm = (
        cq.Workplane("XY")
        .box(arm_length, width, arm_height_root, centered=(False, True, False))
        .translate((wall_thickness, 0, top_z - arm_height_root))
    )
    
    # To taper: subtract a wedge from the top of the arm
    # The wedge starts at x=15 and ends at x=150
    # Height reduction = 35 - 15 = 20mm
    wedge = (
        cq.Workplane("XY")
        .box(arm_length, width + 2, 20, centered=(False, True, False))
        .translate((wall_thickness, 0, top_z + 1)) # Slightly above to ensure clean cut
    )
    # Actually, a simpler way for tapering in CQ is using a loft or just building the arm as a series of segments.
    # Let's use a more robust method: build the arm by extruding a profile along X.
    
    # Define points for the profile (z-coordinates) at x=15 and x=150
    # Profile is a rectangle in YZ plane. 
    # At x=15, z goes from [top_z - 35] to [top_z]
    # At x=150, z goes from [top_z - 15] to [top_z]
    
    # We'll build the arm using a loft between two rectangles.
    # Profile at x=15 (root of arm)
    p1 = cq.Workplane("YZ").rect(width, arm_height_root).center(0, top_z - arm_height_root/2)
    # Profile at x=150 (tip of arm)
    p2 = cq.Workplane("YZ").rect(width, arm_height_tip).center(0, top_z - arm_height_tip/2)
    
    # Since CQ loft is complex for single variables, let's use the "subtraction" method 
    # which is very reliable for a linear taper.
    # Arm: x[15, 150], y[-20, 20], z[top_z - height(x), top_z]
    # We will create a block and then cut a wedge from the bottom to make it taper? 
    # No, R4 says nothing above z=110 for x >= 8. The wall is up to 120.
    # Let's build the arm as a block and subtract a large wedge from the top/bottom.
    # Wait, R4: "Nothing of the bracket may be above z = 110 for x >= 8".
    # This means the wall plate must be cut down to z=110 for x >= 8.
    
    # Refined Construction:
    # A. Wall Plate (x: 0-15, y: -20-20, z: 0-120)
    body = cq.Workplane("XY").box(wall_thickness, width, height_at_root, centered=(False, True, False))
    
    # B. Cut Wall Plate for R4 (x >= 8 must be <= z=110)
    # The wall is x: 0-15. We cut the part where x is [8, 15] and z > 110.
    wall_cut = cq.Workplane("XY").box(7, width, height_at_root - top_z, centered=(False, True, False)).translate((8, 0, top_z + (height_at_root-top_z)/2))
    # Actually simpler: just make the wall two parts or cut a box.
    wall_excess = cq.Workplane("XY").box(7, width, height_at_root - top_z, centered=(False, True, False)).translate((8, 0, top_z + (height_at_root-top_z)/2))
    body = body.cut(wall_excess)

    # C. Shelf Support Arm (x: 15-150, y: -20-20, z: top_z - height(x) to top_z)
    # We'll use a series of boxes for the taper to ensure R4/R5/R6/R7.
    arm = cq.Workplane("XY")
    num_segments = 10
    seg_w = (shelf_length - wall_thickness) / num_segments
    for i in range(num_segments):
        x_start = wall_thickness + i * seg_w
        x_end = x_start + seg_w
        # Linear interpolation of height from 35 to 15
        h_current = 35.0 - (i / num_segments) * (35.0 - 15.0)
        seg = (
            cq.Workplane("XY")
            .box(seg_w, width, h_current, centered=(False, True, False))
            .translate((x_start, 0, top_z - h_current/2))
        )
        arm = arm.union(seg)
    
    body = body.union(arm)

    # D. Screw Holes (R3)
    # Two holes at y=0, z=20 and z=60. Axis along X.
    for z_pos in [20, 60]:
        # Hole: cylinder through the wall plate along X axis
        # The YZ plane is at x=7.5 (center of wall)
        hole = (
            cq.Workplane("YZ")
            .center(0, z_pos)
            .circle(hole_dia/2)
            .extrude(wall_thickness + 2, both=True)
            .translate((wall_thickness/2, 0, 0))
        )
        body = body.cut(hole)
        
        # Access Channel (R3): 10x10 mm centered on axis, x from 10 to 15
        # Center of [10, 15] is 12.5. Length is 5.
        access = cq.Workplane("XY").box(5, 10, 10).translate((12.5, 0, z_pos))
        body = body.cut(access)

    return body

result = build_bracket()