import cadquery as cq

# Parameters
screw_hole_dia = 4.5
plate_thickness = 2.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)

# 1. Create the Back Plate (R2, R3)
# x: [0, 2], y: [-8, 8], z: [-5, 45]
# Center of box is at (1, 0, 20)
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((1, 0, 20))

# Add Screw Holes (R3)
# The holes are centered at absolute (y=0, z=0) and (y=0, z=40).
# Relative to the plate center (1, 0, 20), these points are (0, -20) and (0, 20).
plate = plate.faces("<X").workplane().center(0, 0).pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6)
# A continuous block from x=2 to x=34 to ensure a robust load path.
# We use a thick arm to satisfy R6 strength requirements.
# x: [2, 34], y: [-7, 7], z: [-14, 0] (approximate)
arm_part = cq.Workplane("XY").box(32, 14, 14).translate((18, 0, -7))

# 3. Create the Strap Seat and Lip (R4, R5)
# Define Seat Block: x[34, 52], y[-6, 6], z[-14, 0]
seat_block = cq.Workplane("XY").box(18, 12, 14).translate((43, 0, -7))

# Subtract Pocket (R4): x[35, 45], y[-6, 6], z[-13, -6]
pocket = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))
seat_with_pocket = seat_block.cut(pocket)

# Define Retaining Lip (R5): x[47, 52], y[-4, 4], z[-13, -8]
lip_part = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# 4. Combine all parts into a single solid (R1)
# We union the plate, arm, seat, and lip.
# The geometry is designed to overlap at boundaries to ensure manifoldness.
combined = plate.union(arm_part).union(seat_with_pocket).union(lip_part)

result = combined