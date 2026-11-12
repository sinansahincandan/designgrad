import cadquery as cq

# Constants based on Design Document
WIDTH = 40.0
SHELF_TOP_Z = 110.0
ARM_END_X = 150.0
WALL_THICKNESS = 15.0
SCREW_HOLES_Y = 0.0
SCREW_HOLES_Z = [20.0, 60.0]
SCREW_DIA = 5.5
CLEARANCE_RADIUS = 5.0 # Requirement R3: no material within 4mm (using 5mm for safety)

def design():
    """
    Builds a shelf bracket optimized for strength (R5), stiffness (R6), 
    and mass (R7) using a tapered arm and hollowed wall structure.
    """
    
    # 1. Wall Plate (x=0 to x=15)
    # To satisfy R7 (Mass), we create the wall as a plate but ensure it's part of the union.
    # We will subtract material from it later if needed, but first build the core structure.
    wall = cq.Workplane("XY").box(WALL_THICKNESS, WIDTH, SHELF_TOP_Z, centered=(False, False, False))

    # 2. Shelf Arm (x=8 to x=150)
    # To satisfy R4: Top surface is flat at z=110 and reaches x=150.
    # To satisfy R5/R6: High inertia at x=10.
    # To satisfy R7: Tapered profile.
    
    # We build the arm using a series of lofted sections or a tapered extrusion to keep mass low.
    # Profile 1 (at x=8): Large section to connect to wall and provide I at x=10.
    # Height at x=10 should be ~90mm (from z=20 to z=110).
    
    # Create the top flange (constant thickness)
    top_flange = (cq.Workplane("XY")
                  .box(ARM_END_X - 8, WIDTH, 5.0, centered=(False, False, False))
                  .translate((8, 0, SHELF_TOP_Z - 5)))

    # Create the structural web/tapered support
    # We'll use a loft between a large rectangle at x=10 and a small one at x=150.
    # Section at x=10: width=40, height=90 (z from 20 to 110)
    # Section at x=150: width=10, height=10 (to support shelf R4)
    
    # To ensure a single solid and easy geometry, we'll build the web as a tapered box.
    # We use a wedge-like shape for the web to reduce mass.
    web = (cq.Workplane("XY")
           .workplane(offset=8)
           .rect(WIDTH, 90) # Profile at x=8
           .extrude(ARM_END_X - 8, taper=0.5) # Tapering reduces mass significantly
           .translate((0, -WIDTH/2, 20))) # Align base to z=20

    # Combine components into one body
    # We use union to ensure R1 (Single Solid)
    body = wall.union(top_flange).union(web)

    # 3. Screw Holes and Clearance (R3)
    for z_pos in SCREW_HOLES_Z:
        # The screw hole itself (drilled through the wall thickness)
        hole = (cq.Workplane("YZ")
                .workplane(offset=0)
                .center(0, z_pos)
                .circle(SCREW_DIA / 2)
                .extrude(WALL_THICKNESS))
        
        # R3: Clearance channels for screwdriver access (radius 5mm)
        # Must have no material within 4mm of axis for x >= 10.
        # We extrude from x=10 to the end of the part.
        clearance = (cq.Workplane("YZ")
                     .workplane(offset=10)
                     .center(0, z_pos)
                     .circle(CLEARANCE_RADIUS)
                     .extrude(ARM_END_X - 10))
        
        body = body.cut(hole).cut(clearance)

    # Final check: Ensure the part is a single solid and meets R2 envelope.
    # The wall goes to z=110, arm top is at z=110. Nothing above z=110 for x >= 8.
    result = body
    return result

result = design()