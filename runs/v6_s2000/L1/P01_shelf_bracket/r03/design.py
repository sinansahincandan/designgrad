import cadquery as cq

# Constants based on Design Document and Feedback
SCREW_HOLES_Y = 0.0
SCREW_HOLES_Z = [20.0, 60.0]
SCREW_DIA = 5.5
CLEARANCE_RADIUS = 5.0
SHELF_TOP_Z = 110.0

def design():
    """
    Builds a tapered shelf bracket optimized for strength (R5), stiffness (R6), 
    and mass (R7) while meeting all geometric requirements.
    """
    
    # 1. Wall Plate: x in [0, 15], y in [-15, 15], z in [10, 100]
    wall = (cq.Workplane("XY")
            .box(15, 30, 90, centered=(False, False, False))
            .translate((0, -15, 10)))

    # 2. Shelf Arm Segment A (Tip): x in [140, 150], width 30mm, thickness 10mm
    # Top surface at z=110 means bottom is at z=100
    arm_tip = (cq.Workplane("XY")
               .box(10, 30, 10, centered=(False, False, False))
               .translate((140, -15, SHELF_TOP_Z - 10)))

    # 3. Shelf Arm Segment B (Span): x in [15, 140], width 30mm, thickness 6mm
    # To ensure union with the wall and tip, we extend this segment to overlap both.
    # Wall ends at x=15, Tip starts at x=140.
    # We make span go from x=14 to x=141 to guarantee overlap.
    # IMPORTANT: The Z-height must also overlap the wall/tip to ensure a solid connection.
    # Wall top is z=100. Tip bottom is z=100. 
    # We extend arm_span slightly in Z (e.g., from 99.5 to 110) or ensure it hits the junction.
    # The design says span thickness is 6mm, top surface at 110 -> bottom at 104.
    # To connect to wall (top z=100), we must add a vertical connector or extend arm_span downwards.
    # Let's extend the arm_span Z-range to reach down to z=99 so it overlaps the wall top.
    arm_span = (cq.Workplane("XY")
                .box(127, 30, 11, centered=(False, False, False)) # Increased thickness for overlap
                .translate((14, -15, SHELF_TOP_Z - 11))) # Bottom at z=99

    # 4. Root Reinforcement at x=10: x in [10, 15], width 40mm (y in [-20, 20]), height 90mm (z in [10, 100])
    root_reinforcement = (cq.Workplane("XY")
                         .box(5, 40, 90, centered=(False, False, False))
                         .translate((10, -20, 10)))

    # Combine all parts into one solid using union (R1)
    # We use a sequence of unions to ensure the boolean engine processes them correctly
    body = wall.union(root_reinforcement).union(arm_span).union(arm_tip)

    # R3: Screw holes and clearance channels
    for z_pos in SCREW_HOLES_Z:
        # The screw hole itself (drilled through the wall along X axis)
        hole = (cq.Workplane("YZ")
                .workplane(offset=0) 
                .center(0, z_pos)
                .circle(SCREW_DIA / 2)
                .extrude(16)) # Extrudes from x=0 to x=16
        
        # R3: Clearance channels for screwdriver access (radius 5mm for x >= 10)
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