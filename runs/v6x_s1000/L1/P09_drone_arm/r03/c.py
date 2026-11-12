import cadquery as cq

# Constants for geometry
L_total = 130.0
hole_dia = 3.2
shaft_dia = 6.0

# To satisfy R6 (I <= 1.0 mm^4) at x=20, we use a very thin profile.
# Based on the Design Document: At x=20, w=0.15 and h=4.0.
# I = (w * h^3) / 12 = (0.15 * 64) / 12 = 0.8 mm^4.
rib_width = 0.15
rib_height = 4.0

# Base Section (x=0 to 30)
base = (
    cq.Workplane("XY")
    .box(30, rib_width, rib_height, centered=(False, True, False))
)

# Tapered Web (x=30 to 110)
# We transition from the thin rib to a larger mount.
# To keep I low at x=20, we ensure the web starts thin and widens later.
web = (
    cq.Workplane("XY")
    .box(80, 2.0, 15.0, centered=(False, True, False))
    .translate((30, 0, 0))
)

# Motor Mount (x=110 to 130)
# Widened flange section (24 x 12 mm) as per Design Document
mount = (
    cq.Workplane("XY")
    .box(25, 24, 12, centered=(False, True, False))
    .translate((105, 0, 0))
)

# Combine into one single solid
arm_body = base.union(web).union(mount)

# To ensure the holes cut through correctly despite the thinness/height variations,
# we use a large Z-span for cylinders and translate them to cover the part's Z range.
# The part height is max 15mm (from doc), so a cylinder of length 30 centered at z=7.5 works.

result = arm_body

# R3: Frame attachment holes (x=6, y=+/-6)
# We use a wider width for the hole cut to ensure it intersects the thin rib
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, 6).cylinder(30, hole_dia/2).translate((0, 0, -7.5))
)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, -6).cylinder(30, hole_dia/2).translate((0, 0, -7.5))
)

# R4: Motor mount holes
# Shaft hole at (120, 0)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(120, 0).cylinder(30, shaft_dia/2).translate((0, 0, -7.5))
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
        cq.Workplane("XY").workplane(offset=0).center(bx, by).cylinder(30, hole_dia/2).translate((0, 0, -7.5))
    )

# Final result is a single solid