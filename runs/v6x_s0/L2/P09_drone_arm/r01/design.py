import cadquery as cq

# Constants from Design Document
L_TOTAL = 130.0
HEIGHT = 14.0
WIDTH_BASE = 30.0
WIDTH_TIP = 20.0
FLANGE_THICKNESS = 1.5
WEB_THICKNESS = 1.2

def design():
    # To create a lofted solid in CadQuery, we can define the profiles on different planes
    # and use the loft method. A robust way is to create two workplanes with wires.
    
    # Profile 1 at x=0 (YZ plane)
    p1_wire = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .polyline([
            (-WIDTH_BASE/2, 0),                  # Bottom Left
            (WIDTH_BASE/2, 0),                   # Bottom Right
            (WIDTH_BASE/2, FLANGE_THICKNESS),    # Flange Right Bottom
            (WEB_THICKNESS/2, FLANGE_THICKNESS), # Web Right Bottom
            (WEB_THICKNESS/2, HEIGHT - FLANGE_THICKNESS), # Web Right Top
            (WIDTH_BASE/2, HEIGHT - FLANGE_THICKNESS),    # Flange Right Top
            (WIDTH_BASE/2, HEIGHT),              # Top Right
            (-WIDTH_BASE/2, HEIGHT),             # Top Left
            (-WIDTH_BASE/2, HEIGHT - FLANGE_THICKNESS),   # Flange Left Top
            (-WEB_THICKNESS/2, HEIGHT - FLANGE_THICKNESS), # Web Left Top
            (-WEB_THICKNESS/2, FLANGE_THICKNESS),    # Web Left Bottom
            (-WIDTH_BASE/2, FLANGE_THICKNESS)    # Flange Left Bottom
        ])
        .close()
    ).vertices().each(lambda loc: loc) # This is a trick to get the wire via vals()

    # Profile 2 at x=L_TOTAL (YZ plane)
    p2_wire = (
        cq.Workplane("YZ")
        .workplane(offset=L_TOTAL)
        .polyline([
            (-WIDTH_TIP/2, 0),                   # Bottom Left
            (WIDTH_TIP/2, 0),                    # Bottom Right
            (WIDTH_TIP/2, FLANGE_THICKNESS),     # Flange Right Bottom
            (WEB_THICKNESS/2, FLANGE_THICKNESS), # Web Right Bottom
            (WEB_THICKNESS/2, HEIGHT - FLANGE_THICKNESS), # Web Right Top
            (WIDTH_TIP/2, HEIGHT - FLANGE_THICKNESS),     # Flange Right Top
            (WIDTH_TIP/2, HEIGHT),               # Top Right
            (-WIDTH_TIP/2, HEIGHT),              # Top Left
            (-WIDTH_TIP/2, HEIGHT - FLANGE_THICKNESS),    # Flange Left Top
            (-WEB_THICKNESS/2, HEIGHT - FLANGE_THICKNESS), # Web Left Top
            (-WEB_THICKNESS/2, FLANGE_THICKNESS),    # Web Left Bottom
            (-WIDTH_TIP/2, FLANGE_THICKNESS)     # Flange Left Bottom
        ])
        .close()
    ).vertices().each(lambda loc: loc)

    # In CadQuery 2.x, lofting can be done by passing the wires to a Workplane
    # We create a workplane and add the wires from p1 and p2
    arm = cq.Workplane("XY").loft([p1_wire.vals()[0], p2_wire.vals()[0]])

    # 3. Subtractive Boolean Operations for Holes
    # The lofted object has X as length, Y as width, Z as height.
    # We use the top face (>Z) to drill holes through the whole part.
    
    # R3: Frame attachment holes (6, +-6), diameter 3.2
    arm = arm.faces(">Z").workplane().center(6, 6).hole(3.2)
    arm = arm.faces(">Z").workplane().center(6, -6).hole(3.2)

    # R4: Motor mount holes
    # Shaft hole (120, 0), diameter 6
    arm = arm.faces(">Z").workplane().center(120, 0).hole(6)
    
    # Four motor mounting holes (120 +- 8, +- 9.5), diameter 3.2
    arm = arm.faces(">Z").workplane().center(112, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(112, -9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(128, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(128, -9.5).hole(3.2)

    return arm

# Re-implementing design using a more direct loft approach to ensure success
def design_fixed():
    # Create the two profiles as wires
    def get_wire(w, h, ft, wt, offset):
        return cq.Workplane("YZ").workplane(offset=offset).polyline([
            (-w/2, 0), (w/2, 0), (w/2, ft), (wt/2, ft), (wt/2, h-ft), 
            (w/2, h-ft), (w/2, h), (-w/2, h), (-w/2, h-ft), 
            (-wt/2, h-ft), (-wt/2, ft), (-w/2, ft)
        ]).close().vals()[0]

    wire1 = get_wire(WIDTH_BASE, HEIGHT, FLANGE_THICKNESS, WEB_THICKNESS, 0)
    wire2 = get_wire(WIDTH_TIP, HEIGHT, FLANGE_THICKNESS, WEB_THICKNESS, L_TOTAL)
    
    arm = cq.Workplane("XY").loft([wire1, wire2])

    # Holes
    arm = arm.faces(">Z").workplane().center(6, 6).hole(3.2)
    arm = arm.faces(">Z").workplane().center(6, -6).hole(3.2)
    arm = arm.faces(">Z").workplane().center(120, 0).hole(6)
    arm = arm.faces(">Z").workplane().center(112, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(112, -9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(128, 9.5).hole(3.2)
    arm = arm.faces(">Z").workplane().center(128, -9.5).hole(3.2)
    
    return arm

result = design_fixed()