import cadquery as cq
import math

# Constants
PIPE_RADIUS = 12.5
VOID_RADIUS = 12.6
BAND_INNER = 12.7
BAND_OUTER = 15.5
CLAMP_WIDTH = 20.0
FLANGE_X = 27.0
HOLE_DIA = 6.6
BASE_THICKNESS = 3.0
PIPE_AXIS_Z = 12.5

# The error reports a persistent gap between Z=15.55 and Z=18.62.
# This suggests that the 'band' or 'walls' are being treated as separate solids 
# because they don't overlap with the 'base' in a way the union operation recognizes,
# OR there is a coordinate system mismatch.

# Let's rebuild everything from scratch using a single Workplane flow to avoid disconnected solids.

# 1. Create the Base (Flanges and connector)
base = cq.Workplane("XY").box(60, CLAMP_WIDTH, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS/2))

# 2. Create the Band (R4: material in radial band [12.7, 15.5])
# We create a ring on XZ and extrude it along Y.
band = (cq.Workplane("XZ")
        .workplane(offset=PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(CLAMP_WIDTH, both=True)
       )

# 3. Create Connecting Walls (to ensure single solid and bridge base to band)
# The gap is at Z=[15.55, 18.62]. 
# We will create a pillar that spans from the very bottom of the base (z=0) 
# all the way to the top of the band (z=30).
# To ensure it overlaps, we'll make it go from z=-5 to z=40.
walls = cq.Workplane("XY").box(14, CLAMP_WIDTH + 2, 45).translate((0, 0, 17.5))

# 4. Combine all parts into one solid using a single union chain.
# To force connectivity in CadQuery when solids are reported as disconnected, 
# we ensure the connecting piece (walls) is large enough to intersect both.
result = base.union(band).union(walls)

# 5. Subtract the Pipe Void (R3: radius 12.6 at x=0, z=12.5)
# The pipe runs along the Y axis.
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 100, VOID_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5: diameter 6.6 at +-27, 0 from z=0 to 3)
# We use the base's top face for hole placement.
result = result.faces(">Z").workplane().center(FLANGE_X, 0).hole(HOLE_DIA)
result = result.faces(">Z").workplane().center(-FLANGE_X, 0).hole(HOLE_DIA)

# Final check: The 'walls' box is [ -7, 7 ] in X, [ -11, 11 ] in Y, and [ 17.5-22.5, 17.5+22.5 ] = [-5, 40] in Z.
# The 'base' box is [ -30, 30 ] in X, [ -10, 10 ] in Y, and [ 0, 3 ] in Z.
# Since walls (z=-5 to 40) overlaps base (z=0 to 3), they MUST union.
# The 'band' box is centered at z=12.5 with radius 15.5 -> z=[-3, 28].
# Since walls (z=-5 to 40) overlaps band (z=-3 to 28), they MUST union.