import cadquery as cq

# Constants based on Design Document and Specification
CLAMP_WIDTH = 20.0  # Y-extent: [-10, 10]
BASE_THICKNESS = 3.0
PIPE_AXIS_Z = 12.5
VOID_RADIUS = 12.6

BAND_INNER = 12.7
BAND_OUTER = 15.5
BAND_X_LIMIT = 7.0

# Flange dimensions (R6: covers |x| in [18.5, 23] and |y| <= 4)
FLANGE_X = 27.0
FLANGE_WIDTH = 17.0  # Spans from 27 - 8.5 to 27 + 8.5 (18.5 to 35.5)
FLANGE_Y_HALF = 4.0  # |y| <= 4

# Connecting Walls (bridge between flange and band)
WALL_X_START = 7.0
WALL_X_END = 18.5
HOLE_DIA = 6.6

# 1. Create Flange Blocks (R6/R5)
flange_right = cq.Workplane("XY").box(FLANGE_WIDTH, FLANGE_Y_HALF * 2, BASE_THICKNESS).translate((FLANGE_X, 0, BASE_THICKNESS/2))
flange_left = cq.Workplane("XY").box(FLANGE_WIDTH, FLANGE_Y_HALF * 2, BASE_THICKNESS).translate((-FLANGE_X, 0, BASE_THICKNESS/2))

# 2. Create Connecting Walls (Bridge between flanges and band)
wall_width = WALL_X_END - WALL_X_START
# We make the walls very tall to ensure they bridge from Z=0 up through the pipe area.
# To guarantee connectivity, we extend them from Z=-5 to Z=30.
wall_right = (cq.Workplane("XY")
              .box(wall_width, CLAMP_WIDTH, 40.0)
              .translate((WALL_X_START + wall_width/2, 0, 15.0))
             )

wall_left = (cq.Workplane("XY")
             .box(wall_width, CLAMP_WIDTH, 40.0)
             .translate((-WALL_X_START - wall_width/2, 0, 15.0))
            )

# 3. Create Upper Band (R4)
band = (cq.Workplane("XZ")
        .workplane(offset=PIPE_AXIS_Z)
        .circle(BAND_OUTER)
        .circle(BAND_INNER)
        .extrude(CLAMP_WIDTH, both=True)
       )

# Refine band to |x| <= 7 using intersection with a box mask
band_mask = cq.Workplane("XY").box(BAND_X_LIMIT * 2 + 1, CLAMP_WIDTH + 1, 100).translate((0, 0, PIPE_AXIS_Z))
band = band.intersect(band_mask)

# 4. Create a continuous Base/Connecting Structure (R2)
# This base plate spans the entire X range of the part and connects everything at Z=0 to Z=3.
base_plate = cq.Workplane("XY").box(60, CLAMP_WIDTH, BASE_THICKNESS).translate((0, 0, BASE_THICKNESS/2))

# To ensure connectivity between all parts:
# The band is centered at Z=12.5 with radius ~14-15 -> spans roughly Z=[-3, 28].
# The base plate is at Z=[0, 3].
# We add a central vertical block that covers the center area |x| <= 7 and spans from Z=-5 up to Z=30.
# This ensures it overlaps with the band (Z ~ -3 to 28) AND the base_plate (Z: 0-3).
center_connector = cq.Workplane("XY").box(BAND_X_LIMIT * 2 + 1, CLAMP_WIDTH, 40).translate((0, 0, 15))

# 5. Combine all parts into one solid using union (R1)
result = flange_left.union(flange_right).union(wall_left).union(wall_right).union(band).union(base_plate).union(center_connector)

# 6. Subtract the Pipe Void (R3)
pipe_void = cq.Workplane("YZ").cylinder(CLAMP_WIDTH + 100, VOID_RADIUS).translate((0, 0, PIPE_AXIS_Z))
result = result.cut(pipe_void)

# 7. Subtract Screw Holes (R5)
# We ensure the holes are cut through the flange blocks at X = +/- 27
result = (result.faces("<Z").workplane()
          .center(FLANGE_X, 0).hole(HOLE_DIA)
          .center(-2 * FLANGE_X, 0).hole(HOLE_DIA))

# Final result is a single solid assigned to 'result'