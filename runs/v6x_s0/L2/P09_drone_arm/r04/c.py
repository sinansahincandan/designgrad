import cadquery as cq

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

    # Create the tapered I-beam using lofting.
    # We start on YZ plane at x=0 and move to x=L.
    p1 = get_i_points(W_START, H, FT, WT)
    p2 = get_i_points(W_END, H, FT, WT)

    arm = (cq.Workplane("YZ")
           .polyline(p1).close()
           .workplane(offset=L)
           .polyline(p2).close()
           .loft(combine=True))

    # The lofted object extends from x=0 to x=L along the X axis.
    # Its height H is along the Z axis (from z=0 to z=H).
    # To place holes at absolute (x, y) coordinates:
    # 1. Select the top face (>Z).
    # 2. The current origin of that workplane is the centroid of the top face.
    # 3. For a linear taper from W_START to W_END over L, the center at x is:
    #    y_center = 0 (symmetric)
    #    x_center(x) = x. However, we need to move the workplane origin back to global (0,0).
    # Since the lofted body's X-range is [0, L], and it is symmetric about Y=0:
    # The centroid of the top face in X is roughly L/2. 
    # We use .center(L/2, 0) to shift the workplane origin from (L/2, 0) back to (0,0).

    top_face = arm.faces(">Z")
    
    # Create a workplane on top face and move its origin to global (0,0)
    # We use L/2 because the lofted body's X-axis is centered at roughly L/2 in the local face frame.
    workplane = top_face.workplane().center(L/2, 0)

    # R3: Frame holes (x=6, y=6 and x=6, y=-6)
    arm = workplane.pushPoints([(6, 6), (6, -6)]).hole(3.2)

    # R4: Motor mount and shaft
    # Shaft hole at (120, 0) diameter 6mm
    arm = workplane.center(120, 0).hole(6)
    
    # Reset to the original top face workplane origin to place motor holes accurately
    # Or more simply, use absolute coordinates relative to our established (0,0)
    workplane_for_motor = top_face.workplane().center(L/2, 0)
    
    # Motor mount holes at (120 +- 8, +-9.5) -> (112, 9.5), (112, -9.5), (128, 9.5), (128, -9.5)
    motor_holes = [(112, 9.5), (112, -9.5), (128, 9.5), (128, -9.5)]
    arm = workplane_for_motor.pushPoints(motor_holes).hole(3.2)

    return arm

result = design()