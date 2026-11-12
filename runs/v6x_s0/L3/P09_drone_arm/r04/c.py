import cadquery as cq

# Constants from Design Document
L_TOTAL = 130.0
WIDTH_BASE = 30.0
WIDTH_TIP = 20.0
HEIGHT = 14.0
FLANGE_THICKNESS = 1.5
WEB_THICKNESS = 1.0

def get_i_profile_points(width, height, flange_t, web_t):
    """
    Returns a list of (y, z) points for an I-beam profile.
    The bottom flange starts at z=0.
    """
    # Points ordered to form a closed loop: 
    # Bottom edge -> Right flange -> Web side -> Top flange -> Left flange -> Web side
    return [
        (-width/2, 0),               # Bottom-left
        (width/2, 0),                # Bottom-right
        (width/2, flange_t),         # Up to top of bottom flange (right)
        (web_t/2, flange_t),         # Inward to web (right)
        (web_t/2, height - flange_t),# Up to bottom of top flange (right)
        (width/2, height - flange_t),# Outward to top flange (right)
        (width/2, height),           # Top-right corner
        (-width/2, height),          # Top-left corner
        (-width/2, height - flange_t),# Down to bottom of top flange (left)
        (-web_t/2, height - flange_t),# Inward to web (left)
        (-web_t/2, flange_t),        # Down to top of bottom flange (left)
        (-width/2, flange_t),        # Outward to bottom flange (left)
    ]

def make_arm():
    # 1. Create the tapered I-beam using lofting between two YZ profiles
    pts_base = get_i_profile_points(WIDTH_BASE, HEIGHT, FLANGE_THICKNESS, WEB_THICKNESS)
    pts_tip = get_i_profile_points(WIDTH_TIP, HEIGHT, FLANGE_THICKNESS, WEB_THICKNESS)

    # In CadQuery lofting works best by creating two workplanes at different offsets 
    # and then calling loft on the combined object.
    # We create a single Workplane and add two separate sketches to it.
    
    arm = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .polyline(pts_base)
        .close()
        .workplane(offset=L_TOTAL)
        .polyline(pts_tip)
        .close()
        .loft(ruled=True)
    )

    # 2. Create Subtractive Holes (Vertical cylinders parallel to Z-axis)
    # The design specifies holes are vertical (parallel to Z).
    # To cut through the entire part, we create cylinders along the Z axis.
    # Since the arm is oriented along X, and height is in Z, 
    # a cylinder along Z with length > HEIGHT will pass through.
    
    # We need to ensure the holes are positioned correctly in XY.
    # The lofted part exists from x=0 to x=130.
    # Holes must be centered at (x, y) and extend through the thickness (z).
    
    # R3: Frame attachment holes (6, +-6), diameter 3.2
    h_frame1 = cq.Workplane("XY").workplane(offset=0).center(6, 6).cylinder(HEIGHT + 10, 3.2/2).translate((0,0,-5))
    h_frame2 = cq.Workplane("XY").workplane(offset=0).center(6, -6).cylinder(HEIGHT + 10, 3.2/2).translate((0,0,-5))

    # R4: Motor mount holes (112, +-9.5) and (128, +-9.5), diameter 3.2
    h_motor1 = cq.Workplane("XY").workplane(offset=0).center(112, 9.5).cylinder(HEIGHT + 10, 3.2/2).translate((0,0,-5))
    h_motor2 = cq.Workplane("XY").workplane(offset=0).center(112, -9.5).cylinder(HEIGHT + 10, 3.2/2).translate((0,0,-5))
    h_motor3 = cq.Workplane("XY").workplane(offset=0).center(128, 9.5).cylinder(HEIGHT + 10, 3.2/2).translate((0,0,-5))
    h_motor4 = cq.Workplane("XY").workplane(offset=0).center(128, -9.5).cylinder(HEIGHT + 10, 3.2/2).translate((0,0,-5))

    # R4: Shaft clearance hole (120, 0), diameter 6
    h_shaft = cq.Workplane("XY").workplane(offset=0).center(120, 0).cylinder(HEIGHT + 10, 6/2).translate((0,0,-5))

    # Combine all holes into one object for a single boolean cut operation
    all_holes = h_frame1.union(h_frame2)\
                       .union(h_motor1).union(h_motor2)\
                       .union(h_motor3).union(h_motor4)\
                       .union(h_shaft)

    # Perform the cut to ensure R1 (one single solid)
    result = arm.cut(all_holes)

    return result

result = make_arm()