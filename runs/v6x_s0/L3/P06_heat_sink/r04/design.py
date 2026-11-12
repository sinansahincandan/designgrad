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
clearance_radius = 3.0  # Radius for screwdriver access (6mm diameter)

# 1. Create the base
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create the fins
spacing = (base_size - fin_thick) / (num_fins - 1)

fin_solids = []
for i in range(num_fins):
    x_pos = -base_size/2 + fin_thick/2 + i * spacing
    f = (
        cq.Workplane("XY")
        .workplane(offset=base_thick)
        .box(fin_thick, base_size, fin_height, centered=(True, True, False))
        .translate((x_pos, 0, 0))
    )
    fin_solids.append(f)

# Union all fins and the base into one solid
result = base
for f in fin_solids:
    result = result.union(f)

# 3. Subtract mounting holes and screwdriver clearance (R5)
# Instead of chaining workplanes on a multi-object Workplane, we create two separate subtraction solids
# and union them before cutting from the main body.

# Hole through base (z=0 to z=3)
base_holes = (
    cq.Workplane("XY")
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(hole_diam / 2)
    .extrude(base_thick)
)

# Clearance voids through fins (z=3 to z=22)
clearance_voids = (
    cq.Workplane("XY")
    .workplane(offset=base_thick)
    .pushPoints([(-hole_x, 0), (hole_x, 0)])
    .circle(clearance_radius)
    .extrude(fin_height)
)

# Combine the subtraction volumes and cut from the result
subtraction = base_holes.union(clearance_voids)
result = result.cut(subtraction)