import cadquery as cq

# Constants from Design Document and Feedback
hole_dia = 3.2
shaft_dia = 6.0

# 1. Create the main body using a thin-plate architecture to satisfy R5, R6, and R7.
# We use centered=(False, True, False) so that:
# - Z=0 is the bottom surface
# - Y=0 is the centerline
# - X starts at 0

# Base Section (x=0 to 30): Widened to accommodate R3 holes (y = +/- 6)
# Design Doc says width y in [-2, 2] but also requires R3 holes at y = +/- 6.
# Feedback suggests widening base to y in [-8, 8].
base = cq.Workplane("XY").box(30, 16, 15, centered=(False, True, False))

# Tapered Web (x=30 to 110): A spine that provides structural continuity.
# To satisfy R6 (low I), we keep the width narrow.
# We'll use a loft between two rectangles to create the taper in height.
web_start = cq.Workplane("XY").workplane(offset=30).rect(4, 15).extrude(80)
# Note: To simplify and ensure R1 (single solid), we will use a series of boxes or a loft.
# Let's use a simplified approach: a thin box for the web that overlaps base and mount.
web = cq.Workplane("XY").box(80, 4, 12, centered=(False, True, False)).translate((30, 0, 0))

# Motor Mount (x=110 to 130): Widened flange for R4 holes (y = +/- 9.5)
mount = cq.Workplane("XY").box(20, 24, 15, centered=(False, True, False)).translate((110, 0, 0))

# Combine into one solid
arm_body = base.union(web).union(mount)

result = arm_body

# 2. Add Frame Attachment Holes (R3)
# x=6, y=+/-6 through the base.
# We use a cylinder with length 20 and translate it to ensure it cuts through Z=[0, 15]
for y_pos in [6, -6]:
    result = result.cut(
        cq.Workplane("XY")
        .workplane(offset=0)
        .center(6, y_pos)
        .cylinder(20, hole_dia / 2)
        .translate((0, 0, -2.5)) # Center the cylinder vertically relative to Z=0
    )

# 3. Add Motor Mount Holes (R4)
# Shaft hole at (120, 0)
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(120, 0)
    .cylinder(20, shaft_dia / 2)
    .translate((0, 0, -2.5))
)

# Four bolt holes at (120 +- 8, +- 9.5)
bolt_holes = [
    (120 + 8, 9.5),
    (120 - 8, 9.5),
    (120 + 8, -9.5),
    (120 - 8, -9.5)
]

for bx, by in bolt_holes:
    result = result.cut(
        cq.Workplane("XY")
        .workplane(offset=0)
        .center(bx, by)
        .cylinder(20, hole_dia / 2)
        .translate((0, 0, -2.5))
    )

# Final result is a single solid 'result'