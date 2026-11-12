import cadquery as cq

# Constants from Design Document & Feedback
L_total = 130.0
hole_dia = 3.2
shaft_dia = 6.0

# Geometry dimensions to balance R5 (Strength) and R6 (Stiffness/I <= 1)
base_width = 0.5  
base_height = 18.0 
base_length = 30.0

web_width = 0.5
web_height = 18.0
web_length = 80.0 

mount_width = 24.0
mount_depth = 12.0
mount_height = 12.0
mount_length = 20.0 

# To ensure R3 holes (at y=6) actually hit the solid, we must widen the base at those points.
# The design doc says "thin vertical blade", but for a single valid solid with holes at +/- 6,
# there must be material at y = +/- 6. We will add two small mounting tabs to the base.
base_tabs = (
    cq.Workplane("XY")
    .box(base_length, 15.0, base_height, centered=(False, False, False))
    .translate((0, -7.5, 0)) # Center a wide block to cover y in [-7.5, 7.5]
)
# However, the design doc calls for a thin blade at x=20. 
# Let's instead create the base as a single piece that is wider where needed or just use a wider base.
# To satisfy R3 (holes at y=6), we'll make the base width 15mm to ensure connectivity.

base = cq.Workplane("XY").box(base_length, 15.0, base_height, centered=(False, False, False))

# Web section
web = (
    cq.Workplane("XY")
    .box(web_length, web_width, web_height, centered=(False, False, False))
    .translate((base_length, 0, 0))
)

# Motor mount flange
mount = (
    cq.Workplane("XY")
    .box(mount_length, mount_width, mount_height, centered=(False, False, False))
    .translate((base_length + web_length, 0, 0))
)

# Combine into one solid using union
arm_body = base.union(web).union(mount)

# Start with the arm body as the result
result = arm_body

# R3: Frame attachment holes at (6, 6) and (6, -6)
# We use a cylinder to cut through the solid to avoid "findSolid" errors on empty workplanes.
# The cylinders are oriented along Z.
cyl1 = cq.Workplane("XY").cylinder(base_height + 2, hole_dia/2).translate((6, 6, -1))
cyl2 = cq.Workplane("XY").cylinder(base_height + 2, hole_dia/2).translate((6, -6, -1))

# R4: Motor mount holes
# Shaft hole at (120, 0)
cyl_shaft = cq.Workplane("XY").cylinder(mount_height + 2, shaft_dia/2).translate((120, 0, -1))

# Four bolt holes at (120 +- 8, +- 9.5)
bolt_holes_coords = [
    (120 + 8, 9.5),
    (120 - 8, 9.5),
    (120 + 8, -9.5),
    (120 - 8, -9.5)
]

# Perform subtractions
result = result.cut(cyl1)
result = result.cut(cyl2)
result = result.cut(cyl_shaft)

for bx, by in bolt_holes_coords:
    cyl_bolt = cq.Workplane("XY").cylinder(mount_height + 2, hole_dia/2).translate((bx, by, -1))
    result = result.cut(cyl_bolt)

# Final result is a single solid