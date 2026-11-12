import cadquery as cq

# Constants
L_total = 130.0
width_base = 12.0
height_base = 12.0
motor_x = 120.0
motor_y_offset = 9.5
hole_dia = 3.2
shaft_dia = 6.0

# 1. Create the main body using a tapered profile
# We'll build it in three segments: Base, Transition/Web, and Motor Mount
# To ensure they are one solid, we use non-centered boxes or overlap them correctly.
# Using box(..., centered=False) makes life easier for positioning relative to x=0

base = cq.Workplane("XY").box(30, width_base, height_base, centered=(False, True, False)).translate((0, 0, 0))

# Web section (tapered spine)
# To ensure union works, we make it overlap the base and mount
web = (
    cq.Workplane("XY")
    .box(85, 8, 12, centered=(False, True, False))
    .translate((25, 0, 0)) # Overlap with base at x=30
)

# Motor mount flange
mount = (
    cq.Workplane("XY")
    .box(25, 24, 12, centered=(False, True, False))
    .translate((105, 0, 0)) # Overlap with web at x=110
)

# Combine into one solid
arm_body = base.union(web).union(mount)

# The design document says z in [0, 15]. Our boxes are height 12.
# Let's align the bottom to Z=0. Since we used centered=(False, True, False),
# the Y is centered on 0, but Z starts at 0.
result = arm_body

# 2. Add Frame Attachment Holes (R3)
# x=6, y=+/-6 through the base.
# We use a cylinder to cut through the whole part for reliability.
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, 6).cylinder(20, hole_dia/2).translate((0,0,10))
)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, -6).cylinder(20, hole_dia/2).translate((0,0,10))
)

# 3. Add Motor Mount Holes (R4)
# Shaft hole at (120, 0)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(120, 0).cylinder(20, shaft_dia/2).translate((0,0,10))
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
        cq.Workplane("XY").workplane(offset=0).center(bx, by).cylinder(20, hole_dia/2).translate((0,0,10))
    )

# Final check: The cylinder translation (0,0,10) ensures it cuts through the Z range [0, 12]