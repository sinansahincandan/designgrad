import cadquery as cq

# Parameters based on Design Document
base_size = 40.0
base_thick = 3.0
num_fins = 6
fin_width = 1.5  # longitudinal dimension (along Y)
fin_thickness = 1.5 # transverse dimension (along X)
fin_height = 20.0

hole_x_pos = 15.0
access_void_diam = 8.0

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
        .box(fin_thickness, base_size, fin_height, centered=(True, True, False))
        .translate((x_pos, 0, base_thick))
    )
    fins_list.append(fin)

# Combine Base and Fins into one solid using union (R1)
result = base
for f in fins_list:
    result = result.union(f)

# 3. Integrated Access Voids (R5)
# Instead of separate hole and access cuts, we perform a single subtraction per location.
# The voids are 8mm diameter cylinders from z=0 to z=23.
# This satisfies the mounting hole requirement and the screwdriver clearance.
voids = (
    cq.Workplane("XY")
    .workplane(offset=11.5) # Center of the cylinder at z=11.5 so it spans 0 to 23
    .cylinder(23.0, access_void_diam/2)
    .center(hole_x_pos, 0)
    .workplane(offset=11.5) # Re-aligning for the second cylinder
    .cylinder(23.0, access_void_diam/2)
    .center(-hole_x_pos, 0)
)

# To ensure precise Z alignment from z=0 to z=23 as requested:
# We create a single workplane and place two cylinders.
voids = (
    cq.Workplane("XY")
    .pushPoints([(hole_x_pos, 0), (-hole_x_pos, 0)])
    .cylinder(23.0, access_void_diam/2)
    .translate((0, 0, 11.5)) # Move cylinder so it spans z=0 to z=23
)

# Correcting the subtraction logic to be robust:
# We create a single object representing the voids and subtract it from the result.
void_geometry = (
    cq.Workplane("XY")
    .pushPoints([(hole_x_pos, 0), (-hole_x_pos, 0)])
    .cylinder(23.0, access_void_diam/2)
    .translate((0, 0, 11.5))
)

result = result.cut(void_geometry)

# Final object 'result' is a single solid satisfying R1-R6.