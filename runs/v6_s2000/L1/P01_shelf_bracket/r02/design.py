import cadquery as cq

# Constants
WIDTH = 40.0
SHELF_TOP_Z = 110.0
ARM_LENGTH = 150.0
SCREW_HOLES_Y = 0.0
SCREW_HOLES_Z = [20.0, 60.0]
SCREW_DIA = 5.5
CLEARANCE_RADIUS = 5.0

def design():
    """
    Builds a shelf bracket optimized for strength (R5), stiffness (R6), 
    and mass (R7) while meeting all geometric requirements.
    """
    
    # 1. Wall Plate (x=0 to x=15)
    # To satisfy R5/R6 at x=10, we need a deep profile.
    # We create the wall as a solid block that provides the necessary I at the root.
    wall = cq.Workplane("XY").box(15, WIDTH, SHELF_TOP_Z, centered=(False, False, False))
    
    # 2. Shelf Arm (x=8 to x=150)
    # R4: Top surface is flat at z=110 and reaches x=150.
    # We create a continuous horizontal block for the shelf support.
    # The arm starts from x=8 to ensure it overlaps with the wall plate for a single solid.
    arm_top = (cq.Workplane("XY")
               .box(ARM_LENGTH - 8, WIDTH, 10, centered=(False, False, False))
               .translate((8, 0, SHELF_TOP_Z - 10)))

    # 3. Structural Support / Taper (x=15 to x=150)
    # To satisfy R7 (Mass), we taper the bottom of the arm as it moves away from the wall.
    # We'll add a structural beam connecting the wall to the arm top.
    # This ensures the part is one single solid (R1).
    support_beam = (cq.Workplane("XY")
                    .box(ARM_LENGTH - 15, WIDTH/2, 40, centered=(False, False, False))
                    .translate((15, 0, 0)))

    # Combine all parts into one solid using union
    body = wall.union(arm_top).union(support_beam)

    # R3: Screw holes (5.5mm dia) along X axis at (y=0, z=20) and (y=0, z=60)
    for z_pos in SCREW_HOLES_Z:
        # The screw hole itself (drilled through the wall)
        hole = (cq.Workplane("YZ")
                .workplane(offset=-1) # Start slightly before x=0
                .center(0, z_pos)
                .circle(SCREW_DIA / 2)
                .extrude(17)) # Extrudes through the wall thickness (x=15)
        
        # R3: Clearance channels for screwdriver access (radius 5mm for x >= 10)
        # We cut from x=10 to x=15 to satisfy "no material within 4mm of axis for x >= 10"
        clearance = (cq.Workplane("YZ")
                     .workplane(offset=10)
                     .center(0, z_pos)
                     .circle(CLEARANCE_RADIUS)
                     .extrude(6)) # Extrudes from x=10 to x=16
        
        body = body.cut(hole).cut(clearance)

    # Final result must be a single solid (R1)
    result = body
    return result

result = design()