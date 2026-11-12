import cadquery as cq

# Parameters based on Design Document
width = 40.0           # y range: -20 to 20
spine_x_end = 15.0     # x range of spine: 0 to 15
arm_x_end = 160.0      # total length x: up to 160
height_top = 110.0     # z top surface
screw_dia = 5.5        # R3 requirement
hole_z_coords = [20.0, 60.0]

# --- 1. Optimized I-Beam Spine (x: 0 to 15) ---
spine_flange_w = 40.0
spine_flange_t = 8.0
spine_web_t = 6.0
spine_height = 110.0

# Create I-beam profile in YZ plane using a single polyline to ensure it's a valid face for extrusion
# The spine is centered at y=0, so width goes from -20 to 20. 
# In YZ plane (normal X), Y is the vertical axis? No, design says y is width (-20 to 20) and z is height.
# So profile in YZ: Y is horizontal, Z is vertical.
spine_profile = (
    cq.Workplane("YZ")
    .polyline([
        (-spine_flange_w/2, 0),
        (spine_flange_w/2, 0),
        (spine_flange_w/2, spine_flange_t),
        (spine_web_t/2, spine_flange_t),
        (spine_web_t/2, spine_height - spine_flange_t),
        (spine_flange_w/2, spine_height - spine_flange_t),
        (spine_flange_w/2, spine_height),
        (-spine_flange_w/2, spine_height),
        (-spine_flange_w/2, spine_height - spine_flange_t),
        (-spine_web_t/2, spine_height - spine_flange_t),
        (-spine_web_t/2, spine_flange_t),
        (-spine_flange_w/2, spine_flange_t),
    ])
    .close()
)
# Extrude along X from 0 to 15. To ensure it connects to the arm (starting at x=15), we extend it slightly.
spine = spine_profile.extrude(spine_x_end + 1.0)

# --- 2. Trussed Shelf Arm (x: 15 to 160) ---
chord_thickness = 4.0
chord_width = 10.0 

# Top Chord (at z=110, y from -5 to 5). Start at x=14 to overlap spine.
top_chord = (
    cq.Workplane("XY")
    .box(arm_x_end - 14.0, chord_width, chord_thickness)
    .translate((14.0, -chord_width/2, height_top - chord_thickness))
)

# Bottom Chord (at z=5, y from -5 to 5). Start at x=14 to overlap spine.
bottom_chord = (
    cq.Workplane("XY")
    .box(arm_x_end - 14.0, chord_width, chord_thickness)
    .translate((14.0, -chord_width/2, 5.0))
)

# Diagonal Web Members (Truss)
num_segments = 8
segment_length = (arm_x_end - 14.0) / num_segments
arm_webs_list = []

for i in range(num_segments):
    x0 = 14.0 + i * segment_length
    x1 = x0 + segment_length
    
    # Diagonal 1 (bottom-left to top-right)
    d1 = (
        cq.Workplane("XZ")
        .polyline([(x0, 5), (x1, height_top - chord_thickness), (x1, height_top), (x0, 5 + chord_thickness)])
        .close()
        .extrude(chord_width)
        .translate((0, -chord_width/2, 0))
    )
    # Diagonal 2 (top-left to bottom-right)
    d2 = (
        cq.Workplane("XZ")
        .polyline([(x0, height_top - chord_thickness), (x1, 5), (x1, 5 + chord_thickness), (x0, height_top)])
        .close()
        .extrude(chord_width)
        .translate((0, -chord_width/2, 0))
    )
    arm_webs_list.append(d1)
    arm_webs_list.append(d2)

# Combine all webs into one solid using union
arm_webs_ext = arm_webs_list[0]
for i in range(1, len(arm_webs_list)):
    arm_webs_ext = arm_webs_ext.union(arm_webs_list[i])

# --- 3. R4 Support Pillar (x: 140 to 150, y: -5 to 5, z: 0 to 110) ---
support_pillar = (
    cq.Workplane("XY")
    .box(10, 10, height_top)
    .translate((140, -5, 0))
)

# Combine all main parts into one solid
bracket = spine.union(top_chord).union(bottom_chord).union(arm_webs_ext).union(support_pillar)

# --- 4. Subtract Screw Holes (R3) and Clearance Pockets ---
for z_pos in hole_z_coords:
    # The actual screw hole (cylindrical, axis along X)
    hole = (
        cq.Workplane("YZ")
        .center(0, z_pos)
        .circle(screw_dia / 2)
        .extrude(arm_x_end + 10)
    )
    bracket = bracket.cut(hole)

    # R3: Rectangular clearance pocket for screwdriver access (x >= 10)
    clearance_pocket = (
        cq.Workplane("XY")
        .box(arm_x_end, 12, 8)
        .translate((10, -6, z_pos - 4)) # Centered on hole axis
    )
    bracket = bracket.cut(clearance_pocket)

# --- 5. Final Constraint Check (R4: No part above z=110 for x >= 8) ---
forbidden_zone = (
    cq.Workplane("XY")
    .box(arm_x_end + 1, 40, 500)
    .translate((8, -20, 110)) 
)
bracket = bracket.cut(forbidden_zone)

result = bracket