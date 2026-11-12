import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
num_fins = 10
fin_thickness = 1.0
fin_height = 22.0
hole_diam = 3.2
access_diam = 7.0

# 1. Create the Base (z=0 to z=3)
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create Fins
fins_list = []
gap = (base_size - (num_fins * fin_thickness)) / (num_fins + 1)

for i in range(num_fins):
    # Calculate X position for each fin using linear spacing
    x_pos = -base_size/2 + gap/2 + i * (fin_thickness + gap)
    
    # Fins sit on top of the base (from z=3 to z=25)
    fin = (
        cq.Workplane("XY")
        .box(fin_thickness, base_size, fin_height, centered=(True, True, False))
        .translate((x_pos, 0, base_thick))
    )
    fins_list.append(fin)

# Combine Base and Fins into one solid
result = base
for f in fins_list:
    result = result.union(f)

# 3. Mounting Holes and Screwdriver Access (R5)
hole_centers = [(15.0, 0.0), (-15.0, 0.0)]

for cx, cy in hole_centers:
    # Hole: Diameter 3.2mm through the base (z=0 to z=3)
    # We use a cylinder centered at (cx, cy) and translate it so it covers z=0 to z=3
    hole = (
        cq.Workplane("XY")
        .cylinder(base_thick, hole_diam/2)
        .translate((cx, cy, base_thick/2))
    )
    result = result.cut(hole)
    
    # Access Cutout: Diameter 7mm from z=3 to top (z=25)
    # We create a cylinder of height fin_height and place it at the base surface
    access_cutout = (
        cq.Workplane("XY")
        .cylinder(fin_height, access_diam/2)
        .translate((cx, cy, base_thick))
    )
    result = result.cut(access_cutout)

# Final check: The resulting object is a single solid (R1).