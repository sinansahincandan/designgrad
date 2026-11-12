import cadquery as cq

def build_bracket():
    # Constants from Design Document
    top_z = 110.0
    shelf_end_x = 150.0
    wall_thickness = 15.0
    hole_dia = 5.5
    access_radius = 5.0  # Increased to 5mm for R3 compliance
    
    # --- 1. Wall Plate Construction (R2, R4, R7) ---
    # Lower part: y in [-20, 20], z in [0, 60]
    wall_lower = cq.Workplane("XY").box(
        wall_thickness, 40.0, 60.0, 
        centered=(False, True, False)
    )
    # Upper part: y in [-15, 15], z in [60, 110] (tapered Y to save mass R7)
    wall_upper = cq.Workplane("XY").box(
        wall_thickness, 30.0, 50.0, 
        centered=(False, True, False)
    ).translate((0, 0, 60))
    
    bracket = wall_lower.union(wall_upper)

    # --- 2. Shelf Support Construction (R4, R5, R6, R7) ---
    # We use a segmented approach to create the tapered I-beam profile
    num_segments = 30
    shelf_start_x = wall_thickness
    segment_length = (shelf_end_x - shelf_start_x) / num_segments
    
    for i in range(num_segments):
        # Current x position
        curr_x = shelf_start_x + i * segment_length
        next_x = curr_x + segment_length
        
        # Interpolate dimensions for tapering (R7)
        # Width Y: 40 at root to 30 at tip
        ratio = i / num_segments
        curr_width = 40.0 * (1 - ratio) + 30.0 * ratio
        
        # Thickness Z: 35 at root to 12 at tip (R5/R6 strength)
        # We define the thickness of the 'I-beam' structure
        curr_thick = 35.0 * (1 - ratio) + 12.0 * ratio
        
        # R4: Top surface must be exactly top_z. 
        # Bottom surface is top_z - curr_thick.
        # To satisfy R4, we ensure the segment doesn't exceed top_z.
        z_bottom = top_z - curr_thick
        
        # Create the main segment block
        segment = (
            cq.Workplane("XY")
            .box(segment_length + 0.1, curr_width, curr_thick, centered=(False, True, False))
            .translate((curr_x, 0, z_bottom + curr_thick/2))
        )
        
        # R7: Hollow the underside (I-beam style)
        # Only hollow if we aren't at the very end (R4 requires solid material at x=140-150)
        if next_x < 140.0:
            pocket_width = curr_width * 0.6
            pocket_height = curr_thick * 0.7
            # Pocket is removed from the bottom
            pocket = (
                cq.Workplane("XY")
                .box(segment_length + 0.1, pocket_width, pocket_height, centered=(False, True, False))
                .translate((curr_x, 0, z_bottom + pocket_height/2))
            )
            segment = segment.cut(pocket)
            
        bracket = bracket.union(segment)

    # --- 3. Screw Holes and Access (R3) ---
    hole_z_positions = [20.0, 60.0]
    
    for z_pos in hole_z_positions:
        # A. The actual screw holes (diameter 5.5mm)
        # Centered at y=0, z=z_pos, axis along X
        h = (
            cq.Workplane("YZ")
            .center(0, z_pos)
            .circle(hole_dia / 2)
            .extrude(wall_thickness + 10.0, both=True) # Ensure it cuts through wall and shelf
        )
        # Align hole to the center of the wall plate (x=7.5 is center of 15mm thickness)
        h = h.translate((7.5, 0, 0))
        bracket = bracket.cut(h)

        # B. Screwdriver Access (R3): radius 5mm for x >= 10
        # We use a larger cylinder to ensure clearance
        access = (
            cq.Workplane("YZ")
            .center(0, z_pos)
            .circle(access_radius)
            .extrude(shelf_end_x + 20.0) # Extrude far enough to clear the tip
        )
        # Start extrusion at x=10
        access = access.translate((10, 0, 0))
        bracket = bracket.cut(access)

    return bracket

result = build_bracket()