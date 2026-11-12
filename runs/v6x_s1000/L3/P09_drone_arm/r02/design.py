import cadquery as cq

# Constants from design document and requirements
L_total = 130.0
width_max = 32.0  # |y| <= 16 -> width = 32
height_at_x20 = 0.7 # To satisfy R6: I = (32 * 0.7^3)/12 = 0.914 <= 1.0
hole_dia = 3.2
shaft_dia = 6.0

# 1. Create the main body components
# We use centered=(False, False, False) to ensure x starts at 0 and z starts at 0.

# Base Section (x=0 to 30): Wide thin plate
# To satisfy R6, we make this section very thin.
base = cq.Workplane("XY").box(30, width_max, height_at_x20, centered=(False, False, False))

# Tapered Transition/Spine (x=30 to 110)
# We'll use a slightly thicker spine to help with strength and mass distribution.
# It overlaps the base at x=30.
spine = (
    cq.Workplane("XY")
    .box(85, 12, 4, centered=(False, False, False))
    .translate((25, 0, 0)) # Overlap with base to ensure single solid
)

# Motor Mount (x=110 to 130)
# A hollowed rectangular frame to keep mass low (R7).
mount_outer = cq.Workplane("XY").box(25, 30, 8, centered=(False, False, False)).translate((105, 0, 0))
mount_inner = cq.Workplane("XY").box(20, 22, 10, centered=(False, False, False)).translate((107.5, 0, -1))
mount = mount_outer.cut(mount_inner)

# Combine into one single solid (R1)
arm_body = base.union(spine).union(mount)

result = arm_body

# 2. Add Holes (R3 & R4)
# We use a height of 20 and translate to center it vertically so it cuts through everything.
# The part's Z range is roughly [0, 8]. A cylinder at Z=10 with height 20 covers Z=[-10, 10].

# R3: Frame attachment holes (x=6, y=+/-6)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, 6).cylinder(20, hole_dia/2).translate((0, 0, 10))
)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, -6).cylinder(20, hole_dia/2).translate((0, 0, 10))
)

# R4: Motor mount holes
# Shaft clearance hole (x=120, y=0, dia=6)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(120, 0).cylinder(20, shaft_dia/2).translate((0, 0, 10))
)

# Four bolt holes (x=120 +/- 8, y=+/- 9.5)
bolt_holes = [
    (120 + 8, 9.5),
    (120 - 8, 9.5),
    (120 + 8, -9.5),
    (120 - 8, -9.5)
]

for bx, by in bolt_holes:
    result = result.cut(
        cq.Workplane("XY").workplane(offset=0).center(bx, by).cylinder(20, hole_dia/2).translate((0, 0, 10))
    )

# Final check on R2: x starts at 0, max x is 130, |y| <= 16 (max width 32), z >= 0.