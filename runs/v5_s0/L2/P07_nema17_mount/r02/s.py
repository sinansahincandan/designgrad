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
            "criteria": [{"condition": "One single, valid solid", "measured": int(n_solids), "ok": True if status == "pass" else False}],
            "note": f"Found {n_solids} solid(s)"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2 & R3: Face plate thickness and Central Bore
    try:
        bore_r_target = 11.25 # 22.5 / 2
        plate_thickness_min = 4.0
        
        # Define the probe region for the face plate (y=0 to y=4)
        # We use a cylinder centered at (0, 2, 30) with height 4 along Y axis
        # Note: pnt is the center of the cylinder in CQ if we define it carefully or use makeBox/makeCylinder correctly.
        # makeCylinder(r, h, pnt, dir): pnt is the center of the base.
        bore_cyl = cq.Solid.makeCylinder(bore_r_target, plate_thickness_min, pnt=cq.Vector(0, 0, 30), dir=cq.Vector(0, 1, 0))
        
        # R3: Verify the bore is empty AND that there is actually a plate present to have a hole in.
        material_in_bore = shape.intersect(bore_cyl).Volume()
        
        # To ensure R3 doesn't pass if no plate exists, we check if the part actually occupies 
        # the space where the face plate should be (e.g., at y=2, z=30).
        # We probe a small volume in the annulus to confirm material presence.
        ring_r_outer = 15.0
        annulus_probe = cq.Solid.makeCylinder(ring_r_outer, plate_thickness_min, pnt=cq.Vector(0, 0, 30), dir=cq.Vector(0, 1, 0))
        total_material_in_region = shape.intersect(annulus_probe).Volume()
        
        # R3: Bore is empty (material < small threshold) AND the region contains material (plate exists)
        r3_ok = (material_in_bore < 0.1) and (total_material_in_region > 1.0)
        
        # R2: Face plate thickness/integrity. 
        # We check if the volume of material in the annulus is close to the expected volume of a solid ring.
        expected_annulus_vol = (np.pi * (ring_r_outer**2 - bore_r_target**2)) * plate_thickness_min
        actual_annulus_mat_vol = total_material_in_region - material_in_bore
        r2_ok = (actual_annulus_mat_vol / expected_annulus_vol > 0.95)

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": float(actual_annulus_mat_vol),
            "method": "Checked annulus volume around bore in y=[0,4] region to ensure plate thickness/integrity",
            "criteria": [{"condition": "Face plate at least 4 mm thick with solid material all around the central bore", "measured": float(actual_annulus_mat_vol), "ok": True if r2_ok else False}],
            "note": f"Annulus Mat: {actual_annulus_mat_vol:.2f}"
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": float(material_in_bore),
            "method": "Measured material volume within the 22.5mm bore cylinder through y=[0,4] and verified plate presence",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": float(material_in_bore), "ok": True if r3_ok else False}],
            "note": f"Bore material: {material_in_bore:.4f}"
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
            best_r = 0.0
            # Search for radius where intersection volume becomes significant
            for r_test in np.linspace(0.1, 5.0, 40):
                h_cyl = cq.Solid.makeCylinder(r_test, 4, pnt=cq.Vector(hx, 0, hz), dir=cq.Vector(0, 1, 0))
                if shape.intersect(h_cyl).Volume() < 0.05: # Very little material in the cylinder means it's a hole
                    best_r = r_test
                else:
                    break
            
            diam = best_r * 2
            measured_diameters.append(diam)
            
            # Verify the hole is actually in the plate (material exists around it)
            h_check_vol = shape.intersect(cq.Solid.makeCylinder(5.0, 4, pnt=cq.Vector(hx, 0, hz), dir=cq.Vector(0, 1, 0))).Volume()
            if h_check_vol < 1.0: # If the cylinder is mostly empty, it's not a hole in a plate, it's just air
                all_holes_present = False

        avg_diam = sum(measured_diameters) / len(measured_diameters) if measured_diameters else 0
        r4_ok = all_holes_present and (abs(avg_diam - 3.4) < 0.7)

        results["R4"] = {
            "status": "pass" if r4_ok else "fail",
            "value": float(avg_diam),
            "method": f"Measured diameters of 4 holes at (+-15.5, 30 +- 15.5) via void cylinder probing",
            "criteria": [{"condition": "Four motor screw holes, diameter 3.4 mm", "measured": float(avg_diam), "ok": True if r4_ok else False}],
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
            "criteria": [{"condition": "Motor clearance: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5", "measured": float(intersect_vol), "ok": True if r5_ok else False}],
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
        # Check if base exists at z=0
        base_slice = cq.Solid.makeBox(100, 100, 2, pnt=cq.Vector(-50, -50, 0))
        if shape.intersect(base_slice).Volume() < 1.0:
            holes_ok = False

        measured_hole_diams = []
        for sx in [-25, 25]:
            # Probe for the diameter of the screw hole at (sx, 25)
            best_r = 0.0
            for r_test in np.linspace(0.1, 4.0, 30):
                h_base_cyl = cq.Solid.makeCylinder(r_test, 10, pnt=cq.Vector(sx, 25, 0), dir=cq.Vector(0, 0, 1))
                if shape.intersect(h_base_cyl).Volume() < 0.1:
                    best_r = r_test
                else:
                    break
            measured_hole_diams.append(best_r * 2)
        
        avg_hole_diam = sum(measured_hole_diams) / len(measured_hole_diams) if measured_hole_diams else 0
        r6_holes_ok = (abs(avg_hole_diam - 5.5) < 1.0) and holes_ok
        r6_ok = r6_z_ok and r6_holes_ok

        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": [float(z_min), float(avg_hole_diam)],
            "method": f"Checked z_min >= 0 and measured screw hole diameters at (+-25, 25)",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": float(z_min), "ok": True if r6_z_ok else False},
                {"condition": "Two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25)", "measured": float(avg_hole_diam), "ok": True if r6_holes_ok else False}
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
        mass_ok = mass_g <= 60 + 0.1
        r7_ok = x_ok and z_ok and mass_ok
        results["R7"] = {
            "status": "pass" if r7_ok else "fail",
            "value": [float(b.xmin), float(b.xmax), float(b.zmax), float(mass_g)],
            "method": f"Checked BBox x[-35, 35], z_max <= 55 and mass = volume * {density_pla} g/mm^3",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": [float(b.xmin), float(b.xmax)], "ok": True if x_ok else False},
                {"condition": "top <= 55 mm", "measured": float(b.zmax), "ok": True if z_ok else False},
                {"condition": "mass <= 60 g", "measured": float(mass_g), "ok": True if mass_ok else False}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()