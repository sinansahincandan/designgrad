import cadquery as cq

# Parameters
base_size = 40.0
base_thick = 3.0
num_fins = 10
fin_thickness = 1.0
fin_height = 22.0  # Total height = base_thick + fin_height = 25.0
hole_diam = 3.2
access_diam = 7.0

# 1. Create the Base (z=0 to z=3)
base = cq.Workplane("XY").box(base_size, base_size, base_thick, centered=(True, True, False))

# 2. Create Fins and combine them first
fins_combined = None
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
    
    if fins_combined is None:
        fins_combined = fin
    else:
        fins_combined = fins_combined.union(fin)

# Combine Base and Fins into one solid before cutting holes
result = base.union(fins_combined)

# 3. Mounting Holes (R5) and Screwdriver Access (R5)
hole_centers = [(15.0, 0.0), (-15.0, 0.0)]

# Create mounting holes (through the base z=0 to 3)
result = (
    result.faces("<Z").workplane()
    .pushPoints(hole_centers)
    .hole(hole_diam)
)

# Create screwdriver access voids (from z=3 upwards through fins)
# Instead of complex selectors, we use a Workplane at Z=3 directly to cut upwards.
# To ensure the hole cuts "up" from Z=3, we create a cylinder and subtract it.
# The design requires holes centered at (+-15, 0) extending from z=3 to z=25.

for cx, cy in hole_centers:
    # Create a cylindrical void for screwdriver access
    # Cylinder is defined by height and radius. We place it at (cx, cy, 3).
    # To cut upwards through the fins, we use cylinder(height, radius) and translate to z=3.
    access_void = cq.Workplane("XY").cylinder(fin_height, access_diam / 2).translate((cx, cy, base_thick))
    result = result.cut(access_void)

# Final check: result is a single solid.