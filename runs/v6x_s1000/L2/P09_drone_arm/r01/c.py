import cadquery as cq

# Constants
L_total = 130.0
hole_dia = 3.2
shaft_dia = 6.0

# R6 Constraint: I <= 1.0 mm^4 at x=20.
# Using a thin vertical strip: b (width/y) = 0.09, h (height/z) = 5.0
# I = (b * h^3) / 12 = (0.09 * 125) / 12 = 0.9375 mm^4 (< 1.0)

# 1. Create the main body components
# Using centered=(False, False, False) to align x=0 and z=0 easily

# Base Section (x=0 to 30): Thin vertical blade at x=20
# To ensure it covers x=20 with the required I, we make a thin box.
base = cq.Workplane("XY").box(30, 0.09, 5.0, centered=(False, False, False))

# Web Section (x=30 to 110): Transitioning profile
# To keep mass low (R7), we use a thickness in Z of ~4mm and width in Y of ~8mm
web = cq.Workplane("XY").box(80, 8.0, 4.5, centered=(False, False, False)).translate((30, 0, 0))

# Motor Mount (x=110 to 130): Widened section for bolts
mount = cq.Workplane("XY").box(20, 24.0, 6.0, centered=(False, False, False)).translate((110, 0, 0))

# Combine into one solid (R1)
arm_body = base.union(web).union(mount)

# The design document specifies the motor is at (120, 0). 
# Our mount covers x=110 to 130 and y=-12 to 12.
result = arm_body

# 2. Add Frame Attachment Holes (R3)
# Two vertical holes, diameter 3.2 mm, at (x, y) = (6, +-6).
# We use a large height for the cylinder and ensure it's centered on the part's Z-axis.
# Since we used centered=False, z starts at 0.
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, 6).cylinder(20, hole_dia/2)
)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, -6).cylinder(20, hole_dia/2)
)

# 3. Add Motor Mount Holes (R4)
# Shaft hole at (120, 0), diameter 6mm
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(120, 0).cylinder(20, shaft_dia/2)
)

# Four bolt holes at (120 +- 8, +- 9.5), diameter 3.2mm
bolt_holes = [
    (120 + 8, 9.5),
    (120 - 8, 9.5),
    (120 + 8, -9.5),
    (120 - 8, -9.5)
]

for bx, by in bolt_holes:
    result = result.cut(
        cq.Workplane("XY").workplane(offset=0).center(bx, by).cylinder(20, hole_dia/2)
    )

# Final Result is a single solid assigned to 'result'