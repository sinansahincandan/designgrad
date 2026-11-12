import cadquery as cq

# Constants
WIDTH = 40.0
SHELF_TOP_Z = 110.0
SCREW_DIA = 5.5
CLEARANCE_RAD = 4.0  # Radius for screwdriver access (R3)
WALL_THICKNESS = 3.0
ARM_THICKNESS = 6.0   # Thickness of the horizontal arm

def design():
    # --- 1. Root Section (x=0 to x=15) ---
    # Hollow rectangular tube at x=10 to satisfy R5/R6.
    # Height is SHELF_TOP_Z, Width is WIDTH.
    root_outer = cq.Workplane("XY").box(15, WIDTH, SHELF_TOP_Z, centered=(False, True, False))
    
    inner_h = SHELF_TOP_Z - 2 * WALL_THICKNESS
    inner_w = WIDTH - 2 * WALL_THICKNESS
    
    if inner_h <= 0 or inner_w <= 0:
        root = root_outer
    else:
        # Subtracting the inner void to create a hollow tube
        root_inner = cq.Workplane("XY").box(15, inner_w, inner_h, centered=(False, True, False))
        root = root_outer.cut(root_inner)

    # --- 2. Shelf Arm (x=15 to x=150) ---
    arm_z_start = SHELF_TOP_Z - ARM_THICKNESS
    
    # Part A: Hollowed arm from x=15 to x=140
    hollow_arm_len = 140 - 15
    hollow_arm = cq.Workplane("XY").box(hollow_arm_len, WIDTH, ARM_THICKNESS, centered=(False, True, False)).translate((15, 0, arm_z_start))
    
    # To keep the top surface at z=110 solid (R4), we subtract from the bottom.
    inner_arm_h = ARM_THICKNESS - 2 * WALL_THICKNESS
    if inner_arm_h > 0:
        inner_arm_w = WIDTH - 2 * WALL_THICKNESS
        # The arm is translated to (15, 0, arm_z_start). 
        # Its Z range is [arm_z_start, SHELF_TOP_Z].
        # We subtract a void that leaves the top and bottom walls.
        inner_void = cq.Workplane("XY").box(hollow_arm_len, inner_arm_w, inner_arm_h, centered=(False, True, False)).translate((15, 0, arm_z_start + WALL_THICKNESS))
        hollow_arm = hollow_arm.cut(inner_void)

    # Part B: Solid arm tip from x=140 to x=150 (R4 requirement: fill fraction 1.0)
    arm_tip = cq.Workplane("XY").box(10, WIDTH, ARM_THICKNESS, centered=(False, True, False)).translate((140, 0, arm_z_start))

    # Combine all main components into one body
    body = root.union(hollow_arm).union(arm_tip)

    # --- 3. Screw Holes and Clearance (R3) ---
    # We use a YZ plane to create cylinders along the X axis.
    # To ensure boolean success, we extrude slightly beyond the part boundaries (-1 to 151).
    
    # R3: Two screw holes (5.5mm dia) at y=0, z=20 and y=0, z=60.
    # We extrude from x=-1 to x=151 to ensure they pierce through the geometry completely.
    h1 = cq.Workplane("YZ").workplane(offset=-1).center(0, 20).circle(SCREW_DIA/2).extrude(152)
    h2 = cq.Workplane("YZ").workplane(offset=-1).center(0, 60).circle(SCREW_DIA/2).extrude(152)

    # R3: Clearance channels (radius 4mm) for x >= 10.
    # We use a diameter of 8.0 (radius 4.0) as requested to ensure no material is within 4mm.
    # Extruding from x=10 to x=151 to guarantee intersection with the arm.
    c1 = cq.Workplane("YZ").workplane(offset=10).center(0, 20).circle(CLEARANCE_RAD).extrude(141)
    c2 = cq.Workplane("YZ").workplane(offset=10).center(0, 60).circle(CLEARANCE_RAD).extrude(141)

    # Final assembly: Subtract holes and clearance channels from the body
    result = body.cut(h1).cut(h2).cut(c1).cut(c2)
    
    return result

result = design()