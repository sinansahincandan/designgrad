import cadquery as cq

# Parameters
plate_thickness = 2.0
plate_width = 16.0  # y direction (from -8 to 8)
plate_height = 50.0 # z direction (from -5 to 45)
screw_hole_dia = 4.5

boss_diameter = 12.5
boss_height = 12.5
# Bosses extend from x=0 to x=12.5. Center of boss in X is 6.25.
boss_x_center = boss_height / 2

arm_width = 18.0    # y direction
arm_height = 13.0   # z direction (increased for R6)
arm_length = 46.0   # x direction (starts at x=6, ends at x=52)
# To ensure the arm cross-section at x=8 is 18x13:
# The arm starts at x=6 and goes to x=52.
arm_z_center = -14.0 + (arm_height / 2) # Top surface at z=-14

# R4: Strap pocket requirements
# Pocket: 35 <= x <= 45, |y| <= 6, -20 <= z <= -14
pocket_x_start = 35.0
pocket_x_end = 45.0
pocket_y_half = 6.0
pocket_z_bottom = -20.0
pocket_z_top = -14.0

# R5: Retaining lip requirements
# Lip: 47 <= x <= 52, |y| <= 4, -13 <= z <= -8
lip_x_start = 47.0
lip_x_end = 52.0
lip_y_half = 4.0
lip_z_bottom = -13.0
lip_z_top = -8.0

# 1. Create the Back Plate (R2)
plate = cq.Workplane("XY").box(plate_thickness, plate_width, plate_height).translate((plate_thickness/2, 0, 20))

# 2. Create Screw Bosses (R3)
boss1 = cq.Workplane("XY").cylinder(boss_height, boss_diameter).translate((boss_x_center, 0, 0))
boss2 = cq.Workplane("XY").cylinder(boss_height, boss_diameter).translate((boss_x_center, 0, 40))

# Combine plate and bosses
base_structure = plate.union(boss1).union(boss2)

# Drill screw holes through the bosses (R3)
# Holes at y=0, z=0 and y=0, z=40. Since they are centered on bosses, 
# we drill along X axis.
base_structure = base_structure.faces("<X").workplane().pushPoints([(0, 0), (0, 40)]).hole(screw_hole_dia)

# 3. Create the Support Arm (R6)
# The arm starts at x=6 to ensure it is well clear of the plate/bosses for R6 calculation
arm_part = cq.Workplane("XY").box(arm_length, arm_width, arm_height).translate((6 + arm_length/2, 0, arm_z_center))

# 4. Create the Retaining Lip (R5)
lip_part = cq.Workplane("XY").box(lip_x_end - lip_x_start, lip_y_half * 2, lip_z_top - lip_z_bottom).translate((lip_x_start + (lip_x_end-lip_x_start)/2, 0, (lip_z_top + lip_z_bottom)/2))

# 5. Combine all solid parts (R1)
combined = base_structure.union(arm_part).union(lip_part)

# 6. Subtract the Strap Pocket (R4)
# The pocket creates the recessed bed at z=-14 and ensures the void above it is empty.
pocket_vol = cq.Workplane("XY").box(pocket_x_end - pocket_x_start, pocket_y_half * 2, pocket_z_top - pocket_z_bottom).translate(((pocket_x_start + pocket_x_end)/2, 0, (pocket_z_top + pocket_z_bottom)/2))

# To satisfy the "empty space" requirement: 35 <= x <= 45, |y| <= 6, -13 <= z <= -6
# We subtract a second volume if necessary, but the design specifies the pocket is the void.
# The arm/body must not exist in that upper region. 
# Let's define the "empty space" void explicitly to ensure R4 compliance.
void_vol = cq.Workplane("XY").box(pocket_x_end - pocket_x_start, pocket_y_half * 2, -6 - (-13)).translate(((pocket_x_start + pocket_x_end)/2, 0, (-6 + -13)/2))

result = combined.cut(pocket_vol).cut(void_vol)