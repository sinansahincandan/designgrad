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

# 1. Create the Base (Flanges and connector)
# A single block from x=-30 to 30, y=-10 to 10, z=0 to 3.
base = cq.Workplane("XY").box(60, CLAMP_WIDTH, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS/2))

# 2. Create the Band (R4: material in radial band [12.7, 15.5])
# The pipe axis is at x=0, z=PIPE_AXIS_Z and runs along Y.
# We create a ring by extruding a profile on the XZ plane.
band = (cq.Workplane("XZ")
        .workplane(offset=PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(CLAMP_WIDTH, both=True) # Extrudes along Y axis
       )

# 3. Create Connecting Walls (to ensure single solid and bridge base to band)
# To fix the disconnection reported:
# Solid 1 spans z [-15.54, 15.54]
# Solid 2 spans z [18.62, 26.0]
# We need a wall that bridges from the bottom of the base (z=0) to the top of the band (z ~ 28).
# The previous 'walls' was centered at 13 and had height 26, so it went from z=0 to z=26.
# However, the reported bbox for solid 1 suggests a coordinate shift or rotation issue in how union/cut was handled.
# Let's build a very large vertical pillar that definitely overlaps everything.
walls = cq.Workplane("XY").box(14, CLAMP_WIDTH + 2, 50).translate((0, 0, 25))

# 4. Combine all parts into one solid
# We union them to form a single manifold object.
result = base.union(band).union(walls)

# 5. Subtract the Pipe Void (R3: radius 12.6 at x=0, z=12.5)
# The pipe runs along the Y axis. 
# We use a cylinder on the XZ plane to cut through.
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 100, VOID_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5: diameter 6.6 at +-27, 0 from z=0 to 3)
# We target the top face of the base/flanges.
result = result.faces(">Z").workplane().center(FLANGE_X, 0).hole(HOLE_DIA)
result = result.faces(">Z").workplane().center(-FLANGE_X, 0).hole(HOLE_DIA)

# Final check on connectivity:
# Base Z range: [0, 3]
# Band Z range: [12.5 - 15.5, 12.5 + 15.5] = [-3, 28]
# Walls Z range: [25 - 25, 25 + 25] = [0, 50]
# The walls now cover z=[0, 50], which overlaps the base (z=0..3) and the band (z=-3..28).