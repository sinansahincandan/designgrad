import cadquery as cq

def build_bracket():
    # Dimensions based on Design Document and Requirements
    width = 40.0          # y direction: spans [-20, 20]
    wall_thickness = 15.0 # x direction for wall plate (x: 0-15)
    shelf_length = 150.0  # total length in x
    top_z = 110.0         # top surface z coordinate
    hole_clearance_radius = 4.0   # R3: screwdriver clearance radius (covers hole)
    
    # 1. Create the Wall Plate (x: 0-15, y: -20 to 20, z: 0-110)
    # Using centered=(False, True, False) means x starts at 0, y is centered on 0, z starts at 0
    wall_plate = cq.Workplane("XY").box(
        wall_thickness, width, top_z, 
        centered=(False, True, False)
    )

    # 2. Create the Tapered Shelf Support (x: 15-150)
    # To satisfy R7 (Mass) and R4 (Top surface at exactly z=110), 
    # we create a tapered solid and then hollow it out.
    
    # Define profiles for lofting to create the outer shell
    # Profile at x = 15 (Root of shelf)
    # Thickness at root is approx 35mm to satisfy R5/R6 strength
    root_thickness = 35.0
    profile_root = cq.Workplane("XZ").rect(width, root_thickness).translate((15, 0, top_z - root_thickness/2))
    
    # Profile at x = 150 (Tip of shelf)
    # Thickness tapers to 4mm for mass reduction
    tip_thickness = 4.0
    profile_tip = cq.Workplane("XZ").rect(width, tip_thickness).translate((shelf_length, 0, top_z - tip_thickness/2))

    # Create the solid tapered shelf using loft
    # We use a more robust approach: create a series of segments or a lofted body
    # For CadQuery, we can loft between two workplanes
    shelf_outer = (
        cq.Workplane("XZ")
        .workplane(offset=15)
        .rect(width, root_thickness)
        .workplane(offset=shelf_length - 15)
        .rect(width, tip_thickness)
        .loft(combine=True)
    ).translate((0, 0, top_z - root_thickness/2)) # This is tricky with loft; let's use a simpler segment approach for precision

    # Re-implementing shelf using segments to ensure exact top surface at z=110 and R4 compliance
    shelf_parts = []
    num_segments = 30
    segment_dx = (shelf_length - wall_thickness) / num_segments
    
    for i in range(num_segments):
        x_start = wall_thickness + i * segment_dx
        x_end = x_start + segment_dx
        
        # Linear interpolation of thickness from root (35mm) to tip (4mm)
        t_start = root_thickness - (root_thickness - tip_thickness) * (i / num_segments)
        t_end = root_thickness - (root_thickness - tip_thickness) * ((i + 1) / num_segments)
        
        # To ensure R4, the top surface is always at z=top_z.
        # The bottom surface of this segment will be at top_z - thickness.
        # We use the average thickness for a box approximation or interpolate.
        avg_t = (t_start + t_end) / 2.0
        
        # Create segment: width=width, depth=segment_dx, height=avg_t
        # Positioned so top is at top_z
        seg = (
            cq.Workplane("XY")
            .box(segment_dx, width, avg_t, centered=(False, True, False))
            .translate((x_start, 0, top_z - avg_t))
        )
        shelf_parts.append(seg)

    # Combine wall and shelf segments into one solid
    bracket = wall_plate
    for part in shelf_parts:
        bracket = bracket.union(part)

    # R7 Mass Reduction: Hollow out the shelf (leaving top surface and side walls)
    # We subtract a smaller tapered volume from the center of the shelf
    hollow_root_t = root_thickness * 0.4 # Keep some thickness for strength
    hollow_tip_t = tip_thickness * 0.2
    
    # Create hollow volume (centered in Y and Z, but we want to keep top surface)
    # To keep the top surface at z=110, the hollow part must be below it.
    # We'll subtract a shape that leaves ~3mm of material at the top.
    hollow_thickness_top = 3.0 
    
    # Create a tapered subtraction volume
    # It starts from x=15 and goes to x=150
    # The Z-range of the hollow part is [top_z - thickness + hollow_thickness_top, top_z - hollow_thickness_top]
    # But simpler: subtract a shape that leaves a shell.
    
    # Let's use a simplified approach for R7: Subtract a tapered block from the middle
    # The subtraction starts at x=15 and ends at x=150 (or 140 to keep tip solid)
    # To satisfy R4, we ensure material remains at z=110 between x=140 and 150.
    
    hollow_volume = (
        cq.Workplane("XZ")
        .workplane(offset=wall_thickness)
        .rect(width - 6, root_thickness - 6) # Leave 3mm walls on sides
        .workplane(offset=shelf_length - wall_thickness - 10) # Stop before the very tip to ensure R4
        .rect(width - 6, tip_thickness - 2)
        .loft(combine=True)
    ).translate((0, 0, top_z - root_thickness + 3)) # Offset Z so it doesn't cut the top surface

    # To ensure R4 (solid at x=140-150), we stop the hollow volume at x=140.
    # The current loft goes to shelf_length - wall_thickness - 10 = 150 - 15 - 10 = 125.
    # Let's adjust:
    hollow_volume = (
        cq.Workplane("XZ")
        .workplane(offset=wall_thickness)
        .rect(width - 6, root_thickness - 8) 
        .workplane(offset=140 - wall_thickness) # Stop at x=140
        .rect(width - 6, tip_thickness - 2)
        .loft(combine=True)
    ).translate((0, 0, top_z - root_thickness + 3))

    bracket = bracket.cut(hollow_volume)

    # 3. Subtract Screw Holes and Access (R3)
    # Single loop for both holes: radius 4mm, from x=10 to x=150
    hole_z_positions = [20.0, 60.0]
    for z_pos in hole_z_positions:
        access_cut = (
            cq.Workplane("YZ")
            .center(0, z_pos)
            .circle(hole_clearance_radius)
            .extrude(150 - 10) # Extends from x=10 to x=150
            .translate((10, 0, 0))
        )
        bracket = bracket.cut(access_cut)

    return bracket

result = build_bracket()