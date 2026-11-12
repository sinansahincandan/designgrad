import cadquery as cq

# Constants based on Design Document and Specification
CLAMP_WIDTH = 20.0  # Y-extent: [-10, 10]
BASE_THICKNESS = 3.0
PIPE_AXIS_Z = 12.5
VOID_RADIUS = 12.6

BAND_INNER = 12.7
BAND_OUTER = 15.5
BAND_X_LIMIT = 7.0

# Updated per Feedback: Wall spans from |x|=7 to |x|=23
WALL_X_START = 7.0
WALL_X_END = 23.0

# Base slab spanning x in [-27, 27] (Total width 54)
BASE_WIDTH = 54.0
FLANGE_X = 27.0
HOLE_DIA = 6.6

# 1. Create the Unified Base Slab
# Spans x from -27 to 27, y from -10 to 10, z from 0 to 3
base = (cq.Workplane("XY")
        .box(BASE_WIDTH, CLAMP_WIDTH, BASE_THICKNESS)
        .translate((0, 0, BASE_THICKNESS/2))
       )

# 2. Create the Upper Band (R4)
# The band is defined by material in radial band [12.7, 15.5] for |x| <= 7.
# We use a sweep or intersection approach. To ensure connectivity, we'll make sure it overlaps the base.
band = (cq.Workplane("XZ")
        .workplane(offset=PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(CLAMP_WIDTH, both=True) # Centers on Y=0, spanning [-10, 10]
       )

# Refine the band to only exist within |x| <= 7 using intersection with a box.
# We extend the Z range of the mask to ensure it covers the whole height and overlaps base/walls.
band_mask = cq.Workplane("XY").box(BAND_X_LIMIT * 2, CLAMP_WIDTH + 1, 100).translate((0, 0, PIPE_AXIS_Z))
band = band.intersect(band_mask)

# 3. Create Connecting Walls (R1/Design Doc)
# Spanning y in [-10, 10], x from |x|=7 to |x|=23.
# Height must cover from base top (z=3) to the band area (~z=28).
wall_width = WALL_X_END - WALL_X_START
wall_height = 30.0 # Sufficiently high to bridge base and band

# Wall Right: x in [7, 23], y in [-10, 10], z from 0 to 30
# To ensure it touches the base (z=0..3), we start at z=0 or lower.
wall_right = (cq.Workplane("XY")
              .box(wall_width, CLAMP_WIDTH, wall_height)
              .translate((WALL_X_START + wall_width/2, 0, wall_height/2))
             )

# Wall Left: x in [-23, -7], y in [-10, 10], z from 0 to 30
wall_left = (cq.Workplane("XY")
             .box(wall_width, CLAMP_WIDTH, wall_height)
             .translate((-WALL_X_START - wall_width/2, 0, wall_height/2))
            )

# 4. Combine all parts into one solid using union
# The previous error showed the band was at a negative Z offset. 
# Let's ensure the band is correctly positioned relative to the pipe axis.
# The 'band' creation used .workplane(offset=PIPE_AXIS_Z) on XZ plane, which means it centers around z=12.5.
# However, extrude(both=True) in CadQuery on a workplane centered at Z=12.5 might be behaving unexpectedly 
# if the extrusion direction is not clearly defined relative to global Z.
# Let's re-verify: XZ plane normal is Y. Extruding 'both' goes along +Y and -Y.
# The band should be a ring in XZ, extruded along Y.

# Re-calculating Band to ensure it's at the right Z height
band = (cq.Workplane("XZ")
        .workplane(offset=PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(CLAMP_WIDTH, both=True)
       )
# The band is centered at Z = 12.5. Its thickness in Z is (15.5 - 12.7) = 2.8.
# So it spans Z from 12.5 - 1.4 to 12.5 + 1.4 -> [11.1, 13.9].

# Refine the band to only exist within |x| <= 7 using intersection with a box.
band_mask = cq.Workplane("XY").box(BAND_X_LIMIT * 2, CLAMP_WIDTH + 1, 40).translate((0, 0, PIPE_AXIS_Z))
band = band.intersect(band_mask)

# Combine all parts into one solid using union
result = base.union(band).union(wall_right).union(wall_left)

# 5. Subtract the Pipe Void (R3)
# Cylinder radius 12.6 centered at x=0, z=12.5, running along Y axis.
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 4, VOID_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5)
# Vertical holes at (+-27, 0), through the base (z=0 to 3).
result = (result.faces("<Z").workplane()
          .center(FLANGE_X, 0).hole(HOLE_DIA)
          .center(-2 * FLANGE_X, 0).hole(HOLE_DIA))

# Final result is a single solid assigned to 'result'