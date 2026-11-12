import cadquery as cq

# Parameters based on Design Document and Specifications
clamp_width = 20.0          # Y extent: [-10, 10] (R2)
base_x_extent = 60.0        # X extent: [-30, 30] (R2)
base_thickness = 4.0        # Z thickness for base
screw_hole_dia = 6.6        # R5
screw_x = 27.0              # R5
pipe_radius = 12.6          # R3 clearance radius
saddle_outer_radius = 15.8  # R4 requirement (between 15.5 and 16.0)
pipe_center_z = 12.5        # Pipe axis height

# The disconnection occurs because the pipe (r=12.6) is wider than the clamp width (y=-10 to 10)
# at x=0, cutting through the center of the base and arch.
# To ensure a single solid, we must provide material that connects the two sides.
# Since R2 restricts Y-width to 20mm, we must add connection material in X or Z.

# 1. Create the Base (R2)
base = (
    cq.Workplane("XY")
    .box(base_x_extent, clamp_width, base_thickness, centered=(True, True, False))
)

# 2. Create the Saddle Arch (R4)
arch_cylinder = (
    cq.Workplane("XY")
    .cylinder(100, saddle_outer_radius)
    .translate((0, 0, pipe_center_z))
)

# Limit the arch to the Y-extent of the clamp
y_limiter = cq.Workplane("XY").box(base_x_extent + 2, clamp_width, 100)
arch_limited = arch_cylinder.intersect(y_limiter)

# 3. Create Connecting Ribs (R1)
# To prevent the pipe from splitting the part into two pieces, we add ribs at |x| > 12.6.
# At x=13, the distance to center is sqrt(13^2 + 0^2) = 13, which is > 12.6 (pipe radius).
# This ensures a continuous path of material from the base to the arch at the sides.
rib_x_pos = 14.0
rib_width = 5.0
rib_depth = clamp_width
rib_height = pipe_center_z + 20.0 # Ensure it reaches from base up through the arch

rib_left = (
    cq.Workplane("XY")
    .box(rib_width, rib_depth, rib_height, centered=(True, True, False))
    .translate((-rib_x_pos, 0, rib_height / 2))
)

rib_right = (
    cq.Workplane("XY")
    .box(rib_width, rib_depth, rib_height, centered=(True, True, False))
    .translate((rib_x_pos, 0, rib_height / 2))
)

# Combine all components into one solid before subtraction
combined_body = base.union(arch_limited).union(rib_left).union(rib_right)

# 4. Subtract Pipe Clearance (R3)
pipe_clearance = (
    cq.Workplane("XY")
    .cylinder(100, pipe_radius)
    .translate((0, 0, pipe_center_z))
)
result = combined_body.cut(pipe_clearance)

# 5. Subtract Screw Holes (R5)
hole_left = (
    cq.Workplane("XY")
    .cylinder(100, screw_hole_dia / 2)
    .translate((-screw_x, 0, -1))
)
hole_right = (
    cq.Workplane("XY")
    .cylinder(100, screw_hole_dia / 2)
    .translate((screw_x, 0, -1))
)

result = result.cut(hole_left).cut(hole_right)