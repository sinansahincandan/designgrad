import cadquery as cq

def build_bracket():
    # Dimensions from Design Document
    width = 40.0  # y-span: -20 to 20
    wall_thickness = 15.0
    shelf_top_z = 110.0
    shelf_end_x = 150.0
    hole_dia = 5.5
    hole_zs = [20, 60]
    
    # Taper parameters (Z-thickness)
    # H(x) = 35 - (x - 10) * (25 / 140)
    # At x=10, thickness is 35. At x=150, thickness is 10.
    # The top surface of the taper must be at z=110 for x >= 8.
    # So for a given x, the bottom surface is at z = 110 - H(x).

    # 1. Create the Wall Plate: x [0, 15], y [-20, 20], z [0, 110]
    wall = cq.Workplane("XY").box(wall_thickness, width, shelf_top_z, centered=(False, False, False))
    
    # 2. Create the Tapered Arm using a series of slices to ensure a single valid solid
    num_slices = 40
    x_start = 10.0
    x_end = 150.0
    step = (x_end - x_start) / num_slices

    arm = cq.Workplane("XY")
    for i in range(num_slices):
        x0 = x_start + i * step
        x1 = x_start + (i + 1) * step
        x_mid = (x0 + x1) / 2.0
        
        # Calculate thickness at the midpoint of this slice for a smooth-ish taper
        h_x = 35.0 - (x_mid - 10.0) * (25.0 / 140.0)
        z_bot = shelf_top_z - h_x
        
        # Create a slice box. We extend it slightly in X to ensure overlap for union.
        slice_box = (
            cq.Workplane("XY")
            .box(step + 1.0, width, h_x, centered=(False, False, False))
            .translate((x0 - 0.5, 0, z_bot))
        )
        arm = arm.union(slice_box)

    # Combine wall and arm
    body = wall.union(arm)

    # 3. Subtract Screw Holes (R3)
    # Diameter 5.5, axis X, centered at y=0, z=20 and z=60
    for z_pos in hole_zs:
        # Hole through the entire structure along X axis
        # We use a large cylinder to ensure it cuts through everything
        hole = (
            cq.Workplane("YZ")
            .workplane(offset=0)
            .circle(hole_dia / 2)
            .extrude(shelf_end_x + 20, both=True)
            .translate((0, 0, z_pos))
        )
        body = body.cut(hole)

        # 4. Access Channels (R3)
        # Rectangular cutout: x in [10, 25], y in [-4, 4] (8mm wide), z in [z_pos-4, z_pos+4] (8mm high)
        # This ensures no material within 4mm of the axis.
        channel = (
            cq.Workplane("XY")
            .box(15, 8, 8, centered=(False, False, False))
            .translate((10, -4, z_pos - 4)) # y-span is [-4, 4], so translate by -width/2
        )
        body = body.cut(channel)

    return body

result = build_bracket()