import cadquery as cq
import math

# Constants
ANGLE = 30.0
RAD = math.radians(ANGLE)
BASE_W = 45.0
BASE_D = 40.0
BASE_H = 5.0
FACE_CENTER_Z = 42.5
SENSOR_HOLE_DIA = 3.2
BASE_HOLE_DIA = 4.5

# Normal vector n = (0, cos(30), sin(30))
NORMAL = cq.Vector(0, math.cos(RAD), math.sin(RAD))

# 1. Create Base (R2: bottom at z=0)
base = cq.Workplane("XY").box(BASE_W, BASE_D, BASE_H).translate((0, 0, BASE_H/2))

# 2. Create Pillar using a wedge approach to satisfy R3 and avoid .rotate() errors
pillar_width = 45.0
y_face_center = 15.0 

# The line is: z - FACE_CENTER_Z = -cot(RAD) * (y - y_face_center)
slope = -(math.cos(RAD) / math.sin(RAD))

# Define the face segment in YZ plane
half_len = 25.0 # Increased to ensure area >= 900
y1 = y_face_center - half_len * math.sin(RAD)
z1 = FACE_CENTER_Z + slope * (y1 - y_face_center)
y2 = y_face_center + half_len * math.sin(RAD)
z2 = FACE_CENTER_Z + slope * (y2 - y_face_center)

# Create a profile in YZ plane that forms the pillar body
profile_yz = [
    (y1, 0),
    (y2, 0),
    (y2, z2),
    (y1, z1),
]

pillar = (
    cq.Workplane("YZ")
    .polyline(profile_yz)
    .close()
    .extrude(pillar_width)
)

# Center the extrusion on X=0
pillar = pillar.translate((-pillar_width/2, 0, 0))

# Calculate current midpoint of the face segment in our local coordinate system
mid_y = (y1 + y2) / 2
mid_z = (z1 + z2) / 2

# Translate so that the face center is at (0, y_face_center, FACE_CENTER_Z)
pillar = pillar.translate((0, y_face_center - mid_y, FACE_CENTER_Z - mid_z))

# R1: Union base and pillar
result = base.union(pillar)

# R2: Base screw holes (vertical)
result = result.faces("<Z").workplane().pushPoints([(20, -10), (-20, -10)]).hole(BASE_HOLE_DIA)

# R3 & R5: Sensor holes perpendicular to the mounting face
target_normal = cq.Vector(0, math.cos(RAD), math.sin(RAD))

# To avoid 'normal' keyword error in workplane(), we use a plane defined by its center and normal.
# We create a cylinder that represents the hole and cut it from the result.
# The drilling axis follows -target_normal (R5).
# Hole positions: +- 10mm along X from face center (0, y_face_center, FACE_CENTER_Z)

hole_pos1 = cq.Vector(10, y_face_center, FACE_CENTER_Z)
hole_pos2 = cq.Vector(-10, y_face_center, FACE_CENTER_Z)

# We need to find the intersection of the line (pos + t*normal) with the solid.
# A safe way is to create a very long cylinder at each position and cut it.
# Since we can't easily rotate cylinders in CQ without complex math, 
# we use the fact that the holes are perpendicular to the face.

# Create a drill bit for hole 1
drill1 = cq.Workplane("XY").cylinder(100, SENSOR_HOLE_DIA/2).translate((0,0,0))
# We need to rotate this cylinder so its axis is target_normal.
# The easiest way to create a tilted cylinder in CQ is to define it on a plane.

def create_tilted_cylinder(center_vec, normal_vec, length, radius):
    # Create a workplane at the center point with the specified normal orientation
    # We use the 'offset' and 'origin' logic by creating a plane from vectors.
    # However, CQ Workplane doesn't take 'normal'. 
    # Instead, we can build it on an axis.
    
    # Create a cylinder along Z, then rotate it to align with normal_vec.
    # We use the rotation matrix approach or simply create it in a plane.
    # Let's define the cylinder using a polyline profile and extrude.
    
    # 1. Define local axes for the tilted plane
    # Z_local = normal_vec
    z_loc = normal_vec.normalized()
    # X_local = any vector perpendicular to z_loc (e.g., if z is not X, use X)
    if abs(z_loc.x) < 0.9:
        x_loc = z_loc.cross(cq.Vector(1, 0, 0)).normalized()
    else:
        x_loc = z_loc.cross(cq.Vector(0, 1, 0)).normalized()
    y_loc = z_loc.cross(x_loc).normalized()
    
    # Now we can define points in this local coordinate system and transform them.
    # But a simpler way: create the cylinder on XY and rotate it.
    # To rotate (0,0,1) to target_normal:
    axis = cq.Vector(0, 0, 1)
    rotation_axis = axis.cross(z_loc).normalized()
    angle = math.acos(axis.dot(z_loc))
    
    # We use a helper function or just build the cylinder via extrusion of a circle on a plane.
    # Let's create a circle in a plane that is perpendicular to the normal.
    return (cq.Workplane("XY")
            .circle(radius)
            .extrude(length, both=True)
            .translate((center_vec.x, center_vec.y, center_vec.z))
            # This doesn't work because extrude is along Z. 
            # We must rotate the whole object.
           )

# Let's use a different approach: Create the holes as cylinders in their own local planes.
# A cylinder on a plane with normal N can be made by creating a circle and extruding.
# To get the correct orientation, we define the workplane using two vectors (u, v).

def create_hole(center_vec, normal_vec, radius, length):
    z_loc = normal_vec.normalized()
    if abs(z_loc.x) < 0.9:
        x_loc = z_loc.cross(cq.Vector(1, 0, 0)).normalized()
    else:
        x_loc = z_loc.cross(cq.Vector(0, 1, 0)).normalized()
    y_loc = z_loc.cross(x_loc).normalized()
    
    # Create a cylinder along the Z axis in its own local space
    # Then we need to transform it to global space.
    # In CQ, we can use .transformed() if available, but let's stick to basics.
    # We will create a large box and cut it.
    
    # Actually, the most robust way: 
    # Create a cylinder at origin along Z, rotate it, then translate it.
    cyl = cq.Workplane("XY").cylinder(length, radius)
    
    # Rotation to align (0,0,1) with normal_vec
    rot_axis = cq.Vector(0, 0, 1).cross(z_loc)
    if rot_axis.length > 1e-6:
        angle = math.acos(cq.Vector(0, 0, 1).dot(z_loc))
        cyl = cyl.rotate(rot_axis, math.degrees(angle))
    
    return cyl.translate((center_vec.x, center_vec.y, center_vec.z))

# Create the two holes
hole1 = create_hole(hole_pos1, target_normal, SENSOR_HOLE_DIA/2, 100)
hole2 = create_hole(hole_pos2, target_normal, SENSOR_HOLE_DIA/2, 100)

# Subtract the holes from the result
result = result.cut(hole1).cut(hole2)

# Final check: ensure it is a single solid assigned to result
result = result