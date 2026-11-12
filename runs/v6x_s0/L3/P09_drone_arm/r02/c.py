import cadquery as cq

# Constants from Design Document
L_TOTAL = 130.0
WIDTH_BASE = 30.0
WIDTH_TIP = 20.0
HEIGHT = 14.0
FLANGE_THICKNESS = 1.5
WEB_THICKNESS = 1.0

def get_i_profile_points(width, height, flange_t, web_t):
    """Returns the points for an I-beam profile."""
    half_w = width / 2.0
    half_h = height / 2.0
    f_t = flange_t
    w_t = web_t
    
    pts = [
        (-half_w, -half_h), (half_w, -half_h), (half_w, -half_h + f_t), 
        (w_t/2, -half_h + f_t), (w_t/2, half_h - f_t), (half_w, half_h - f_t), 
        (half_w, half_h), (-half_w, half_h), (-half_w, half_h - f_t), 
        (-w_t/2, half_h - f_t), (-w_t/2, -half_h + f_t), (-half_w, -half_h + f_t)
    ]
    return pts

# 1. Create the Tapered I-Beam using Loft
# Instead of Sketch objects which can be tricky with lofting in some CQ versions,
# we use Workplane.polyline().close() to create profiles directly on workplanes.

# Profile at x=0
p1 = get_i_profile_points(WIDTH_BASE, HEIGHT, FLANGE_THICKNESS, WEB_THICKNESS)
# Profile at x=L_TOTAL
p2 = get_i_profile_points(WIDTH_TIP, HEIGHT, FLANGE_THICKNESS, WEB_THICKNESS)

arm = (
    cq.Workplane("YZ")
    .polyline(p1).close().extrude(0.1) # Dummy extrusion to create a face if needed, but loft works on wires/faces
)

# A more robust way for Loft in CadQuery: 
# Create two workplanes at different offsets and use them to loft.
arm = (
    cq.Workplane("YZ")
    .workplane(offset=0)
    .polyline(p1).close()
    .workplane(offset=L_TOTAL)
    .polyline(p2).close()
    .loft(combine=True)
)

# 2. Coordinate Alignment: Ensure underside is at z=0
# The lofted part is centered on the YZ plane (y=0, z=0).
arm = arm.translate((0, 0, HEIGHT / 2.0))

# 3. Subtract Holes (R3 & R4)
HOLE_HEIGHT = HEIGHT + 10.0 

# R3: Frame attachment holes at (6, +-6) diameter 3.2
r3_holes = (
    cq.Workplane("XY")
    .pushPoints([(6, 6), (6, -6)])
    .cylinder(HOLE_HEIGHT, 3.2/2.0)
    .translate((0, 0, -HOLE_HEIGHT/2))
)

# R4: Motor mount holes at (112, +-9.5) and (128, +-9.5) diameter 3.2
r4_motor_holes = (
    cq.Workplane("XY")
    .pushPoints([
        (112, 9.5), (112, -9.5), 
        (128, 9.5), (128, -9.5)
    ])
    .cylinder(HOLE_HEIGHT, 3.2/2.0)
    .translate((0, 0, -HOLE_HEIGHT/2))
)

# R4: Shaft clearance hole at (120, 0) diameter 6
r4_shaft_hole = (
    cq.Workplane("XY")
    .pushPoints([(120, 0)])
    .cylinder(HOLE_HEIGHT, 6.0/2.0)
    .translate((0, 0, -HOLE_HEIGHT/2))
)

# Perform subtractions
arm = arm.cut(r3_holes)
arm = arm.cut(r4_motor_holes)
arm = arm.cut(r4_shaft_hole)

result = arm