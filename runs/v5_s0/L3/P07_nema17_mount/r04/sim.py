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
        plane_y = 2.0
        grid_res = 0.15
        x_range = np.arange(-40, 40, grid_res)
        z_range = np.arange(-10, 60, grid_res)
        X_g, Z_g = np.meshgrid(x_range, z_range)
        pts = np.column_stack([np.full(X_g.size, plane_y), X_g.ravel(), Z_g.ravel()])
        inside = mesh.contains(pts).reshape(X_g.shape)
        
        # R3: Central bore diameter 22.5 mm (radius 11.25) at x=0, z=30
        bore_center = (0, 30)
        dist_sq_map = (X_g - bore_center[0])**2 + (Z_g - bore_center[1])**2
        material_mask = inside == True
        if np.any(material_mask):
            dist_to_mat = np.sqrt(np.min(dist_sq_map[material_mask]))
            measured_bore_dia = dist_to_mat * 2
        else:
            measured_bore_dia = 0.0
        r3_ok = abs(measured_bore_dia - 22.5) < 1.5

        # R2: Face plate thickness (y=0 to 4) and material around bore
        grid_res_yz = 0.3
        y_range_check = np.arange(-1, 5, grid_res_yz)
        z_range_check = np.arange(0, 60, grid_res_yz)
        Y_g_yz, Z_g_yz = np.meshgrid(y_range_check, z_range_check)
        pts_yz = np.column_stack([np.full(Y_g_yz.size, 0), Y_g_yz.ravel(), Z_g_yz.ravel()])
        inside_yz = mesh.contains(pts_yz).reshape(Y_g_yz.shape)
        
        # Fix: Use bitwise & for numpy arrays instead of 'and'
        mat_at_y0 = np.any((np.abs(Y_g_yz - 0) < grid_res_yz/2) & inside_yz)
        mat_at_y4 = np.any((np.abs(Y_g_yz - 4) < grid_res_yz/2) & inside_yz)
        
        dist_sq_annulus = (X_g - 0)**2 + (Z_g - 30)**2
        mat_in_annulus = np.any(inside & (np.abs(np.sqrt(dist_sq_annulus) - 15) < 2.0))
        
        r2_ok = mat_at_y0 and mat_at_y4 and mat_in_annulus

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": float(mat_at_y0 and mat_at_y4),
            "method": "Probed Y-Z plane at x=0 for thickness and X-Z plane at y=2 for annulus material",
            "criteria": [{"condition": "Face plate >= 4mm thick with solid material around bore", "measured": float(r2_ok), "ok": r2_ok}],
            "note": f"y0: {mat_at_y0}, y4: {mat_at_y4}, annulus: {mat_in_annulus}"
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": float(measured_bore_dia),
            "method": "Measured distance from (0, 30) to nearest material in X-Z plane at y=2",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": float(measured_bore_dia), "ok": r3_ok}],
            "note": ""
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
            grid_res_h = 0.2
            x_vals = np.linspace(hx - 5, hx + 5, 30)
            z_vals = np.linspace(hz - 5, hz + 5, 30)
            X_h, Z_h = np.meshgrid(x_vals, z_vals)
            pts_h = np.column_stack([np.full(X_h.size, 2.0), X_h.ravel(), Z_h.ravel()])
            inside_h = mesh.contains(pts_h).reshape(X_h.shape)
            
            dist_sq_h = (X_h - hx)**2 + (Z_h - hz)**2
            material_mask = inside_h == True
            if np.any(material_mask):
                dist_to_mat = np.sqrt(np.min(dist_sq_h[material_mask]))
                measured_diameters.append(dist_to_mat * 2)
            else:
                holes_exist = False

        avg_dia = sum(measured_diameters)/len(measured_diameters) if measured_diameters else 0.0
        r4_ok = holes_exist and (abs(avg_dia - 3.4) < 1.0)

        results["R4"] = {
            "status": "pass" if r4_ok else "fail",
            "value": float(avg_dia),
            "method": f"Measured diameter of holes at (+-15.5, 30 +- 15.5) by finding distance to material in X-Z section",
            "criteria": [{"condition": "Four motor screw holes, diameter 3.4 mm", "measured": float(avg_dia), "ok": True if r4_ok else False}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Motor clearance
    try:
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        intersect_vol = shape.intersect(clearance_box).Volume()
        r5_ok = intersect_vol < 0.5
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
        r6_z_ok = z_min <= 0.1
        
        slice_thickness = 0.2
        probe_base = cq.Solid.makeBox(80, 80, slice_thickness, pnt=cq.Vector(-40, -40, 0))
        base_surface_exists = shape.intersect(probe_base).Volume() > 1.0

        holes_ok = True
        measured_base_hole_diameters = []

        for sx in [-25, 25]:
            found_r = 0.0
            material_at_edge = False
            for test_r in np.linspace(0.1, 8.0, 30):
                h_base_cyl = cq.Solid.makeCylinder(test_r, 20, pnt=cq.Vector(sx, 25, -5), dir=cq.Vector(0, 0, 1))
                bore_vol = shape.intersect(h_base_cyl).Volume()
                if bore_vol < 0.5: 
                    found_r = test_r
                else:
                    material_at_edge = True
                    break
            
            if found_r > 0.1 and material_at_edge:
                measured_base_hole_diameters.append(found_r * 2)
            else:
                holes_ok = False

        avg_base_dia = sum(measured_base_hole_diameters)/len(measured_base_hole_diameters) if measured_base_hole_diameters else 0.0
        r6_ok = r6_z_ok and base_surface_exists and holes_ok and (abs(avg_base_dia - 5.5) < 1.5)

        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": [float(z_min), float(avg_base_dia)],
            "method": f"Checked z_min, base surface existence via thin slice at z=0, and measured vertical hole diameters",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": float(z_min), "ok": True if r6_z_ok and base_surface_exists else False},
                {"condition": "Two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25)", "measured": float(avg_base_dia), "ok": True if holes_ok and abs(avg_base_dia - 5.5) < 1.5 else False}
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
        mass_ok = mass_g <= 60 + 1.0
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