import cadquery as cq

# Constants based on Design Document and Feedback
PIPE_RADIUS = 12.6
BAND_INNER = 12.7
BAND_OUTER = 15.5
PIPE_AXIS_Z = 12.5
CLAMP_WIDTH = 20.0  # Y extent (from -10 to 10)
BASE_X_HALF = 27.0
BASE_THICKNESS = 3.0
HOLE_DIA = 6.6
FLANGE_X = 27.0

# 1. Create the Base Plate (R2, R6)
# Spans x in [-27, 27], y in [-10, 10], z in [0, 3]
base = cq.Workplane("XY").box(BASE_X_HALF * 2, CLAMP_WIDTH, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS / 2))

# 2. Create the Upper Band (R4)
# Radial band [12.7, 15.5] centered at x=0, z=12.5, extending along Y axis
# We use XZ plane to draw the ring profile and extrude it along Y
band = (cq.Workplane("XZ")
        .workplane(offset=PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(CLAMP_WIDTH, both=True))

# 3. Create Connecting Walls (R1)
# Bridges the gap between base (z=3) and band (bottom of band is at z = 12.5 - 15.5 = -3, top is 12.5 + 15.5 = 28)
# To ensure connectivity, we create a block that overlaps both the base and the band.
# The feedback suggests x in [-7, 7], y in [-10, 10], z from 3 to 12.7 (approx).
walls = cq.Workplane("XY").box(14, CLAMP_WIDTH, 15).translate((0, 0, (3 + 12.7) / 2))

# 4. Combine components into a single solid (R1)
result = base.union(band).union(walls)

# 5. Subtract the Pipe Void (R3)
# Axis is x=0, z=12.5, running along Y axis.
# We create a cylinder on XZ plane and rotate it to align with Y, or use XY and rotate.
# Using XZ plane: a cylinder on XZ naturally has its axis along Z. 
# To get an axis along Y, we can use the YZ plane.
pipe_void = (cq.Workplane("YZ")
             .center(0, PIPE_AXIS_Z)
             .cylinder(CLAMP_WIDTH + 20, PIPE_RADIUS))

result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5)
# Centered at (+-27, 0), vertical through the base (z=0 to 3).
# We select the bottom face or top face of the base to ensure we hit the flange area.
result = result.faces("<Z").workplane().center(FLANGE_X, 0).hole(HOLE_DIA)
result = result.faces("<Z").workplane().center(-FLANGE_X, 0).hole(HOLE_DIA)