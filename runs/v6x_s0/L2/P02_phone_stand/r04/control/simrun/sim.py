import cadquery as cq
import numpy as np
import trimesh
import json

def solve():
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    results = {}

    # Constants & Phone Geometry
    DENSITY_PLA = 1.24 / 1000  # g/mm3 (converted from 1.24 g/cm3)
    PHONE_MASS = 200.0         # g
    U = np.array([-np.cos(np.radians(65)), 0, np.sin(np.radians(65))])
    N = np.array([np.sin(np.radians(65)), 0, np.cos(np.radians(65))])
    PHONE_COM = np.array([0, 0, 8]) + 80 * U + 4.5 * N

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        is_r1_pass = (n_solids == 1)
        results["R1"] = {
            "status": "pass" if is_r1_pass else "fail",
            "value": float(n_solids),
            "method": f"Counted solids in STEP file: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": bool(is_r1_pass)}],
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
        
        z_ok = abs(z_min) < 0.1
        footprint_ok = (dx <= 100.01) and (dy <= 100.01)
        height_ok = dz <= 120.01
        
        is_r2_pass = z_ok and footprint_ok and height_ok
        results["R2"] = {
            "status": "pass" if is_r2_pass else "fail",
            "value": [float(dx), float(dy), float(dz), float(z_min)],
            "method": f"Measured bbox: x_ext={dx}, y_ext={dy}, z_ext={dz}, z_min={z_min}",
            "criteria": [
                {"condition": "Stands on z=0", "measured": float(z_min), "ok": bool(z_ok)},
                {"condition": "Footprint within 100x100", "measured": [float(dx), float(dy)], "ok": bool(footprint_ok)},
                {"condition": "Height <= 120", "measured": float(dz), "ok": bool(height_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: No intersection with phone
    try:
        pts = []
        samples = 15
        for a_idx in np.linspace(0, 160, samples):
            for b_idx in np.linspace(0, 9, samples):
                for y_idx in np.linspace(-37.5, 37.5, samples):
                    p = np.array([0, y_idx, 8]) + a_idx * U + b_idx * N
                    pts.append(p)
        
        pts_arr = np.array(pts)
        inside_mask = mesh.contains(pts_arr)
        intersect_count = np.sum(inside_mask)
        
        is_r3_pass = (intersect_count == 0)
        results["R3"] = {
            "status": "pass" if is_r3_pass else "fail",
            "value": float(intersect_count),
            "method": f"Point-in-mesh sampling of phone volume ({len(pts)} pts)",
            "criteria": [{"condition": "Must not intersect phone volume", "measured": float(intersect_count), "ok": bool(is_r3_pass)}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4 & R5: Robust Material Probes using volumetric sampling
    def check_region_robust(a_range, b_range, y_range, density=1.0):
        """Returns the fraction of points inside the mesh within a specific region."""
        pts = []
        # Increase resolution to ensure we aren't just hitting empty space
        for a_val in np.linspace(a_range[0], a_range[1], 12):
            for b_val in np.linspace(b_range[0], b_range[1], 8):
                for y_val in np.linspace(y_range[0], y_range[1], 8):
                    p = np.array([0, y_val, 8]) + a_val * U + b_val * N
                    pts.append(p)
        if not pts: return 0.0
        pts_arr = np.array(pts)
        inside_mask = mesh.contains(pts_arr)
        return np.sum(inside_mask) / len(pts_arr)

    try:
        # R4: Back support (-2 <= b <= 0, a in [90, 110], |y| <= 15)
        # We require a significant fraction of the probe volume to be filled.
        r4_val = check_region_robust((90, 110), (-2, 0), (-15, 15))
        is_r4_pass = r4_val > 0.3  # Require ~30% occupancy to ensure it's a real support structure
        results["R4"] = {
            "status": "pass" if is_r4_pass else "fail",
            "value": float(r4_val),
            "method": f"Volumetric sampling in R4 region (a:[90,110], b:[-2,0], y:[-15,15])",
            "criteria": [{"condition": "Material behind phone back", "measured": float(r4_val), "ok": bool(is_r4_pass)}],
            "note": ""
        }

        # R5: Seat and Lip
        seat_val = check_region_robust((-4, 0), (0, 9), (-15, 15))
        lip_val = check_region_robust((0, 8), (9, 13), (-15, 15))
        # Require ~30% occupancy for both to ensure they are substantial features
        is_r5_pass = seat_val > 0.3 and lip_val > 0.3
        results["R5"] = {
            "status": "pass" if is_r5_pass else "fail",
            "value": [float(seat_val), float(lip_val)],
            "method": f"Volumetric sampling for seat and lip regions",
            "criteria": [
                {"condition": "Material below phone bottom (Seat)", "measured": float(seat_val), "ok": bool(seat_val > 0.3)},
                {"condition": "Front lip material", "measured": float(lip_val), "ok": bool(lip_val > 0.3)}
            ],
            "note": ""
        }
    except Exception as e:
        if "R4" not in results:
            results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        if "R5" not in results:
            results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Stability (Combined COM projection)
    try:
        stand_vol = mesh.volume
        stand_mass = stand_vol * DENSITY_PLA
        stand_com = mesh.center_mass
        
        combined_mass = stand_mass + PHONE_MASS
        combined_com = (stand_mass * np.array(stand_com) + PHONE_MASS * PHONE_COM) / combined_mass
        
        x_min, x_max = bbox.xmin, bbox.xmax
        y_min, y_max = bbox.ymin, bbox.ymax
        
        margin = 5.0
        # Check if COM is within the footprint with a margin
        x_ok = (x_min + margin <= combined_com[0] <= x_max - margin)
        y_ok = (y_min + margin <= combined_com[1] <= y_max - margin)
        is_r6_pass = x_ok and y_ok
        
        results["R6"] = {
            "status": "pass" if is_r6_pass else "fail",
            "value": [float(combined_com[0]), float(combined_com[1])],
            "method": f"Combined COM: {combined_com}, Footprint: x[{x_min},{x_max}], y[{y_min},{y_max}] with 5mm margin",
            "criteria": [
                {"condition": "COM projection inside contact area with 5mm margin", "measured": [float(combined_com[0]), float(combined_com[1])], "ok": bool(is_r6_pass)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 60g
    try:
        stand_mass = mesh.volume * DENSITY_PLA
        is_r7_pass = stand_mass <= 60.01
        results["R7"] = {
            "status": "pass" if is_r7_pass else "fail",
            "value": float(stand_mass),
            "method": f"Volume ({mesh.volume:.2f} mm3) * Density ({DENSITY_PLA*1000:.2f} g/cm3) / 1000",
            "criteria": [{"condition": "Mass <= 60 g", "measured": float(stand_mass), "ok": bool(is_r7_pass)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()