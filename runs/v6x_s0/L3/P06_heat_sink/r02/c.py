import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
total_height = 22.0
fin_height = total_height - base_thick
num_fins = 8
fin_thick = 2.0
hole_diam = 3.2
clearance_diam = 6.0  # Diameter for screwdriver access (radius 3mm)
hole_x = 15.0

# Calculate spacing to fit fins within the footprint
gap = (base_size - (num_fins * fin_thick)) / (num_fins - 1)

# 1. Create the base
# Base spans z=0 to z=3
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
# We build them as a single object to union with the base
fins_list = []
for i in range(num_fins):
    # Calculate x position for each fin center
    x_pos = -base_size/2 + (fin_thick/2) + i * (fin_thick + gap)
    
    # Create a single fin and add it to the fins collection
    # Fins extend from z=3 to z=22. We use translate to position them correctly.
    # To avoid workplane errors, we create each fin as its own Workplane object.
    fin = (
        cq.Workplane("XY")
        .box(fin_thick, base_size, fin_height, centered=(True, True, False))
        .translate((x_pos, 0, base_thick))
    )
    fins_list.append(fin)

# Union all fins together first
fins = fins_list[0]
for i in range(1, len(fins_list)):
    fins = fins.union(fins_list[i])

# Combine base and fins into one solid
result = base.union(fins)

# 3. Subtract mounting holes and screwdriver clearance
# We use fresh Workplanes to avoid the "multiple objects" error caused by offset on a complex body.

hole_only = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(hole_diam / 2)
    .extrude(base_thick)
)

# For clearance, we create a new workplane at z=base_thick
clearance_only = (
    cq.Workplane("XY")
    .workplane(offset=base_thick)
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_diam / 2)
    .extrude(fin_height)
)

# Combine subtractions and cut from the result
result = result.cut(hole_only).cut(clearance_only)