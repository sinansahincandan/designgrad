import cadquery as cq

# Constants based on specification and feedback
PIPE_RADIUS = 12.6
BAND_INNER = 12.7
BAND_OUTER = 15.5
CLAMP_WIDTH = 20.0  # Y-extent: [-10, 10]
FLANGE_X = 27.0
HOLE_DIA = 6.6
BASE_THICKNESS = 3.0
PIPE_AXIS_Z = 12.5

# 1. Create the Base (R2, R6)
# Spans x from -30 to 30, y from -10 to 10, z from 0 to 3.
base = cq.Workplane("XY").box(60, CLAMP_WIDTH, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS/2))

# 2. Create the Band (R4)
# We create a ring and intersect it with a box to limit |x| <= 7 and Y extent.
ring = (
    cq.Workplane("XY")
    .workplane(offset=PIPE_AXIS_Z)
    .circle(BAND_OUTER)
    .circle(BAND_INNER)
    .extrude(CLAMP_WIDTH, both=True)
)

# Limiter box to restrict the ring to |x| <= 7 and y in [-10, 10]
band_limiter = cq.Workplane("XY").box(14, CLAMP_WIDTH + 2, 50).translate((0, 0, PIPE_AXIS_Z))

# Intersection produces the band segment.
band = ring.intersect(band_limiter)

# 3. Create Connecting Walls (R1)
# To ensure a single solid, walls must overlap both base and band.
# Base top is at z=3. Band bottom is at PIPE_AXIS_Z - BAND_OUTER = 12.5 - 15.5 = -3.0? No.
# The ring center is at Z=12.5. Inner radius 12.7 means the band exists from z = (12.5-15.5) to (12.5+15.5).
# Wait, if BAND_INNER is 12.7 and PIPE_AXIS_Z is 12.5, the ring bottom is at 12.5 - 15.5 = -3.0.
# Let's make walls that span from z=0 to z=12.5 to ensure overlap with everything.
walls = cq.Workplane("XY").box(14, CLAMP_WIDTH + 2, 15).translate((0, 0, 7.5))

# 4. Combine into one solid (R1)
# We use the solids directly to avoid Workplane stack issues and ensure a single unioned object.
s_base = base.val()
s_walls = walls.val()
s_band = band.val()

# Union all components into one workplane
result = cq.Workplane("XY").add(s_base).union(s_walls).union(s_band)

# 5. Subtract the Pipe Void (R3)
# Cylinder along Y axis at x=0, z=12.5 with radius 12.6.
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 10, PIPE_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5)
# Two holes of diameter 6.6 at (+-27, 0) from z=0 to z=3.
screw_hole_1 = cq.Workplane("XY").cylinder(BASE_THICKNESS + 2, HOLE_DIA/2).translate((FLANGE_X, 0, 0))
screw_hole_2 = cq.Workplane("XY").cylinder(BASE_THICKNESS + 2, HOLE_DIA/2).translate((-FLANGE_X, 0, 0))
result = result.cut(screw_hole_1).cut(screw_hole_2)

# Final safety check for single solid connectivity
solids = result.solids()
if len(solids) > 1:
    combined = solids[0]
    for i in range(1, len(solids)):
        combined = combined.union(solids[i])
    result = cq.Workplane("XY").add(combined)