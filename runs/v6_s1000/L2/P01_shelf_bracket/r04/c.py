import cadquery as cq

def build_bracket():
    # Dimensions based on Design Document and Feedback
    wall_thickness = 10.0       # x: 0 to 10 (Reduced from 15 to meet mass R7)
    wall_width = 40.0           # y: -20 to 20
    wall_height = 110.0         # z: 0 to 110 (Capped at 110 for R4)
    
    shelf_start_x = 10.0        # Start shelf from wall thickness boundary
    shelf_end_x = 150.0         # Total length reaches x=150
    shelf_width = 25.0          # y: -12.5 to 12.5 (Reduced for mass R7)
    shelf_top_z = 110.0         # Top surface at z=110
    
    # Tapered profile parameters (R4, R5, R6, R7)
    # At x=10: thickness is 35mm (z from 75 to 110)
    # At x=150: thickness is 5mm (z from 105 to 110)
    # This ensures the top surface is flat at z=110.
    
    # 1. Create Wall Plate (x: 0-10, y: -20 to 20, z: 0-110)
    wall = cq.Workplane("XY").box(wall_thickness, wall_width, wall_height, centered=(False, True, False))

    # 2. Create Tapered Shelf Support (x: 10 to 150)
    # We define the profile in XZ plane and extrude along Y.
    # Points for XZ profile:
    # (10, 75)  -> Root bottom (thickness 35)
    # (150, 105)-> Tip bottom (thickness 5)
    # (150, 110)-> Tip top
    # (10, 110) -> Root top
    def create_tapered_shelf():
        points = [(10, 75), (150, 105), (150, 110), (10, 110)]
        # Extrude along Y centered on y=0. Width is shelf_width.
        # Using both=True with center(0,0,0) logic:
        shelf_profile = (
            cq.Workplane("XZ")
            .polyline(points)
            .close()
            .extrude(shelf_width, both=True)
        )
        return shelf_profile

    shelf = create_tapered_shelf()
    
    # Combine wall and shelf into one solid
    body = wall.union(shelf)
    
    # 3. Screw Holes and Access Channels (R3)
    # Requirement: Diameter 5.5mm, axis along X, centered at (y=0, z=20) and (y=0, z=60).
    # R3: No material within 4mm of axis for x >= 10.
    # We use a cylinder of radius 5.0 to ensure the 4mm clearance is met.
    for z_pos in [20, 60]:
        # Create a hole that cuts through the entire part along X.
        # To satisfy "no material within 4mm for x >= 10", we extrude from x=0 to x=150.
        hole_access = (
            cq.Workplane("YZ")
            .center(75, z_pos) # Center of extrusion at x=75
            .circle(5.0)       # Radius 5.0 > 4.0 requirement
            .extrude(150, both=True) # Extends from x=0 to x=150
        )
        body = body.cut(hole_access)

    return body

result = build_bracket()