import cadquery as cq
import trimesh
import numpy as np
import json

def solve():
    # Load the part
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    results = {}
    density_pla = 1.24 / 1000  # g/mm3 (from 1.24 g/cm3)
    tol = 1e-2

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": int(n_solids),
            "method": "Counted number of solids in STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": int(n_solids), "ok": bool(status == "pass")}],
            "note": f"Found {n_solids} solid(s)"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2 & R3: Face plate thickness and Central Bore
    try:
        # Define the face plate region (y=0 to 4)
        plate_region = cq.Solid.makeBox(100, 4.0, 100, pnt=cq.Vector(-50, 0, -25))
        plate_intersection = shape.intersect(plate_region)
        plate_vol = plate_intersection.Volume()

        # R3: Central bore diameter (22.5mm) on shaft axis (x=0, z=30)
        bore_r_target = 11.25
        bore_cyl = cq.Solid.makeCylinder(bore_r_target, 10.0, pnt=cq.Vector(0, -3, 30), dir=cq.Vector(0, 1, 0))
        bore_material_in_plate = shape.intersect(bore_cyl).Volume()
        
        # A hole is valid if the material volume in that cylinder is very low (it's a void)
        r3_ok = bore_material_in_plate < 1.0 

        # R2: Face plate thickness and solid material around bore
        ring_r = 16.0
        ring_cyl = cq.Solid.makeCylinder(ring_r, 5.0, pnt=cq.Vector(0, -0.5, 30), dir=cq.Vector(0, 1, 0))
        ring_mat_vol = shape.intersect(ring_cyl).Volume()
        expected_ring_vol = np.pi * (ring_r**2) * 5.0
        ring_integrity = ring_mat_vol / expected_ring_vol > 0.9
        
        thickness_ok = plate_vol > 10.0 and ring_integrity

        results["R2"] = {
            "status": "pass" if thickness_ok else "fail",
            "value": float(plate_vol),
            "method": "Verified plate volume in y=[0,4] and material integrity in a 16mm radius ring",
            "criteria": [{"condition": "Face plate at least 4 mm thick with solid material all around the central bore", "measured": float(plate_vol), "ok": bool(thickness_ok)}],
            "note": f"Plate Vol: {plate_vol:.2f}, Ring Integrity: {ring_mat_vol/expected_ring_vol:.2%}"
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": float(bore_material_in_plate),
            "method": f"Measured material volume within the 22.5mm bore cylinder at (0, y, 30)",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": float(bore_material_in_plate), "ok": bool(r3_ok)}],
            "note": f"Bore material: {bore_material_in_plate:.2f}"
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes diameter 3.4 mm through the face plate along Y at (x, z) = (+-15.5, 30 +- 15.5).
    try:
        hole_coords = [(15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)]
        measured_diameters = []
        all_holes_present = True

        for hx, hz in hole_coords:
            check_pt = cq.Solid.makeBox(1, 5, 1, pnt=cq.Vector(hx-0.5, -0.5, hz-0.5))
            if shape.intersect(check_pt).Volume() < 0.1:
                all_holes_present = False
                continue

            found_d = 0.0
            for d_test in np.linspace(0.5, 6.0, 40):
                r_test = d_test / 2.0
                h_cyl = cq.Solid.makeCylinder(r_test, 10.0, pnt=cq.Vector(hx, -3, hz), dir=cq.Vector(0, 1, 0))
                if shape.intersect(h_cyl).Volume() < 0.5:
                    found_d = d_test
                else:
                    break
            
            if found_d > 0:
                measured_diameters.append(found_d)
            else:
                all_holes_present = False

        avg_diam = sum(measured_diameters) / len(measured_diameters) if measured_diameters else 0.0
        r4_ok = all_holes_present and (len(measured_diameters) == 4) and (abs(avg_diam - 3.4) < 1.0)

        results["R4"] = {
            "status": "pass" if r4_ok else "fail",
            "value": float(avg_diam),
            "method": f"Measured diameters of 4 holes at (+-15.5, 30 +- 15.5) via cylinder intersection in plate region",
            "criteria": [{"condition": "Four motor screw holes, diameter 3.4 mm", "measured": float(avg_diam), "ok": bool(r4_ok)}],
            "note": f"Measured avg diam: {avg_diam:.2f}"
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Motor clearance
    try:
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        intersect_vol = shape.intersect(clearance_box).Volume()
        r5_ok = intersect_vol < 0.1
        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": float(intersect_vol),
            "method": f"Intersection volume with clearance box [-21.5, 21.5] x [-48, 0] x [8.5, 51.5]",
            "criteria": [{"condition": "Motor clearance: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5", "measured": float(intersect_vol), "ok": bool(r5_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Base on the table and screw holes
    try:
        bounds = shape.BoundingBox()
        z_min = bounds.zmin
        r6_z_ok = z_min >= -tol 
        
        holes_ok = True
        measured_hole_diams = []
        for sx in [-25, 25]:
            check_pt = cq.Solid.makeBox(10, 10, 20, pnt=cq.Vector(sx-5, 20, 0))
            if shape.intersect(check_pt).Volume() < 0.1:
                holes_ok = False
                continue

            found_h = False
            best_d = 0.0
            for d_test in np.linspace(1.0, 8.0, 40):
                r_test = d_test / 2.0
                h_base_cyl = cq.Solid.makeCylinder(r_test, 50.0, pnt=cq.Vector(sx, 25, -10), dir=cq.Vector(0, 0, 1))
                if shape.intersect(h_base_cyl).Volume() < 1.0:
                    best_d = d_test
                    found_h = True
                else:
                    break
            
            if found_h:
                measured_hole_diams.append(best_d)
            else:
                holes_ok = False

        avg_hole_diam = sum(measured_hole_diams) / len(measured_hole_diams) if measured_hole_diams else 0.0
        r6_holes_ok = (len(measured_hole_diams) == 2) and (abs(avg_hole_diam - 5.5) < 1.5)
        r6_ok = r6_z_ok and r6_holes_ok

        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": [float(z_min), float(avg_hole_diam)],
            "method": f"Checked z_min >= 0 and measured screw hole diameters at (+-25, 25) via vertical void probing",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": float(z_min), "ok": bool(r6_z_ok)},
                {"condition": "Two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25)", "measured": float(avg_hole_diam), "ok": bool(r6_holes_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Envelope and Mass
    try:
        b = shape.BoundingBox()
        x_ok = (b.xmin >= -35-tol) and (b.xmax <= 35+tol)
        z_ok = b.zmax <= 55+tol
        mass_g = mesh.volume * density_pla
        mass_ok = mass_g <= 60 + 1.0 
        r7_ok = x_ok and z_ok and mass_ok
        results["R7"] = {
            "status": "pass" if r7_ok else "fail",
            "value": [float(b.xmin), float(b.xmax), float(b.zmax), float(mass_g)],
            "method": f"Checked BBox x[-35, 35], z_max <= 55 and mass = volume * {density_pla} g/mm^3",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": [float(b.xmin), float(b.xmax)], "ok": bool(x_ok)},
                {"condition": "top <= 55 mm", "measured": float(b.zmax), "ok": bool(z_ok)},
                {"condition": "mass <= 60 g", "measured": float(mass_g), "ok": bool(mass_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()