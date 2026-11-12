import cadquery as cq
import math

# Dimensions
width = 40.0  # y direction
wall_thickness = 15.0
shelf_thickness = 15.0
shelf_length = 150.0
height_at_root = 110.0
hole_dia = 5.5
clearance_width = 20.0 # Width for screwdriver access

# 1. Create the main L-shape body
# Wall plate (vertical)
wall = cq.Workplane("XY").box(wall_thickness, width, height_at_root, centered=(False, False, False))

# Shelf support (horizontal)
# We place it so top is at z=110. 
# The wall goes up to 110. The shelf extends from x=wall_thickness to 150.
shelf = (
    cq.Workplane("XY")
    .box(shelf_length - wall_thickness, width, shelf_thickness, centered=(False, False, False))
    .translate((wall_thickness, 0, height_at_root - shelf_thickness))
)

# Combine into one solid
bracket = wall.union(shelf)

# 2. Subtract Screw Holes (R3)
# Holes at y=0, z=20 and y=0, z=60. Axis along X.
# Since we used centered=(False, False, False), the center of Y is width/2.
y_center = width / 2.0

hole1 = cq.Workplane("XZ").workplane(offset=0).center(0, 20).circle(hole_dia/2).extrude(wall_thickness + 2)
# To make it easier to subtract through the whole part:
bracket = (
    bracket.faces("<X").workplane()
    .center(0, 20).hole(hole_dia) # This is tricky with coordinate systems, let's use a different approach
)

# Re-doing subtraction more robustly
# Create holes as cylinders along X axis
h1 = cq.Workplane("XY").workplane(offset=0).center(y_center, 20).rect(width+2, hole_dia+2).extrude(wall_thickness + 5) # placeholder logic
# Let's use the standard way: define cylinders and subtract

