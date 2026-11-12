import cadquery as cq

# Constants based on Design Document and Feedback
Y_EXTENT = 20.0
PIPE_RADIUS = 12.65
BAND_INNER = 12.7
BAND_OUTER = 15.5
PIPE_AXIS_Z = 12.5

BASE_X_HALF = 27.0
BASE_THICKNESS = 3.0
HOLE_DIA = 6.6
FLANGE_X = 27.0

# 1. Create the Base Plate (R2, R6)
# Spans x in [-27, 27], y in [-10, 10], z in [0, 3]
# This also covers the flange requirement (R6) as it is a continuous slab.
base = cq.Workplane("XY").box(BASE_X_HALF * 2, Y_EXTENT, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS / 2))

# 2. Create the Upper Band (R4)
# Radial band [12.7, 15.5] centered at x=0, z=12.5, extending along Y axis
# We use XZ plane to draw the ring profile and extrude it along Y
band = (cq.Workplane("XZ")
        .center(0, PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(Y_EXTENT, both=True))

# 3. Create Connecting Walls (R1)
# Bridges the gap between base (z=3) and band (bottom of band is at z = 12.5 - 15.5 = -3, top is 12.5 + 15.5 = 28)
# To ensure connectivity, we create a block that overlaps both the base and the band.
# The feedback suggests x in [-7, 7], y in [-10, 10], z from 3 to 12.7 (approx).
walls = cq.Workplane("XY").box(14, Y_EXTENT, 15).translate((0, 0, (3 + 12.7) / 2))

# 4. Combine components into a single solid (R1)
result = base.union(band).union(walls)

# 5. Subtract the Pipe Void (R3)
# Axis is x=0, z=12.5, running along Y axis.
# Using XZ plane to define the circle and extrude it along Y as per feedback.
pipe_void = (cq.Workplane("XZ")
             .center(0, PIPE_AXIS_Z)
             .circle(PIPE_RADIUS)
             .extrude(Y_EXTENT, both=True))

result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5)
# Centered at (+-27, 0), vertical through the base (z=0 to 3).
# Using a robust subtraction by selecting the bottom face and creating holes.
result = (result.faces("<Z")
          .workplane()
          .center(FLANGE_X, 0)
          .hole(HOLE_DIA)
          .center(-2 * FLANGE_X, 0)
          .hole(HOLE_DIA))