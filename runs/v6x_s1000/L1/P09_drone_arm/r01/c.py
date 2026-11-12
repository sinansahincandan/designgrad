import cadquery as cq

# Constants
hole_dia = 3.2
shaft_dia = 6.0

# 1. Create the Skeletonized Base (x=0 to 30)
# To satisfy R6 (I <= 1.0 at x=20), we use a single narrow vertical sliver.
# The design document specifies a target section of w=0.5, h=2.0 at x=20.
# We'll create a base that is wider at the frame attachment (x=6) to allow holes,
# but extremely thin at the critical x=20 section.

# Base part: A long thin sliver from x=0 to x=30
# To ensure R3 (holes at y=+/-6) can be placed, we'll add two small pads 
# at the frame end (x=6) that connect to the central sliver.
base_sliver = cq.Workplane("XY").box(30, 0.5, 2.0, centered=(False, False, False))

# Pads for R3 holes at x=6, y=+/-6
pad1 = cq.Workplane("XY").box(10, 14, 2.0, centered=(False, False, False)).translate((6, 6, 0))
pad2 = cq.Workplane("XY").box(10, 14, 2.0, centered=(False, False, False)).translate((6, -6, 0))

# 2. Create the Tapered Web (x=30 to 110)
# This connects the base to the mount. We make it thicker than the sliver to satisfy R5.
web = cq.Workplane("XY").box(80, 6.0, 8.0, centered=(False, False, False)).translate((30, 0, 0))

# 3. Create the Motor Mount (x=110 to 130)
mount = cq.Workplane("XY").box(25, 24, 12, centered=(False, False, False)).translate((105, 0, 0))

# Combine into one solid using union
arm_body = base_sliver.union(pad1).union(pad2).union(web).union(mount)

result = arm_body

# 4. Add Frame Attachment Holes (R3)
# x=6, y=+/-6 through the pads. We use a large Z cylinder to ensure it cuts through.
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, 6).cylinder(20, hole_dia/2).translate((0,0,-10))
)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(6, -6).cylinder(20, hole_dia/2).translate((0,0,-10))
)

# 5. Add Motor Mount Holes (R4)
# Shaft hole at (120, 0)
result = result.cut(
    cq.Workplane("XY").workplane(offset=0).center(120, 0).cylinder(20, shaft_dia/2).translate((0,0,-10))
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
        cq.Workplane("XY").workplane(offset=0).center(bx, by).cylinder(20, hole_dia/2).translate((0,0,-10))
    )

# Final check on constraints:
# R6: At x=20, the geometry is just the base_sliver (0.5 x 2.0). I = (0.5 * 2^3)/12 = 0.33 <= 1.0.
# R7: Volume is roughly (30*0.5*2) + (10*14*2)*2 + (80*6*8) + (25*24*12) ... wait, let's refine volume.
# Actually, the web and mount are the bulk. 
# Web: 80 * 6 * 8 = 3840 mm3. Mount: 25 * 24 * 12 = 7200 mm3. Total ~11000 mm3.
# 11000 * 1.24e-3 = 13.6g. This is < 20g.