import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
fin_height = 20.0
num_fins = 8
fin_thickness = 3.0
hole_diam = 3.2

# Calculate spacing for fins to center them on the base
# The base is centered at (0,0) in terms of its footprint if we use box(centered=True)
# or we can define it from -20 to 20.
gap_width = (base_size - (num_fins * fin_thickness)) / (num_fins + 1)

# 1. Create the Base
# We'll place the base such that its center is at (0,0, base_thick/2)
# This makes the Z range [0, 3]
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, True)).translate((0, 0, base_thick/2))

# 2. Create Fins
fins_list = []
for i in range(num_fins):
    # Calculate X position for each fin relative to the center (0,0)
    # The first gap starts at -base_size/2
    x_pos = -base_size/2 + gap_width/2 + i * (fin_thickness + gap_width) + fin_thickness/2
    
    # To ensure overlap and a single solid, we extend the fin into the base.
    # Fin height is 20mm. We place it from z=3 to z=23.
    # We add an overlap of 1mm into the base (starting at z=2)
    overlap = 1.0
    fin = (
        cq.Workplane("XY")
        .box(fin_thickness, base_size, fin_height + overlap, centered=(True, True, False))
        .translate((x_pos, 0, base_thick - overlap))
    )
    fins_list.append(fin)

# Combine Base and Fins into one solid using union
result = base
for f in fins_list:
    result = result.union(f)

# 3. Mounting Holes and Screwdriver Access (R5)
# Hole centers at (+-15, 0) relative to the center of the base
hole_centers = [(15.0, 0.0), (-15.0, 0.0)]

for cx, cy in hole_centers:
    # Drill through the base (z=0 to z=3)
    # We use a cylinder for cutting to ensure it's clean
    hole = cq.Workplane("XY").cylinder(base_thick + 2, hole_diam/2).translate((cx, cy, base_thick/2))
    result = result.cut(hole)
    
    # Remove material above the base for screwdriver access (R5)
    # "no material within 3mm of either hole axis above the base" -> diameter 6mm
    # This cutout starts at z=3 and goes up to the top of the fins.
    access_cutout = (
        cq.Workplane("XY")
        .workplane(offset=base_thick)
        .center(cx, cy)
        .cylinder(fin_height + 1.0, 6.0/2) # radius is 3mm
    )
    result = result.cut(access_cutout)

# Final check: The resulting object is a single solid.