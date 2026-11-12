import cadquery as cq

def build_bracket():
    # Dimensions based on Spec and Design Doc
    width = 40.0          # y direction: -20 to 20
    wall_thickness = 15.0 # x direction: 0 to 15
    shelf_length = 150.0  # total x reach
    top_z = 110.0         # top surface height (R4)
    hole_dia = 5.5        # screw hole diameter (R3)
    
    # 1. Create the Wall Plate (x: 0-15, y: -20 to 20, z: 0-110)
    # Note: Spec R4 says nothing above z=110 for x >= 8. 
    # We'll keep the wall plate at z=110 to be safe and satisfy R4.
    wall_plate = cq.Workplane("XY").box(wall_thickness, width, top_z, centered=(False, False, False))

    # 2. Create the Tapered Shelf Support (x: 15-150)
    # We use a series of stacked boxes to create a tapered profile.
    # The thickness in Z decreases as X increases.
    # At x=10 (root), we need height ~35mm for strength/stiffness.
    # Since the top is at z=110, the bottom of the shelf at x=15 will be around z=75.
    # As x -> 150, the thickness decreases to say, 10mm (z: 100-110).
    
    shelf_parts = []
    num_segments = 10
    segment_width = (shelf_length - wall_thickness) / num_segments
    
    for i in range(num_segments):
        x_start = wall_thickness + i * segment_width
        x_end = x_start + segment_width
        
        # Tapering logic: thickness decreases from 35mm at root to 10mm at tip
        # Thickness at x=15 is approx 35. Thickness at x=150 is 10.
        # t(x) = 35 - (25 * (x-15)/135)
        t_at_start = 35.0 - (25.0 * (x_start - 15.0) / (shelf_length - 15.0))
        t_at_end = 35.0 - (25.0 * (x_end - 15.0) / (shelf_length - 15.0))
        
        # To keep top at z=110, the bottom is at z = 110 - thickness
        z_bottom_start = top_z - t_at_start
        z_bottom_end = top_z - t_at_end
        
        # We use a wedge/trapezoid for each segment to ensure smooth taper
        # A simple way is to create a box and then adjust the bottom face, 
        # but for CadQuery simplicity in a single script, we'll use a loft or stacked boxes.
        # Let's use a simpler approach: build one large block and cut it, 
        # OR just stack boxes of slightly different heights.
        
        # For R5/R6 compliance, the cross section at x=10 is part of the wall_plate.
        # The shelf starts at x=15.
        
        # Create a segment: centered on its own local X to use 'box' easily
        # Segment center X = x_start + segment_width/2
        # Segment center Y = 0
        # Segment center Z = top_z - (t_at_start + t_at_end)/4 (approx)
        
        # To ensure a perfectly flat top at z=110, we'll use the 'extrude' method on a profile.
        pass

    # REVISED APPROACH for Tapered Shelf:
    # Create a 2D profile in the XZ plane and extrude it along Y.
    # Profile points (x, z):
    # (15, 110), (150, 110), (150, 100), (15, 75)
    profile = (
        cq.Workplane("XZ")
        .moveTo(wall_thickness, top_z)
        .lineTo(shelf_length, top_z)
        .lineTo(shelf_length, top_z - 10.0) # Tip thickness 10mm
        .lineTo(wall_thickness, top_z - 35.0) # Root thickness 35mm
        .close()
    )
    shelf = profile.extrude(width, both=True) # Extrudes from y=-20 to y=20

    # Combine Wall and Shelf
    body = wall_plate.union(shelf)

    # 3. Screw Holes (R3) and Access Channels
    # Holes at y=0, z=20 and y=0, z=60. Axis along X.
    for z_pos in [20, 60]:
        # Hole: Cylinder along X axis through the wall plate
        # We use YZ plane to cut through X direction.
        # The wall is at x=[0, 15]. Center of wall is x=7.5.
        hole = (
            cq.Workplane("YZ")
            .center(0, z_pos) # y=0 is center because width is centered on Y axis
            .circle(hole_dia / 2)
            .extrude(wall_thickness + 2, both=True)
        )
        # The hole must be at y=0. Since we used 'both=True' and the plane is YZ (x=0),
        # it covers x from -1 to 16. This is perfect for our wall [0, 15].
        body = body.cut(hole)

        # Access Channel: 10mm x 10mm cutout from x=10 to x=15
        # Centered on hole axis (y=0, z=z_pos).
        # A box of length 5 centered at x=12.5 covers [10, 15].
        channel = (
            cq.Workplane("XY")
            .center(12.5, z_pos) # Center X at 12.5, Y at 0 (since width is centered)
            # Wait, the 'center' in XY refers to (x, y). We need to center on Z too.
            # Let's use box and translate.
        )
        channel = cq.Workplane("XY").box(5, 10, 10).translate((12.5, 0, z_pos))
        body = body.cut(channel)

    return body

result = build_bracket()