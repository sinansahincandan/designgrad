import cadquery as cq

# Constants
WIDTH = 40.0  # y goes from -20 to 20
SHELF_TOP_Z = 110.0
ARM_LENGTH = 150.0
SCREW_DIA = 5.5
CLEARANCE_DIA = 10.0 
WALL_THICKNESS = 15.0

def design():
    # R2: Envelope constraints and Y-centering
    
    # 1. Wall Plate (x=0 to x=15)
    # We use a box that spans from x=0 to x=15.
    wall = (cq.Workplane("XY")
            .box(WALL_THICKNESS, WIDTH, SHELF_TOP_Z, centered=(False, False, False))
            .translate((0, -WIDTH/2, 0)))

    # 2. Shelf Arm Slab (x=8 to x=150)
    arm_slab = (cq.Workplane("XY")
                .box(ARM_LENGTH - 8, WIDTH, 5, centered=(False, False, False))
                .translate((8, -WIDTH/2, SHELF_TOP_Z - 5)))

    # 3. Root Section / Main Body (x=10 to x=150)
    # To ensure union with the wall plate [0, 15], we start this at x=5 instead of x=10.
    # This provides a 10mm overlap between the wall and the root block.
    root_block = (cq.Workplane("XY")
                  .box(ARM_LENGTH - 5, WIDTH, SHELF_TOP_Z, centered=(False, False, False))
                  .translate((5, -WIDTH/2, 0)))

    # Taper the root block to reduce mass (R7) while keeping height at x=10 high.
    # The wedge cut starts from where the root block starts (x=5).
    wedge_cut = (cq.Workplane("XZ")
                 .workplane(offset=5)
                 .polyline([(0, SHELF_TOP_Z), (ARM_LENGTH - 5, 20), (ARM_LENGTH - 5, 0), (0, 0)])
                 .close()
                 .extrude(WIDTH + 10, both=True) 
                 .translate((5, -WIDTH/2 - 5, 0)))

    # Combine primitives into one body using union.
    # We explicitly use a large overlap for the wall and root_block.
    # The wall is [0, 15], root_block is [5, 150]. Overlap is [5, 15].
    # To fix the disconnected solid issue, we perform union on all parts together.
    body = wall.union(arm_slab).union(root_block)
    
    # Subtract the wedge from the combined body
    body = body.cut(wedge_cut)

    # R3: Screw holes (5.5mm dia) at y=0, z=20 and y=0, z=60. Axis along X.
    h1 = (cq.Workplane("YZ")
         .workplane(offset=-1)
         .center(0, 20)
         .circle(SCREW_DIA/2)
         .extrude(WALL_THICKNESS + 5))
    
    h2 = (cq.Workplane("YZ")
         .workplane(offset=-1)
         .center(0, 60)
         .circle(SCREW_DIA/2)
         .extrude(WALL_THICKNESS + 5))

    # R3: Clearance channels (diameter 10mm) for x >= 10.
    c1 = (cq.Workplane("YZ")
         .workplane(offset=10)
         .center(0, 20)
         .circle(CLEARANCE_DIA/2)
         .extrude(ARM_LENGTH))
    
    c2 = (cq.Workplane("YZ")
         .workplane(offset=10)
         .center(0, 60)
         .circle(CLEARANCE_DIA/2)
         .extrude(ARM_LENGTH))

    # Final assembly: Single solid via subtraction
    result = body.cut(h1).cut(h2).cut(c1).cut(c2)
    
    return result

result = design()