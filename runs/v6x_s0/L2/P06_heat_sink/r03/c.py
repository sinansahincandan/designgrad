import cadquery as cq

# Parameters based on Design Document optimization
base_size = 40.0
base_thick = 3.0
total_height = 23.0  # z=0 to z=23
fin_height = total_height - base_thick
num_fins = 8
fin_thick = 1.8      # Optimized for Mass (R6) and Thermal (R4)
hole_diam = 3.2
hole_x = 15.0
clearance_radius = 3.0 # Radius for screwdriver access (diameter 6mm)

# Calculate spacing to fit fins within the footprint
# Gap is the space between the edges of adjacent fins
gap = (base_size - (num_fins * fin_thick)) / (num_fins - 1)

# 1. Create the base
# Base is from z=0 to z=3, centered on origin in XY
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
fins_union = None
for i in range(num_fins):
    # Calculate x position for each fin to distribute them evenly across the footprint
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

# Combine base and fins into one solid
result = base.union(fins_union)

# 3. Subtract mounting holes and screwdriver clearance
# As per feedback, create a single subtraction volume that covers the entire vertical span.
# A circle with radius 3.0 (diameter 6mm) satisfies both the 3.2mm hole requirement 
# and the 3mm clearance requirement from the axis.
subtraction = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_radius) 
    .extrude(total_height)     # Extrude from z=0 to total_height
)

# Final result: subtract the large cylinders from the base+fins solid
result = result.cut(subtraction)