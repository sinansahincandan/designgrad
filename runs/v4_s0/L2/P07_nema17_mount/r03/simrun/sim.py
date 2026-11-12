import cadquery as cq
import trimesh
import numpy as np
import json

# Load the part
try:
    shape = cq.importers.importStep('part.step').val()
    mesh = trimesh.load('part.stl')
except Exception as e:
    print(f"Critical error loading files: {e}")
    exit(1)

# Constants from spec
DENSITY_PLA = 1.24 / 1000  # g/mm3 (converted from 1.24 g/cm3)

results = {}

# R1: One single, valid solid
try:
    n_solids = len(shape.Solids())
    status = "pass" if n_solids == 1 else "fail"
    results["R1"] = {
        "status": status,
        "value": n_solids,
        "method": f"Counted solids in STEP file: {n_solids}",
        "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": status == "pass"}],
        "note": ""
    }
except Exception as e:
    results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

# R2 & R3: Face plate thickness and Central Bore
try:
    # R3: Central bore diameter 22.5 mm (r=11.25) through the face plate at x=0, z=30.
    # The bore is a void in the part. We check if material exists inside this cylinder.
    bore_cyl = cq.Solid.makeCylinder(11.25, 100, pnt=cq.Vector(0, -50, 30), dir=cq.Vector(0, 1, 0))
    bore_material_vol = shape.intersect(bore_cyl).Volume()
    # If the bore is correct, the volume of material inside this cylinder should be near zero.
    r3_ok = bore_material_vol < 5.0 

    # R2: Face plate at least 4 mm thick (y=0 to 4) with solid material all around the central bore.
    # We check thickness by probing several points in the face plate region (y=0 to 4).
    # To ensure "all around the bore", we probe a ring of points outside the bore radius.
    thickness_ok = True
    test_radii = [15.0, 20.0] # Points clearly outside the 11.25mm bore but within typical plate width
    for r in test_radii:
        for angle in [0, np.pi/2, np.pi, 3*np.pi/2]:
            px = r * np.cos(angle)
            pz = 30 + r * np.sin(angle)
            # Probe a small box at the face plate thickness (y=0 to 4)
            # A 1x4x1 probe should have volume ~4 if material is present
            probe = cq.Solid.makeBox(1, 4, 1, pnt=cq.Vector(px-0.5, 0, pz-0.5))
            if shape.intersect(probe).Volume() < (probe.Volume() * 0.8):
                thickness_ok = False
                break
        if not thickness_ok: break

    # Also check the plate itself is at least 4mm thick by checking if material exists in y=[0,4] 
    # across a representative area (excluding the bore).
    # We'll use a probe that covers the face plate region.
    plate_probe = cq.Solid.makeBox(50, 4, 50, pnt=cq.Vector(-25, 0, 5))
    # Subtracting the bore volume from this probe to check "material around"
    bore_in_plate = shape.intersect(bore_cyl).Volume() # This is actually material in the bore (should be ~0)
    # We want to ensure that if we look at the region y=[0,4], there's plenty of material.
    # A better way: check thickness at a specific point like x=25, z=30.
    thickness_probe = cq.Solid.makeBox(1, 4, 1, pnt=cq.Vector(24.5, 0, 29.5))
    thick_vol = shape.intersect(thickness_probe).Volume()
    r2_thickness_ok = thick_vol > (thickness_probe.Volume() * 0.9)

    r2_ok = r2_thickness_ok and thickness_ok

    results["R2"] = {
        "status": "pass" if r2_ok else "fail",
        "value": thick_vol,
        "method": f"Thickness probe vol (1x4x1): {thick_vol} mm3; Continuity check around bore: {thickness_ok}",
        "criteria": [{"condition": "Face plate at least 4 mm thick with solid material all around the central bore", "measured": r2_ok, "ok": r2_ok}],
        "note": ""
    }
    results["R3"] = {
        "status": "pass" if r3_ok else "fail",
        "value": bore_material_vol,
        "method": f"Material volume inside cylinder (r=11.25) at x=0, z=30: {bore_material_vol} mm3",
        "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate, on the shaft axis", "measured": bore_material_vol, "ok": r3_ok}],
        "note": ""
    }
