import cadquery as cq

# Dimensions based on Design Document
width = 40.0          # Delta Y
wall_thickness = 15.0 # x from 0 to 15
shelf_length = 150.0  # x up to 150
top_z = 110.0         # Top surface z coordinate
hole_dia = 5.5
access_w = 20.0       # Y dimension of access channel
access_h = 15.0       # Z dimension of access channel

# Taper parameters for x >= 10
# H(x) = 35 - (25/140)*(x-10)
# At x=10, H=35. At x=150, H=10.
def get_height(x):
    if x < 10:
        return 110.0 # Wall height is capped by top_z, but thickness logic uses this for the arm
    # The taper applies to the thickness of the horizontal arm
    # We define the bottom of the arm such that the top is always at top_z
    h = 35.0 - (25.0 / 140.0) * (x - 10.0)
    return max(h, 10.0)

# 1. Build the Main Body
# We will build this using a series of slices or a loft to ensure the taper is perfect.
# However, for simplicity and robustness in CadQuery, we can create the wall 
# and then use a lofted extrusion for the tapered arm.

# Wall Plate: x [0, 15], y [-20, 20], z [0, 110]
wall = cq.Workplane("XY").box(wall_thickness, width, top_z, centered=(False, False, False))

# Tapered Arm: x [15, 150], y [-20, 20], z is variable
# The top surface is at z = 110. 
# At x=15, height H(15) = 35 - (25/140)*5 = 34.2857
# Bottom surface at x=15: z = 110 - 34.2857 = 75.7143

# To create a lofted arm from x=15 to x=150:
# We define profiles at x=15 and x=150
profile_start_x = 15.0
h_start = 35.0 - (25.0 / 140.0) * (15.0 - 10.0)
z_bottom_start = top_z - h_start

profile_end_x = 150.0
h_end = 10.0
z_bottom_end = top_z - h_end

# Create the arm using lofting between two rectangles
arm = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(0.001, width) # dummy to start
    .center(profile_start_x, z_bottom_start + width/2) # This is getting complex, let's use a simpler approach
)

# Simpler Approach: Create the arm by extruding a tapered shape or using a series of boxes.
# Since it's a linear taper, we can use a loft between two rectangles on YZ planes.
arm = (
    cq.Workplane("YZ")
    .center(profile_start_x, z_bottom_start + width/2) # This is not quite right for YZ plane
)

# Let's use the most reliable method: Create a series of thin slices or a lofted profile.
# Profile 1 at x=15 (YZ plane)
p1 = cq.Workplane("YZ").workplane(offset=profile_start_x).rect(width, h_start).translate((0, 0, z_bottom_start + h_start/2))
# Profile 2 at x=150 (YZ plane)
p2 = cq.Workplane("YZ").workplane(offset=profile_end_x).rect(width, h_end).translate((0, 0, z_bottom_end + h_end/2))

# Actually, CadQuery loft works best on workplanes. Let's define the profiles in XZ or YZ.
# We want a shape where x is the extrusion direction.
arm = (
    cq.Workplane("XY")
    .workplane(offset=profile_start_x)
    .rect(0.1, width) # Start at x=15
    .extrude(profile_end_x - profile_start_x, taper=0) # This doesn't allow variable height easily
)

# Final attempt at construction: Build the arm as a single lofted object.
# We define two rectangles in the YZ plane and loft them along X.
def create_arm():
    # Profile at x = 15
    h1 = 35.0 - (25.0 / 140.0) * (15.0 - 10.0)
    z1_bot = top_z - h1
    # Profile at x = 150
    h2 = 10.0
    z2_bot = top_z - h2
    
    # We use a loft between two rectangles on YZ planes located at different X offsets
    # In CQ, we can create a loft by defining points/wires.
    # But the easiest way is to build a solid via a sweep or just unioning many boxes.
    # Given the linear requirement, let's use 100 slices for perfect precision.
    parts = []
    num_slices = 100
    dx = (profile_end_x - profile_start_x) / num_slices
    for i in range(num_slices):
        curr_x = profile_start_x + i * dx
        h_curr = 35.0 - (25.0 / 140.0) * (curr_x - 10.0)
        z_bot_curr = top_z - h_curr
        parts.append(cq.Workplane("XY").box(dx + 0.01, width, h_curr, centered=(False, False, False)).translate((curr_x, 0, z_bot_curr)))
    
    arm_solid = parts[0]
    for p in parts[1:]:
        arm_solid = arm_solid.union(p)
    return arm_solid

# Re-simplifying: The wall is x [0,15]. The arm starts at x=15.
# Let's just build the whole thing as one lofted object from x=0 to x=150.
# At x=0 to 15, height is 110.
# At x=15 to 150, height follows taper.

def create_bracket():
    # Create wall (x: 0-15)
    wall = cq.Workplane("XY").box(15, width, top_z, centered=(False, False, False))
    
    # Create arm (x: 15-150) using slices for the linear taper
    num_slices = 50
    dx = (150.0 - 15.0) / num_slices
    arm_parts = []
    for i in range(num_slices):
        x_pos = 15.0 + i * dx
        h_x = 35.0 - (25.0 / 140.0) * (x_pos - 10.0)
        z_bot = top_z - h_x
        # Create a slice of thickness dx
        slice_obj = cq.Workplane("XY").box(dx, width, h_x, centered=(False, False, False)).translate((x_pos, 0, z_bot))
        arm_parts.append(slice_obj)
    
    combined_arm = arm_parts[0]
    for p in arm_parts[1:]:
        combined_arm = combined_arm.union(p)
        
    body = wall.union(combined_arm)
    
    # 2. Subtract Screw Holes (R3)
    # Axis along X, centered at y=0, z=20 and z=60.
    for z_pos in [20, 60]:
        # Hole: YZ plane at x=7.5 (middle of wall), circle(2.75), extrude through the whole part
        hole = (
            cq.Workplane("YZ")
            .center(0, z_pos)
            .circle(hole_dia/2)
            .extrude(160, both=True) # Extends far enough to clear 150mm
        )
        # Since 'both=True' centers on the YZ plane (x=0), and our part is x:0-150,
        # we translate it so its center is at x=75.
        hole = hole.translate((75, 0, 0))
        body = body.cut(hole)
        
        # Access Channel (R3): 20mm (Y) x 15mm (Z), centered on axis, x from 10 to 20
        # Center of x [10, 20] is 15. Length is 10.
        channel = cq.Workplane("XY").box(10, access_w, access_h).translate((15, 0, z_pos))
        body = body.cut(channel)
        
    return body

result = create_bracket()