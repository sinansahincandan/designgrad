import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
total_height = 22.0
fin_height = total_height - base_thick
num_fins = 8
fin_thick = 1.5  # Reduced to meet mass and design doc requirements
hole_diam = 3.2
hole_x = 15.0
clearance_radius = 3.0 # Radius for screwdriver access (6mm diameter)

# Calculate spacing to fit fins within the footprint
gap = (base_size - (num_fins * fin_thick)) / (num_fins - 1)

# 1. Create the base
# Base is from z=0 to z=3
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
fins_union = None
for i in range(num_fins):
    start_x = -base_size/2 + fin_thick/2
    x_pos = start_x + i * (fin_thick + gap)
    
    # Check if this fin's X-range overlaps with the screwdriver clearance zones
    # Clearance zone is [hole_x - clearance_radius, hole_x + clearance_radius]
    # We skip adding fins that would intersect the clearance zones to ensure R5
    fin_left = x_pos - fin_thick/2
    fin_right = x_pos + fin_thick/2
    
    overlap_pos = abs(hole_x)
    # If the fin is within the 6mm diameter zone (radius 3 around +/- 15)
    if (fin_left < overlap_pos + clearance_radius and fin_right > overlap_pos - clearance_radius):
        continue

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
if fins_union is not None:
    result = base.union(fins_union)
else:
    result = base

# 3. Subtract mounting holes and screwdriver clearance
# Hole through the base (z=0 to z=base_thick)
hole_cylinders = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(hole_diam / 2)
    .extrude(base_thick)
)

# Screwdriver access: A cylinder of diameter 6mm from z=3 to top
access_cylinders = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_radius)
    .extrude(fin_height)
    .translate((0, 0, base_thick))
)

# Combine the subtraction volumes
subtraction = hole_cylinders.union(access_cylinders)

# Final result: subtract from the solid
result = result.cut(subtraction)