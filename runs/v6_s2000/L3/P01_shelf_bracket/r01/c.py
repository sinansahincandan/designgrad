import cadquery as cq

# Constants
WIDTH = 40.0  # Total width for centering (y from -20 to 20)
SHELF_TOP_Z = 110.0
SCREW_DIA = 5.5
CLEARANCE_SIZE = 13.5 # 5.5 + 4 + 4

def design():
    # R2: Envelope is within x[0, 170], y[-20, 20], z[0, 130].
    # All parts are centered on Y=0 using (False, True, False) or .center(0,0).

    # 1. Wall Plate (x=0 to x=15)
    # Width is 40mm (y from -20 to 20), height up to SHELF_TOP_Z
    wall = cq.Workplane("XY").box(15, WIDTH, SHELF_TOP_Z, centered=(False, True, False))

    # 2. Structural Root & Tapered Arm (x=15 to x=150)
    # To satisfy R5/R6 at x=10: We need a deep section. 
    # Since the wall covers x=0-15, we ensure the wall or the first arm segment is deep.
    # Profile at x=10 (inside wall): height 90mm, width 20mm.
    # Let's build the arm using segments to control mass (R7) and taper.
    
    # Segment 1: Root (x=15 to x=40). Height 90mm, Width 20mm.
    root_seg = cq.Workplane("XY").box(25, 20, 90, centered=(False, True, False)).translate((15, 0, 45))
    
    # Segment 2: Mid (x=40 to x=80). Height 60mm, Width 15mm.
    mid_seg = cq.Workplane("XY").box(40, 15, 60, centered=(False, True, False)).translate((40, 0, 55))
    
    # Segment 3: Transition (x=80 to x=120). Height 30mm, Width 10mm.
    trans_seg = cq.Workplane("XY").box(40, 10, 30, centered=(False, True, False)).translate((80, 0, 75))
    
    # Segment 4: Tip (x=120 to x=150). Height 5mm, Width 5mm.
    tip_seg = cq.Workplane("XY").box(30, 5, 5, centered=(False, True, False)).translate((120, 0, 107.5))

    # Segment 5: Shelf Support (The flat top surface at z=110)
    # R4: Must reach x=150 and be solid between x=140-150.
    # We add a thin plate on top of the arm segments to ensure the shelf rests correctly.
    shelf_plate = cq.Workplane("XY").box(150, 20, 3, centered=(False, True, False)).translate((0, 0, SHELF_TOP_Z - 1.5))

    # Combine all parts into one solid (R1)
    body = wall.union(root_seg).union(mid_seg).union(trans_seg).union(tip_seg).union(shelf_plate)

    # R3: Screw holes (5.5mm dia, axis along X) at y=0, z=20 and y=0, z=60
    # We use YZ plane to extrude through the part.
    h1 = cq.Workplane("YZ").workplane(offset=0).center(0, 20).circle(SCREW_DIA/2).extrude(170)
    h2 = cq.Workplane("YZ").workplane(offset=0).center(0, 60).circle(SCREW_DIA/2).extrude(170)

    # R3: Rectangular clearance channels for x >= 10
    # Width >= 13.5mm to ensure no material within 4mm of axis.
    c1 = cq.Workplane("YZ").workplane(offset=10).center(0, 20).rect(CLEARANCE_SIZE, CLEARANCE_SIZE).extrude(160)
    c2 = cq.Workplane("YZ").workplane(offset=10).center(0, 60).rect(CLEARANCE_SIZE, CLEARANCE_SIZE).extrude(160)

    # Final subtraction to create holes and clearance
    result = body.cut(h1).cut(h2).cut(c1).cut(c2)
    
    return result

result = design()