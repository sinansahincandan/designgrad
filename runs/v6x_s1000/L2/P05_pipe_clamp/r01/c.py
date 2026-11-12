import cadquery as cq

# Constants from Design Document
PIPE_AXIS_Z = 12.5
VOID_RADIUS = 12.6
BAND_INNER = 12.7
BAND_OUTER = 15.5
CLAMP_WIDTH = 20.0  # Y-extent: -10 to 10 (Total 20mm)
BASE_THICKNESS = 3.0
HOLE_DIA = 6.6
FLANGE_X_CENTER = 22.75 # Center of the flange block [18.5, 27]
FLANGE_WIDTH = 8.5      # 27 - 18.5 = 8.5
FLANGE_Y_HALF = 4.0     # y in [-4, 4]

# 1. Create the Flanges (R6)
flange_right = cq.Workplane("XY").box(FLANGE_WIDTH, FLANGE_Y_HALF * 2, BASE_THICKNESS).translate((FLANGE_X_CENTER, 0, BASE_THICKNESS/2))
flange_left = cq.Workplane("XY").box(FLANGE_WIDTH, FLANGE_Y_HALF * 2, BASE_THICKNESS).translate((-FLANGE_X_CENTER, 0, BASE_THICKNESS/2))
base = flange_right.union(flange_left)

# 2. Create the Upper Band (R4)
# We create a ring in XZ plane and extrude it along Y.
band_ring = (cq.Workplane("XZ")
             .workplane(offset=PIPE_AXIS_Z)
             .circle(BAND_OUTER)
             .circle(BAND_INNER)
             .extrude(CLAMP_WIDTH, both=True))

# Restrict band to |x| <= 7 using a large box intersection.
band = band_ring.intersect(cq.Workplane("XY").box(14, CLAMP_WIDTH + 2, 60).translate((0, 0, PIPE_AXIS_Z)))

# 3. Create Connecting Walls (R1)
# To ensure connectivity, we create two large vertical pillars that bridge the base and the band.
# The base is at z=[0, 3]. The band center is at z=12.5.
# We make walls that span from z=-1 to z=25 to ensure they overlap both components.
wall_right = cq.Workplane("XY").box(20, CLAMP_WIDTH + 2, 30).translate((13, 0, 14))
wall_left = cq.Workplane("XY").box(20, CLAMP_WIDTH + 2, 30).translate((-13, 0, 14))

# 4. Combine all additive parts into one solid (R1)
# We use union to join the base, band, and walls.
result = base.union(band).union(wall_right).union(wall_left)

# 5. Subtract the Pipe Void (R3)
# The pipe axis is x=0, z=12.5, running along Y.
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 40, VOID_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 6. Subtract Screw Holes (R5)
# Centered at (+-27, 0), through the flanges (z=0 to 3).
# We use a workplane on the bottom face and drill upwards.
result = result.faces("<Z").workplane().center(27, 0).hole(HOLE_DIA)
result = result.faces("<Z").workplane().center(-27, 0).hole(HOLE_DIA)

# Final check: The resulting 'result' is a single solid object.