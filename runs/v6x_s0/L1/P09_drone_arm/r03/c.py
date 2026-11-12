import cadquery as cq

def design_final():
    # Design Constants
    L_TOTAL = 130.0
    H = 14.0
    W_START = 30.0
    W_END = 20.0
    TF = 1.5
    TW = 2.0

    def get_i_profile_pts(w, h, tf, tw):
        # Returns a list of points for the I-beam cross section in YZ plane
        # The profile is centered on Y=0 and starts at Z=0
        # Points: (y, z)
        pts = [
            (-w/2, 0),           # Bottom left corner
            (w/2, 0),            # Bottom right corner
            (w/2, tf),           # Bottom flange top-right
            (tw/2, tf),          # Web bottom-right
            (tw/2, h - tf),      # Web top-right
            (w/2, h - tf),       # Top flange bottom-right
            (w/2, h),            # Top flange top-right
            (-w/2, h),           # Top flange top-left
            (-w/2, h - tf),      # Top flange bottom-left
            (-tw/2, h - tf),     # Web top-left
            (-tw/2, tf),         # Web bottom-left
            (-w/2, tf)           # Bottom flange top-left
        ]
        return pts

    # To avoid the "More than one wire" error caused by .add() behavior in some CQ versions,
    # we create a single Workplane and use multiple .polyline().close() calls 
    # on different offsets to populate the workplane with wires.
    
    p1_pts = get_i_profile_pts(W_START, H, TF, TW)
    p2_pts = get_i_profile_pts(W_END, H, TF, TW)

    # We start on YZ plane at x=0. 
    # Then we move to x=L and add the second profile.
    arm = (cq.Workplane("YZ")
           .workplane(offset=0)
           .polyline(p1_pts).close()
           .workplane(offset=L_TOTAL)
           .polyline(p2_pts).close()
           .loft())

    # Hole drilling using absolute coordinates relative to the top face (0, 0, H)
    # R3: Frame attachment holes at (6, +- 6), diameter 3.2
    arm = arm.faces(">Z").workplane().center(6, 6).hole(3.2)
    arm = arm.faces(">Z").workplane().center(6, -6).hole(3.2)

    # R4: Motor mount holes
    # Shaft hole at (120, 0), diameter 6
    arm = arm.faces(">Z").workplane().center(120, 0).hole(6)

    # Four motor holes at (120 +- 8, +-9.5), diameter 3.2
    arm = arm.faces(">Z").workplane().center(112, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(112, -9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(128, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(128, -9.5).hole(3.2)

    return arm

result = design_final()