import cadquery as cq
import math

def design():
    # Constants from Design Document
    L = 130.0
    H = 14.0
    W_START = 30.0
    W_END = 20.0
    FT = 2.0  # Flange thickness
    WT = 1.5  # Web thickness

    # The I-shape is defined in the YZ plane.
    # Points in (y, z) coordinates:
    def get_i_points(w, h, ft, wt):
        return [
            (-w/2, 0), (w/2, 0), (w/2, ft), (wt/2, ft), 
            (wt/2, h-ft), (w/2, h-ft), (w/2, h), (-w/2, h), 
            (-w/2, h-ft), (-wt/2, h-ft), (-wt/2, ft), (-w/2, ft)
        ]

    # Create the lofted I-beam.
    # We start on YZ plane at x=0 and move to x=L.
    p1 = get_i_points(W_START, H, FT, WT)
    p2 = get_i_points(W_END, H, FT, WT)

    arm = (cq.Workplane("YZ")
           .polyline(p1).close()
           .workplane(offset=L)
           .polyline(p2).close()
           .loft(combine=True))

    # The lofted object extends from x=0 to x=L along the X axis.
    # Its height H is along the Z axis.
    # We need vertical holes (along Z axis). 
    # We select the top face (>Z) and create a workplane on it.
    # The centroid of the top face will be at approximately x=L/2, y=0.
    
    arm = arm.faces(">Z").workplane()
    
    # Find the center of the top face to align our coordinate system.
    # Since we lofted from 0 to L, the centroid is roughly (L/2, 0).
    # We move the workplane origin back to X=0, Y=0 relative to the global frame.
    # In CadQuery, after .faces(">Z").workplane(), the new origin is at the face's center.
    # To place holes at absolute (x, y), we calculate the offset from current origin.
    
    # A more robust way: find the bounding box or just use a known point.
    # The centroid of a trapezoidal top face for x in [0, L] is roughly L/2.
    arm = arm.center(-L/2, 0)

    # R3: Frame holes (x=6, y=6 and x=6, y=-6)
    # Note: We use .hole() which drills through the thickness of the solid at that point.
    # Since we are on the top face, it will drill downwards.
    arm = arm.center(6, 6).hole(3.2)
    arm = arm.center(0, -12).hole(3.2)

    # R4: Motor mount and shaft (x=120, y=0 is the center)
    # Shaft hole at (120, 0)
    arm = arm.center(120, 0).hole(6)
    
    # Motor holes at (112, +-9.5) and (128, +-9.5)
    # Relative to the shaft hole at (120, 0):
    arm = arm.center(-8, 9.5).hole(3.2)   # (112, 9.5)
    arm = arm.center(0, -19).hole(3.2)    # (112, -9.5)
    arm = arm.center(16, 19).hole(3.2)    # (128, 9.5)
    arm = arm.center(0, -19).hole(3.2)    # (128, -9.5)

    return arm

result = design()