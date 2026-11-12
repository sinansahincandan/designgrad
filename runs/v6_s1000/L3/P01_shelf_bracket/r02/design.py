import cadquery as cq

def build_bracket():
    # Dimensions based on Design Document and Requirements
    width = 40.0          # y direction: spans [-20, 20]
    wall_thickness = 15.0 # x direction for wall plate
    shelf_length = 150.0  # total length in x
    top_z = 110.0         # top surface z coordinate
    hole_dia = 5.5        # screw hole diameter
    access_radius = 4.0   # screwdriver clearance radius (R3)
    
    # 1. Create the Wall Plate (x: 0-15, y: -20 to 20, z: 0-110)
    wall_plate = cq.Workplane("XY").box(
        wall_thickness, width, top_z, 
        centered=(False, True, False)
    )

    # 2. Create the Tapered Shelf Support (x: 15-150)
    shelf_parts = []
    num_segments = 20 # Increased segments for smoother taper
    segment_width = (shelf_length - wall_thickness) / num_segments
    
    for i in range(num_segments):
        x_start = wall_thickness + i * segment_width
        x_end = x_start + segment_width
        
        # Linear interpolation of thickness from 15 to 6
        t_start = 15.0 - (15.0 - 6.0) * (i / num_segments)
        t_end = 15.0 - (15.0 - 6.0) * ((i + 1) / num_segments)
        
        avg_t = (t_start + t_end) / 2.0
        z_bottom_avg = top_z - avg_t
        
        # Create segment and ensure it overlaps with the wall plate for union
        segment = (
            cq.Workplane("XY")
            .box(segment_width + 1.0, width, avg_t, centered=(False, True, False))
            .translate((x_start - 0.5, 0, z_bottom_avg + avg_t/2))
        )
        shelf_parts.append(segment)

    # Combine wall and shelf
    bracket = wall_plate
    for part in shelf_parts:
        bracket = bracket.union(part)

    # 3. Subtract Screw Holes and Access Channels (R3)
    hole_z_positions = [20.0, 60.0]
    
    for z_pos in hole_z_positions:
        # A. The actual screw holes (diameter 5.5) through the wall plate
        h = (
            cq.Workplane("YZ")
            .center(0, z_pos)
            .circle(hole_dia / 2)
            .extrude(wall_thickness + 2.0, both=True) # Ensure it cuts all the way through
        )
        h = h.translate((7.5, 0, 0))
        bracket = bracket.cut(h)

        # B. Screwdriver Access (R3): radius 4mm from x=10 to x=150
        access = (
            cq.Workplane("YZ")
            .center(0, z_pos)
            .circle(access_radius)
            .extrude(shelf_length - 10 + 1.0) # Extrude along X axis
        )
        # Translate so it starts at x=10 (the extrusion starts from the plane x=0)
        access = access.translate((10, 0, 0))
        bracket = bracket.cut(access)

    return bracket

result = build_bracket()