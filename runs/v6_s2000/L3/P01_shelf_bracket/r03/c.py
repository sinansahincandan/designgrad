import cadquery as cq
import math

# Constants
WIDTH = 40.0
SHELF_TOP_Z = 110.0
ARM_LENGTH = 150.0
SCREW_HOLES = [(0, 20), (0, 60)]
SCREW_DIA = 5.5
CLEARANCE_DIA = 8.2  # Must be >= 8mm to satisfy R3 (4mm radius)

def design():
    """
    Builds a tapered, hollowed cantilever bracket.
    Uses a single base primitive and subtractions to ensure R1 compliance.
    """
    
    # 1. Create the Main Body (Base Primitive)
    # Base block: x from 0 to 150, y from -20 to 20, z from 0 to 110
    # We use centered=False so min corner is at (0,0,0)
    base_body = cq.Workplane("XY").box(ARM_LENGTH, WIDTH, SHELF_TOP_Z, centered=(False, False, False))

    # 2. Define Tapering and Hollow Geometry
    # To ensure a single solid, we must make sure the subtractions don't slice the body into pieces.
    # The previous error occurred because wedge_cut and hollow_void were translated to x=15,
    # but their extrusion/offset logic caused them to be separate from the wall plate (x < 15).
    
    # We will define the subtractions starting from x=15 and extending to x=140.
    # To ensure they overlap with the wall plate for a clean boolean, we'll start them at x=14.
    
    # Create a tapered wedge to cut out the bottom part of the arm (to create L-shape)
    # We use XZ plane. The polyline defines the shape in the XZ plane.
    wedge_cut = (cq.Workplane("XZ")
                 .workplane(offset=14) # Start at x=14 to overlap wall plate
                 .polyline([
                     (0, 0),               # At x=14, z=0
                     (126, 80),            # At x=140, z=80
                     (126, 110),           # Up to top surface at x=140
                     (0, 110)              # Back to start at x=14
                 ])
                 .close()
                 .extrude(WIDTH + 2, both=True) # Extrude across Y (centered on y=0)
                 .translate((14, 0, 0))         # Move to correct X position
                )
    
    # Now we have an L-shape. To satisfy R7 (Mass), we hollow it out.
    # We subtract a tapered internal void from x=15 to x=140.
    hollow_void = (cq.Workplane("XZ")
                   .workplane(offset=14) # Start at x=14 to overlap wall plate
                   .polyline([
                       (0, 10),              # Bottom thickness at root
                       (126, 30),            # Tapered bottom
                       (126, 100),           # Top thickness
                       (0, 100)              # Back to start
                   ])
                   .close()
                   .extrude(WIDTH - 6, both=True) # Thinner width for hollow
                   .translate((14, 0, 0))
                  )

    # Combine the base and subtract the shapes
    body = base_body.cut(wedge_cut).cut(hollow_void)

    # 3. Screw Holes (R3)
    # Holes at y=0, z=20 and y=0, z=60. Axis along X.
    for z_pos in [20, 60]:
        # The actual screw hole (5.5mm) through the wall plate
        h = (cq.Workplane("YZ")
             .workplane(offset=0)
             .center(0, z_pos)
             .circle(SCREW_DIA / 2)
             .extrude(16) # Through the wall plate
            )
        # The clearance channel (8.2mm) starting at x=10
        c = (cq.Workplane("YZ")
             .workplane(offset=10)
             .center(0, z_pos)
             .circle(CLEARANCE_DIA / 2)
             .extrude(ARM_LENGTH + 10) # Ensure it goes through the whole arm
            )
        body = body.cut(h).cut(c)

    # Final result
    result = body
    return result

result = design()