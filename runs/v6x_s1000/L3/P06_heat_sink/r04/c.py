import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
num_fins = 10
fin_thickness = 1.0
fin_height = 22.0
hole_diam = 3.2
access_diam = 6.1

# 1. Create the Base (z=0 to z=3)
# centered=(True, True, False) ensures the base starts at z=0 and is centered on X/Y
body = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Subtract mounting holes from base first (R3 compliance)
# This ensures the only subtractions in the z=0 to 3 range are the 3.2mm holes
for cx, cy in [(15.0, 0.0), (-15.0, 0.0)]:
    hole = (
        cq.Workplane("XY")
        .cylinder(base_thick, hole_diam / 2)
        .translate((cx, cy, base_thick / 2))
    )
    body = body.cut(hole)

# 3. Create and Union Fins
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

for f in fins_list:
    body = body.union(f)

# 4. Subtract access cutouts from the unioned body (R5 compliance)
# These voids are defined strictly for z >= 3 to ensure base integrity
for cx, cy in [(15.0, 0.0), (-15.0, 0.0)]:
    access_cutout = (
        cq.Workplane("XY")
        .cylinder(fin_height, access_diam / 2)
        .translate((cx, cy, base_thick + fin_height / 2))
    )
    body = body.cut(access_cutout)

result = body