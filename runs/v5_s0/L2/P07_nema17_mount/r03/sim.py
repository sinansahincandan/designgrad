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
        bore_r = 11.25
        plate_thickness = 4.0
        # Define the region of interest for the face plate (y=0 to y=4)
        # We use a cylinder probe that spans exactly through this thickness
        bore_probe = cq.Solid.makeCylinder(bore_r, plate_thickness, pnt=cq.Vector(0, 0, 30), dir=cq.Vector(0, 1, 0))
        
        # R3: Verify the bore exists by checking if material volume in that cylinder is near zero
        material_in_bore = shape.intersect(bore_probe).Volume()
        r3_ok = material_in_bore < 0.5 # Allow small tolerance for mesh artifacts

        # R2: Verify face plate thickness and solid material around the bore.
        # We check an annulus in the y=[0,4] region.
        ring_r_outer = 15.0
        annulus_probe = cq.Solid.makeCylinder(ring_r_outer, plate_thickness, pnt=cq.Vector(0, 0, 30), dir=cq.Vector(0, 1, 0))
        # Material in annulus is (Intersection with outer) - (Intersection with inner)
        # But since we already know the bore is empty, intersection with annulus_probe should be the material.
        annulus_mat_vol = shape.intersect(annulus_probe).Volume()
        
        expected_annulus_vol = (np.pi * (ring_r_outer**2 - bore_r**2)) * plate_thickness
        # Check if annulus is mostly full AND the material exists in the y=0..4 range
        r2_ok = (annulus_mat_vol / expected_annulus_vol > 0.9) and (annulus_mat_vol > 10.0)

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": float(annulus_mat_vol),
            "method": "Checked annulus volume in y=[0,4] to ensure plate existence and thickness",
            "criteria": [{"condition": "Face plate at least 4 mm thick with solid material all around the central bore", "measured": float(annulus_mat_vol), "ok": True if r2_ok else False}],
            "note": f"Annulus Mat: {annulus_mat_vol:.2f}"
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": float(material_in_bore),
            "method": "Measured material volume within the 22.5mm bore cylinder through y=[0,4]",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": float(material_in_bore), "ok": True if r3_ok else False}],
            "note": ""
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
            # We probe along Y (the axis of the holes)
            for r_test in np.linspace(0.1, 5.0, 40):
                h_cyl = cq.Solid.makeCylinder(r_test, 10.0, pnt=cq.Vector(hx, -3, hz), dir=cq.Vector(0, 1, 0))
                if shape.intersect(h_cyl).Volume() < 0.05: 
                    best_r = r_test
                else:
                    break
            
            diam = best_r * 2
            measured_diameters.append(diam)
            
            # Verify the hole is actually in a plate (material exists around it at y=0..4)
            h_check_vol = shape.intersect(cq.Solid.makeCylinder(5.0, 10.0, pnt=cq.Vector(hx, -3, hz), dir=cq.Vector(0, 1, 0))).Volume()
            if h_check_vol < 1.0: 
                all_holes_present = False

        avg_diam = sum(measured_diameters) / len(measured_diameters) if measured_diameters else 0
        r4_ok = all_holes_present and (abs(avg_diam - 3.4) < 0.7)

        results["R4"] = {
            "status": "pass" if r4_ok else "fail",
            "value": float(avg_diam),
            "method": f"Measured diameters of 4 holes at (+-15.5, 30 +- 15.5) via void cylinder probing along Y",
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
        # Check if base exists at z=0 (material must be present in a thin slice at z=0)
        base_slice = cq.Solid.makeBox(100, 100, 1.0, pnt=cq.Vector(-50, -50, 0))
        if shape.intersect(base_slice).Volume() < 1.0:
            holes_ok = False

        measured_hole_diams = []
        for sx in [-25, 25]:
            best_r = 0.0
            # Robust diameter measurement using cross-sectioning or volumetric probing
            # We probe a cylinder along Z at (sx, 25). To avoid sensitivity to exact Z, we use a long cylinder.
            for r_test in np.linspace(0.1, 4.0, 40):
                h_base_cyl = cq.Solid.makeCylinder(r_test, 20.0, pnt=cq.Vector(sx, 25, -5), dir=cq.Vector(0, 0, 1))
                if shape.intersect(h_base_cyl).Volume() < 0.1:
                    best_r = r_test
                else:
                    break
            measured_hole_diams.append(best_r * 2)
        
        avg_hole_diam = sum(measured_hole_diams) / len(measured_hole_diams) if measured_hole_diams else 0
        # Requirement: diameter 5.5 mm
        r6_holes_ok = (abs(avg_hole_diam - 5.5) < 1.2) and holes_ok
        r6_ok = r6_z_ok and r6_holes_ok

        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": [float(z_min), float(avg_hole_diam)],
            "method": f"Checked z_min >= 0 and measured screw hole diameters at (+-25, 25) via Z-axis probing",
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