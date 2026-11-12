import cadquery as cq

# Constants based on Design Document and Specification
CLAMP_WIDTH = 20.0  # Y-extent: [-10, 10]
BASE_THICKNESS = 3.0
PIPE_AXIS_Z = 12.5
VOID_RADIUS = 12.6

BAND_INNER = 12.7
BAND_OUTER = 15.5
BAND_X_LIMIT = 7.0

# Wall spans from |x|=7 to |x|=23
WALL_X_START = 7.0
WALL_X_END = 23.0

# Base slab spanning x in [-30, 30] (Total width 60) per updated Design Doc
BASE_WIDTH = 60.0
FLANGE_X = 24.0
HOLE_DIA = 6.6

# 1. Create the Unified Base Slab
# Spans x from -30 to 30, y from -10 to 10, z from 0 to 3
base = (cq.Workplane("XY")
        .box(BASE_WIDTH, CLAMP_WIDTH, BASE_THICKNESS)
        .translate((0, 0, BASE_THICKNESS/2))
       )

# 2. Create the Upper Band (R4)
# The band is defined by material in radial band [12.7, 15.5] for |x| <= 7.
# We use a sweep or intersection approach on the XZ plane.
# Note: To avoid disconnected solids due to coordinate system confusion in previous attempts,
# we define the band explicitly relative to the pipe axis center (0, y, 12.5).
band = (cq.Workplane("XZ")
        .workplane(offset=PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(CLAMP_WIDTH, both=True) # Centers on Y=0, spanning [-10, 10]
       )

# Refine the band to only exist within |x| <= 7 using intersection with a box mask.
band_mask = cq.Workplane("XY").box(BAND_X_LIMIT * 2, CLAMP_WIDTH + 1, 100).translate((0, 0, PIPE_AXIS_Z))
band = band.intersect(band_mask)

# 3. Create Connecting Walls (R1/Design Doc)
# Spanning y in [-10, 10], x from |x|=7 to |x|=23.
wall_width = WALL_X_END - WALL_X_START
# The band is located around Z=12.5. To ensure connectivity:
# Wall must span from the base (z=3) up to the band (approx z=12.5 +/- 15.5).
# We'll make walls go from Z=-20 to Z=40 to guarantee overlap with both base and band.
wall_height = 60.0 

# Wall Right: x in [7, 23], y in [-10, 10], z from -20 to 40
wall_right = (cq.Workplane("XY")
              .box(wall_width, CLAMP_WIDTH, wall_height)
              .translate((WALL_X_START + wall_width/2, 0, 10)) # Center at Z=10 to cover range
             )

# Wall Left: x in [-23, -7], y in [-10, 10], z from -20 to 40
wall_left = (cq.Workplane("XY")
             .box(wall_width, CLAMP_WIDTH, wall_height)
             .translate((-WALL_X_START - wall_width/2, 0, 10)) # Center at Z=10 to cover range
            )

# 4. Combine all parts into one solid using union
# We ensure the band is moved to its correct position if it was created around origin
# In step 2, .workplane(offset=PIPE_AXIS_Z) on XZ plane means the circle center is at Z=12.5.
result = base.union(band).union(wall_right).union(wall_left)

# 5. Subtract the Pipe Void (R3)
# Cylinder radius 12.6 centered at x=0, z=12.5, running along Y axis.
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 4, VOID_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5)
# Vertical holes at (+-24, 0), through the base (z=0 to 3).
result = (result.faces("<Z").workplane()
          .center(FLANGE_X, 0).hole(HOLE_DIA)
          .center(-2 * FLANGE_X, 0).hole(HOLE_DIA))

# Final result is a single solid assigned to 'result'