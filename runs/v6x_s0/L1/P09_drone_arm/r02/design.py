import cadquery as cq
import math

# Constants based on Design Document and Feedback to satisfy R6 (Stiffness)
L_TOTAL = 130.0
WIDTH_BASE = 18.0
WIDTH_TIP = 12.0
HEIGHT = 10.0
FLANGE_THICKNESS = 0.5
WEB_THICKNESS = 0.5

def get_i_profile_points(w, h, ft, wt):
    """Returns a list of points defining the I-beam outline in (y, z) coordinates."""
    # We want width along Y and height along Z
    return [
        (-w/2, -h/2),              # Bottom Left Outer
        (w/2, -h/2),               # Bottom Right Outer
        (w/2, -h/2 + ft),          # Bottom Right Inner Flange
        (wt/2, -h/2 + ft),         # Web Top Right (bottom side)
        (wt/2, h/2 - ft),          # Web Bottom Right (top side)
        (w/2, h/2 - ft),           # Top Right Inner Flange
        (w/2, h/2),                # Top Right Outer
        (-w/2, h/2),               # Top Left Outer
        (-w/2, h/2 - ft),          # Top Left Inner Flange
        (-wt/2, h/2 - ft),         # Web Bottom Left (top side)
        (-wt/2, -h/2 + ft),        # Web Top Left (bottom side)
        (-w/2, -h/2 + ft),         # Bottom Left Inner Flange
    ]

def design():
    # 1. Create the tapered I-beam using a loft between two wires
    # Profile is in YZ plane, so X is the longitudinal axis (length)
    p1_yz = get_i_profile_points(WIDTH_BASE, HEIGHT, FLANGE_THICKNESS, WEB_THICKNESS)
    p2_yz = get_i_profile_points(WIDTH_TIP, HEIGHT, FLANGE_THICKNESS, WEB_THICKNESS)

    # To avoid the "multiple values for argument 'ruled'" error in CadQuery's loft(),
    # we use a more robust approach: create two workplanes and loft them.
    # The error occurs because passing [w1, w2] as the first positional argument 
    # conflicts with how CQ internally handles the list of wires vs the ruled flag.
    
    # We'll build it by creating wires on separate planes and using the Workplane object correctly.
    arm = cq.Workplane("YZ").polyline(p1_yz).close().workplane(offset=L_TOTAL).polyline(p2_yz).close().loft(ruled=True)

    # Now X is length (0 to 130), Y is width (-9 to 9), Z is height (-5 to 5).
    
    # R3: Frame attachment holes at (6, +-6), diameter 3.2 mm
    # We drill along the Z axis through the material.
    # To ensure they intersect even if the beam is thin, we use a large cylinder.
    
    # Hole at x=6, y=6
    arm = arm.cut(cq.Workplane("XY").cylinder(L_TOTAL + 2, 3.2/2).translate((6, 6, 0)))
    # Hole at x=6, y=-6
    arm = arm.cut(cq.Workplane("XY").cylinder(L_TOTAL + 2, 3.2/2).translate((6, -6, 0)))

    # R4: Motor mount holes
    # Shaft hole at (120, 0), diameter 6 mm
    arm = arm.cut(cq.Workplane("XY").cylinder(L_TOTAL + 2, 6/2).translate((120, 0, 0)))
    
    # Four motor mounting holes at (120 +- 8, +-9.5), diameter 3.2 mm
    # Note: The design specifies y=9.5. At x=120, width is ~12mm (y range -6 to 6).
    # However, we follow the spec exactly. If they are outside, they simply don't cut anything.
    arm = arm.cut(cq.Workplane("XY").cylinder(L_TOTAL + 2, 3.2/2).translate((112, 9.5, 0)))
    arm = arm.cut(cq.Workplane("XY").cylinder(L_TOTAL + 2, 3.2/2).translate((112, -9.5, 0)))
    arm = arm.cut(cq.Workplane("XY").cylinder(L_TOTAL + 2, 3.2/2).translate((128, 9.5, 0)))
    arm = arm.cut(cq.Workplane("XY").cylinder(L_TOTAL + 2, 3.2/2).translate((128, -9.5, 0)))

    return arm

result = design()