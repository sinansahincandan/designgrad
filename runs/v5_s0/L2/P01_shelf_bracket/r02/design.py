import cadquery as cq

# Parameters based on Updated Design Document
spine_thickness = 10.0
width = 20.0  # Y-range: -10 to 10
height_wall = 110.0
arm_length = 160.0
shelf_z = 110.0

# Taper parameters for the arm (bottom surface z goes from 0 at x=10 to 90 at x=160)
# This means thickness at wall (x=10) is 110, and at tip (x=160) is 20.
arm_thickness_start = 110.0
arm_thickness_end = 20.0

screw_dia = 5.5
hole_z_positions = [20.0, 60.0]

# 1. Create the Wall Spine (x: 0 to 10, y: -10 to 10, z: 0 to 110)
spine = cq.Workplane("XY").box(
    spine_thickness, width, height_wall, 
    centered=(False, True, False) # x starts at 0, y centered on 0, z starts at 0
)

# 2. Create the Tapered Arm (x: 10 to 160, y: -10 to 10, top surface z=110)
# We define the side profile in the XZ plane and extrude it along Y.
# Profile points: (x, z)
# Start at x=10, bottom z=0; end at x=160, bottom z=90.
# Top surface is always at z=110.
arm_profile = [
    (spine_thickness, 0),                   # Bottom start (x=10, z=0)
    (arm_length, 90),                       # Bottom end (x=160, z=90)
    (arm_length, shelf_z),                  # Top end (x=160, z=110)
    (spine_thickness, shelf_z)              # Top start (x=10, z=110)
]

arm = (
    cq.Workplane("XZ")
    .polyline(arm_profile)
    .close()
    .extrude(width, both=True) # Extrude along Y, centered on 0
)

# Combine Spine and Arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3) and Clearance (R3)
for z_pos in hole_z_positions:
    # The screw hole itself (axis along X)
    # Centered at x=5 (middle of the 10mm spine), y=0, z=z_pos
    bracket = bracket.cut(
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(spine_thickness / 2, 0)
        .circle(screw_dia / 2)
        .extrude(arm_length + spine_thickness) # Ensure it goes through the whole part
    )

    # R3: Screwdriver clearance. No material within 4 mm of axis for x >= 10.
    # Clearance zone: a box from x=10 to x=25, covering diameter + 8mm (4mm each side).
    clearance_size = screw_dia + 8.0
    bracket = bracket.cut(
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(17.5, 0) # Center of [10, 25] is (10+25)/2 = 17.5
        .box(15, clearance_size, clearance_size, centered=(True, True, True))
    )

# R4: Ensure nothing is above z=110 for x >= 8. 
# Our construction already places the top surface at exactly z=110.
# We'll add a safety cut just in case of floating point errors or geometry overlaps.
bracket = bracket.cut(
    cq.Workplane("XY")
    .workplane(offset=110.001)
    .center(8, 0)
    .box(arm_length + spine_thickness, width + 2, 10, centered=(False, True, False))
)

result = bracket