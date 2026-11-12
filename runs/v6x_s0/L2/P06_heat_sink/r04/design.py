import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
total_height = 25.0
fin_height = total_height - base_thick
num_fins = 8
fin_thick = 1.8
hole_diam = 3.2
hole_x = 15.0
clearance_radius = 3.0  # Radius for screwdriver access (6mm diameter)

# Calculate spacing to fit fins within the footprint
# The gap is the distance between the center of one fin and the next, minus thickness
gap = (base_size - (num_fins * fin_thick)) / (num_fins - 1)

# 1. Create the base
# centered=(True, True, False) ensures the bottom face is at z=0
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
fins_union = None
for i in range(num_fins):
    # Calculate x position for each fin center
    start_x = -base_size/2 + fin_thick/2
    x_pos = start_x + i * (fin_thick + gap)
    
    # Create a single fin
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
# To satisfy R5 robustly, we create a single subtraction volume that covers 
# the entire vertical span from z=0 to z=total_height.
# Using the clearance_radius (3.0mm) ensures both the 3.2mm hole and the 
# required screwdriver access are removed in one operation.
subtraction = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_radius)
    .extrude(total_height)
)

# Final result: subtract the entire cylinder volume from the solid
result = result.cut(subtraction)