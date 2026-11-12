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
FLANGE_X_POS = 27.0 # Center of screw holes as per R5

# 1. Create the Base Plate (R2)
# Spans x in [-27, 27], y in [-10, 10], z in [0, 3]
base = cq.Workplane("XY").box(BASE_X_HALF * 2, Y_EXTENT, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS / 2))

# 2. Create Flanges (R6)
# Explicitly covering x in [18.5, 23] and [-23, -18.5], y in [-4, 4], z in [0, 3]
flange_l = cq.Workplane("XY").box(4.5, 8, 3).translate((-20.75, 0, 1.5))
flange_r = cq.Workplane("XY").box(4.5, 8, 3).translate((20.75, 0, 1.5))

# 3. Create the Upper Band (R4)
# Radial band [12.7, 15.5] centered at x=0, z=12.5, extending along Y axis
band = (cq.Workplane("XZ")
        .center(0, PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(Y_EXTENT, both=True))

# 4. Create Connecting Walls (R1)
# Bridges the gap between base (z=3) and band. 
walls = cq.Workplane("XY").box(14, Y_EXTENT, 16).translate((0, 0, (3 + 12.5) / 2))

# 5. Combine components into a single solid (R1)
result = base.union(flange_l).union(flange_r).union(band).union(walls)

# 6. Subtract the Pipe Void (R3)
pipe_void = (cq.Workplane("XZ")
             .center(0, PIPE_AXIS_Z)
             .circle(PIPE_RADIUS)
             .extrude(Y_EXTENT + 2, both=True)) # Extend slightly to ensure clean cut

result = result.cut(pipe_void)

# 7. Subtract Screw Holes (R5)
# Instead of selecting faces which might fail if the geometry is complex, 
# we use absolute coordinates on the XY plane and extrude downwards.
hole_l = cq.Workplane("XY").circle(HOLE_DIA / 2).translate((FLANGE_X_POS, 0, 0)).extrude(-BASE_THICKNESS - 1)
hole_r = cq.Workplane("XY").circle(HOLE_DIA / 2).translate((-FLANGE_X_POS, 0, 0)).extrude(-BASE_THICKNESS - 1)

result = result.cut(hole_l).cut(hole_r)