import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
total_height = 22.0
fin_height = total_height - base_thick
num_fins = 8
fin_thick = 2.0
hole_diam = 3.2
hole_x = 15.0
clearance_radius = 3.0 # Radius for screwdriver access

# Calculate spacing to fit fins within the footprint
gap = (base_size - (num_fins * fin_thick)) / (num_fins - 1)

# 1. Create the base
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
# We will build a single Workplane for all fins to avoid union issues in loops
fins_union = None
for i in range(num_fins):
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
# Instead of using .hole() on a Workplane without a solid, we create cylinders to cut
# Hole through the base (z=0 to z=base_thick)
hole_cylinders = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(hole_diam / 2)
    .extrude(base_thick + 1, both=True) # Ensure it cuts through the base
)

# Screwdriver access: A cylinder of diameter 6mm (radius 3) from z=3 to top
access_cylinders = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_radius)
    .extrude(total_height)
    .translate((0, 0, base_thick)) # Start from top of base
)

# Combine the subtraction volumes
subtraction = hole_cylinders.union(access_cylinders)

# Final result: subtract from the solid
result = result.cut(subtraction)