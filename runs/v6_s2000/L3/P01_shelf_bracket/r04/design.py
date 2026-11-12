import cadquery as cq

# Constants
WIDTH = 40.0
SHELF_TOP_Z = 110.0
ARM_START_X = 15.0
ARM_END_X = 150.0
SCREW_HOLES_Y_Z = [(0, 20), (0, 60)]
SCREW_DIA = 5.5
CLEARANCE_RAD = 4.0

def design():
    # 1. Create the Wall Plate (x=0 to x=15)
    # We use a thick block and then pocket it to create an I-beam/webbed structure for mass reduction (R7).
    # The profile at x=10 must be deep (approx 90mm height, 40mm width) to satisfy R5/R6.
    wall_plate = cq.Workplane("XY").box(15, WIDTH, SHELF_TOP_Z, centered=(False, True, False))
    
    # Pocketing the wall plate: Create a central void to leave vertical webs and top/bottom flanges.
    # This maintains high Moment of Inertia (I) while reducing mass.
    pocket_width = WIDTH * 0.6  # Leave 12mm webs on each side
    pocket_height = SHELF_TOP_Z - 15.0 # Leave top and bottom flanges
    wall_pocket = (cq.Workplane("XY")
                   .box(15, pocket_width, pocket_height, centered=(False, True, False))
                   .translate((0, 0, 7.5))) # Offset to leave bottom flange at z=0
    
    body = wall_plate.cut(wall_pocket)

    # 2. Create the Shelf Arm (x=15 to x=150)
    # The arm is a thin plate with top surface at z=110.
    # Thickness tapers from 5mm at x=15 to 3mm at x=150.
    # We'll approximate this using a loft or a series of segments. 
    # To ensure R4 (solid material between x=140 and x=150), we use a tapered extrusion approach.
    
    arm_length = ARM_END_X - ARM_START_X
    
    # Create the arm using a lofted profile to achieve linear taper
    # Profile 1 at x=15: thickness 5mm (z from 105 to 110)
    # Profile 2 at x=150: thickness 3mm (z from 107 to 110)
    p1 = cq.Workplane("XZ").workplane(offset=ARM_START_X).rect(arm_length, WIDTH, centered=(False, True)) # Placeholder logic
    # Simpler approach for CadQuery: Create a tapered box via lofting two rectangles
    
    # Profile at x=15 (Start of arm)
    prof_start = cq.Workplane("XY").workplane(offset=ARM_START_X).rect(0.1, WIDTH).extrude(5).translate((0, 0, SHELF_TOP_Z - 5))
    # Profile at x=150 (End of arm)
    prof_end = cq.Workplane("XY").workplane(offset=ARM_END_X).rect(0.1, WIDTH).extrude(3).translate((0, 0, SHELF_TOP_Z - 3))
    
    # Using a loft between two rectangles on the XZ plane to create the tapered arm
    arm = (cq.Workplane("XZ")
           .workplane(offset=ARM_START_X)
           .rect(WIDTH, 5) # Width is along Y (in XZ plane this is width), thickness is 5
           .workplane(offset=arm_length)
           .rect(WIDTH, 3)
           .loft(combine=True)
           .translate((ARM_START_X, 0, SHELF_TOP_Z - 5)) # Adjusting to align top at z=110
          )
    # Correcting arm placement: The loft above is in XZ plane. Let's rebuild carefully.
    
    # Re-build Arm: Top surface must be exactly z=110.
    # We define the profile in the XZ plane and extrude/loft along Y.
    # Profile at x=15: (x=15, z=105) to (x=15, z=110)
    # Profile at x=150: (x=150, z=107) to (x=150, z=110)
    arm_profile = (cq.Workplane("XZ")
                   .workplane(offset=ARM_START_X)
                   .polyline([(0, 110), (arm_length, 110), (arm_length, 107), (0, 105)])
                   .close()
                   .extrude(WIDTH, both=True) # Extrude along Y axis
                   .translate((ARM_START_X, 0, 0))
                  )
    # The extrude 'both' with WIDTH/2 on each side of Y=0 gives y in [-20, 20]
    arm = arm_profile.translate((0, 0, 0)) # Adjusting Z if needed. Let's refine:
    
    # Final Arm Construction (Robust)
    arm_pts = []
    steps = 10
    for i in range(steps + 1):
        x = ARM_START_X + (i / steps) * arm_length
        t = 5.0 - (2.0 * (i / steps)) # Taper from 5 to 3
        arm_pts.append((x, SHELF_TOP_Z))
        arm_pts.append((x, SHELF_TOP_Z - t))
    
    # Create arm by lofting slices or using a single tapered extrusion logic
    # For simplicity and R1/R4 compliance:
    arm = (cq.Workplane("XY")
           .workplane(offset=ARM_START_X)
           .rect(arm_length, WIDTH, centered=(False, True)) # This is just a base
          )
    # Let's use the most reliable method for a tapered plate:
    arm = (cq.Workplane("XZ")
           .workplane(offset=ARM_START_X)
           .rect(arm_length, WIDTH, centered=(False, True)) # This is wrong plane. 
          )

    # Corrected Arm Construction:
    # Create a wedge-like shape in XZ and extrude along Y
    arm = (cq.Workplane("XZ")
           .workplane(offset=ARM_START_X)
           .polyline([(0, 110), (arm_length, 110), (arm_length, 107), (0, 105)])
           .close()
           .extrude(WIDTH, both=True) # This creates y from -20 to 20
          )
    # The extrusion is along the Z axis in XZ plane? No, extrude in XZ goes along Y.
    # In CadQuery, extrude on XZ plane moves along Y.
    # So arm is now: x in [15, 150], z in [105-ish, 110], y in [-20, 20].
    # We need to translate it so the top surface (z=110) is correct.
    # The polyline was defined with Z values. Extruding on XZ plane moves along Y.
    # This results in a shape where 'thickness' is in Z and 'width' is in Y.
    arm = arm.translate((ARM_START_X, 0, 0))

    # Combine Wall and Arm
    body = body.union(arm)

    # 3. Subtract Screw Holes (R3)
    # Holes: diameter 5.5mm, axis along X, centered at (y=0, z=20) and (y=0, z=60).
    # Clearance: radius 4mm for x >= 10.
    for y_pos, z_pos in SCREW_HOLES_Y_Z:
        # The screw hole itself (must go through the wall plate at x=0)
        hole = (cq.Workplane("YZ")
                .workplane(offset=0)
                .center(y_pos, z_pos)
                .circle(SCREW_DIA / 2)
                .extrude(16)) # Extends through the wall plate (x=0 to x=15)
        
        # The clearance channel (radius 4mm, starts at x=10)
        clearance = (cq.Workplane("YZ")
                     .workplane(offset=10)
                     .center(y_pos, z_pos)
                     .circle(CLEARANCE_RAD)
                     .extrude(ARM_END_X)) # Extends to the end of the part
        
        body = body.cut(hole).cut(clearance)

    return body

result = design()