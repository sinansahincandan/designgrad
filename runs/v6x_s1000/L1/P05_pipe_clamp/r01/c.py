import cadquery as cq

# Constants based on Design Document and Specification
CLAMP_WIDTH = 20.0  # Y-extent: [-10, 10]
BASE_THICKNESS = 3.0
PIPE_AXIS_Z = 12.5
VOID_RADIUS = 12.6

BAND_INNER = 12.7
BAND_OUTER = 15.5
BAND_X_LIMIT = 7.0

WALL_X_START = 7.0
WALL_X_END = 18.5

FLANGE_X = 27.0
HOLE_DIA = 6.6

# 1. Create the Base (Flanges and connector)
# Covers x from -30 to 30, y from -10 to 10, z from 0 to 3
base = cq.Workplane("XY").box(60, CLAMP_WIDTH, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS/2))

# 2. Create the Upper Band (R4)
# The band is defined by material in radial band [12.7, 15.5] for |x| <= 7.
# We create a ring on XZ plane and extrude it along Y with the exact CLAMP_WIDTH.
# To ensure no disconnected solids at negative Z, we use absolute positioning for extrusion.
band = (cq.Workplane("XZ")
        .workplane(offset=PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(CLAMP_WIDTH, both=True) # Centers on Y=0, spanning [-10, 10]
       )

# Refine the band to only exist within |x| <= 7 using intersection with a box.
# We use a large Z-extent for the mask to ensure it covers the whole band.
band_mask = cq.Workplane("XY").box(BAND_X_LIMIT * 2, CLAMP_WIDTH + 1, 100).translate((0, 0, PIPE_AXIS_Z))
band = band.intersect(band_mask)

# 3. Create Connecting Walls (R1/Design Doc)
# Spanning y in [-10, 10], x in [7, 18.5], and z from base top (3) to band top (~28).
wall_width = WALL_X_END - WALL_X_START

# Wall Right: x in [7, 18.5], y in [-10, 10], z from 0 to 30
wall_right = (cq.Workplane("XY")
              .box(wall_width, CLAMP_WIDTH, 30)
              .translate((WALL_X_START + wall_width/2, 0, 15))
             )

# Wall Left: x in [-18.5, -7], y in [-10, 10], z from 0 to 30
wall_left = (cq.Workplane("XY")
             .box(wall_width, CLAMP_WIDTH, 30)
             .translate((-WALL_X_START - wall_width/2, 0, 15))
            )

# 4. Combine all parts into one solid using union
# We perform unions sequentially to ensure a single manifold object.
result = base.union(band).union(wall_right).union(wall_left)

# 5. Subtract the Pipe Void (R3)
# Cylinder radius 12.6 centered at x=0, z=12.5, running along Y axis.
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 4, VOID_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5)
# Vertical holes at (+-27, 0), through the base (z=0 to 3).
# We use a workplane on the bottom face (<Z) and create holes.
result = (result.faces("<Z").workplane()
          .center(FLANGE_X, 0).hole(HOLE_DIA)
          .center(-2 * FLANGE_X, 0).hole(HOLE_DIA))

# Final result is a single solid assigned to 'result'