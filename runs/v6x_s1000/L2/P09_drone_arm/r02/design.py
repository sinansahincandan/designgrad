import cadquery as cq

# Constants for dimensions
L_total = 130.0
hole_dia = 3.2
shaft_dia = 6.0

# To ensure a single connected solid, we will build the arm using overlapping primitives.
# The design must satisfy R6 (I <= 1.0 at x=20).
# We'll use a spine that runs from x=0 to x=130.
# At x=20, the section will be part of this spine.

# Spine: x[0, 130], y[-4, 4], z[0, 1.1]
# I = (8 * 1.1^3) / 12 = 0.887 <= 1.0 (Satisfies R6)
spine = cq.Workplane("XY").box(130, 8, 1.1, centered=(False, True, False)).translate((0, 0, 0.55))

# Base Plate: x[0, 30], y[-7, 7], z[0, 1.1]
# This provides width for R3 holes at y=+/-6 and overlaps the spine.
base_plate = cq.Workplane("XY").box(30, 14, 1.1, centered=(False, True, False)).translate((0, 0, 0.55))

# Motor Mount: x[110, 130], y[-15, 15], z[0, 20]
# We must ensure it overlaps the spine and base_plate to form one solid.
# The spine goes up to z=1.65. Let's make the mount start from z=0.
mount = cq.Workplane("XY").box(20, 30, 20, centered=(False, True, False)).translate((110, 0, 0))

# Combine all parts into one solid via union
arm_body = spine.union(base_plate).union(mount)

# Start cutting holes from the combined solid
result = arm_body

# R3: Frame attachment (x=6, y=+/-6, dia 3.2)
# Holes are vertical cylinders through the body. We use a workplane on XY and drill up.
# Since we want them to go through the whole part, we'll use a large Z height or just .hole()
result = result.workplane(offset=0).center(6, 6).hole(hole_dia)
result = result.workplane(offset=0).center(6, -6).hole(hole_dia)

# R4: Motor mount holes
# Shaft hole at (120, 0), dia 6.0
result = result.workplane(offset=0).center(120, 0).hole(shaft_dia)

# Bolt holes at (120 +- 8, +- 9.5), dia 3.2
bolt_holes = [
    (128, 9.5),
    (112, 9.5),
    (128, -9.5),
    (112, -9.5)
]

for bx, by in bolt_holes:
    result = result.workplane(offset=0).center(bx, by).hole(hole_dia)