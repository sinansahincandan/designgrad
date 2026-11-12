import cadquery as cq

# Constants based on specification
PIPE_RADIUS = 12.6
BAND_INNER = 12.7
BAND_OUTER = 15.5
CLAMP_WIDTH = 20.0  # Y-extent: [-10, 10]
FLANGE_X = 27.0
HOLE_DIA = 6.6
BASE_THICKNESS = 3.0
PIPE_AXIS_Z = 12.5

# 1. Create the Base (R2, R6)
# Spans x from -27 to 27, y from -10 to 10, z from 0 to 3.
base = cq.Workplane("XY").box(54, CLAMP_WIDTH, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS/2))

# 2. Create the Band (R4)
# The band covers |x| <= 7 and spans y in [-10, 10].
# We create a full ring centered at (0, 0, 12.5).
full_ring = (
    cq.Workplane("XY")
    .workplane(offset=PIPE_AXIS_Z)
    .circle(BAND_OUTER)
    .circle(BAND_INNER)
    .extrude(CLAMP_WIDTH, both=True)
)

# To ensure it is an "upper" band (z > 12.5), we intersect with a box that covers the top half.
# We use a slightly larger Y to ensure overlap during intersection.
band_limiter = cq.Workplane("XY").box(14, CLAMP_WIDTH + 2, 30).translate((0, 0, PIPE_AXIS_Z + 15))
band = full_ring.intersect(band_limiter)

# 3. Create Connecting Walls (R1)
# The previous error showed a gap between z=6 and z=18.
# We must ensure the walls bridge the entire gap from the base (z=3) to the band (z~25).
# A single block from z=0 to z=30 will definitely overlap both.
walls = cq.Workplane("XY").box(14, CLAMP_WIDTH + 2, 30).translate((0, 0, 15))

# 4. Combine into one solid (R1)
# Union everything to create a single manifold.
result = base.union(band).union(walls)

# 5. Subtract the Pipe Void (R3)
# Cylinder along Y axis at x=0, z=12.5 with radius 12.6.
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 10, PIPE_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5)
# Vertical holes through the base at (+-27, 0).
result = result.faces("<Z").workplane().center(FLANGE_X, 0).hole(HOLE_DIA)
result = result.faces("<Z").workplane().center(-FLANGE_X, 0).hole(HOLE_DIA)