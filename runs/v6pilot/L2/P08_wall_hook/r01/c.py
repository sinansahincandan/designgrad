import cadquery as cq

# Parameters
screw_hole_dia = 4.5
plate_thickness_base = 2.0
boss_thickness = 6.0
boss_width = 10.0
boss_height = 10.0

# 1. Create the Back Plate with thickened bosses (R2, R3)
# Base plate: x in [0, 2], y in [-8, 8], z in [-5, 45]
base_plate = cq.Workplane("XY").box(plate_thickness_base, 16, 50).translate((plate_thickness_base/2, 0, 20))

# Bosses: x in [0, 6], centered at (y=0, z=0) and (y=0, z=40)
# Note: translate(3, ...) puts the center of a 6mm box at x=3, so range is [0, 6]
boss1 = cq.Workplane("XY").box(boss_thickness, boss_width, boss_height).translate((boss_thickness/2, 0, 0))
boss2 = cq.Workplane("XY").box(boss_thickness, boss_width, boss_height).translate((boss_thickness/2, 0, 40))

# Combine plate and bosses
p = base_plate.union(boss1).union(boss2)

# Create the screw holes through the combined plate (R3)
# Holes are at (y=0, z=0) and (y=0, z=40). 
# Since the bosses are centered on these points, the hole is centered in the x=[0,6] region.
p = p.faces("<X").workplane().pushPoints([(0, 0), (0, 40)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6)
# We build a robust arm that connects to the plate and provides the strap seat.
# To ensure R6 (strength), we make it thick near the wall.
arm_part = (
    cq.Workplane("XY")
    .box(50, 14, 20) # Main structural mass
    .translate((26, 0, -10)) # Positioned to extend from plate towards x=52
)

# 3. Create the Retaining Lip (R5)
# R5: solid material at 47 <= x <= 52, |y| <= 4, -13 <= z <= -8
lip_part = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# Combine Plate + Arm + Lip (R1)
combined = p.union(arm_part).union(lip_part)

# 4. Create the Strap Pocket (R4)
# R4: space (35 <= x <= 45, |y| <= 6, -13 <= z <= -6) must be empty.
# The strap bed top should be at z = -14.
# We create a pocket that leaves the bed at z=-14 and clears the specified volume.
pocket_vol = cq.Workplane("XY").box(10, 12, 7).translate((40, 0, -9.5))

# Subtract the pocket from the combined solid
result = combined.cut(pocket_vol)

# Verification of R4:
# Pocket center z = -9.5. Height = 7. 
# Z range = [-9.5 - 3.5, -9.5 + 3.5] = [-13, -6]. Matches requirement exactly.
# The material below the pocket (at z=-14) is preserved by the arm_part thickness.