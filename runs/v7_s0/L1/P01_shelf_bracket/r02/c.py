import cadquery as cq

# Parameters based on Design Document
width = 30.0            # y-dimension (-15 to 15)
spine_x_end = 15.0      # x-dimension of spine
spine_height = 110.0    # z-dimension (0 to 110)
arm_x_end = 160.0       # total length in x
thickness_wall_arm = 30.0 # thickness at x=15
thickness_tip_arm = 10.0  # thickness at x=160
screw_dia = 5.5

# Hole positions (y, z)
hole_centers = [(0.0, 20.0), (0.0, 60.0)]

# 1. Create the Wall Spine
# From x=0 to 15, y=-15 to 15, z=0 to 110
spine = cq.Workplane("XY").box(spine_x_end, width, spine_height, centered=(False, False, False))

# 2. Create the Tapered Arm
def create_arm():
    # Full block for the arm: x from 15 to 160, y from -15 to 15, z from 80 to 110
    # Top is at 110. Thickness at x=15 is 30 (z: 80-110). Thickness at x=160 is 10 (z: 100-110).
    full_arm = cq.Workplane("XY").box(arm_x_end - spine_x_end, width, thickness_wall_arm, centered=(False, False, False)).translate((spine_x_end, 0, spine_height - thickness_wall_arm))
    
    # We want to remove a wedge from the bottom.
    # The wedge is in the XZ plane.
    # At x=15 (local x=0), height of cut is 0.
    # At x=160 (local x=145), height of cut is 20 (from z=80 to z=100).
    # Vertices in XZ relative to spine_x_end: (0, 80), (145, 80), (145, 100)
    # However, the arm block is translated. Let's use a simpler subtraction approach.
    
    # Create a wedge shape to subtract from the bottom of the arm
    wedge = (
        cq.Workplane("XZ")
        .workplane(offset=spine_x_end)
        .polyline([(0, 80), (arm_x_end - spine_x_end, 80), (arm_x_end - spine_x_end, 100)])
        .close()
        .extrude(width) # Extrudes along Y by default in XZ plane if we use the right axis? 
        # Actually, extrude on XZ goes along Y. We need to ensure it covers the width.
    )
    # To be safe and avoid 'centered' error or orientation issues:
    # Let's build the arm by lofting two rectangles in XZ plane.
    
    # Profile 1 at x=15: y from -15 to 15, z from 80 to 110
    # Profile 2 at x=160: y from -15 to 15, z from 100 to 110
    
    # We'll use a different approach for the arm to ensure it is one solid.
    # Create two rectangles on XZ planes and loft them.
    # Since we want to extrude along Y (the width), we define profiles in XZ.
    
    # Profile 1: x=15, z=[80, 110], y=[-15, 15]
    # Profile 2: x=160, z=[100, 110], y=[-15, 15]
    
    # In CadQuery, lofting between two workplanes:
    # We create a sketch on XZ at x=15 and another on XZ at x=160.
    # But we need to extrude the width. The easiest way is to define the profile in XZ 
    # and extrude it along Y. However, that's for constant profiles.
    
    # Let's go back to the wedge cut but fix the extrusion.
    # The arm block is from x=15 to 160, y=-15 to 15, z=80 to 110.
    # We want to remove material where z < 100 - (20/145)*(x-15) ? No.
    # At x=15, z_bottom = 80. At x=160, z_bottom = 100.
    # Linear equation for bottom: z = 80 + (20/145)*(x-15)
    
    # Let's use a simple wedge subtraction.
    # The wedge is a triangular prism.
    wedge_prism = (
        cq.Workplane("XZ")
        .workplane(offset=spine_x_end)
        .polyline([(0, 80), (arm_x_end - spine_x_end, 80), (arm_x_end - spine_x_end, 100)])
        .close()
        .extrude(width) # This extrudes along Y if the workplane is XZ
    )
    # Note: In CQ, for XZ plane, extrusion goes along Y. 
    # We need to make sure it's centered on y=0.
    wedge_prism = wedge_prism.translate((0, -width/2, 0))
    
    return full_arm.cut(wedge_prism)

arm = create_arm()

# Combine spine and arm
bracket = spine.union(arm)

# 3. Subtract Screw Holes (R3) and Clearance (R3)
for y_pos, z_pos in hole_centers:
    # The screw holes are along X axis.
    # Hole diameter 5.5mm. We extrude it long enough to pass through everything.
    hole = (
        cq.Workplane("XY")
        .workplane(offset=z_pos)
        .center(0, y_pos)
        .circle(screw_dia/2)
        .extrude(arm_x_end + 10, both=True) # Extrude along Z? No, we need to extrude along X.
    )
    # Correct way for hole along X: Use YZ plane or rotate.
    # Or just use a cylinder on the YZ plane at the correct X position.
    # But the holes are "screw access channels", implying they go through the thickness.
    # The design says "cylindrical voids... centered on screw axes". 
    # Screw axis is likely perpendicular to the wall (along X).
    
    hole = cq.Workplane("YZ").workplane(offset=0).center(y_pos, z_pos).circle(screw_dia/2).extrude(arm_x_end + 10)
    # Wait, YZ plane normal is X. So extrude goes along X.
    # We need to translate the hole to its (y, z) position.
    hole = cq.Workplane("YZ").center(y_pos, z_pos).circle(screw_dia/2).extrude(arm_x_end + 10)
    bracket = bracket.cut(hole)
    
    # Clearance: Rectangular cutout 20mm (width/y) x 10mm (height/z), from x=10 to x=25.
    # Centered on the screw axis.
    # The box is in XZ plane, extruded along Y.
    clearance_cut = (
        cq.Workplane("XZ")
        .workplane(offset=0) # We'll use a different approach for clearance
    )
    # Let's just create a box and cut it.
    # x: 10 to 25 (length 15, center at 17.5)
    # y: -10 to 10 (width 20, center at 0)
    # z: z_pos-5 to z_pos+5 (height 10, center at z_pos)
    clearance_box = cq.Workplane("XY").box(15, 20, 10, centered=(True, True, True)).translate((17.5, 0, z_pos))
    # But the box is in XY plane. We need it to be oriented such that its length is along X.
    # A box(dx, dy, dz) has dx along X, dy along Y, dz along Z.
    # So: dx=15 (x-dir), dy=20 (y-dir), dz=10 (z-dir).
    # Center of x is 17.5. Center of y is 0. Center of z is z_pos.
    clearance_box = cq.Workplane("XY").box(15, 20, 10, centered=(True, True, True)).translate((17.5, 0, z_pos))
    # Wait, if we use box(15, 20, 10) and translate to (17.5, 0, z_pos), 
    # the x-range is [17.5 - 7.5, 17.5 + 7.5] = [10, 25]. Correct.
    # The y-range is [-10, 10]. Correct.
    # The z-range is [z_pos - 5, z_pos + 5]. Correct.
    bracket = bracket.cut(clearance_box)

result = bracket