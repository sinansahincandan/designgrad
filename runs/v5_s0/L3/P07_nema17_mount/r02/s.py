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
        shaft_z = 30.0

        # R3 Check: Verify bore existence (diameter 22.5mm through the plate)
        # We check if a cylinder of diameter 22.5 exists as a void in the plate region AND that material exists around it.
        bore_probe_r = bore_r + 0.01
        bore_cyl = cq.Solid.makeCylinder(bore_probe_r, plate_y_max - plate_y_min, pnt=cq.Vector(0, plate_y_min, shaft_z), dir=cq.Vector(0, 1, 0))
        bore_void_vol = shape.intersect(bore_cyl).Volume()
        
        # To ensure the bore actually exists (not just a small cube with no hole), 
        # we check that there is material in an annulus immediately surrounding the bore.
        annulus_r_inner = bore_r
        annulus_r_outer = bore_r + 2.0
        annulus_cyl = cq.Solid.makeCylinder(annulus_r_outer, plate_y_max - plate_y_min, pnt=cq.Vector(0, plate_y_min, shaft_z), dir=cq.Vector(0, 1, 0))
        bore_cyl_inner = cq.Solid.makeCylinder(annulus_r_inner, plate_y_max - plate_y_min, pnt=cq.Vector(0, plate_y_min, shaft_z), dir=cq.Vector(0, 1, 0))
        # Material in the annulus = Intersection with outer cylinder MINUS intersection with inner cylinder
        annulus_mat_vol = shape.intersect(annulus_cyl).Volume() - shape.intersect(bore_cyl_inner).Volume()
        
        # R3 is ok if void volume is small AND material exists around it (proving the hole is in a plate)
        r3_ok = (bore_void_vol < 0.5) and (annulus_mat_vol > 10.0)

        # R2 Check: Face plate thickness (at least 4mm) with solid material all around central bore.
        # We verify the thickness by checking if there is material at y=0 and y=4 within a ring that avoids the bore.
        # A robust way: intersect a thin slice at y=0 and y=4 with an annulus.
        thickness_ok = True
        check_radii = [15.0, 20.0] 
        for r in check_radii:
            # Slice at y=0 (approx)
            p1 = cq.Solid.makeCylinder(r, 0.1, pnt=cq.Vector(0, -0.05, shaft_z), dir=cq.Vector(0, 1, 0))
            p2 = cq.Solid.makeCylinder(r, 0.1, pnt=cq.Vector(0, plate_y_max-0.05, shaft_z), dir=cq.Vector(0, 1, 0))
            # Check if material exists at these boundaries in the annulus region
            # We use a small cylinder at radius r to probe existence
            probe_r = 0.5
            for check_r in [15.0, 25.0]:
                p_y0 = cq.Solid.makeCylinder(probe_r, 0.2, pnt=cq.Vector(check_r, -0.05, shaft_z), dir=cq.Vector(0, 1, 0))
                p_y4 = cq.Solid.makeCylinder(probe_r, 0.2, pnt=cq.Vector(check_r, plate_y_max-0.05, shaft_z), dir=cq.Vector(0, 1, 0))
                if shape.intersect(p_y0).Volume() < 0.01 or shape.intersect(p_y4).Volume() < 0.01:
                    thickness_ok = False
        
        # R2 requires thickness >= 4mm (implied by y=0 to 4) and material around bore.
        # We check the actual Y-span of the intersection with a probe cylinder at x=20, z=30
        probe_y_cyl = cq.Solid.makeCylinder(1.0, 10.0, pnt=cq.Vector(20, -1, 30), dir=cq.Vector(0, 1, 0))
        intersected_y_vol = shape.intersect(probe_y_cyl).Volume()
        # If the intersection volume is roughly (Area * thickness), we check thickness
        # Area of probe cylinder cross section = pi * 1^2 = 3.14
        measured_thickness = intersected_y_vol / np.pi
        r2_ok = thickness_ok and (measured_thickness >= 3.9)

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": float(measured_thickness),
            "method": "Checked plate Y-span via probe cylinder and annulus material integrity",
            "criteria": [{"condition": "Face plate >= 4mm thick with solid material around bore", "measured": float(r2_ok), "ok": r2_ok}],
            "note": f"Thickness: {measured_thickness:.2f}, Annulus Mat: {annulus_mat_vol:.2f}"
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": float(bore_void_vol),
            "method": "Verified bore diameter 22.5mm and existence via annulus material check",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": float(bore_void_vol), "ok": r3_ok}],
            "note": f"Void Vol: {bore_void_vol:.2f}, Annulus Mat: {annulus_mat_vol:.2f}"
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes diameter 3.4 mm through the face plate along Y at (x, z) = (+-15.5, 30 +- 15.5).
    try:
        hole_coords = [(15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)]
        measured_diameters = []
        holes_exist = True
        
        for hx, hz in hole_coords:
            found_r = 0.0
            # Probe with cylinders of increasing radius to find the void diameter
            for test_r in np.linspace(0.1, 5.0, 50):
                h_cyl = cq.Solid.makeCylinder(test_r, 20, pnt=cq.Vector(hx, -5, hz), dir=cq.Vector(0, 1, 0))
                bore_vol = shape.intersect(h_cyl).Volume()
                if bore_vol < 0.5: # If volume is low, it's a hole
                    found_r = test_r
                else:
                    break
            
            # Verify material exists around the hole to avoid false positives from empty space.
            h_check_cyl = cq.Solid.makeCylinder(10.0, 20, pnt=cq.Vector(hx, -5, hz), dir=cq.Vector(0, 1, 0))
            h_check_vol = shape.intersect(h_check_cyl).Volume()
            
            if found_r > 0.5 and h_check_vol > 5.0: # Ensure it's actually in a solid part
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
            
            # Verify material exists around the hole location to ensure it's a hole in a part, not just empty space.
            h_check_cyl = cq.Solid.makeCylinder(10.0, 20, pnt=cq.Vector(sx, 25, -5), dir=cq.Vector(0, 0, 1))
            h_check_vol = shape.intersect(h_check_cyl).Volume()
            if found_r > 0.5 and h_check_vol > 1.0:
                measured_base_hole_diameters.append(found_r * 2)
            else:
                holes_ok = False

        avg_base_dia = sum(measured_base_hole_diameters)/len(measured_base_hole_diameters) if measured_base_hole_diameters else 0.0
        # R6 requires both z=0 and the holes to exist correctly
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