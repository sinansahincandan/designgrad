import cadquery as cq

# Constants from Design Document
L_TOTAL = 130.0
WIDTH_BASE = 30.0
WIDTH_TIP = 20.0
HEIGHT = 14.0
FLANGE_THICKNESS = 2.0
WEB_THICKNESS = 1.5

def design():
    """
    Creates the tapered I-beam drone arm by lofting three components:
    top flange, bottom flange, and web. This ensures a single continuous solid.
    """

    def create_loft_component(w_start, w_end, h, z_center):
        # We use the YZ plane to define profiles. 
        # The loft will extend along the X axis (the normal of the YZ plane).
        # rect() in a Workplane("YZ") creates a rectangle in the YZ plane.
        return (cq.Workplane("YZ")
                .workplane(offset=0)
                .rect(w_start, h)
                .workplane(offset=L_TOTAL)
                .rect(w_end, h)
                .loft(combine=True))

    # Component 1: Bottom Flange (z from -HEIGHT/2 to -HEIGHT/2 + FLANGE_THICKNESS)
    # To center the whole I-beam on Z=0, we offset the components.
    # Total height is HEIGHT. Let's range Z from -HEIGHT/2 to HEIGHT/2.
    
    # Bottom Flange: z ranges from -HEIGHT/2 to -HEIGHT/2 + FLANGE_THICKNESS
    z_bottom_center = -HEIGHT/2 + FLANGE_THICKNESS/2
    bottom_flange = create_loft_component(WIDTH_BASE, WIDTH_TIP, FLANGE_THICKNESS, z_bottom_center)
    # We must translate the component to its correct Z position because rect() is centered on origin.
    bottom_flange = bottom_flange.translate((0, 0, z_bottom_center))

    # Top Flange: z ranges from HEIGHT/2 - FLANGE_THICKNESS to HEIGHT/2
    z_top_center = HEIGHT/2 - FLANGE_THICKNESS/2
    top_flange = create_loft_component(WIDTH_BASE, WIDTH_TIP, FLANGE_THICKNESS, z_top_center)
    top_flange = top_flange.translate((0, 0, z_top_center))

    # Web: z ranges from -HEIGHT/2 + FLANGE_THICKNESS to HEIGHT/2 - FLANGE_THICKNESS
    z_web_center = 0 # Since it's symmetric
    web_h = HEIGHT - 2 * FLANGE_THICKNESS
    web = create_loft_component(WEB_THICKNESS, WEB_THICKNESS, web_h, z_web_center)
    web = web.translate((0, 0, z_web_center))

    # Combine into one solid using union
    # Note: We add a tiny overlap to ensure they are treated as one solid if needed, 
    # but since the math is exact and they touch at faces, union should work.
    arm = bottom_flange.union(top_flange).union(web)

    # R3: Frame attachment holes at (6, +-6), diameter 3.2
    # The arm exists from x=0 to x=130. Holes are on the top/bottom faces or side?
    # Design says "at (6, +-6)". This implies X=6 and Y=+/-6.
    # We'll use the top face (>Z) for hole placement logic, but we need to ensure 
    # they actually cut through the material. Since the flange is at Z ~ +/-7, 
    # a hole at (6, 6) on the XY plane will work if we select the correct face.
    
    # Let's use the top surface for all holes as it's easiest to reference.
    # We need to make sure the holes are drilled through the thickness.
    
    # R3: Frame attachment holes at (6, +-6)
    arm = arm.faces(">Z").workplane().center(6, 6).hole(3.2)
    arm = arm.faces(">Z").workplane().center(6, -6).hole(3.2)

    # R4: Motor mount holes
    # Shaft hole (diameter 6) at (120, 0)
    arm = arm.faces(">Z").workplane().center(120, 0).hole(6)
    # Four motor holes (3.2) at (120 +- 8, +-9.5)
    arm = arm.faces(">Z").workplane().center(112, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(112, -9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(128, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(128, -9.5).hole(3.2)

    return arm

result = design()