import cadquery as cq

def build_bracket():
    # Dimensions based on Design Document and Feedback
    width = 30.0          # y direction: -15 to 15
    wall_thickness = 15.0 # x direction: 0 to 15
    shelf_top_z = 110.0
    shelf_tip_start_x = 140.0
    shelf_tip_end_x = 150.0
    wall_height = 120.0
    hole_dia = 5.5
    access_size = 15.0    # 15mm x 15mm for screwdriver access (R3)

    # 1. Vertical Wall Plate (x: 0-15, y: -15 to 15, z: 0-120)
    wall_plate = cq.Workplane("XY").box(
        wall_thickness, width, wall_height, centered=(False, False, False)
    )

    # 2. Tapered Horizontal Arm (x: 15 to 140)
    # To satisfy R7 (Mass), we use a tapered profile in Z.
    # At x=15, height is 40mm (z from 70 to 110).
    # At x=140, height is 20mm (z from 90 to 110).
    # We can approximate this with a wedge or a series of boxes.
    # Let's use a loft between two rectangles for a smooth taper.
    
    # Profile at x = 15: width=30, height=40 (z: 70 to 110)
    # Profile at x = 140: width=30, height=20 (z: 90 to 110)
    
    arm_start_x = wall_thickness
    arm_end_x = shelf_tip_start_x
    
    # Create the tapered arm using a loft or simplified geometry.
    # A simpler way for CadQuery is to create a series of boxes or use a single wedge-like shape.
    # Let's build it as a trapezoid in the XZ plane and extrude along Y.
    arm_profile = (
        cq.Workplane("XZ")
        .workplane(offset=0)
        .moveTo(arm_start_x, shelf_top_z)
        .lineTo(arm_end_x, shelf_top_z)
        .lineTo(arm_end_x, shelf_top_z - 20.0)
        .lineTo(arm_start_x, shelf_top_z - 40.0)
        .close()
    )
    # Extrude the profile along Y to create the arm
    tapered_arm = arm_profile.extrude(width, both=True).translate((0, 0, 0))
    # Note: extrude(both=True) centers on the workplane. 
    # Since our XZ plane is at x=0 (implicitly), we need to align it.
    # Let's use a more robust method for the arm.
    
    arm_points = [
        (arm_start_x, shelf_top_z),             # Top-left root
        (arm_end_x, shelf_top_z),               # Top-right tip
        (arm_end_x, shelf_top_z - 20.0),        # Bottom-right tip
        (arm_start_x, shelf_top_z - 40.0)       # Bottom-left root
    ]
    
    # Create the arm by extruding a polygon along Y
    # We use a Workplane on XZ to define the shape and extrude it in Y.
    arm = (
        cq.Workplane("XZ")
        .polyline(arm_points)
        .close()
        .extrude(width, both=True)
    )
    # Since 'both=True' centers on y=0, and width is 30, it spans -15 to 15. Correct.

    # 3. Solid Block for Shelf Tip (x: 140-150, y: -15 to 15, z: 90-110)
    tip_block = (
        cq.Workplane("XY")
        .box(shelf_tip_end_x - shelf_tip_start_x, width, 20.0, centered=(False, False, False))
        .translate((shelf_tip_start_x, 0, shelf_top_z - 20.0))
    )

    # Combine main components
    body = wall_plate.union(arm).union(tip_block)

    # 4. Screw Holes and Access Channels (R3)
    for z_pos in [20, 60]:
        # Hole: Cylinder along X axis through the wall plate
        # We'll use a YZ plane at x=7.5 to cut through the thickness of the wall
        hole = (
            cq.Workplane("YZ")
            .center(0, z_pos) # Center on y=0 (since width is centered), z=z_pos
            # Wait, 'width' is 30, so Y goes -15 to 15. Hole center at y=0.
            # In YZ plane, the axes are Y and Z.
            .center(0, z_pos) 
            .circle(hole_dia / 2)
            .extrude(wall_thickness + 2, both=True) # Extends through X
        )
        body = body.cut(hole)

        # Access Channel: Rectangular cutout (R3)
        # "No material within 4mm of axis for x >= 10"
        # A 15x15 box centered at (y=0, z=z_pos) from x=10 to the front.
        # The feedback suggests: cq.Workplane("XY").box(145, 15, 15).translate((80, 0, z_pos))
        # This creates a box centered at x=80, y=0, z=z_pos.
        # X range: [80 - 72.5, 80 + 72.5] -> [7.5, 152.5]. 
        # Since it starts at 7.5, the part for x >= 10 is cleared.
        access = (
            cq.Workplane("XY")
            .box(145, access_size, access_size)
            .translate((80, 0, z_pos))
        )
        body = body.cut(access)

    return body

result = build_bracket()