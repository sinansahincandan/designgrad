import cadquery as cq

# Parameters based on Design Document and Structural Requirements
spine_x_end = 15.0
arm_x_start = 15.0
arm_x_end = 160.0
height_top = 110.0
y_limit = 20.0
screw_dia = 5.5
hole_z_coords = [20.0, 60.0]

# Spine Parameters (R5/R6 optimization)
spine_plate_thickness = 8.0
spine_plate_y = 15.0
spine_web_thickness = 4.0

# Arm Parameters (I-beam)
arm_flange_thickness = 6.0
arm_web_thickness = 4.0
arm_width = 30.0 # Total width of I-beam flange/web structure

# To ensure union, we use a significant overlap between the spine and the arm.
# The previous error showed that even with x=15 start, they didn't fuse.
# We will extend the spine to x=20 and start the arm at x=18.
spine_overlap_x = 20.0
arm_start_x = 18.0

# 1. Create the Hollow Wall Spine
# Plates and web extended to spine_overlap_x
spine_plate1 = cq.Workplane("XY").box(spine_overlap_x, spine_plate_thickness, height_top, centered=(False, False, False)).translate((0, spine_plate_y - spine_plate_thickness/2, 0))
spine_plate2 = cq.Workplane("XY").box(spine_overlap_x, spine_plate_thickness, height_top, centered=(False, False, False)).translate((0, -spine_plate_y + spine_plate_thickness/2, 0))
spine_web = cq.Workplane("XY").box(spine_overlap_x, spine_web_thickness, height_top, centered=(False, False, False)).translate((0, -spine_web_thickness/2, 0))

bracket = spine_plate1.union(spine_plate2).union(spine_web)

# 2. Create the I-Beam Shelf Arm
# We center the arm width on Y=0 to ensure it hits the spine plates and web
arm_len = arm_x_end - arm_start_x

# Top Flange (at z=110)
top_flange = cq.Workplane("XY").box(arm_len, arm_width, arm_flange_thickness, centered=(False, False, False)).translate((arm_start_x, -arm_width/2, height_top - arm_flange_thickness))

# Bottom Flange (to provide stiffness/support)
bottom_flange = cq.Workplane("XY").box(arm_len, arm_width, arm_flange_thickness, centered=(False, False, False)).translate((arm_start_x, -arm_width/2, 10))

# Arm Web (connecting flanges)
arm_web = cq.Workplane("XY").box(arm_len, arm_web_thickness, height_top - 10 - arm_flange_thickness, centered=(False, False, False)).translate((arm_start_x, -arm_web_thickness/2, 10 + arm_flange_thickness))

# Union the arm parts with the spine
bracket = bracket.union(top_flange).union(bottom_flange).union(arm_web)

# 3. Add Shelf Support Pillar (R4: solid material at x in [140, 150])
# Ensure pillar overlaps the arm flanges/web by centering it on Y=0 and extending its height
pillar = cq.Workplane("XY").box(10, 20, height_top - 10, centered=(False, False, False)).translate((140, -10, 10))
bracket = bracket.union(pillar)

# 4. Subtract Screw Holes and Clearance (R3)
for z_pos in hole_z_coords:
    # The actual screw hole (cylinder along X)
    # We use a large enough length to ensure it cuts through the spine and arm if necessary
    hole = cq.Workplane("YZ").center(0, z_pos).circle(screw_dia / 2).extrude(arm_x_end + 10)
    bracket = bracket.cut(hole)
    
    # Screwdriver access: Rectangular clearance from x=10 to end
    access_cut = (
        cq.Workplane("XZ")
        .rect(arm_x_end, 15) # Width along X, Height along Z
        .extrude(40)         # Depth along Y
        .translate((10, -20, z_pos)) # Ensure depth covers the whole part width
    )
    bracket = bracket.cut(access_cut)

# 5. Enforce Height Constraint (R4: Nothing above z=110 for x >= 8)
height_limiter = cq.Workplane("XY").box(arm_x_end + 10, 60, 20, centered=(False, False, False)).translate((8, -30, 110))
bracket = bracket.cut(height_limiter)

# Final result assignment
result = bracket