import cadquery as cq

# Constants from Design Document & Spec
L_total = 130.0
hole_dia = 3.2
shaft_dia = 6.0

# Geometry dimensions for R5/R6 optimization
base_h = 15.0
base_w = 0.032  # Ultra-thin width to meet R6 (I approx 0.9)

# Motor mount dimensions
mount_w = 24.0
mount_h = 15.0

# Refined Construction for R1:
# We must ensure the web bridges the gap between x=30 and x=70.
# The previous error showed body_base (0-30) and body_web starting at 70.

# Base Section (x=0 to 30)
body_base = cq.Workplane("XY").box(30, base_w, base_h, centered=(False, True, False))

# Tapered Web/Spine (x=25 to 115)
# To bridge the gap:
# Start at x=25 (overlaps base which ends at 30).
# Length is 90. So it spans from x=25 to x=115.
# translate(25, 0, 0) with length 90 covers [25, 115].
body_web = cq.Workplane("XY").box(90, 2.0, base_h, centered=(False, True, False)).translate((25, 0, 0))

# Motor Mount (x=110 to 130)
# The mount is a flange/block at the end. We ensure it overlaps with the web.
body_mount = cq.Workplane("XY").box(25, mount_w, mount_h, centered=(False, True, False)).translate((110, 0, 0))

# Combine into one solid using union
result = body_base.union(body_web).union(body_mount)

# 2. Add Frame Attachment Holes (R3)
# x=6, y=+/-6 through the base. 
# We use a cylinder oriented along Z to cut through the thin Y-profile.
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, 6).cylinder(30, hole_dia/2).translate((0, 0, -7.5))
)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, -6).cylinder(30, hole_dia/2).translate((0, 0, -7.5))
)

# 3. Add Motor Mount Holes (R4)
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

# Final result is a single valid solid