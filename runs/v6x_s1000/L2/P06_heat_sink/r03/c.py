import cadquery as cq

# Parameters based on Design Document
base_size = 40.0
base_thick = 3.0
num_fins = 6
fin_width = 40.0  # longitudinal dimension (along Y)
fin_thickness = 1.5 # transverse dimension (along X)
fin_height = 20.0

hole_diam = 3.2
access_void_diam = 8.0
hole_x_pos = 15.0

# 1. Create the Base
# Occupies z=0 to z=3. centered=(True, True, False) puts bottom at z=0.
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create Fins
# To center them, we calculate positions such that gaps are equal.
# Total thickness of fins = 6 * 1.5 = 9.0
# Remaining width = 40 - 9 = 31.0
# Number of gaps (including edges) = 7
gap_width = (base_size - (num_fins * fin_thickness)) / (num_fins + 1)

fins_list = []
for i in range(num_fins):
    # Calculate X position for the center of each fin
    x_pos = -base_size/2 + gap_width/2 + i * (fin_thickness + gap_width) + fin_thickness/2
    
    # Create fin: 1.5mm thick (X), 40mm wide (Y), 20mm high (Z)
    # We place it starting at z=3 (top of base)
    fin = (
        cq.Workplane("XY")
        .box(fin_thickness, fin_width, fin_height, centered=(True, True, False))
        .translate((x_pos, 0, base_thick))
    )
    fins_list.append(fin)

# Combine Base and Fins into one solid using union (R1)
result = base
for f in fins_list:
    result = result.union(f)

# 3. Mounting Holes and Screwdriver Access (R5)
hole_centers = [(hole_x_pos, 0.0), (-hole_x_pos, 0.0)]

# Perform subtractions using workplanes coincident with the base surfaces 
# to ensure R3 (base thickness integrity) and R5 (access voids) are met correctly.

for cx, cy in hole_centers:
    # Step 1: Drill through the base (z=0 to z=3)
    # We select the bottom face (<Z) to ensure the cylinder is perfectly aligned with the base thickness
    result = result.faces("<Z").workplane().center(cx, cy).cut(
        cq.Workplane("XY").cylinder(base_thick, hole_diam / 2)
    )

# Step 2: Remove material above the base for screwdriver access (R5)
# "no material within 8mm of either hole axis above the base"
for cx, cy in hole_centers:
    # We select the top face (>Z) which is at z=3. 
    # The cylinder will extend from z=3 upwards through the fins.
    result = result.faces(">Z").workplane().center(cx, cy).cut(
        cq.Workplane("XY").cylinder(fin_height, access_void_diam / 2)
    )

# Final object 'result' is a single solid satisfying R1-R6.