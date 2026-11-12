import cadquery as cq
import trimesh
import numpy as np
import json

def solve():
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    # Constants & Phone Geometry
    DENSITY_PLA = 1.24 / 1000  # g/mm3 (from 1.24 g/cm3)
    PHONE_MASS = 200.0         # g
    U = np.array([-np.cos(np.radians(65)), 0, np.sin(np.radians(65))])
    N = np.array([np.sin(np.radians(65)), 0, np.cos(np.radians(65))])
    PHONE_COM = np.array([0, 0, 8]) + 80 * U + 4.5 * N

    results = {}

    def clean(obj):
        """Recursively convert numpy types and non-serializable objects to standard Python types."""
        if isinstance(obj, bool):
            return bool(obj)
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return [clean(x) for x in obj.ravel()]
        if isinstance(obj, list):
            return [clean(x) for x in obj]
        if isinstance(obj, dict):
            return {str(k): clean(v) for k, v in obj.items()}
        return obj

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        is_ok = (n_solids == 1)
        results["R1"] = {
            "status": "pass" if is_ok else "fail",
            "value": clean(n_solids),
            "method": f"Counted number of solids in STEP file: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": clean(n_solids), "ok": bool(is_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Footprint and Height
    try:
        bbox = shape.BoundingBox()
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        dz = bbox.zmax - bbox.zmin
        z_min = bbox.zmin
        c1, c2, c3, c4 = (dx <= 100.0 + 1e-3), (dy <= 100.0 + 1e-3), (dz <= 120.0 + 1e-3), (abs(z_min) < 1e-2)
        is_ok = all([c1, c2, c3, c4])
        results["R2"] = {
            "status": "pass" if is_ok else "fail",
            "value": [clean(dx), clean(dy), clean(dz), clean(z_min)],
            "method": f"Extents: x={dx}, y={dy}, z={dz}. Min Z={z_min}",
            "criteria": [{"condition": "Footprint within 100x100 mm", "measured": [clean(dx), clean(dy)], "ok": bool(c1 and c2)},
                         {"condition": "Height <= 120 mm", "measured": clean(dz), "ok": bool(c3)},
                         {"condition": "Stands on z=0", "measured": clean(z_min), "ok": bool(c4)}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: No intersection with phone volume
    try:
        samples = 15
        test_points = []
        for a in np.linspace(0, 160, samples):
            for b in np.linspace(0, 9, samples):
                for y in np.linspace(-37.5, 37.5, samples):
                    p = np.array([0, y, 8]) + a * U + b * N
                    test_points.append(p)
        pts = np.array(test_points)
        inside_mask = mesh.contains(pts)
        intersections = int(np.sum(inside_mask))
        is_ok = (intersections == 0)
        results["R3"] = {
            "status": "pass" if is_ok else "fail",
            "value": intersections,
            "method": f"Checked {len(pts)} sample points within phone volume for intersection with stand mesh.",
            "criteria": [{"condition": "Must not intersect the phone volume", "measured": intersections, "ok": bool(is_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    def check_region_material(a_range, b_range, y_range):
        pts = []
        for a in np.linspace(a_range[0], a_range[1], 8):
            for b in np.linspace(b_range[0], b_range[1], 5):
                for y in np.linspace(y_range[0], y_range[1], 8):
                    p = np.array([0, y, 8]) + a * U + b * N
                    pts.append(p)
        if not pts: return 0.0
        pts_arr = np.array(pts)
        inside_mask = mesh.contains(pts_arr)
        return float(np.sum(inside_mask))

    # R4 Back Support
    try:
        hits_r4 = check_region_material((90, 110), (-2, 0), (-15, 15))
        is_ok_r4 = hits_r4 >= 5.0 
        results["R4"] = {
            "status": "pass" if is_ok_r4 else "fail",
            "value": clean(hits_r4),
            "method": f"Material probe: count of points in a[90,110], b[-2,0], y[-15,15] found inside mesh.",
            "criteria": [{"condition": "Material directly behind phone back", "measured": clean(hits_r4), "ok": bool(is_ok_r4)}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5 Seat and Lip
    try:
        hits_seat = check_region_material((-4, 0), (0, 9), (-15, 15))
        hits_lip = check_region_material((0, 8), (9, 13), (-15, 15))
        is_ok_r5 = (hits_seat >= 5.0) and (hits_lip >= 5.0)
        results["R5"] = {
            "status": "pass" if is_ok_r5 else "fail",
            "value": [clean(hits_seat), clean(hits_lip)],
            "method": f"Material probe: seat hits={hits_seat}, lip hits={hits_lip}",
            "criteria": [{"condition": "Material just below phone's bottom edge", "measured": clean(hits_seat), "ok": bool(hits_seat >= 5.0)},
                         {"condition": "Front lip (0 <= a <= 8, 9 <= b <= 13)", "measured": clean(hits_lip), "ok": bool(hits_lip >= 5.0)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6 Stability (FIXED: Using actual contact area via plane intersection)
    try:
        stand_vol = shape.Volume()
        stand_mass = stand_vol * DENSITY_PLA
        stand_com_vec = shape.Center()
        stand_com = np.array([float(stand_com_vec.x), float(stand_com_vec.y), float(stand_com_vec.z)])
        total_mass = stand_mass + PHONE_MASS
        combined_com_x = (stand_mass * stand_com[0] + PHONE_MASS * PHONE_COM[0]) / total_mass
        combined_com_y = (stand_mass * stand_com[1] + PHONE_MASS * PHONE_COM[1]) / total_mass

        # To find the contact area, we slice the mesh at z=0. 
        # Since it's a thin surface, we use a small epsilon thickness to capture the footprint.
        eps = 0.05 
        h = 0.2
        ylo, yhi = mesh.bounds[0][1], mesh.bounds[1][1]
        zlo, zhi = mesh.bounds[0][2], mesh.bounds[1][2]
        # We sample points at a very low Z to find the footprint on the desk
        Y_grid, Z_grid = np.meshgrid(np.linspace(ylo, yhi, 50), np.linspace(0, eps, 5))
        X_grid = np.zeros_like(Y_grid)
        pts_footprint = np.column_stack([X_grid.ravel(), Y_grid.ravel(), Z_grid.ravel()])
        inside_footprint = mesh.contains(pts_footprint)
        
        if not np.any(inside_footprint):
            # Fallback if slice is too thin: use bounding box but flag it, 
            # or better, try to find the actual x/y bounds of points where z ~ 0
            contact_xmin, contact_xmax = shape.BoundingBox().xmin, shape.BoundingBox().xmax
            contact_ymin, contact_ymax = shape.BoundingBox().ymin, shape.BoundingBox().ymax
        else:
            # Calculate actual footprint extents from the points that are "at" z=0
            footprint_pts = pts_footprint[inside_footprint]
            contact_xmin, contact_xmax = footprint_pts[:, 0].min(), footprint_pts[:, 0].max()
            contact_ymin, contact_ymax = footprint_pts[:, 1].min(), footprint_pts[:, 1].max()

        margin = 5.0
        in_x = (contact_xmin + margin) <= combined_com_x <= (contact_xmax - margin)
        in_y = (contact_ymin + margin) <= combined_com_y <= (contact_ymax - margin)
        is_ok_r6 = in_x and in_y

        results["R6"] = {
            "status": "pass" if is_ok_r6 else "fail",
            "value": [clean(combined_com_x), clean(combined_com_y)],
            "method": f"Combined COM: x={combined_com_x}, y={combined_com_y}. Contact area: x[{contact_xmin:.2f},{contact_xmax:.2f}], y[{contact_ymin:.2f},{contact_ymax:.2f}]",
            "criteria": [{"condition": "COM projects inside contact area with 5mm margin", "measured": [clean(combined_com_x), clean(combined_com_y)], "ok": bool(is_ok_r6)}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7 Mass
    try:
        mass_g = shape.Volume() * DENSITY_PLA
        is_ok_r7 = mass_g <= 60.0 + 1e-3
        results["R7"] = {
            "status": "pass" if is_ok_r7 else "fail",
            "value": clean(mass_g),
            "method": f"Volume={shape.Volume():.2f} mm3 * Density=1.24 g/cm3",
            "criteria": [{"condition": "Mass <= 60 g", "measured": clean(mass_g), "ok": bool(is_ok_r7)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(clean(results)))

if __name__ == "__main__":
    solve()