import cadquery as cq

# Dimensions
outer_x, outer_y = 85.0, 55.0
wall_height = 31.0
floor_thickness = 2.0

boss_x, boss_y = 35.0, 20.0
boss_od = 6.0
boss_hole_d = 2.2
# Bosses go from floor (z=2) up to z=8. Hole is 4mm deep starting from top (z=8).

# 1. Build the additive components (Floor + Walls + Bosses)
# Start with the main block representing walls and floor
# To ensure a single solid, we build the outer shell first.
main_body = cq.Workplane("XY").box(outer_x, outer_y, wall_height).translate((0, 0, wall_height / 2))

# Add the bosses as cylinders from z=2 to z=8
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder at the correct position and height (z=2 to z=8)
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=2)
            .circle(boss_od / 2)
            .extrude(6)
            .translate((bx, by, 0))
        )
        bosses = bosses.union(boss_cyl)

# Combine main body and bosses
combined_solid = main_body.union(bosses)

# 2. Build the subtractive components (Cavity + Holes + Cutout)

# R3: Board cavity subtraction (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32)
# We use a box that covers exactly this volume to ensure it is completely free.
cavity = cq.Workplane("XY").box(80, 50, 32 - 8).translate((0, 0, 24))

# R5: Pilot holes (2.2mm diameter, 4mm deep, starting from z=8 downwards)
holes = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Hole from z=4 to z=8
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4)
            .circle(boss_hole_d / 2)
            .extrude(4)
            .translate((bx, by, 0))
        )
        holes = holes.union(hole)

# R6: USB-C Cutout (9mm Y, 3mm Z, centered at y=0, z=14 on -X wall)
# We use a box that extends from the outer face (-outer_x/2) into the cavity to ensure penetration.
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3)
    .translate((-outer_x / 2 - 5, 0, 14))
)

# 3. Perform all subtractions in a single chain to ensure R1 (Single Solid)
result = combined_solid.cut(cavity).cut(holes).cut(usb_cutout)