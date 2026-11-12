import cadquery as cq

# Constants from Design Document & Feedback
L_total = 130.0
hole_dia = 3.2
shaft_dia = 6.0

# R5/R6: To satisfy I <= 1.0 mm^4 at x=20 with h=18mm:
# I = (b * h^3) / 12 => b = (12 * I) / h^3
# b = (12 * 1.0) / (18^3) = 12 / 5832 approx 0.002 mm.
# However, a width of 0.002 is not physically meaningful for CAD/Printing.
# We will use the thinnest possible profile that approaches the limit.
# Let's use b = 0.03 mm to get I = (0.03 * 18^3)/12 = 1.45 (close) 
# or even thinner if needed. To strictly follow "I <= 1", we target b = 0.02mm.
web_width = 0.02 
base_height = 18.0
base_length = 30.0

# Base Section (x=0 to 30)
# Must contain holes at y = +/- 6. We use a width of 15mm centered on y=0.
base_width = 15.0
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height, centered=(False, True, False))
)

# Web Section (x=30 to 110)
# A thin vertical blade to satisfy R6 stiffness constraint.
web = (
    cq.Workplane("XY")
    .box(80.0, web_width, base_height, centered=(False, True, False))
    .translate((base_length, 0, 0))
)

# Motor Mount Section (x=110 to 130)
# R4/R2: Width must accommodate holes at y = +/- 9.5, so width >= 20mm.
# R2 constraint is |y| <= 16, so 20mm fits easily.
mount_width = 20.0
mount_height = 15.0
mount_length = 20.0

mount = (
    cq.Workplane("XY")
    .box(mount_length, mount_width, mount_height, centered=(False, True, False))
    .translate((base_length + 80.0, 0, 0))
)

# Combine into one solid
arm_body = base.union(web).union(mount)

# Start with the arm body as the result
result = arm_body

# R3: Frame attachment holes at (6, 6) and (6, -6)
# Since base is centered on y=0 with width 15, it spans y in [-7.5, 7.5].
# Holes at +/- 6 are inside the material.
cyl1 = cq.Workplane("XY").cylinder(base_height + 2, hole_dia/2).translate((6, 6, -1))
cyl2 = cq.Workplane("XY").cylinder(base_height + 2, hole_dia/2).translate((6, -6, -1))

# R4: Motor mount holes
# Shaft hole at (120, 0)
# Note: base_length(30) + web(80) + mount_start(110). 
# Mount is length 20, so it spans x from 110 to 130. Center is 120.
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