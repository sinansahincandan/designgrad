import cadquery as cq

# Constants
WIDTH = 40.0
SHELF_TOP_Z = 110.0
ARM_LENGTH = 150.0
SCREW_HOLES = [(0, 20), (0, 60)]
SCREW_DIA = 5.5

def design():
    # To satisfy R4: Top surface is flat at z=110 from x=8 to x=150.
    # To satisfy R5/R6: Profile at x=10 must be deep (approx 90mm height, 40mm width).
    # To satisfy R7: Minimize mass via tapering.

    # We build the part using a series of boxes and union them to ensure a single solid.
    # This is more robust than lofting in CadQuery for complex shapes.
    
    # 1. Wall Plate (x=0 to x=15)
    wall = cq.Workplane("XY").box(15, WIDTH, SHELF_TOP_Z, centered=(False, False, False))
    
    # 2. Structural Root (x=15 to x=30) - ensures stiffness at x=10
    root = cq.Workplane("XY").box(15, WIDTH, SHELF_TOP_Z, centered=(False, False, False)).translate((15, 0, 0))
    
    # 3. Tapered Arm (x=30 to x=150)
    # We'll use a wedge-like shape by creating a box and cutting it.
    arm_base = cq.Workplane("XY").box(ARM_LENGTH - 30, WIDTH, SHELF_TOP_Z, centered=(False, False, False)).translate((30, 0, 0))
    
    # Create the taper wedge to remove material from bottom as x increases
    # The wedge starts at x=30 (relative offset 0) and goes to x=150 (offset 120)
    # We want the height at x=150 to be small, say 20mm.
    wedge_cut = (cq.Workplane("XZ")
                 .workplane(offset=30)
                 .polyline([(0, SHELF_TOP_Z), (ARM_LENGTH - 30, 20), (ARM_LENGTH - 30, 0), (0, 0)])
                 .close()
                 .extrude(WIDTH + 2, both=True) # Extrude across Y
                 .translate((30, -1, 0)) # Center it on Y
                )
    # Instead of complex wedge subtraction, let's use a simpler approach:
    # A series of blocks to approximate the taper for mass reduction (R7).
    arm_segment1 = cq.Workplane("XY").box(40, WIDTH, SHELF_TOP_Z, centered=(False, False, False)).translate((30, 0, 0))
    arm_segment2 = cq.Workplane("XY").box(40, WIDTH/2, 60, centered=(False, False, False)).translate((70, -WIDTH/4, 50))
    arm_segment3 = cq.Workplane("XY").box(40, WIDTH/4, 20, centered=(False, False, False)).translate((110, -WIDTH/8, 90))
    arm_segment4 = cq.Workplane("XY").box(40, WIDTH/8, 10, centered=(False, False, False)).translate((150-40, -WIDTH/16, 100))

    # Combine all parts into one solid
    body = wall.union(root).union(arm_segment1).union(arm_segment2).union(arm_segment3).union(arm_segment4)

    # R3: Screw holes (5.5mm dia) at y=0, z=20 and y=0, z=60. Axis along X.
    # We create cylinders in the YZ plane to extrude through the X axis.
    h1 = cq.Workplane("YZ").workplane(offset=-1).center(0, 20).circle(SCREW_DIA/2).extrude(ARM_LENGTH + 2)
    h2 = cq.Workplane("YZ").workplane(offset=-1).center(0, 60).circle(SCREW_DIA/2).extrude(ARM_LENGTH + 2)

    # R3: Clearance channels for screwdriver access (radius 4mm from axis for x >= 10)
    c1 = cq.Workplane("YZ").workplane(offset=10).center(0, 20).circle(4.0).extrude(ARM_LENGTH)
    c2 = cq.Workplane("YZ").workplane(offset=10).center(0, 60).circle(4.0).extrude(ARM_LENGTH)

    # Final subtraction
    result = body.cut(h1).cut(h2).cut(c1).cut(c2)
    
    return result

result = design()