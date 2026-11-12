import cadquery as cq
import math

# Parameters
pipe_radius = 12.5
clearance_radius = 12.6
saddle_outer_radius = 15.5
clamp_width = 20.0
screw_hole_dia = 6.6
screw_x = 27.0
flange_thickness = 3.0
base_thickness = 4.0

# Constructive approach to ensure one single solid (R1)

# A: The base plate (z=0 to 4)
# R2: Width is 20mm, X extent is 54mm (|x|=27), sits on z=0.
base = cq.Workplane("XY").box(54, clamp_width, base_thickness).translate((0, 0, base_thickness/2))

# B: The flanges (R6) - centered at screw locations to ensure they are solid and connected
# Flanges must be at |x| near 27. We'll make them wide enough to overlap the base.
flange = cq.Workplane("XY").box(10, clamp_width, 25).translate((screw_x, 0, 12.5))
flange_left = flange.translate((-2 * screw_x, 0, 0))
flange_right = flange

# C: The Saddle Arch (R4) - material between r=12.6 and r=15.5
# We create a cylinder for the outer radius and subtract one for the inner radius.
# To ensure it's connected to the base, we use a connector or make sure they overlap.
# The arch is centered at (0, 0, 12.5). Its Z range is [12.5 - 15.5, 12.5 + 15.5] = [-3, 28].
# Since the base ends at z=4, they should overlap significantly.
arch_outer = cq.Workplane("XY").workplane(offset=12.5).circle(saddle_outer_radius).extrude(30, both=True)
arch_inner = cq.Workplane("XY").workplane(offset=12.5).circle(clearance_radius).extrude(30, both=True)
arch_band = arch_outer.cut(arch_inner)

# D: Connector to bridge the gap between base (z=4) and arch (centered at z=12.5)
# We'll make a larger connector block that ensures overlap with everything.
connector = cq.Workplane("XY").box(30, clamp_width, 15).translate((0, 0, 7.5))

# Combine all main parts
# To ensure union works perfectly in CadQuery, we use the base as the starting point
combined_body = base.union(flange_left).union(flange_right).union(arch_band).union(connector)

# E: Subtract screw holes (R5)
# Holes are at (+-27, 0) through the flanges.
# We use a large extrusion to ensure it cuts completely through.
hole_left = cq.Workplane("XY").workplane(offset=0).center(screw_x, 0).circle(screw_hole_dia/2).extrude(50)
hole_right = cq.Workplane("XY").workplane(offset=0).center(-screw_x, 0).circle(screw_hole_dia/2).extrude(50)

result = combined_body.cut(hole_left).cut(hole_right)