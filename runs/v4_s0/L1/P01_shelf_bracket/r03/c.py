import cadquery as cq

# Parameters based on Design Document
width = 24.0
spine_x_max = 8.0
height_wall = 110.0
arm_x_start = 8.0
arm_x_end = 160.0
arm_z_top = 110.0
arm_thickness_start = 30.0
arm_thickness_end = 15.0

screw_dia = 5.5
clearance_radius = 4.0
hole_centers_z = [20, 60]

# 1. Create the Wall Spine (x: 0 to 8)
spine = cq.Workplane("XY").box(spine_x_max, width, height_wall, centered=(False, False, False))

# 2. Create the Arm with Taper (x: 8 to 160)
arm_length = arm_x_end - arm_x_start

# To avoid "Nothing to loft" or "No pending wires", we create a solid via subtraction.
# Start with a rectangular block for the arm.
arm_block = (
    cq.Workplane("XY")
    .box(arm_length, width, arm_thickness_start, centered=(False, False, False))
    .translate((arm_x_start, -width/2, arm_z_top - arm_thickness_start))
)

# Define the wedge to subtract from the bottom of the block to create the taper.
# The wedge is a triangular prism in the XZ plane extruded along Y.
# At x=8 (local 0), height = 0.
# At x=160 (local arm_length), height = arm_thickness_start - arm_thickness_end.
wedge_height_at_end = arm_thickness_start - arm_thickness_end

wedge_profile = (
    cq.Workplane("XZ")
    .workplane(offset=arm_x_start)
    .polyline([
        (0, 0), 
        (arm_length, wedge_height_at_end), 
        (arm_length, 0), 
        (0, 0)
    ])
    .close()
)

# We need to translate the wedge profile so it aligns with the bottom of the arm block.
# The bottom of the arm block is at z = arm_z_top - arm_thickness_start.
wedge_solid = (
    wedge_profile.extrude(width, both=True)
    .translate((0, 0, arm_z_top - arm_thickness_start))
)

arm = arm_block.cut(wedge_solid)

# Combine spine and arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
for z_pos in hole_centers_z:
    # The screw hole goes through the whole part along X.
    # We use a cylinder on YZ plane, centered at y=0, z=z_pos.
    screw_hole = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_x_end + 10) # Extrudes from x=0 to arm_x_end+10
    )
    bracket = bracket.cut(screw_hole)

    # Screwdriver clearance (R3): radius 4mm for x >= 10
    clearance_cyl = (
        cq.Workplane("YZ")
        .workplane(offset=10) 
        .center(0, z_pos)
        .circle(clearance_radius)
        .extrude(arm_x_end - 10 + 20) # Extends from x=10 to the end
    )
    bracket = bracket.cut(clearance_cyl)

result = bracket