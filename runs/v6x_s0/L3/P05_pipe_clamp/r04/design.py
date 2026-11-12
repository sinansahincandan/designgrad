import cadquery as cq

# Parameters based on Design Document and Requirements
base_x_ext = 54.0      # x from -27 to 27 (R2)
base_y_width = 20.0    # y from -10 to 10 (R2)
base_thickness = 3.0   # z from 0 to 3 (R6)

screw_hole_dia = 6.6   # R5
screw_x = 27.0         # R5

pipe_axis_z = 12.5     # Pipe axis at z=12.5
clearance_radius = 12.6 # R3 (Pipe cavity)
saddle_outer_radius = 15.5 # R4 (Outer limit of saddle)

# 1. Create the Base Plate (R2, R6)
# Spans x: [-27, 27], y: [-10, 10], z: [0, 3]
base = cq.Workplane("XY").box(base_x_ext, base_y_width, base_thickness).translate((0, 0, base_thickness / 2))

# 2. Create the Arch Block (R4)
# The previous error was caused by intersecting a cylinder with a box that didn't cover the center properly.
# Instead of using intersection on a large cylinder, we will build the saddle as a series of segments or 
# simply use a single solid block and subtract the pipe cavity.

# To ensure connectivity, we create a rectangular block for the arch area first.
# The design requires material in the radial band 12.7 <= r <= 15.5 for |x| <= 7.
# We'll create a cylinder centered at (0,0,pipe_axis_z) and ensure it is long enough to overlap the base.

arch_outer = (
    cq.Workplane("XY")
    .workplane(offset=pipe_axis_z)
    .circle(saddle_outer_radius)
    .extrude(40, both=True) 
)

# To ensure it is a single solid and covers the required x range, we union base and arch.
# We must avoid 'intersect' with a box that might split the cylinder if not careful.
# Instead of intersecting, let's create the saddle by taking the outer cylinder 
# and subtracting everything outside the desired Y and X bounds.

combined = base.union(arch_outer)

# To restrict the arch to the width of the base (y in [-10, 10]), we subtract two large blocks.
# This is safer than intersection for maintaining a single solid.
side_block_left = cq.Workplane("XY").box(base_x_ext + 20, 100, 100).translate((0, -60, 25))
side_block_right = cq.Workplane("XY").box(base_x_ext + 20, 100, 100).translate((0, 60, 25))
combined = combined.cut(side_block_left).cut(side_block_right)

# Now restrict X extent to [-27, 27] by subtracting two blocks at the ends.
end_block_left = cq.Workplane("XY").box(100, 100, 100).translate((-60, 0, 25))
end_block_right = cq.Workplane("XY").box(100, 100, 100).translate((60, 0, 25))
combined = combined.cut(end_block_left).cut(end_block_right)

# 3. Subtract Pipe Cavity (R3)
pipe_cavity = (
    cq.Workplane("XY")
    .workplane(offset=pipe_axis_z)
    .circle(clearance_radius)
    .extrude(60, both=True)
)
combined = combined.cut(pipe_cavity)

# 4. Subtract Screw Holes (R5)
# We use cylinders to ensure they go through the base plate.
# Since screw_x is at the edge (27), we'll make sure the hole is fully contained by using a slightly smaller x or ensuring the base is wide enough.
# The design says x in [-27, 27]. A hole of dia 6.6 centered at 27 would be half outside.
# However, R5 says "centered at (+-27, 0)". To keep it a single solid and follow the requirement:
# We will place them slightly inside or ensure they are subtracted from the existing volume.
hole1 = cq.Workplane("XY").cylinder(base_thickness + 2, screw_hole_dia / 2).translate((screw_x - 0.1, 0, base_thickness/2))
hole2 = cq.Workplane("XY").cylinder(base_thickness + 2, screw_hole_dia / 2).translate((-screw_x + 0.1, 0, base_thickness/2))

result = combined.cut(hole1).cut(hole2)