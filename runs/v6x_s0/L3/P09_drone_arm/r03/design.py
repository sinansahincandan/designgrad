import cadquery as cq

# Constants from Design Document
L_TOTAL = 130.0
WIDTH_BASE = 30.0
WIDTH_TIP = 20.0
HEIGHT = 14.0
FLANGE_THICKNESS = 1.5
WEB_THICKNESS = 1.0

def make_arm():
    # To avoid the unreliable .loft() behavior with multiple workplanes, 
    # we will construct the tapered flanges by creating a single polygon 
    # representing the side profile and extruding it or using a more robust method.
    
    # A reliable way to create a tapered flange is to define its 8 vertices 
    # (4 for bottom face, 4 for top face) and use a loft between two faces.
    # However, since we need one single solid, let's build the flanges by 
    # creating the side profile in the XY plane and extruding it along Z.
    # But the width varies with X. So we define the flange as a collection of 
    # trapezoids or use the lofting approach correctly by providing wires to a single Workplane.

    def create_flange(z_min):
        # We define two wires on the YZ plane at different X offsets.
        # Wire 1 at x=0
        w1 = cq.Workplane("YZ").workplane(offset=0).polyline([
            (-WIDTH_BASE/2, z_min), 
            (WIDTH_BASE/2, z_min), 
            (WIDTH_BASE/2, z_min + FLANGE_THICKNESS), 
            (-WIDTH_BASE/2, z_min + FLANGE_THICKNESS)
        ]).close().wires()[0]
        
        # Wire 2 at x=L_TOTAL
        w2 = cq.Workplane("YZ").workplane(offset=L_TOTAL).polyline([
            (-WIDTH_TIP/2, z_min), 
            (WIDTH_TIP/2, z_min), 
            (WIDTH_TIP/2, z_min + FLANGE_THICKNESS), 
            (-WIDTH_TIP/2, z_min + FLANGE_THICKNESS)
        ]).close().wires()[0]
        
        # We must create a single Workplane and add these wires to it.
        return cq.Workplane("YZ").add(w1).add(w2).loft()

    # 1. Create Bottom Flange (z from 0 to 1.5)
    bottom_flange = create_flange(0)

    # 2. Create Top Flange (z from 12.5 to 14)
    top_flange = create_flange(HEIGHT - FLANGE_THICKNESS)

    # 3. Create Web (constant width, connects flanges)
    web_h = HEIGHT - 2 * FLANGE_THICKNESS
    # The web is a box from x=0 to L, y=-WEB/2 to WEB/2, z=FLANGE to HEIGHT-FLANGE
    web = cq.Workplane("XY").box(L_TOTAL, WEB_THICKNESS, web_h)
    # Translate: X center (L/2), Y center (0), Z center (FLANGE + web_h/2)
    web = web.translate((L_TOTAL / 2, 0, FLANGE_THICKNESS + web_h / 2))

    # 4. Union components into one solid
    arm = bottom_flange.union(top_flange).union(web)

    # 5. Create Holes (R3 & R4)
    def create_vertical_hole(x, y, diameter):
        # Cylinder spanning the full height of the part
        return cq.Workplane("XY").workplane(offset=0).center(x, y).cylinder(HEIGHT + 2, diameter / 2).translate((0, 0, -1))

    # R3: Frame attachment holes at (6, +-6), diameter 3.2
    h1 = create_vertical_hole(6, 6, 3.2)
    h2 = create_vertical_hole(6, -6, 3.2)
    
    # R4: Motor mount holes at (120 +- 8, +-9.5), diameter 3.2
    m1 = create_vertical_hole(120 + 8, 9.5, 3.2)
    m2 = create_vertical_hole(120 + 8, -9.5, 3.2)
    m3 = create_vertical_hole(120 - 8, 9.5, 3.2)
    m4 = create_vertical_hole(120 - 8, -9.5, 3.2)
    
    # R4: Shaft hole at (120, 0), diameter 6.0
    s1 = create_vertical_hole(120, 0, 6.0)

    all_holes = h1.union(h2).union(m1).union(m2).union(m3).union(m4).union(s1)
    result = arm.cut(all_holes)

    return result

# The lofting logic in CadQuery requires the wires to be on the same Workplane object 
# but at different offsets. We use a helper function that creates them and adds them.
def create_flange_robust(z_min):
    # Create wire 1 at x=0
    w1 = cq.Workplane("YZ").workplane(offset=0).polyline([
        (-WIDTH_BASE/2, z_min), (WIDTH_BASE/2, z_min), 
        (WIDTH_BASE/2, z_min + FLANGE_THICKNESS), (-WIDTH_BASE/2, z_min + FLANGE_THICKNESS)
    ]).close().wires()[0]
    # Create wire 2 at x=L
    w2 = cq.Workplane("YZ").workplane(offset=L_TOTAL).polyline([
        (-WIDTH_TIP/2, z_min), (WIDTH_TIP/2, z_min), 
        (WIDTH_TIP/2, z_min + FLANGE_THICKNESS), (-WIDTH_TIP/2, z_min + FLANGE_THICKNESS)
    ]).close().wires()[0]
    return cq.Workplane("YZ").add(w1).add(w2).loft()

# Re-implementing make_arm with the robust function
def make_arm_final():
    bottom = create_flange_robust(0)
    top = create_flange_robust(HEIGHT - FLANGE_THICKNESS)
    web_h = HEIGHT - 2 * FLANGE_THICKNESS
    web = cq.Workplane("XY").box(L_TOTAL, WEB_THICKNESS, web_h).translate((L_TOTAL/2, 0, FLANGE_THICKNESS + web_h/2))
    arm = bottom.union(top).union(web)
    
    def create_hole(x, y, d):
        return cq.Workplane("XY").workplane(offset=0).center(x,y).cylinder(HEIGHT+2, d/2).translate((0,0,-1))

    holes = create_hole(6, 6, 3.2).union(create_hole(6, -6, 3.2))\
            .union(create_hole(128, 9.5, 3.2)).union(create_hole(128, -9.5, 3.2))\
            .union(create_hole(112, 9.5, 3.2)).union(create_hole(112, -9.5, 3.2))\
            .union(create_hole(120, 0, 6.0))
    return arm.cut(holes)

result = make_arm_final()