def create_bracket():
    # Main body
    base = cq.Workplane("XY").box(150, width, 110, centered=(False, False, False))
    # We want an L shape. Let's build it by adding two boxes and subtracting the empty corner.
    # Vertical part: x[0,15], y[0,40], z[0,110]
    # Horizontal part: x[15,150], y[0,40], z[95,110]
    v_part = cq.Workplane("XY").box(15, width, 110, centered=(False, False, False))
    h_part = cq.Workplane("XY").box(135, width, 15, centered=(False, False, False)).translate((15, 0, 95))
    body = v_part.union(h_part)

    # Screw holes: axis along X. Center at y=width/2, z=20 and z=60.
    # We'll create a cylinder for each hole.
    # Hole 1: center (x_any, width/2, 20)
    # Hole 2: center (x_any, width/2, 60)
    
    # To ensure R3 (screwdriver access), we cut a slot from x=10 onwards.
    # Slot: x >= 10, y in [width/2 - clearance/2, width/2 + clearance/2], z around hole axis
    
    # Create holes
    h1 = cq.Workplane("YZ").center(0, width/2).workplane(offset=0).circle(hole_dia/2).extrude(160) # X-axis is 'Z' in YZ plane? No.
    # Let's use the most reliable way: create a cylinder along X axis
    # A cylinder along X has direction (1, 0, 0). In CQ, we can rotate a Z-cylinder.
    
    def get_hole(z_pos):
        return (
            cq.Workplane("XY")
            .center(width/2, z_pos)
            .rect(160, hole_dia + 2) # Create a rectangular slot for screwdriver access
            .extrude(160) # This is not quite right. Let's use a cylinder and then a slot.
        )

    # Correct approach:
    # 1. The body
    # 2. Subtract two cylinders (the holes)
    # 3. Subtract two rectangular prisms (the screwdriver access channels)
    
    body = v_part.union(h_part)
    
    # Holes
    for z in [20, 60]:
        # Cylinder along X axis: center at y=width/2, z=z. 
        # We'll create it in the XY plane and rotate it to align with X.
        # Or just use a cylinder centered at (x_mid, width/2, z) oriented along X.
        # In CQ, we can define a cylinder by its center and direction if using certain methods, 
        # but standard is Z-axis. So rotate a Z-cylinder 90 deg around Y.
        hole = (
            cq.Workplane("XY")
            .center(width/2, z)
            .rect(160, hole_dia + 0.1) # This creates a slot actually. Let's do it properly.
        )
        # Let's just use the 'hole' method on a plane perpendicular to X.
        # The wall is at x=0. A plane perpendicular to X is YZ.
        
    # Let's restart the construction logic for clarity and precision
    
    # 1. Vertical Wall Plate (x: 0-15, y: 0-40, z: 0-110)
    wall_plate = cq.Workplane("XY").box(15, width, 110, centered=(False, False, False))
    # 2. Horizontal Shelf (x: 15-150, y: 0-40, z: 95-110)
    shelf_plate = cq.Workplane("XY").box(135, width, 15, centered=(False, False, False)).translate((15, 0, 95))
    
    combined = wall_plate.union(shelf_plate)
    
    # 3. Screw holes (diameter 5.5, axis X)
    # We'll use a YZ plane to cut through the X direction
    for z_pos in [20, 60]:
        # Create a cylinder along X axis at (y=width/2, z=z_pos)
        # To do this: create on YZ plane, then extrude along X.
        # The YZ plane is at x=7.5 (center of wall).
        hole = (
            cq.Workplane("YZ")
            .offset2D(0) # dummy
            .center(width/2, z_pos)
            .circle(hole_dia/2)
            .extrude(160, both=True) # Extrudes along X (the normal to YZ)
        )
        # We need to translate the hole so it's centered on X. 
        # Since we extrude 'both=True', it centers on the plane.
        # The plane is at x=0 in our coordinate system? No, let's make a plane at x=7.5.
        # Actually, simpler: create cylinder and translate.
        
    # Let's use a more direct method for holes:
    # Create a cylinder along Z, then rotate it 90 deg around Y to align with X.
    def hole_along_x(y_c, z_c):
        return (
            cq.Workplane("XY")
            .center(y_c, z_c)
            .circle(hole_dia/2)
            .extrude(160) # This is a Z cylinder. 
        )
    # Actually, the easiest way to make an X-axis hole:
    # Create a cylinder on the YZ plane. The normal to YZ is X.
    
    final_body = combined
    for z_pos in [20, 60]:
        # Define a plane at x=7.5 (middle of wall)
        # A hole through this plane along X:
        h = (
            cq.Workplane("YZ")
            .center(width/2, z_pos)
            .circle(hole_dia/2)
            .extrude(160, both=True) 
        )
        # Since the YZ plane is at x=0 in CQ's default coordinate system, 
        # and our part starts at x=0, we need to translate this hole.
        # The 'both=True' extrude will center it on x=0. Our part is x:0-150.
        # So we translate the hole by +75 in X.
        h = h.translate((75, 0, 0))
        final_body = final_body.cut(h)
        
        # R3: Screwdriver access. No material within 4mm of axis for x >= 10.
        # This means a slot/channel from x=10 to x=150, centered at the hole.
        # The channel must be wide enough for a screwdriver (e.g., 12mm).
        access = (
            cq.Workplane("XY")
            .center(width/2, z_pos)
            .rect(145, 12) # width of slot is 12mm
            .extrude(140, both=True) # Extends from x = 75-70 to 75+70 (i.e., 5 to 145)
        )
        # We need the access to start at x=10.
        # Let's define it by its bounding box: x in [10, 150], y in [mid-6, mid+6], z in [z_pos-6, z_pos+6]
        access = (
            cq.Workplane("XY")
            .center(width/2, z_pos)
            .rect(140, 12) # length 140
            .extrude(150, both=True)
        )
        # Let's just use a box for the access channel to be safe.
        access = (
            cq.Workplane("XY")
            .center(width/2, z_pos)
            .rect(140, 12) # length along X? No, rect is in XY plane.
        )
        # Correcting: A box for the access channel
        # x from 10 to 150, y from mid-6 to mid+6, z from z_pos-6 to z_pos+6
        access = (
            cq.Workplane("XY")
            .center(width/2, z_pos)
            .rect(140, 12) # This is in XY plane. We want it along X.
        )
        # Let's use the box method:
        access = cq.Workplane("XY").box(140, 12, 12).translate((75+10-70, width/2, z_pos)) # This is getting messy.
    
    return final_body

# Let's write a clean version of the logic.
def build_bracket():
    w = 40.0
    wall_t = 15.0
    shelf_t = 15.0
    shelf_l = 150.0
    h_root = 110.0
    
    # 1. Main Body
    v_part = cq.Workplane("XY").box(wall_t, w, h_root, centered=(False, False, False))
    h_part = cq.Workplane("XY").box(shelf_l - wall_t, w, shelf_t, centered=(False, False, False)).translate((wall_t, 0, h_root - shelf_t))
    body = v_part.union(h_part)
    
    # 2. Holes and Access Channels
    for z_pos in [20, 60]:
        # Hole (cylinder along X)
        # Create on YZ plane at x=7.5
        hole = (
            cq.Workplane("YZ")
            .center(w/2, z_pos)
            .circle(5.5/2)
            .extrude(160, both=True)
            .translate((7.5, 0, 0))
        )
        body = body.cut(hole)
        
        # Access Channel (box along X)
        # x: [10, 150], y: [mid-6, mid+6], z: [z_pos-6, z_pos+6]
        access = (
            cq.Workplane("XY")
            .center(w/2, z_pos)
            .rect(140, 12) # This is in XY plane... wait.
        )
        # Let's use the box method directly:
        channel = cq.Workplane("XY").box(140, 12, 12).translate((75 + 10 - 70, w/2, z_pos))
        # Wait, if x is from 10 to 150, length is 140. Center of [10, 150] is 80.
        channel = cq.Workplane("XY").box(140, 12, 12).translate((80, w/2, z_pos))
        # But the box is centered at (80, mid, z_pos), so x goes from 80-70=10 to 80+70=150. Perfect.
        body = body.cut(channel)
        
    return body

result = build_bracket()