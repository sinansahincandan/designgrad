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

# --- STEP 1: Create the additive components (Union) ---

# Floor: Covers the whole footprint from z=0 to z=2
floor = cq.Workplane("XY").box(outer_x, outer_y, floor_thickness).translate((0, 0, floor_thickness / 2))

# Walls: Outer perimeter box minus the inner board area (to create hollow walls)
# We build a solid block for the walls and then subtract the cavity later? 
# No, R1 says union floor, walls, and bosses first.
# Let's build the wall shell as a single solid.
walls = (
    cq.Workplane("XY")
    .box(outer_x, outer_y, wall_height)
    .translate((0, 0, wall_height / 2))
)

# Bosses: Cylinders from z=0 to z=8
bosses = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        # Create cylinder at origin then translate to position
        boss_cyl = (
            cq.Workplane("XY")
            .workplane(offset=0)
            .circle(boss_od / 2)
            .extrude(8)
            .translate((bx, by, 0))
        )
        bosses = bosses.union(boss_cyl)

# Combine additive parts: Floor + Walls + Bosses
# Note: The walls block currently includes the space where the board goes.
# We will subtract that cavity in Step 2.
main_body = floor.union(walls).union(bosses)

# --- STEP 2: Create the subtractive components (Cuts) ---

# R3: Board Cavity (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32)
cavity = (
    cq.Workplane("XY")
    .box(board_x, board_y, 32 - 8)
    .translate((0, 0, 8 + (32 - 8) / 2))
)

# R5: Pilot Holes (2.2mm diameter, from z=8 down to z=4)
holes = cq.Workplane("XY")
for sx in [-1, 1]:
    for sy in [-1, 1]:
        bx = boss_x * sx
        by = boss_y * sy
        hole = (
            cq.Workplane("XY")
            .workplane(offset=4) # Start at z=4
            .circle(boss_hole_d / 2)
            .extrude(4) # Extrude up to z=8
            .translate((bx, by, 0))
        )
        holes = holes.union(hole)

# R6: USB-C Cutout (Through the -X wall)
# x in [-43, -39], y in [-4.5, 4.5], z in [12.5, 15.5]
# Centered at y=0, z=14. Width(Y)=9, Height(Z)=3.
# We use a box with enough X-depth to ensure it cuts through the wall.
usb_cutout = (
    cq.Workplane("XY")
    .box(10, 9, 3) # 10mm depth in X to ensure penetration
    .translate((-outer_x / 2 - 5, 0, 14)) # Shift so it intersects the wall face
)

# Perform all subtractions on the unified solid
result = main_body.cut(cavity).cut(holes).cut(usb_cutout)