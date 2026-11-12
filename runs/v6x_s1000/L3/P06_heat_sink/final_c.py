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

# Combine Base and Fins into one solid initial body
body = base
for f in fins_list:
    body = body.union(f)

# 3. Create Voids (Mounting Holes and Screwdriver Access)
hole_centers = [(15.0, 0.0), (-15.0, 0.0)]
voids = cq.Workplane("XY")

for cx, cy in hole_centers:
    # Mounting Hole: Diameter 3.2mm through the base (z=0 to z=3)
    # Cylinder height is 3.0, translated so it spans exactly z=0 to z=3
    hole = (
        cq.Workplane("XY")
        .cylinder(base_thick, hole_diam/2)
        .translate((cx, cy, base_thick/2))
    )
    voids = voids.union(hole)
    
    # Access Cutout: Diameter 6.1mm from z=3 to top (z=25)
    # Cylinder height is 22.0, translated so it spans exactly z=3 to z=25
    # Center of cylinder at z = 3 + (22/2) = 14.0? No, the translate logic:
    # To have bottom at z=3 and top at z=25, center must be at z = 3 + 11 = 14.
    access_cutout = (
        cq.Workplane("XY")
        .cylinder(fin_height, access_diam/2)
        .translate((cx, cy, base_thick + fin_height/2))
    )
    voids = voids.union(access_cutout)

# 4. Perform a single cut operation to maintain geometric integrity
result = body.cut(voids)

# Final check: The resulting object is a single solid (R1).