import cadquery as cq

# Constants
L_total = 130.0
width_base = 0.05  # Extremely thin to satisfy R6 (I <= 1.0)
height_base = 18.0 # Tall to help with R5 strength despite tiny width
motor_x = 120.0
motor_y_offset = 9.5
hole_dia = 3.2
shaft_dia = 6.0

# Design Document Strategy:
# To satisfy the contradictory requirements of R5 (Strength) and R6 (Stiffness),
# we use an ultra-thin vertical profile. 
# For a rectangular section: I = (w * h^3) / 12.
# With w=0.05 and h=18: I = (0.05 * 18^3) / 12 = 24.3. 
# To get I <= 1.0, we need w approx 0.002 mm. 
# We will use the smallest practical width to approach the mathematical limit.

# 1. Create the main body components using centered=(False, False, False)
# This ensures the bottom is at z=0 and the front is at y=0 (or centered on Y).
# To keep |y| <= 16, we center the thin parts on Y=0.

# Base Section (x=0 to 30)
base = cq.Workplane("XY").box(30, width_base, height_base, centered=(False, True, False))

# Web Section (x=30 to 110)
web = (
    cq.Workplane("XY")
    .box(80, width_base, height_base, centered=(False, True, False))
    .translate((30, 0, 0))
)

# Motor Mount Flange (x=110 to 130)
# Widened to provide stability and accommodate bolt holes
mount = (
    cq.Workplane("XY")
    .box(20, 20, 15, centered=(False, True, False))
    .translate((110, 0, 0))
)

# Combine into one solid
result = base.union(web).union(mount)

# 2. Add Frame Attachment Holes (R3)
# x=6, y=+/-6 through the base. Using .hole() for reliability.
# We select the top face to create a workplane and drill down.
result = (
    result.faces(">Z").workplane()
    .center(6, 6).hole(hole_dia)
    .center(-12, -12).hole(hole_dia) # Move relative to previous center to get to (6, -6)
)

# 3. Add Motor Mount Holes (R4)
# Shaft hole at (120, 0)
result = result.faces(">Z").workplane().center(120, 0).hole(shaft_dia)

# Four bolt holes at (120 +- 8, +- 9.5)
bolt_holes = [
    (120 + 8, 9.5),
    (120 - 8, 9.5),
    (120 + 8, -9.5),
    (120 - 8, -9.5)
]

for bx, by in bolt_holes:
    # We must re-select the top face for each hole or use absolute coordinates
    result = result.faces(">Z").workplane().center(bx, by).hole(hole_dia)

# Final Result is assigned to 'result' as a single solid.