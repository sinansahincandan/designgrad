import cadquery as cq

# Parameters based on Design Document and Specifications
base_x_extent = 60.0          # X extent: [-30, 30] (R2)
clamp_width = 20.0            # Y extent: [-10, 10] (R2)
base_thickness = 4.0          # Z thickness for base
flange_x_start = 18.5         # R6 requirement
flange_x_end = 23.0           # R6 requirement
flange_y_half = 4.0           # R6 requirement (total width 8)
flange_thickness = 3.0        # R6 requirement

screw_hole_dia = 6.6          # R5
screw_x = 27.0                # R5

pipe_radius = 12.6            # R3 clearance radius
saddle_outer_radius = 17.0    # R4: ensures material up to 15.5mm
pipe_center_z = 12.5          # Pipe axis height (R3/R4)

# 1. Create the Base (R2)
# Bottom surface at z=0, centered on X and Y.
base = cq.Workplane("XY").box(base_x_extent, clamp_width, base_thickness).translate((0, 0, base_thickness/2))

# 2. Create the Flanges (R6)
# Explicitly define flange volumes to ensure compliance with R6 dimensions.
# Flange 1: Positive X
flange_pos = cq.Workplane("XY").box(
    flange_x_end - flange_x_start, 
    flange_y_half * 2, 
    flange_thickness
).translate((
    (flange_x_start + flange_x_end) / 2, 
    0, 
    flange_thickness / 2
))

# Flange 2: Negative X
flange_neg = cq.Workplane("XY").box(
    flange_x_end - flange_x_start, 
    flange_y_half * 2, 
    flange_thickness
).translate((
    -(flange_x_start + flange_x_end) / 2, 
    0, 
    flange_thickness / 2
))

# Combine Base and Flanges (R1)
combined_base = base.union(flange_pos).union(flange_neg)

# 3. Create the Saddle Arch (R4)
# A cylinder centered at (0, 0, pipe_center_z) that provides material in the required band.
arch_height = 40.0
arch = cq.Workplane("XY").cylinder(arch_height, saddle_outer_radius).translate((0, 0, pipe_center_z))

# Combine Base/Flanges and Arch (R1)
combined_body = combined_base.union(arch)

# 4. Subtract Pipe Clearance (R3)
# The pipe volume must be free of material.
pipe_clearance = cq.Workplane("XY").cylinder(50.0, pipe_radius).translate((0, 0, pipe_center_z))
result = combined_body.cut(pipe_clearance)

# 5. Subtract Screw Holes (R5)
# Vertical holes at (+-27, 0), diameter 6.6mm.
# We use a large Z extent to ensure they penetrate the base completely.
hole_radius = screw_hole_dia / 2
hole_left = cq.Workplane("XY").cylinder(10.0, hole_radius).translate((-screw_x, 0, 0))
hole_right = cq.Workplane("XY").cylinder(10.0, hole_radius).translate((screw_x, 0, 0))

result = result.cut(hole_left).cut(hole_right)