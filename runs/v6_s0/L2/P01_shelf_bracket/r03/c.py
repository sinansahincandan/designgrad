import cadquery as cq

# Parameters based on Design Document
width_spine = 30.0
height_spine = 110.0
thickness_spine = 15.0
screw_dia = 5.5
clearance_y_width = 14.0  # > 5.5 + 2*4 (R3)
hole_z_positions = [20.0, 60.0]

# 1. Create the Wall Spine
# Centered on Y=0, spanning x: 0 to 15, y: -15 to 15, z: 0 to 110
spine = (
    cq.Workplane("XY")
    .box(thickness_spine, width_spine, height_spine, centered=(False, True, False))
)

# 2. Create the Lofted Arm
# Profile at x=15: Width 30 (y:-15 to 15), Height 30 (z:80 to 110)
# Profile at x=160: Width 10 (y:-5 to 5), Height 10 (z:100 to 110)

def create_profile_wire(x_pos, width, height):
    """Creates a single wire profile in the YZ plane at x_pos."""
    return (
        cq.Workplane("YZ")
        .workplane(offset=x_pos)
        .center(0, 110 - height/2)
        .rect(width, height)
        .vertices() # This ensures we have a wire-like object for lofting
    )

# In CadQuery, to loft between two distinct planes using the loft command on a single Workplane:
# We create one workplane and add multiple wires to it.
arm = (
    cq.Workplane("YZ")
    .workplane(offset=thickness_spine)
    .center(0, 110 - 30/2)
    .rect(30, 30)
    .workplane(offset=160 - thickness_spine)
    .center(0, 110 - 10/2)
    .rect(10, 10)
    .loft()
)

# Combine Spine and Arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3)
for z_pos in hole_z_positions:
    # Create a cylinder through the spine at the specified Z
    hole = (
        cq.Workplane("YZ")
        .workplane(offset=0)
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(thickness_spine + 1) # Extend slightly to ensure clean cut
    )
    bracket = bracket.cut(hole)

# 4. Subtract Screwdriver Clearance (R3)
# No material within 4mm of hole axis for x >= 10.
for z_pos in hole_z_positions:
    # Create a box centered at y=0, z=z_pos, spanning x from 10 to 160
    # We use a height (dz) that covers the clearance area around the screw axis
    clearance_box = (
        cq.Workplane("XY")
        .box(150, clearance_y_width, 20, centered=(False, True, True))
        .translate((10, 0, z_pos))
    )
    bracket = bracket.cut(clearance_box)

# Final result assignment
result = bracket