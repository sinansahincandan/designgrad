import cadquery as cq

def build_bracket():
    # Dimensions & Constants
    width_root = 40.0
    height_root = 110.0
    wall_thickness = 15.0
    shelf_length = 150.0
    hole_dia = 5.5
    
    # Tapering parameters (to satisfy R7: Mass <= 90g)
    width_tip = 12.0

    # 1. Create the Wall Plate
    # x in [0, 15], y in [-20, 20], z in [0, 110]
    wall = cq.Workplane("XY").box(wall_thickness, width_root, height_root, centered=(False, False, False))

    # 2. Create the Shelf Support
    # Since lofting with wires can be finicky in different CQ versions, 
    # we use a robust method: creating two rectangles and using loft on them directly.
    # We define profiles at x=15 and x=150 on the YZ plane.
    
    # Profile 1 (at x=15)
    p1 = cq.Workplane("YZ").workplane(offset=15).rect(width_root, 10, centered=(False, False))
    # Profile 2 (at x=150)
    p2 = cq.Workplane("YZ").workplane(offset=150).rect(width_tip, 10, centered=(False, False))
    
    # In CadQuery 2.x, lofting between two workplanes is best done by creating a single 
    # Workplane object that contains both sketches via the 'loft' method on a list of wires.
    # However, to ensure maximum compatibility and avoid AttributeError:
    # We use the approach of building the shelf as a series of extruded segments or a tapered box.
    # A tapered box (frustum) is perfectly valid for this design.
    
    # Let's build the shelf using a lofted shape by creating two sketches on the same workplane 
    # with different offsets and then calling loft().
    shelf = (
        cq.Workplane("YZ")
        .workplane(offset=15)
        .rect(width_root, 10, centered=(False, False))
        .workplane(offset=135) # This is at x = 15 + 135 = 150
        .rect(width_tip, 10, centered=(False, False))
        .loft()
    )

    # Combine Wall and Shelf
    body = wall.union(shelf)

    # 3. Subtract Screw Holes (R3)
    # Axis along X, centered at y=0, z=20 and z=60.
    for z_pos in [20, 60]:
        # Hole: Cylinder along X axis
        # We use a cylinder on the YZ plane and extrude it through the body.
        hole = (
            cq.Workplane("YZ")
            .workplane(offset=0)
            .center(0, z_pos)
            .circle(hole_dia/2)
            .extrude(160) 
        )
        body = body.cut(hole)

        # Access Channel (R3): x in [10, 150], y in [-width_tip/2 - 2, width_tip/2 + 2], z in [z_pos-6, z_pos+6]
        # Requirement: no material exists within 4mm of the hole axes for x >= 10.
        # A 10x10 box centered at (y=0, z=z_pos) satisfies this.
        channel = (
            cq.Workplane("XY")
            .box(150, 12, 12, centered=(False, False, False))
            .translate((10, -6, z_pos - 6))
        )
        body = body.cut(channel)

    return body

result = build_bracket()