import cadquery as cq

# Parameters
clamp_width = 20.0
screw_hole_dia = 6.6
screw_x = 27.0
base_thickness = 3.0
base_x_extent = 59.0  # From |x|=29.5 to -29.5

saddle_inner_radius = 12.6
saddle_outer_radius = 16.0
pipe_axis_z = 12.5

# R1: Constructive approach to ensure one single solid

# A: The base plate (z=0 to 3)
# Connects the flanges and provides the foundation.
base = cq.Workplane("XY").box(base_x_extent, clamp_width, base_thickness).translate((0, 0, base_thickness/2))

# B: The flanges (R6) - centered at screw locations (+-27, 0)
# Flanges are 5mm wide in X (|x| from 24.5 to 29.5), 3mm thick (z=0 to 3).
flange = cq.Workplane("XY").box(5, clamp_width, base_thickness).translate((screw_x, 0, base_thickness/2))
flange_left = flange.translate((-2 * screw_x, 0, 0))
flange_right = flange

# C: The Saddle Arch (R4)
# Material between r=12.6 and r=16.0 centered at (0, 0, 12.5).
# We extrude a ring to ensure it is a solid part of the geometry.
arch_outer = cq.Workplane("XY").workplane(offset=pipe_axis_z).circle(saddle_outer_radius).extrude(30, both=True)
arch_inner = cq.Workplane("XY").workplane(offset=pipe_axis_z).circle(saddle_inner_radius).extrude(30, both=True)
arch_band = arch_outer.cut(arch_inner)

# D: Connector to bridge the gap between base (z=3) and arch (centered at z=12.5)
# This ensures R1 (single solid) by creating a continuous volume from the base to the arch.
connector = cq.Workplane("XY").box(20, clamp_width, 15).translate((0, 0, 7.5))

# Combine all main parts using union
combined_body = base.union(flange_left).union(flange_right).union(arch_band).union(connector)

# E: Subtract screw holes (R5)
# Holes are at (+-27, 0), diameter 6.6mm, vertical.
hole_left = cq.Workplane("XY").workplane(offset=0).center(screw_x, 0).circle(screw_hole_dia/2).extrude(50)
hole_right = cq.Workplane("XY").workplane(offset=0).center(-screw_x, 0).circle(screw_hole_dia/2).extrude(50)

# Final result: subtract holes from the combined solid
result = combined_body.cut(hole_left).cut(hole_right)