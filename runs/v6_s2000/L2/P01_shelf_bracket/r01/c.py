import cadquery as cq

# Constants
WIDTH = 40.0
SHELF_TOP_Z = 110.0
SCREW_DIA = 5.5
CLEARANCE_RAD = 4.0
WALL_THICKNESS = 3.0  # Thickness of the hollow walls
ARM_THICKNESS = 4.0   # Thickness of the horizontal arm

def design():
    # R2: Envelope width is 40mm, centered on y=0 (y from -20 to 20)
    # We use centered=(False, True, False) for Y-axis centering logic where applicable
    
    # 1. Root Section (x=0 to x=15): Hollow rectangular tube at x=10
    # To satisfy R5/R6, we need a high Moment of Inertia I.
    # A hollow box with outer dims: Width=40, Height=110.
    root_outer = cq.Workplane("XY").box(15, WIDTH, SHELF_TOP_Z, centered=(False, True, False))
    # Subtract inner part to make it a tube (leaving walls of ~3mm)
    inner_h = SHELF_TOP_Z - 2 * WALL_THICKNESS
    inner_w = WIDTH - 2 * WALL_THICKNESS
    root_inner = cq.Workplane("XY").box(15, inner_w, inner_h, centered=(False, True, False))
    # We must ensure the root is a single solid; we'll union parts later.
    # However, for boolean operations, it's easier to build the shell.
    root = root_outer.cut(root_inner)

    # 2. Shelf Arm (x=15 to x=150): Thin-walled horizontal beam
    # R4: Top surface at z=110. Height of arm is ARM_THICKNESS.
    # So arm spans z from [110 - ARM_THICKNESS, 110].
    arm_length = 150 - 15
    arm_z_start = SHELF_TOP_Z - ARM_THICKNESS
    
    # Create the arm as a solid box first
    arm = cq.Workplane("XY").box(arm_length, WIDTH, ARM_THICKNESS, centered=(False, True, False)).translate((15, 0, arm_z_start))
    
    # To satisfy R7 (Mass), we hollow the arm as well or keep it thin.
    # Let's make the arm a hollowed rectangular profile to save mass.
    arm_inner_w = WIDTH - 2 * WALL_THICKNESS
    arm_inner_h = ARM_THICKNESS - 2 * WALL_THICKNESS # If thickness is too small, this fails; let's use a solid thin slab instead for simplicity if volume allows.
    # Given R7 target < 72500 mm3:
    # Root vol approx: (15 * 40 * 110) - (15 * 34 * 104) = 66000 - 53040 = 12960
    # Arm vol approx: 135 * 40 * 4 = 21600
    # Total ~35000 mm3. This is well under the limit (72500). We will use a solid thin arm.

    # Combine Root and Arm
    body = root.union(arm)

    # R3: Screw holes (diameter 5.5mm) at y=0, z=20 and y=0, z=60. Axis along X.
    # Holes go through the wall plate (x=0 to x=15).
    h1 = cq.Workplane("YZ").workplane(offset=0).center(0, 20).circle(SCREW_DIA/2).extrude(15)
    h2 = cq.Workplane("YZ").workplane(offset=0).center(0, 60).circle(SCREW_DIA/2).extrude(15)

    # R3: Clearance channels (radius 4mm) for x >= 10.
    # We subtract from x=10 to the front of the part.
    # The arm starts at x=15, so we need to ensure the clearance reaches through the root and into the arm if needed.
    # However, R3 says "no material within 4mm of either hole axis for x >= 10".
    # This means a cylindrical void from x=10 to x=150.
    c1 = cq.Workplane("YZ").workplane(offset=10).center(0, 20).circle(CLEARANCE_RAD).extrude(160)
    c2 = cq.Workplane("YZ").workplane(offset=10).center(0, 60).circle(CLEARANCE_RAD).extrude(160)

    # Final assembly: Subtract holes and clearance channels
    result = body.cut(h1).cut(h2).cut(c1).cut(c2)
    
    return result

result = design()