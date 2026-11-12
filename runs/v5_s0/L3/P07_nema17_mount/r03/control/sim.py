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
        plate_y_min = 0.0
        plate_y_max = 4.0
        
        # R2 Check: Face plate thickness and integrity
        # We define the face plate region as a slab y=[0, 4]
        plate_probe = cq.Solid.makeBox(100, plate_y_max - plate_y_min, 100, pnt=cq.Vector(-50, plate_y_min, -50))
        actual_plate_material = shape.intersect(plate_probe)
        plate_vol = actual_plate_material.Volume()

        # To ensure "solid material all around the central bore", 
        # we check if a ring (annulus) at radius 15mm in the plate region is filled.
        annulus_r = 15.0
        annulus_thickness = 2.0
        annulus_probe = cq.Solid.makeCylinder(annulus_r, plate_y_max - plate_y_min, pnt=cq.Vector(0, plate_y_min, 30), dir=cq.Vector(0, 1, 0))
        # We need to check the volume of the annulus specifically.
        # A more robust way: Check if a small probe at radius 15 is solid.
        integrity_ok = True
        for angle in [0, 90, 180, 270]:
            rad = np.radians(angle)
            px, pz = annulus_r * np.cos(rad), 30 + annulus_r * np.sin(rad)
            # Probe a small cylinder at the edge of the plate
            probe = cq.Solid.makeCylinder(1.0, 5.0, pnt=cq.Vector(px, 2.0, pz), dir=cq.Vector(0, 1, 0))
            if shape.intersect(probe).Volume() < 0.5:
                integrity_ok = False
                break

        # R3 Check: Central bore diameter 22.5 mm through the face plate
        # Instead of just checking if volume is low (which fails on a tiny cube),
        # we verify that the cylinder defined by the bore radius is actually empty,
        # AND that there is material at the edges of the plate to prove it's a hole in a plate.
        bore_probe = cq.Solid.makeCylinder(bore_r + 0.1, 6.0, pnt=cq.Vector(0, -1, 30), dir=cq.Vector(0, 1, 0))
        bore_in_plate_vol = shape.intersect(bore_probe).Volume()
        
        # A real bore must be empty (low volume) AND the plate must exist around it.
        # We check if the intersection of the part with a larger cylinder is significantly larger than the bore void.
        large_cyl_probe = cq.Solid.makeCylinder(20.0, 6.0, pnt=cq.Vector(0, -1, 30), dir=cq.Vector(0, 1, 0))
        total_plate_in_region = shape.intersect(large_cyl_probe).Volume()
        
        # R3 is valid if the bore volume is low AND there's actually a plate (total_plate_in_region > bore_vol)
        r3_ok = (bore_in_plate_vol < 0.5) and (total_plate_in_region > 1.0)
        r2_ok = integrity_ok and (plate_vol > 10.0)

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": float(plate_vol),
            "method": "Checked plate volume and material integrity at radius 15mm",
            "criteria": [{"condition": "Face plate >= 4mm thick with solid material around bore", "measured": float(r2_ok), "ok": r2_ok}],
            "note": f"Plate Vol: {plate_vol:.2f}, Integrity: {integrity_ok}"
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": float(bore_in_plate_vol),
            "method": "Checked bore volume at (0, 2, 30) and verified surrounding material exists",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": float(bore_in_plate_vol), "ok": r3_ok}],
            "note": f"Bore Vol: {bore_in_plate_vol:.4f}, Surrounding Mat: {total_plate_in_region:.2f}"
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes, diameter 3.4 mm through the face plate along Y at (x, z) = (+-15.5, 30 +- 15.5).
    try:
        hole_coords = [(15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)]
        measured_diameters = []
        holes_exist = True
        
        for hx, hz in hole_coords:
            found_r = 0.0
            # Probe with cylinders of increasing radius to find the void diameter
            for test_r in np.linspace(0.1, 5.0, 50):
                h_cyl = cq.Solid.makeCylinder(test_r, 10, pnt=cq.Vector(hx, -3, hz), dir=cq.Vector(0, 1, 0))
                bore_vol = shape.intersect(h_cyl).Volume()
                if bore_vol < 0.5: # Cylinder is mostly in the void
                    found_r = test_r
                else:
                    break
            
            # Verify material exists around the hole to avoid false positives from empty space
            h_check_vol = shape.intersect(cq.Solid.makeCylinder(10.0, 10, pnt=cq.Vector(hx, -3, hz), dir=cq.Vector(0, 1, 0))).Volume()
            if found_r > 0.5 and h_check_vol > 1.0:
                measured_diameters.append(found_r * 2)
            else:
                holes_exist = False

        avg_dia = sum(measured_diameters)/len(measured_diameters) if measured_diameters else 0.0
        r4_ok = holes_exist and (abs(avg_dia - 3.4) < 1.0)

        results["R4"] = {
            "status": "pass" if r4_ok else "fail",
            "value": float(avg_dia),
            "method": f"Measured diameters of 4 holes at (+-15.5, 30 +- 15.5) via void probing",
            "criteria": [{"condition": "Four motor screw holes, diameter 3.4 mm", "measured": float(avg_dia), "ok": True if r4_ok else False}],
            "note": ""
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
        
        base_surface_exists = False
        if r6_z_ok:
            probe_base = cq.Solid.makeBox(50, 50, 0.1, pnt=cq.Vector(-25, -25, 0))
            if shape.intersect(probe_base).Volume() > 0.1:
                base_surface_exists = True

        holes_ok = True
        measured_base_hole_diameters = []

        for sx in [-25, 25]:
            found_r = 0.0
            # Probe vertical holes at (sx, 25)
            for test_r in np.linspace(0.1, 6.0, 60):
                h_base_cyl = cq.Solid.makeCylinder(test_r, 20, pnt=cq.Vector(sx, 25, -5), dir=cq.Vector(0, 0, 1))
                bore_vol = shape.intersect(h_base_cyl).Volume()
                if bore_vol < 0.5:
                    found_r = test_r
                else:
                    break
            
            h_check_vol = shape.intersect(cq.Solid.makeCylinder(10.0, 20, pnt=cq.Vector(sx, 25, -5), dir=cq.Vector(0, 0, 1))).Volume()
            if found_r > 0.5 and h_check_vol > 1.0:
                measured_base_hole_diameters.append(found_r * 2)
            else:
                holes_ok = False

        avg_base_dia = sum(measured_base_hole_diameters)/len(measured_base_hole_diameters) if measured_base_hole_diameters else 0.0
        r6_ok = r6_z_ok and base_surface_exists and holes_ok and (abs(avg_base_dia - 5.5) < 1.0)

        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": [float(z_min), float(avg_base_dia)],
            "method": f"Checked z_min >= 0, base surface existence, and measured base screw hole diameters at (+-25, 25)",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": float(z_min), "ok": True if r6_z_ok and base_surface_exists else False},
                {"condition": "Two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25)", "measured": float(avg_base_dia), "ok": True if holes_ok and abs(avg_base_dia - 5.5) < 1.0 else False}
            ],
            "note": f"z_min: {z_min:.3f}, base_surface: {base_surface_exists}"
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