except Exception as e:
    results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
    results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

# R4: Four motor screw holes (3.4mm) at (+-15.5, 30 +- 15.5)
try:
    holes_ok = True
    hole_coords = [(15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)]
    for hx, hz in hole_coords:
        h_cyl = cq.Solid.makeCylinder(1.7, 20, pnt=cq.Vector(hx, -5, hz), dir=cq.Vector(0, 1, 0))
        h_mat = shape.intersect(h_cyl).Volume()
        if h_mat > (h_cyl.Volume() * 0.15): 
            holes_ok = False
    
    status = "pass" if holes_ok else "fail"
    results["R4"] = {
        "status": status,
        "value": holes_ok,
        "method": f"Probed 4 cylinders (r=1.7) at (+-15.5, 30 +- 15.5)",
        "criteria": [{"condition": "Four motor screw holes, diameter 3.4 mm", "measured": holes_ok, "ok": holes_ok}],
        "note": ""
    }
except Exception as e:
    results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

# R5: Motor clearance (-21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5)
try:
    clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
    interference_vol = shape.intersect(clearance_box).Volume()
    r5_ok = interference_vol < 0.5 
    
    status = "pass" if r5_ok else "fail"
    results["R5"] = {
        "status": status,
        "value": interference_vol,
        "method": f"Intersection volume with clearance box: {interference_vol}",
        "criteria": [{"condition": "Motor clearance: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5", "measured": interference_vol, "ok": r5_ok}],
        "note": ""
    }
except Exception as e:
    results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

# R6: Base on table (z>=0) and two vertical screw holes (5.5mm) at (+-25, 25)
try:
    bbox = shape.BoundingBox()
    z_min = bbox.zmin
    r6_base_ok = z_min >= -0.1
    
    holes_ok = True
    hole_coords = [(25, 25), (-25, 25)]
    for hx, hy in hole_coords:
        h_cyl = cq.Solid.makeCylinder(2.75, 60, pnt=cq.Vector(hx, hy, -5), dir=cq.Vector(0, 0, 1))
        h_mat = shape.intersect(h_cyl).Volume()
        if h_mat > (h_cyl.Volume() * 0.3):
             holes_ok = False

    status = "pass" if (r6_base_ok and holes_ok) else "fail"
    results["R6"] = {
        "status": status,
        "value": [z_min, holes_ok],
        "method": f"Checked z_min={z_min} and probed 5.5mm diameter cylinders at (+-25, 25)",
        "criteria": [
            {"condition": "Base on the table (minimum z = 0)", "measured": z_min, "ok": r6_base_ok},
            {"condition": "Two vertical screw holes, diameter 5.5 mm", "measured": holes_ok, "ok": holes_ok}
        ],
        "note": ""
    }
except Exception as e:
    results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

# R7: Envelope and Mass
try:
    bbox = shape.BoundingBox()
    x_min, x_max = bbox.xmin, bbox.xmax
    z_max = bbox.zmax
    vol_mm3 = shape.Volume()
    mass_g = vol_mm3 * DENSITY_PLA
    
    r7_env_x = (-35 <= x_min) and (x_max <= 35)
    r7_env_z = z_max <= 55
    r7_mass = mass_g <= 60
    
    status = "pass" if (r7_env_x and r7_env_z and r7_mass) else "fail"
    results["R7"] = {
        "status": status,
        "value": [x_min, x_max, z_max, mass_g],
        "method": f"BBox: x[{x_min}, {x_max}], z_max={z_max}; Mass: {mass_g}g (vol={vol_mm3}mm3, rho=1.24)",
        "criteria": [
            {"condition": "-35 <= x <= 35", "measured": [x_min, x_max], "ok": r7_env_x},
            {"condition": "top <= 55 mm", "measured": z_max, "ok": r7_env_z},
            {"condition": "mass <= 60 g", "measured": mass_g, "ok": r7_mass}
        ],
        "note": ""
    }
except Exception as e:
    results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

print(json.dumps(results))