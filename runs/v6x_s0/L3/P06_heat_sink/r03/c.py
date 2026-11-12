import cadquery as cq

# Parameters from Design Document
base_size = 40.0
base_thick = 3.0
total_height = 22.0  # Total height of the part (z=0 to z=22)
fin_height = total_height - base_thick
num_fins = 8
fin_thick = 2.0
hole_diam = 3.2
clearance_radius = 3.0 # Radius for screwdriver access (6mm diameter)
hole_x = 15.0

# Calculate spacing to fit fins within the footprint exactly
# gap is the distance between the edges of adjacent fins
gap = (base_size - (num_fins * fin_thick)) / (num_fins - 1)

# 1. Create the base
# Base from z=0 to z=3, centered on XY origin
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
# Fins are oriented along the Y-axis (width = base_size)
fins_union = None
for i in range(num_fins):
    # Calculate x position for each fin center
    # The first fin starts at -base_size/2 + fin_thick/2
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

# Combine base and fins into one solid before subtraction (R1)
result = base.union(fins_union)

# 3. Subtract mounting holes and screwdriver clearance (R5)
# We create a single unified subtraction volume to avoid topological errors.
# The hole cuts through the base (z=0 to z=3).
# The clearance cylinder cuts from the top of the base (z=3) upwards.

subtraction = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(hole_diam / 2)
    .extrude(base_thick)
).union(
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_radius)
    .extrude(total_height - base_thick) # Extends from z=3 to the top
    .translate((0, 0, base_thick))      # Move start point to z=base_thick
)

# Final result: subtract the combined voids from the solid
result = result.cut(subtraction)