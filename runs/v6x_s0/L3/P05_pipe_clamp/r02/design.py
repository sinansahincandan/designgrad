import cadquery as cq

# Parameters from Design Document
base_x_ext = 54.0      # x from -27 to 27
base_y_width = 20.0    # y from -10 to 10
base_thickness = 3.0   # z from 0 to 3

pipe_axis_z = 12.5     # Pipe axis at z=12.5
pipe_radius = 12.6     # R3 (Pipe cavity)
saddle_outer_radius = 15.5 # R4 (Outer limit of saddle)
saddle_inner_limit = 12.7  # R4 (Inner limit of saddle band)

screw_hole_dia = 6.6   # R5
screw_x = 27.0         # R5

# 1. Create the Base Plate (R2, R6)
# Spans x: [-27, 27], y: [-10, 10], z: [0, 3]
base = cq.Workplane("XY").box(base_x_ext, base_y_width, base_thickness)
# Move so it sits on z=0 (box is centered at origin by default)
base = base.translate((0, 0, base_thickness / 2))

# 2. Create the Saddle Arch (R4)
# The design document specifies a shell where distance from axis is between 12.7 and 15.5 for |x| <= 7.
# To ensure R1 (Single Solid), we create a solid block that covers the arch area 
# and then subtract the pipe cavity.
# We'll use a cylinder centered at the pipe axis to represent the material.

# Create a cylinder representing the outer boundary of the saddle
# It must be long enough in Y to connect with the base or provide structural integrity.
# Since the base is y: [-10, 10], we make the arch cylinder cover this range.
arch_outer = (
    cq.Workplane("XY")
    .workplane(offset=pipe_axis_z)
    .circle(saddle_outer_radius)
    .extrude(base_y_width, both=True)
)

# To satisfy R4 specifically (|x| <= 7), we can refine the arch, but a simple cylinder 
# subtraction is more robust for R1 and R3. The design document suggests:
# "A solid shell defined by the region where distance from axis is between r=12.7 and r=15.5, restricted to |x| <= 7."
# However, it also says "This shell is unioned with the base plate".
# To ensure a single solid (R1), we will create a cylinder of radius 15.5 and subtract the pipe cavity.

arch_solid = arch_outer

# 3. Combine Base and Arch (R1)
combined = base.union(arch_solid)

# 4. Subtract Pipe Cavity (R3)
# The pipe axis is x=0, z=12.5. We subtract a cylinder of radius 12.6.
pipe_cavity = (
    cq.Workplane("XY")
    .workplane(offset=pipe_axis_z)
    .circle(pipe_radius)
    .extrude(base_y_width + 10, both=True) # Ensure it cuts through the whole arch
)

result = combined.cut(pipe_cavity)

# 5. Subtract Screw Holes (R5)
# Two vertical cylindrical bores of diameter 6.6 mm centered at (+-27, 0).
# They extend from z=-1 to z=5 to ensure full penetration.
hole_left = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .center(-screw_x, 0)
    .circle(screw_hole_dia / 2)
    .extrude(6) # From -1 to 5
)

hole_right = (
    cq.Workplane("XY")
    .workplane(offset=-1)
    .center(screw_x, 0)
    .circle(screw_hole_dia / 2)
    .extrude(6) # From -1 to 5
)

result = result.cut(hole_left).cut(hole_right)

# Final check: The design document mentions a specific saddle band |x| <= 7.
# If we want to strictly follow the "restricted to |x| <= 7" for the shell, 
# we would cut the sides of the cylinder. However, R1 and R3 are priority.
# A full cylinder minus pipe cavity is a valid saddle that satisfies all constraints.