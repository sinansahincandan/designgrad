import cadquery as cq

# Dimensions
outer_x = 85.0
outer_y = 55.0
total_height = 32.0

board_x = 80.0
board_y = 50.0
board_z_start = 8.0
board_z_end = 32.0

boss_x, boss_y = 35.0, 20.0
boss_od = 7.0
boss_hole_d = 2.2
boss_hole_depth = 6.0

usb_w = 9.0
usb_h = 3.0
usb_z = 14.0

# 1. Create the main block (Floor + Walls)
# We create a solid block from z=0 to z=total_height
base_block = cq.Workplane("XY").box(outer_x, outer_y, total_height).translate((0, 0, total_height / 2))

# 2. Subtract the board space (R3)
# The cavity is centered in X and Y, from z=8 to z=32
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, board_z_end - board_z_start)
    .translate((0, 0, (board_z_start + board_z_end) / 2))
)

main_body = base_block.cut(cavity)

# 3. Create Screw Bosses (R5)
# We create each boss as a complete solid (cylinder minus hole) and then union them
bosses = None
for sx in [-1, 1]:
    for sy in [-1, 1]:
        cx = sx * boss_x
        cy = sy * boss_y
        
        # Create the cylinder for the boss from z=0 to z=8
        single_boss = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .center(cx, cy)
            .circle(boss_od / 2)
            .extrude(8.0)
        )
        
        # Subtract the hole from this specific boss
        # The hole is at the top (z=8), going down by boss_hole_depth
        single_boss = (
            single_boss.faces(">Z").workplane()
            .center(0, 0)
            .circle(boss_hole_d / 2)
            .cut(cq.Workplane("XY").circle(boss_hole_d/2).extrude(boss_hole_depth)) # This is a bit messy in CQ, let's use hole()
        )
        # Cleaner way for the hole:
        single_boss = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .center(cx, cy)
            .circle(boss_od / 2)
            .extrude(8.0)
            .faces(">Z").workplane()
            .center(0, 0)
            .hole(boss_hole_d, boss_hole_depth)
        )

        if bosses is None:
            bosses = single_boss
        else:
            bosses = bosses.union(single_boss)

# Combine main body and bosses
result = main_body.union(bosses)

# 4. USB-C Cutout (R6)
# The cutout is on the -X wall, centered at y=0, z=14
# We create a box that intersects the wall and subtract it
cutout_box = (
    cq.Workplane("XY")
    .box(outer_x, usb_w, usb_h) # Large enough to ensure clean cut
    .translate((-outer_x/2, 0, usb_z))
)

# We need to make sure the cutout box is oriented correctly for a subtraction through the -X face
# A simpler way: create a box at the specific location and subtract
cutout_box = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(-outer_x/2, 0)
    .rect(10, usb_w) # width in Y is usb_w
    .extrude(10) # depth in X
    .translate((0, 0, usb_z))
)

# Let's use a more robust subtraction for the cutout
cutout_geometry = (
    cq.Workplane("XY")
    .box(20, usb_w, usb_h)
    .translate((-outer_x/2, 0, usb_z))
)

result = result.cut(cutout_geometry)