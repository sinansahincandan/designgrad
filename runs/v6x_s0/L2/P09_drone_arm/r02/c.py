import cadquery as cq

# Constants from Design Document
L_TOTAL = 130.0
W_BASE = 30.0
W_TIP = 20.0
HEIGHT = 14.0
WALL_THICKNESS = 1.2
WEB_THICKNESS = 1.2

def i_profile_points(w, h, wt, ft):
    """Returns points for an I-shape outline in the YZ plane."""
    half_w = w / 2.0
    half_h = h / 2.0
    # Points for an I-shape outline (clockwise)
    return [
        (-half_w,  half_h),              # Top left outer
        ( half_w,  half_h),              # Top right outer
        ( half_w,  half_h - ft),         # Top right inner corner 1
        ( wt/2,    half_h - ft),         # Top right inner corner 2 (web start)
        ( wt/2,   -half_h + ft),         # Bottom right inner corner 1 (web end)
        ( half_w, -half_h + ft),         # Bottom right inner corner 2
        ( half_w, -half_h),              # Bottom right outer
        (-half_w, -half_h),              # Bottom left outer
        (-half_w, -half_h + ft),         # Bottom left inner corner 1
        (-wt/2,   -half_h + ft),         # Bottom left inner corner 2
        (-wt/2,    half_h - ft),         # Top left inner corner 1
        (-half_w,  half_h - ft),         # Top left inner corner 2
    ]

def design():
    # To avoid the "More than one wire or face is required" error in loft(),
    # we must ensure that the Workplane object contains multiple wires/faces 
    # in its internal list before calling loft().
    # The most reliable way to create a single solid I-beam with taper is:
    # 1. Create two separate Workplanes for the profiles.
    # 2. Use cq.Workplane("YZ").add(wire1).add(wire2) which puts both wires into one object.
    # However, if 'add' fails to register them as distinct wires for lofting, 
    # we can use a single Workplane and create the profiles using multiple polyline calls.

    # Create the first wire (at x=0)
    w1 = cq.Workplane("YZ").polyline(i_profile_points(W_BASE, HEIGHT, WEB_THICKNESS, WALL_THICKNESS)).close()
    
    # Create the second wire (at x=L)
    # We use a separate Workplane to define the geometry and then add it.
    w2 = cq.Workplane("YZ").workplane(offset=L_TOTAL).polyline(i_profile_points(W_TIP, HEIGHT, WEB_THICKNESS, WALL_THICKNESS)).close()
    
    # Combine them into a single Workplane object and loft.
    # We use the first wire's workplane as the base and add the second one.
    arm = w1.add(w2).loft()

    # R3: Frame attachment holes (6, +-6), diameter 3.2
    # Holes are vertical (along Z axis). Create a workplane on the top face (>Z).
    # We use hole() which cuts through the solid.
    arm = arm.faces(">Z").workplane().pushPoints([(6, 6), (6, -6)]).hole(3.2)

    # R4: Motor mount holes
    # Shaft hole (120, 0), diameter 6
    arm = arm.faces(">Z").workplane().pushPoints([(120, 0)]).hole(6)
    
    # Motor holes (120 +- 8, +- 9.5), diameter 3.2
    motor_holes = [
        (112, 9.5), (112, -9.5), (128, 9.5), (128, -9.5)
    ]
    arm = arm.faces(">Z").workplane().pushPoints(motor_holes).hole(3.2)

    return arm

# If the loft error persists due to how 'add' works in specific CQ versions, 
# we can use a fallback: create two solids and union them? No, that won't taper correctly.
# Let's try one more approach for the lofting logic.

def design_final():
    # Create wire 1
    w1 = cq.Workplane("YZ").polyline(i_profile_points(W_BASE, HEIGHT, WEB_THICKNESS, WALL_THICKNESS)).close()
    # Create wire 2
    w2 = cq.Workplane("YZ").polyline(i_profile_points(W_TIP, HEIGHT, WEB_THICKNESS, WALL_THICKNESS)).close().translate((L_TOTAL, 0, 0))
    
    # In some CQ versions, 'loft' needs to be called on a Workplane that has multiple wires.
    # We use the add() method which is intended for this.
    arm = w1.add(w2).loft()

    # R3: Frame attachment holes (6, +-6), diameter 3.2
    arm = arm.faces(">Z").workplane().pushPoints([(6, 6), (6, -6)]).hole(3.2)

    # R4: Motor mount holes
    arm = arm.faces(">Z").workplane().pushPoints([(120, 0)]).hole(6)
    motor_holes = [(112, 9.5), (112, -9.5), (128, 9.5), (128, -9.5)]
    arm = arm.faces(">Z").workplane().pushPoints(motor_holes).hole(3.2)

    return arm

result = design_final()