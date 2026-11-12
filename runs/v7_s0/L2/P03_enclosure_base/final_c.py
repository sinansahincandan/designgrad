import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
boss_hole_depth = 4.0

# 1. Create the base floor and walls block
# We start with a solid block that encompasses the outer dimensions and height
base_block = cq.Workplane("XY").box(outer_x, outer_y, wall_height)

# Shift the block so the bottom is at z=0
# box() centers on origin, so we move it up by wall_height/2
base_block = base_block.translate((0, 0, wall_height / 2))

# 2. Create the board cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
# Since our walls only go to 31, we subtract up to wall_height.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, wall_height - 8)
    .translate((0, 0, 8 + (wall_height - 8) / 2))
)

# 3. Create the screw bosses (R5)
# Bosses are solid from floor (z=2) up to z=8. 
# However, R5 says "from the floor up to z=8". Let's interpret floor as z=0 or z=2.
# To ensure a single solid, we build them as cylinders and union them.
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder from z=2 to z=8 (or slightly higher to ensure union)
        bosses = bosses.union(
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_od / 2)
            .extrude(6) # Goes from z=2 to z=8
            .translate((bx, by, 0))
        )

# Subtract pilot holes from bosses
# Hole at least 4mm deep, starting from top (z=8) downwards
bosses = (
    bosses.faces("<Z").workplane() # This is tricky with multiple parts, 
    # easier to just subtract the holes from the main body later
)

# Let's rebuild the logic for a single solid more cleanly:
# Start with Floor + Walls
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height/2))

# Subtract Board Cavity
main_body = main_body.cut(cavity)

# Add Bosses (as cylinders)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        boss_cyl = cq.Workplane("XY").workplane(offset=2).circle(boss_od/2).extrude(6).translate((bx, by, 0))
        main_body = main_body.union(boss_cyl)

# Subtract Pilot Holes (R5)
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = cq.Workplane("XY").workplane(offset=8 - boss_hole_depth).circle(boss_hole_d/2).extrude(boss_hole_depth).translate((bx, by, 0))
        main_body = main_body.cut(hole)

# Subtract USB-C Cutout (R6)
# Centered at y=0, z=14 on the -X wall.
# Wall is at x = -outer_x/2 = -42.5. 
# Cutout: 9mm wide (Y), 3mm high (Z).
cutout = (
    cq.Workplane("XY")
    .workplane(offset=14) # z center
    .center(0, 0)
    .rect(3, 9) # x is height (3), y is width (9) in local plane? No, rect(width, height)
    # Let's use a box for clarity
)
# A box at the -X face:
usb_cutout = cq.Workplane("XY").box(5, 9, 3).translate((-outer_x/2, 0, 14))
main_body = main_body.cut(usb_cutout)

result = main_body