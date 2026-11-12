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
base = cq.Workplane("XY").box(base_x_ext, base_y_width, base_thickness)
# Move so it sits on z=0 (box is centered at origin by default, so translate by thickness/2)
base = base.translate((0, 0, base_thickness / 2))

# 2. Create the Saddle Arch (R1, R3, R4, R7)
# To ensure a single solid and satisfy R4, we create a block that covers the saddle area
# and then subtract the pipe cavity. We'll use a cylinder for the arch material itself
# to keep mass low (R7). 
# The arch needs to be connected to the base. We'll add a vertical support/connector 
# that is part of the arch geometry.

# Create the saddle shell: Material between r=12.6 and r=15.5
# We create a cylinder for the outer radius and subtract the inner one.
# To ensure it connects to the base (z=3), we extrude it from z=3 upwards.
arch_outer = cq.Workplane("XY").workplane(offset=pipe_axis_z).circle(saddle_outer_radius).extrude(20, both=True)
arch_inner = cq.Workplane("XY").workplane(offset=pipe_axis_z).circle(clearance_radius).extrude(25, both=True)
arch_shell = arch_outer.cut(arch_inner)

# To ensure R1 (Single Solid), we need a connector between the base (z=3) and the arch shell.
# We'll use a central block that is part of the subtraction logic or an additive one.
# Let's add a vertical pillar at the center to bridge base and arch.
connector = cq.Workplane("XY").box(base_y_width, base_y_width, pipe_axis_z - base_thickness/2).translate((0, 0, (pipe_axis_z - base_thickness/2)/2))
# Wait, simpler: Create a solid block that encompasses the arch and subtract the pipe.
# Let's build a cylinder of radius 15.5 from z=3 to z=30, then subtract the inner radius.
arch_solid = cq.Workplane("XY").workplane(offset=3).circle(saddle_outer_radius).extrude(27)
# Subtract the pipe cavity (R3)
pipe_cavity = cq.Workplane("XY").workplane(offset=pipe_axis_z).circle(clearance_radius).extrude(30, both=True)
arch_final = arch_solid.cut(pipe_cavity)

# To ensure R1 and connection: The arch_solid starts at z=3, which is exactly the top of the base.
# We also need to make sure the arch covers the Y-width or provides enough contact.
# Let's refine the arch to be a cylinder centered at (0,0) extending from z=3 upwards.

# 3. Combine Base and Arch (R1)
combined = base.union(arch_final)

# 4. Subtract Screw Holes (R5)
# Holes are vertical, diameter 6.6, centered at (+-27, 0), through the base.
# Since our base is x in [-27, 27], a hole at 27 is on the edge. 
# To ensure it's "through the flanges", we make sure the base covers the hole area.
hole_left = cq.Workplane("XY").workplane(offset=0).center(-screw_x, 0).circle(screw_hole_dia/2).extrude(base_thickness + 1)
hole_right = cq.Workplane("XY").workplane(offset=0).center(screw_x, 0).circle(screw_hole_dia/2).extrude(base_thickness + 1)

result = combined.cut(hole_left).cut(hole_right)