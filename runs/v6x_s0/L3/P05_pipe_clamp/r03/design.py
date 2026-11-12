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
# We translate by thickness/2 so the bottom face is at z=0
base = cq.Workplane("XY").box(base_x_ext, base_y_width, base_thickness).translate((0, 0, base_thickness / 2))

# 2. Create the Saddle Block (R1, R4)
# To ensure a single solid and satisfy R4, we create a cylinder that covers the saddle area.
# The saddle block must be large enough to connect with the base and provide material for the band.
# We'll use a cylinder centered at (0, 0, pipe_axis_z).
# To ensure it connects to the base (z=3), we make it tall enough.
arch_solid = cq.Workplane("XY").workplane(offset=pipe_axis_z).circle(saddle_outer_radius).extrude(30, both=True)

# 3. Combine Base and Arch (R1)
# This creates the single continuous solid before subtractions.
combined = base.union(arch_solid)

# 4. Subtract Pipe Cavity (R3)
# The pipe cavity must be a cylinder centered at (0, 0, 12.5) spanning the entire Z height.
pipe_cavity = cq.Workplane("XY").workplane(offset=pipe_axis_z).circle(clearance_radius).extrude(50, both=True)
combined_with_cavity = combined.cut(pipe_cavity)

# 5. Subtract Screw Holes (R5)
# We use the .faces().workplane() method to drill vertical holes through the base.
# The holes are centered at (+-27, 0).
result = (
    combined_with_cavity.faces(">Z").workplane()
    .center(screw_x, 0)
    .hole(screw_hole_dia)
    .center(-2 * screw_x, 0)
    .hole(screw_hole_dia)
)

# Final check: result is a single solid (R1).