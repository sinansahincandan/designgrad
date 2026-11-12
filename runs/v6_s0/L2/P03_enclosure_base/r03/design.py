import cadquery as cq

# Dimensions
floor_thickness = 2.0
board_x, board_y = 80.0, 50.0
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
# Bosses extend from z=2 to z=8 (height 6)
# Hole extends from z=8 down to z=4 (depth 4)

# 1. Create the main body (Floor + Walls)
# We create a block that goes from z=0 to z=wall_height
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# 2. Subtract the Board Cavity (R3)
# The region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be free.
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, 32 - 8)
    .translate((0, 0, 8 + (32 - 8) / 2))
)
main_body = main_body.cut(cavity)

# 3. Add Screw Bosses (R5)
# Create all four bosses as a single object to ensure clean union
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx, by = boss_x * sx, boss_y * sy
        # We use center(bx, by) then extrude, but to keep the loop logic clean 
        # for a single object, we build them relative to origin or just union them.
        # The feedback suggests: bosses = bosses.center(bx, by).circle(...).extrude(6).center(-bx, -by)
        # However, it's more robust in CQ to create individual objects and union at the end 
        # OR use a single workplane with multiple circles. Let's follow the feedback logic:
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .center(bx, by)
            .circle(boss_od / 2)
            .extrude(6)
        )
        if bosses.objects:
            bosses = bosses.union(boss_cyl)
        else:
            bosses = boss_cyl

main_body = main_body.union(bosses)

# 4. Subtract Pilot Holes (R5)
# Hole starts from top of boss (z=8) and goes down to z=4
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx, by = boss_x * sx, boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4) # Start at z=4
            .center(bx, by)
            .circle(boss_hole_d / 2)
            .extrude(4) # Extends from z=4 to z=8
        )
        main_body = main_body.cut(hole)

# 5. Subtract USB-C Cutout (R6)
# Opening at least 9mm wide (Y) and 3mm high (Z), centered at y=0, z=14 on the -X wall.
# Box parameters: X=depth of cut, Y=width, Z=height.
# To ensure penetration from x=-42.5 to inside the wall, we use x range [-45, -35].
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # X=10, Y=9, Z=3
    .translate((-40, 0, 14)) # Center of the 10mm box is at x=-40 (so it spans -45 to -35)
)
main_body = main_body.cut(usb_cutout)

result = main_body