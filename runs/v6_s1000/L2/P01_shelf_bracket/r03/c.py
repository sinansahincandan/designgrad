import cadquery as cq

def build_bracket():
    # Dimensions from Design Document
    wall_width = 40.0        # y: -20 to 20
    wall_thickness = 15.0    # x: 0 to 15
    wall_height = 120.0      # z: 0 to 120
    
    shelf_length = 135.0     # from x=15 to x=150 (total length 150)
    shelf_width = 25.0       # y: -12.5 to 12.5
    shelf_top_z = 110.0      # Top surface at z=110
    
    # 1. Create Wall Plate (x: 0-15, y: -20 to 20, z: 0-120)
    # We use centered=(False, True, False) for Y [-20, 20] and X [0, 15]
    wall = cq.Workplane("XY").box(wall_thickness, wall_width, wall_height, centered=(False, True, False))

    # 2. Create Tapered Shelf Support (x: 15-150)
    def create_tapered_shelf():
        # We'll build the shelf using a wedge/trapezoid shape in XZ plane and extrude along Y.
        # To ensure it connects to the wall, we extend the profile slightly into the wall (x=14 instead of 15).
        # Profile points in XZ: 
        # (14, 75) -> Root bottom
        # (150, 100) -> Tip bottom
        # (150, 110) -> Tip top
        # (14, 110) -> Root top
        points = [(14, 75), (150, 100), (150, 110), (14, 110)]
        shelf_profile = cq.Workplane("XZ").polyline(points).close().extrude(shelf_width, both=True)
        return shelf_profile

    shelf = create_tapered_shelf()
    
    # Combine wall and shelf
    body = wall.union(shelf)
    
    # 3. Screw Holes and Access Channels (R3)
    # Two holes: diameter 5.5, axis X, centered at (y=0, z=20) and (y=0, z=60).
    # R3: No material within 4mm of axis for x >= 10.
    # We use a cylinder of radius 5.0 to satisfy the requirement.
    for z_pos in [20, 60]:
        # The access channel must be centered on y=0 and z=z_pos.
        # It extends along X. To ensure it cuts through the wall and shelf:
        hole_access = (
            cq.Workplane("YZ")
            .center(0, z_pos) 
            .circle(5.0)      
            .extrude(160, both=True) # Extends along X from -80 to 80 (covers 0-150)
        )
        body = body.cut(hole_access)

    return body

result = build_bracket()