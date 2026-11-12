import cadquery as cq

# Parameters based on Design Document and Specifications
clamp_width = 20.0          # Y extent: [-10, 10] (R2)
base_x_extent = 60.0        # X extent: [-30, 30] (R2)
base_thickness = 4.0        # Z thickness for base
screw_hole_dia = 6.6        # R5
screw_x = 27.0              # R5
pipe_radius = 12.6          # R3 clearance radius
saddle_outer_radius = 15.5  # R4 outer boundary
pipe_center_z = 12.5        # Pipe axis height (Z)
arch_length = 100.0         # Length along Y-axis to ensure coverage

# 1. Create the Base (R2, R6)
# The base is a box centered at (0,0,2) so that its bottom surface is at z=0.
# Dimensions: X=60, Y=20, Z=4. This covers the flange requirements (R6).
base = cq.Workplane("XY").box(base_x_extent, clamp_width, base_thickness).translate((0, 0, base_thickness/2))

# 2. Create the Saddle Arch (R4)
# The pipe axis is x=0, z=12.5, running along the Y-axis.
# We create a cylinder on the YZ plane to represent the arch material.
# A cylinder in "YZ" workplane with height 'arch_length' will extend along the Y direction.
arch_cylinder = (
    cq.Workplane("YZ")
    .cylinder(arch_length, saddle_outer_radius)
    .translate((0, 0, pipe_center_z)) # Center of cylinder at z=12.5
)

# Combine Base and Arch to form a single continuous solid (R1)
combined = base.union(arch_cylinder)

# 3. Subtract Pipe Clearance (R3)
# The pipe volume (radius 12.6 mm) lies along the Y-axis at x=0, z=12.5.
pipe_clearance = (
    cq.Workplane("YZ")
    .cylinder(arch_length + 20, pipe_radius) # Slightly longer to ensure clean cut
    .translate((0, 0, pipe_center_z))
)

# 4. Subtract Screw Holes (R5)
# Vertical holes at (+-27, 0), diameter 6.6mm.
# These are cylinders along the Z-axis.
hole_left = cq.Workplane("XY").cylinder(base_thickness + 10, screw_hole_dia/2).translate((-screw_x, 0, base_thickness/2))
hole_right = cq.Workplane("XY").cylinder(base_thickness + 10, screw_hole_dia/2).translate((screw_x, 0, base_thickness/2))

# Final Boolean Operations (R1)
result = combined.cut(pipe_clearance).cut(hole_left).cut(hole_right)