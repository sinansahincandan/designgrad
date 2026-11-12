import cadquery as cq

# Parameters based on Design Document and Feedback
plate_thickness = 4.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

arm_start_x = 4.0
arm_end_x = 47.0
arm_width_start = 16.0
arm_width_end = 10.0
arm_height = 20.0 # thickness in Z to ensure R6 strength

strap_pocket_x_range = (35, 45)
strap_pocket_y_half = 6.0
strap_pocket_z_range = (-13, -6)

lip_width = 5.0
lip_thickness = 8.0 # height in Z: from -13 to -5
lip_depth = 8.0     # y direction: from -4 to 4

# 1. Create the Back Plate (R2, R3)
# x range [0, 4], y [-8, 8], z [-5, 45]
# Center of box is at (2, 0, 20)
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# Create Screw Holes (R3)
# Holes at (y=0, z=0) and (y=0, z=40). 
# Since plate is translated by 20 in Z, local coordinates for holes are -20 and +20.
# We use the face at x=0 (<X) to create the workplane.
plate = plate.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Tapered Support Arm (R6, R7)
# We use a loft between two rectangles to transition width from 16 to 10.
# Profile 1 at x=4: width 16, height 20
# Profile 2 at x=47: width 10, height 20 (keeping height constant for simplicity/strength)
# We'll build the arm as a lofted solid.

# Define profiles for lofting
# Note: Lofting in CadQuery is easiest by creating workplanes on different X-slices or using a series of boxes.
# To ensure R1 (single solid), we will use a sequence of boxes to approximate a taper, 
# which is more robust for boolean operations than complex lofts.

arm_segments = 10
segment_length = (arm_end_x - arm_start_x) / arm_segments
arm_parts = []

for i in range(arm_segments):
    curr_x = arm_start_x + i * segment_length
    next_x = arm_start_x + (i + 1) * segment_length
    
    # Linear interpolation of width
    t = i / arm_segments
    w_curr = arm_width_start - t * (arm_width_start - arm_width_end)
    w_next = arm_width_start - (i + 1) / arm_segments * (arm_width_start - arm_width_end)
    
    # Create a segment. We'll use the center of the segment for translation.
    # Segment x-center: curr_x + segment_length/2
    # Z-center: we want the bottom to be at z=-14 (for strap bed), 
    # but the arm is structural. Let's set arm Z range such that it covers the pocket area.
    # If height is 20, and we want top at -6, center is -13.
    seg = (
        cq.Workplane("XY")
        .box(segment_length, w_curr, arm_height)
        .translate((curr_x + segment_length/2, 0, -13))
    )
    arm_parts.append(seg)

# Combine all segments into one arm body
arm_body = arm_parts[0]
for part in arm_parts[1:]:
    arm_body = arm_body.union(part)

# 3. Create the Retaining Lip (R5)
# x in [47, 52], |y| <= 4, z in [-13, -8]
lip = (
    cq.Workplane("XY")
    .box(lip_width, 8, 5) # width 5, y-depth 8, height 5
    .translate((49.5, 0, -10.5)) # x center: 47 + 2.5 = 49.5; z range: [-13, -8]
)

# 4. Combine everything (R1)
combined_solid = plate.union(arm_body).union(lip)

# 5. Subtract the Strap Pocket (R4)
# pocket is x[35,45], y[-6,6], z[-13,-6]
pocket_vol = (
    cq.Workplane("XY")
    .box(10, 12, 7)
    .translate((40, 0, -9.5)) # x center: 40; y center: 0; z range: [-13, -6]
)

result = combined_solid.cut(pocket_vol)