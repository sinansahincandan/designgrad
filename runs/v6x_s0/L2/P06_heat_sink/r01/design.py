import cadquery as cq

# Parameters based on Design Document and Feedback
base_size = 40.0
base_thick = 3.0
total_height = 23.0  # z=0 to z=23
num_fins = 8
fin_thick = 2.0
hole_diam = 3.2
hole_x = 15.0
clearance_diam = 6.2

# Calculate spacing for fins within the footprint (40mm)
# The gap is between the edges of adjacent fins
gap = (base_size - (num_fins * fin_thick)) / (num_fins - 1)

# 1. Create the base
# Base sits from z=0 to z=3
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
# Fins extend from z=3 to z=total_height (fin_height = total_height - base_thick)
fin_height = total_height - base_thick
fins_union = None

for i in range(num_fins):
    # Calculate x position for each fin center
    start_x = -base_size/2 + fin_thick/2
    x_pos = start_x + i * (fin_thick + gap)
    
    fin = (
        cq.Workplane("XY")
        .workplane(offset=base_thick)
        .box(fin_thick, base_size, fin_height, centered=(True, True, False))
        .translate((x_pos, 0, 0))
    )
    
    if fins_union is None:
        fins_union = fin
    else:
        fins_union = fins_union.union(fin)

# Combine base and fins into one solid (R1)
result = base.union(fins_union)

# 3. Subtract mounting holes and screwdriver clearance
# Hole through the base (z=0 to z=base_thick)
hole_cylinders = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(hole_diam / 2)
    .extrude(base_thick)
)

# Corrected screwdriver access: diameter 6.2mm from z=3 to top of fins
access_cylinders = (
    cq.Workplane("XY")
    .workplane(offset=base_thick)
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_diam / 2)
    .extrude(fin_height)
)

# Combine the subtraction volumes into one single solid to ensure clean cut
subtraction = hole_cylinders.union(access_cylinders)

# Final result: subtract from the main solid
result = result.cut(subtraction)