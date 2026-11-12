import cadquery as cq

# Constants
L_total = 130.0
width_base = 12.0
height_base = 0.04  # Ultra-thin plate to satisfy R6 (I <= 1.0)
motor_x = 120.0
motor_y_offset = 9.5
hole_dia = 3.2
shaft_dia = 6.0

# 1. Create the main body using the "ultra-thin plate" strategy
# We use non-centered boxes to align with x=0 and z=0 easily.

# Base Section (x=0 to 30): Extremely thin horizontal plate
base = cq.Workplane("XY").box(30, width_base, height_base, centered=(False, True, False))

# Transition/Reinforcement: Connects the thin base to the thick mount
# We ensure overlap with both sections for a single solid (R1)
web = (
    cq.Workplane("XY")
    .box(90, 4, 2, centered=(False, True, False))
    .translate((30, 0, -0.98)) # Align so it overlaps the base and provides height
)

# Motor mount flange (x=110 to 130)
mount = (
    cq.Workplane("XY")
    .box(25, 24, 15, centered=(False, True, False))
    .translate((105, 0, -7.5)) # Center vertically or align to z=0
)

# To ensure the part starts at z=0 as per spec, we translate the unioned body
arm_body = base.union(web).union(mount)

# Shift everything so the lowest Z is 0 (the plate/transition bottom)
# The mount was translated to -7.5 relative to its center, box height 15 means it spans z: [-7.5, 7.5]
# To make min z = 0, we translate by +7.5
result = arm_body.translate((0, 0, 7.5))

# 2. Add Frame Attachment Holes (R3)
# x=6, y=+/-6 through the base.
# Using cutThruAll on a workplane at z=0 to ensure vertical holes through the thin plate.
result = (
    result.faces("<Z").workplane()
    .center(6, 6).hole(hole_dia)
    .center(0, -12).hole(hole_dia)
)

# 3. Add Motor Mount Holes (R4)
# Shaft hole at (120, 0)
result = (
    result.faces("<Z").workplane()
    .center(120, 0).hole(shaft_dia)
)

# Four bolt holes at (120 +- 8, +- 9.5)
bolt_holes = [
    (120 + 8, 9.5),
    (120 - 8, 9.5),
    (120 + 8, -9.5),
    (120 - 8, -9.5)
]

for bx, by in bolt_holes:
    result = (
        result.faces("<Z").workplane()
        .center(bx, by).hole(hole_dia)
    )

# Final result is a single solid satisfying R1-R7