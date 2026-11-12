import cadquery as cq

# Dimensions from Design Document
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 7.0  # Updated per feedback and design doc
boss_hole_d = 2.2
boss_hole_depth = 4.0

# 1. Create the main body (Floor + Walls)
# The box is centered at Z=wall_height/2, so it spans z=0 to z=31
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract the Board Cavity (R3)
# Region: -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
# We use a box that covers the required Z range to ensure it clears any ceiling material.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, 32 - 8)
    .translate((0, 0, 8 + (32 - 8) / 2))
)
main_body = main_body.cut(cavity)

# 3. Add Screw Bosses (R5)
# Bosses are solid from floor (z=2) up to z=8.
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create the boss cylinder starting at z=2 and extending to z=8 (height 6)
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(6)
        )
        # Subtract the pilot hole from the top of the boss (z=8) downwards
        # Using .faces(">Z").workplane().hole() as suggested in feedback
        boss_with_hole = boss_cyl.faces(">Z").workplane().hole(boss_hole_d)
        main_body = main_body.union(boss_with_hole)

# 4. Subtract USB-C Cutout (R6)
# Requirement: 10mm (Y) x 4mm (Z) x 10mm (X) centered at y=0, z=14.
# X-range [-45, -35] ensures it penetrates the -X wall (outer face is at -42.5).
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 10, 4) # Width Y=10, Height Z=4, Depth X=10
    .translate((-40, 0, 14)) # Centered such that it spans -35 to -45 in X
)
# Note: To strictly follow the "X-range of [-45, -35]" instruction from design doc:
# center_x = (-45 + -35) / 2 = -40.
main_body = main_body.cut(usb_cutout)

result = main_body