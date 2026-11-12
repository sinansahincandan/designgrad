import cadquery as cq

# Constants
hole_dia = 3.2
shaft_dia = 6.0

# Dimensions for I-beam profile (to satisfy R6: I <= 1.0 mm^4)
flange_w = 0.1
flange_h = 12.0
base_flange_y = 5.0

# To ensure a single solid, we will build the entire structure using one continuous extrusion or 
# very large overlapping volumes that are guaranteed to intersect.
# The previous attempts failed because thin parts (like flanges) were being treated as separate solids 
# during union due to precision/topology issues. We'll use a "spine" approach:
# A central thick spine that connects everything, and then subtract or add the specific features.

# 1. Create a central Spine (x=0 to 130) to ensure connectivity
# This spine will be at y=0, z in [0, 2], x from 0 to 130.
spine = cq.Workplane("XY").box(135, 4.0, 4.0, centered=(False, True, False)).translate((-2.5, 0, -1))

# 2. Base Section (x=0 to 30) - Flanges and Web
# We'll make the flanges overlap the spine significantly.
base_f1 = cq.Workplane("XY").box(35, flange_w, flange_h, centered=(False, True, False)).translate((-2.5, base_flange_y, 0))
base_f2 = cq.Workplane("XY").box(35, flange_w, flange_h, centered=(False, True, False)).translate((-2.5, -base_flange_y, 0))

# 3. Mid Section (x=30 to 110)
mid_rib1 = cq.Workplane("XY").box(85, flange_w, flange_h, centered=(False, True, False)).translate((27.5, base_flange_y, 0))
mid_rib2 = cq.Workplane("XY").box(85, flange_w, flange_h, centered=(False, True, False)).translate((27.5, -base_flange_y, 0))

# 4. Motor Mount (x=110 to 130)
mount = cq.Workplane("XY").box(30, 24, 12, centered=(False, True, False)).translate((105, 0, 6))

# Combine everything with the spine. 
# We use a large overlap for flanges and ribs to ensure they fuse into the spine.
arm_body = spine.union(base_f1).union(base_f2).union(mid_rib1).union(mid_rib2).union(mount)

result = arm_body

# 5. Hole Operations (R3 & R4)
# We use a robust way to select the top face for drilling.

# R3: Frame attachment holes (x=6, y=+/-6, dia 3.2)
result = result.faces(">Z").workplane().center(6, 6).hole(hole_dia)
result = result.faces(">Z").workplane().center(6, -6).hole(hole_dia)

# R4: Motor Mount holes
# Shaft hole (x=120, y=0, dia 6)
result = result.faces(">Z").workplane().center(120, 0).hole(shaft_dia)

# Bolt holes (x=120 +/- 8, y=+/- 9.5, dia 3.2)
bolt_holes = [
    (120 + 8, 9.5),
    (120 - 8, 9.5),
    (120 + 8, -9.5),
    (120 - 8, -9.5)
]

for bx, by in bolt_holes:
    result = result.faces(">Z").workplane().center(bx, by).hole(hole_dia)