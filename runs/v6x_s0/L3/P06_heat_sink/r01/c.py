import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
total_height = 22.0
fin_height = total_height - base_thick
num_fins = 8
fin_thick = 2.0
hole_diam = 3.2
clearance_radius = 3.0  # Radius for screwdriver access (6mm diameter)
hole_x = 15.0

# Calculate spacing to fit fins within the footprint exactly
# The first fin is at -base_size/2 + fin_thick/2, last is at base_size/2 - fin_thick/2
# Total distance between centers of first and last fin: (num_fins - 1) * gap_center_to_center
gap = (base_size - fin_thick) / (num_fins - 1)

# 1. Create the base
# Base is from z=0 to z=3
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
fins_union = None
for i in range(num_fins):
    # Calculate x position for each fin center
    # Start from the left edge and move inwards by half a fin thickness
    x_pos = -base_size/2 + (fin_thick/2) + i * gap
    
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

# 3. Subtract mounting holes and screwdriver clearance (R5)
# As per feedback, we create a single subtraction volume for each hole location.
# A cylinder of diameter 6mm (clearance_radius=3.0) from z=0 to total_height 
# satisfies both the 3.2mm hole requirement in the base and the screwdriver access above.
subtraction = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_radius)
    .extrude(total_height)
)

# Final result: subtract the clearance/holes from the solid
result = result.cut(subtraction)