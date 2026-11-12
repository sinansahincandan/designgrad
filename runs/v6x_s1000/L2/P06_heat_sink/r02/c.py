import cadquery as cq

# Parameters based on Design Document
base_size = 40.0
base_thick = 3.0
num_fins = 6
fin_width = 40.0  # longitudinal dimension (along Y)
fin_thickness = 1.5 # transverse dimension (along X)
fin_height = 20.0

hole_x_pos = 15.0
access_void_diam = 8.0

# 1. Create the Base
# Occupies z=0 to z=3. centered=(True, True, False) puts bottom at z=0.
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create Fins
# We need to space 6 fins across the 40mm width.
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

# Step 1 (Union): Combine Base and Fins into one solid
result = base
for f in fins_list:
    result = result.union(f)

# Step 2 (Subtraction): Create two 8mm diameter voids from z=0 to z=23 at (+-15, 0)
# This satisfies R5 by providing both the screw hole and screwdriver access.
voids = (
    cq.Workplane("XY")
    .pushPoints([(hole_x_pos, 0), (-hole_x_pos, 0)])
    .cylinder(base_thick + fin_height, access_void_diam/2, centered=(True, True, False))
)

# Perform the single subtraction to maintain topological integrity
result = result.cut(voids)

# Final object 'result' is a single solid satisfying R1-R6.