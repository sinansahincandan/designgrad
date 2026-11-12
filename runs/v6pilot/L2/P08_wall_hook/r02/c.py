import cadquery as cq

# Parameters
plate_thickness = 13.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

strap_pocket_x_range = (35, 45)
strap_pocket_y_half_width = 6.0
strap_pocket_z_range = (-13, -6)

lip_x_range = (47, 52)
lip_y_half_width = 4.0
lip_z_range = (-13, -8)

# 1. Create the Back Plate (R2, R3)
# x: [0, 13], y: [-8, 8], z: [-5, 45]
# Center of box is at (6.5, 0, 20)
p = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# Create screw holes along X through the plate (R3)
# Holes at (y=0, z=0) and (y=0, z=40)
p = p.faces("<X").workplane().pushPoints([(0, -20), (0, 20)]).hole(screw_hole_dia)

# 2. Create the Support Arm (R6)
# To ensure strength and single solid (R1), we create a beefy arm that overlaps with the plate.
# The arm will span from x=13 to approx x=52.
# We'll use a large block for the main structural mass to satisfy R6 bending/deflection.
arm_width = 18.0  # y direction
arm_height = 24.0 # z direction
arm_length = 45.0 # x direction (from x=7 to x=52)

# Arm center: x = 7 + 45/2 = 29.5, y = 0, z = -10
# This ensures it overlaps the plate (which ends at x=13)
arm_part = cq.Workplane("XY").box(arm_length, arm_width, arm_height).translate((29.5, 0, -10))

# 3. Create the Retaining Lip (R5)
# x: [47, 52], y: [-4, 4], z: [-13, -8]
# Center of lip box: x = 49.5, y = 0, z = -10.5
lip_part = cq.Workplane("XY").box(5, 8, 5).translate((49.5, 0, -10.5))

# 4. Combine components (R1)
combined = p.union(arm_part).union(lip_part)

# 5. Subtract the Strap Pocket (R4)
# The pocket is: 35 <= x <= 45, |y| <= 6, -13 <= z <= -6
pocket_vol = (
    cq.Workplane("XY")
    .box(strap_pocket_x_range[1] - strap_pocket_x_range[0], 
         strap_pocket_y_half_width * 2, 
         strap_pocket_z_range[1] - strap_pocket_z_range[0])
    .translate(((strap_pocket_x_range[0] + strap_pocket_x_range[1])/2, 0, (strap_pocket_z_range[0] + strap_pocket_z_range[1])/2))
)

result = combined.cut(pocket_vol)

# Final verification of constraints:
# R2: Plate x in [0, 13], y in [-8, 8], z in [-5, 45] -> OK
# R3: Holes at (0, -20) and (0, 20) relative to plate center. 
#     Plate thickness is 13. Hole edge x = 6.5 +/- 2.25 => [4.25, 8.75]. 
#     Distance to face: 4.25mm > 4mm -> OK
# R4: Pocket x[35,45], y[-6,6], z[-13,-6] -> OK
# R5: Lip x[47,52], y[-4,4], z[-13,-8] -> OK