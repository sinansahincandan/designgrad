import cadquery as cq

def build_bracket():
    # Dimensions based on design document and requirements
    width = 40.0          # y direction (from -20 to 20)
    wall_thickness = 15.0 # x direction for the vertical part
    shelf_thickness = 15.0
    shelf_length = 150.0  # total x reach
    height_at_root = 110.0 # top surface z
    hole_dia = 5.5
    
    # 1. Create the Main Body (L-shape)
    # Vertical Wall Plate: x in [0, 15], y in [-20, 20], z in [0, 110]
    # Note: To satisfy R4 (nothing above z=110 for x>=8), we ensure the wall plate height is 110.
    v_part = cq.Workplane("XY").box(wall_thickness, width, height_at_root, centered=(False, False, False))
    
    # Horizontal Shelf: x in [15, 150], y in [-20, 20], z in [95, 110] (top surface at 110)
    h_part = (
        cq.Workplane("XY")
        .box(shelf_length - wall_thickness, width, shelf_thickness, centered=(False, False, False))
        .translate((wall_thickness, 0, height_at_root - shelf_thickness))
    )
    
    body = v_part.union(h_part)

    # 2. Subtract Screw Holes and Access Channels (R3)
    # Requirements: holes at y=0, z=20 and y=0, z=60. Axis along X.
    # Screwdriver access: no material within 4mm of axis for x >= 10.
    # This means a void from x=10 to x=150 with height/width > 8mm.
    
    for z_pos in [20, 60]:
        # A. Screw Hole (Cylinder along X)
        # We use the YZ plane at x=7.5 (middle of wall) to cut through
        hole = (
            cq.Workplane("YZ")
            .center(0, z_pos) # centered on y=0 and z=z_pos in the YZ plane
            .workplane(offset=7.5) # move to middle of wall thickness
            .circle(hole_dia / 2)
            .extrude(wall_thickness + 2, both=True) # Extrude through the wall
        )
        # Since the YZ plane is at x=0 in CQ, and we want it centered on the part's X-axis:
        # The 'both=True' extrude centers the hole on the plane. 
        # We need to ensure the hole spans the whole length of the bracket for safety.
        hole_long = (
            cq.Workplane("YZ")
            .center(0, z_pos)
            .circle(hole_dia / 2)
            .extrude(shelf_length + 20, both=True) # Long enough to clear everything
        )
        # Translate the hole so it is centered on the X-axis of our part (x=75)
        hole_long = hole_long.translate((75, 0, 0))
        body = body.cut(hole_long)

        # B. Access Channel (Box along X)
        # Requirement: x in [10, 150], y in [-7.5, 7.5], z in [z_pos-7.5, z_pos+7.5]
        # This provides a 15x15mm clearance, satisfying the "4mm from axis" rule.
        channel = (
            cq.Workplane("XY")
            .box(shelf_length - 10, 15, 15) # Length is 140 (from x=10 to 150)
            .translate((80, 0, z_pos))      # Center of [10, 150] is 80
        )
        body = body.cut(channel)

    return body

result = build_bracket()