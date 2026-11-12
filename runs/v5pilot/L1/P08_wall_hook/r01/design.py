import cadquery as cq

# Parameters
plate_thickness = 5.0
plate_width = 16.0 # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

# 1. Create the Back Plate (R2, R3)
# x: [0, 5], y: [-8, 8], z: [-5, 45]
p = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height, centered=False).translate((0, -8, -5))

# Holes at (y=0, z=0) and (y=0, z=40). 
# Plate Y range is [-8, 8], so y=0 is offset 8 from the min corner.
# Plate Z range is [-5, 45], so z=0 is offset 5 from the min corner.
p = p.faces("<X").workplane().pushPoints([(8, 5), (8, 45)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6)
# To ensure connectivity and avoid disconnected solids, we build the arm as a single unioned object
# that overlaps the plate significantly in X and Y.

# Block A: x [0, 35], y [-8, 8], z [-10, 2] (Height 12 at x=8 satisfies R6)
arm_core = cq.Workplane("XY").box(35, 16, 12, centered=False).translate((0, -8, -10))

# Block B: x [35, 50], y [-8, 8], z [-14, 2] (Height 16)
arm_end = cq.Workplane("XY").box(15, 16, 16, centered=False).translate((35, -8, -14))

# Wedge Filler: x [0, 35], y [-8, 8], z [-14, -10]
# We use a polyline in XZ and extrude it. To ensure it's part of the same solid, 
# we must make sure the extrusion covers the Y range [-8, 8].
wedge_filler = (
    cq.Workplane("XZ")
    .polyline([(0, -14), (35, -14), (0, -10)])
    .close()
    .extrude(16, both=True) # Extrudes along Y from -8 to 8
)

# Combine arm parts into one solid
arm = arm_core.union(arm_end).union(wedge_filler)

# 3. Strap Seat (R4)
# Subtract a pocket: x in [35, 45], y in [-6, 6], z in [-13, -6]
pocket = cq.Workplane("XY").box(10, 12, 7, centered=False).translate((35, -6, -13))
arm_with_seat = arm.cut(pocket)

# 4. Retaining Lip (R5)
# x in [47, 52], y in [-4, 4], z in [-13, -8]
lip = cq.Workplane("XY").box(5, 8, 5, centered=False).translate((47, -4, -13))

# Final Union: Ensure the arm is unioned with the plate.
# Since arm_core starts at x=0 and plate ends at x=5, they overlap by 5mm in X.
# Since both have y range [-8, 8], they overlap in Y.
# Since arm_core z is [-10, 2] and plate z is [-5, 45], they overlap in Z.
result = p.union(arm_with_seat).union(lip)