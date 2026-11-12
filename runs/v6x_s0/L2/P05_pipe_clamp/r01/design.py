import cadquery as cq

# Parameters based on Design Document and Specifications
clamp_width = 20.0          # Y extent: [-10, 10] (R2)
base_x_extent = 60.0        # X extent: [-30, 30] (R2)
base_thickness = 4.0        # Z thickness for base
flange_thickness = 3.0      # R6 requirement
screw_hole_dia = 6.6        # R5
screw_x = 27.0              # R5
pipe_radius = 12.6          # R3 clearance radius
saddle_outer_radius = 15.5  # R4 outer boundary
pipe_center_z = 12.5        # Pipe axis height

# 1. Create the Base (R2, R6)
# The bottom surface sits at z=0.
# Using centered=False and translating to ensure min corner is at (-30, -10, 0)
base = cq.Workplane("XY").box(base_x_extent, clamp_width, base_thickness, centered=False).translate((-base_x_extent/2, -clamp_width/2, 0))

# 2. Create the Saddle Arch (R4)
# The arch is a cylinder centered at (0, 0, pipe_center_z).
# To ensure it connects to the base (which ends at z=4), we extend the cylinder downwards.
# Pipe center is at 12.5. Base top is at 4.0. 
# We need the cylinder to reach from pipe_center_z down to at least z=3 to overlap with the base.
# Height of cylinder = (pipe_center_z - 0) + some extra for safety.
arch_height = pipe_center_z + 10.0 

# We use a Workplane on XY and translate it so the center is at (0, 0, pipe_center_z).
# Note: cylinder(h, r) in CadQuery creates a cylinder of height h centered at the workplane origin.
# To place its center at z=12.5, we translate the whole object.
arch_cylinder = cq.Workplane("XY").cylinder(arch_height, saddle_outer_radius).translate((0, 0, pipe_center_z))

# Combine Base and Arch to form a single continuous solid (R1)
combined_body = base.union(arch_cylinder)

# 3. Subtract Pipe Clearance (R3)
# The pipe volume (radius 12.6) must be free of material.
pipe_clearance = cq.Workplane("XY").cylinder(pipe_center_z * 3, pipe_radius).translate((0, 0, pipe_center_z))
result = combined_body.cut(pipe_clearance)

# 4. Subtract Screw Holes (R5)
# Vertical holes at (+-27, 0), diameter 6.6mm.
# We create cylinders that go through the base.
hole_left = cq.Workplane("XY").cylinder(base_thickness + 2, screw_hole_dia/2).translate((-screw_x, 0, base_thickness/2))
hole_right = cq.Workplane("XY").cylinder(base_thickness + 2, screw_hole_dia/2).translate((screw_x, 0, base_thickness/2))

result = result.cut(hole_left).cut(hole_right)