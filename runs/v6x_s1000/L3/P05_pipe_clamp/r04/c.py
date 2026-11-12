import cadquery as cq

# Constants based on Design Document and Feedback
Y_EXTENT = 20.0
PIPE_RADIUS = 12.6
BAND_INNER = 12.7
BAND_OUTER = 15.5
PIPE_AXIS_Z = 12.5

BASE_X_HALF = 27.0
BASE_THICKNESS = 3.0
HOLE_DIA = 6.6
FLANGE_X_POS = 27.0

# 1. Create the Base Plate (R2, R6)
# Spans x in [-27, 27], y in [-10, 10], z in [0, 3]
# Using Y_EXTENT as total width to satisfy R2
base = cq.Workplane("XY").box(BASE_X_HALF * 2, Y_EXTENT, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS / 2))

# 2. Create the Flanges (R6)
# Explicitly define flange blocks to ensure R6 compliance: |x| in [18.5, 23], |y| <= 4, z in [0, 3]
# Note: The base plate already covers this area, but we add them explicitly as per Design Doc
flange_width = 23.0 - 18.5
flange_x_center = (23.0 + 18.5) / 2
flanges = (cq.Workplane("XY")
           .box(flange_width, 8.0, BASE_THICKNESS) # y in [-4, 4]
           .translate((flange_x_center, 0, BASE_THICKNESS / 2))
           .union(cq.Workplane("XY")
                  .box(flange_width, 8.0, BASE_THICKNESS)
                  .translate((-flange_x_center, 0, BASE_THICKNESS / 2))))

# 3. Create the Upper Band (R4)
# Radial band [12.7, 15.5] centered at x=0, z=12.5, extending along Y axis
band = (cq.Workplane("XZ")
        .center(0, PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(Y_EXTENT, both=True))

# 4. Create Connecting Walls (R1)
# Bridges the gap between base (z=3) and band center (z=12.5)
# Ensuring connectivity for a single solid
walls = cq.Workplane("XY").box(14, Y_EXTENT, 15).translate((0, 0, (3 + 12.7) / 2))

# 5. Combine components into a single solid (R1)
result = base.union(flanges).union(band).union(walls)

# 6. Subtract the Pipe Void (R3)
# Axis is x=0, z=12.5, running along Y axis.
pipe_void = (cq.Workplane("XZ")
             .center(0, PIPE_AXIS_Z)
             .circle(PIPE_RADIUS)
             .extrude(Y_EXTENT, both=True))

result = result.cut(pipe_void)

# 7. Subtract Screw Holes (R5)
# Centered at (+-27, 0), vertical through the base (z=0 to 3).
# Using pushPoints for correct absolute placement relative to workplane origin.
result = (result.faces("<Z")
          .workplane()
          .pushPoints([(FLANGE_X_POS, 0), (-FLANGE_X_POS, 0)])
          .hole(HOLE_DIA))