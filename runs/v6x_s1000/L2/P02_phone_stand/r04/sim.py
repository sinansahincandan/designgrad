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
    DENSITY_PLA = 1.24 / 1000  # g/mm3
    PHONE_MASS = 200.0         # g
    U = np.array([-np.cos(np.radians(65)), 0, np.sin(np.radians(65))])
    N = np.array([np.sin(np.radians(65)), 0, np.cos(np.radians(65))])
    PHONE_COM = np.array([0, 0, 8]) + 80 * U + 4.5 * N

    results = {}

    def clean(obj):
        if isinstance(obj, (bool, np.bool_)):
            return bool(obj)
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        if isinstance(obj, (np.ndarray, list)):
            return [clean(x) for x in obj]
        if isinstance(obj, dict):
            return {k: clean(v) for k, v in obj.items()}
        return obj

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        is_ok = (n_solids == 1)
        results["R1"] = {
            "status": "pass" if is_ok else "fail",
            "value": clean(n_solids),
            "method": f"Counted number of solids in STEP file: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": clean(n_solids), "ok": is_ok}],
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
        c1, c2, c3, c4 = (dx <= 100.01, dy <= 100.01, dz <= 120.01, abs(z_min) < 0.1)
        is_ok = all([c1, c2, c3, c4])
        results["R2"] = {
            "status": "pass" if is_ok else "fail",
            "value": [clean(dx), clean(dy), clean(dz), clean(z_min)],
            "method": f"Extents: x={dx}, y={dy}, z={dz}. Min Z={z_min}",
            "criteria": [
                {"condition": "Footprint within 100x100 mm", "measured": [clean(dx), clean(dy)], "ok": c1 and c2},
                {"condition": "Height <= 120 mm", "measured": clean(dz), "ok": c3},
                {"condition": "Stands on z=0", "measured": clean(z_min), "ok": c4}
            ],
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
        inside = mesh.contains(pts)
        intersections = int(np.sum(inside))
        is_ok = (intersections == 0)
        results["R3"] = {
            "status": "pass" if is_ok else "fail",
            "value": intersections,
            "method": f"Checked {len(pts)} sample points within phone volume for intersection with stand mesh.",
            "criteria": [{"condition": "Must not intersect the phone volume", "measured": intersections, "ok": is_ok}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4 & R5 helper - FIXED logic to ensure we check for presence of material in the specific region.
    # The previous error was that it might pass if 'points inside' were calculated incorrectly or inverted.
    # We use a dense grid and require at least one point (or a significant fraction) to be INSIDE the stand mesh.
    def check_region_presence(a_range, b_range, y_range):
        pts_list = []
        for a in np.linspace(a_range[0], a_range[1], 12):
            for b in np.linspace(b_range[0], b_range[1], 6):
                for y in np.linspace(y_range[0], y_range[1], 6):
                    p = np.array([0, y, 8]) + a * U + b * N
                    pts_list.append(p)
        if not pts_list: return 0.0
        pts = np.array(pts_list)
        # mesh.contains returns True if point is inside the stand.
        inside_count = np.sum(mesh.contains(pts))
        return float(inside_count) / len(pts)

    # R4 Back Support
    try:
        r4_frac = check_region_presence((90, 110), (-2, 0), (-15, 15))
        is_ok_r4 = r4_frac > 0.0  # If any material is found in this specific region
        results["R4"] = {
            "status": "pass" if is_ok_r4 else "fail",
            "value": clean(r4_frac),
            "method": f"Sampled points in phone-relative region: a[90,110], b[-2,0], y[-15,15]",
            "criteria": [{"condition": "Material directly behind phone back", "measured": clean(r4_frac), "ok": is_ok_r4}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5 Seat and Lip
    try:
        r5_seat = check_region_presence((-4, 0), (0, 9), (-15, 15))
        r5_lip = check_region_presence((0, 8), (9, 13), (-15, 15))
        is_ok_r5 = (r5_seat > 0.0) and (r5_lip > 0.0)
        results["R5"] = {
            "status": "pass" if is_ok_r5 else "fail",
            "value": [clean(r5_seat), clean(r5_lip)],
            "method": f"Sampled points in seat region (a[-4,0], b[0,9]) and lip region (a[0,8], b[9,13])",
            "criteria": [
                {"condition": "Material just below phone's bottom edge", "measured": clean(r5_seat), "ok": r5_seat > 0.0},
                {"condition": "Front lip (0 <= a <= 8, 9 <= b <= 13)", "measured": clean(r5_lip), "ok": r5_lip > 0.0}
            ],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6 Stability
    try:
        stand_vol = shape.Volume()
        stand_mass = stand_vol * DENSITY_PLA
        c_vec = shape.Center()
        stand_com = np.array([float(c_vec.x), float(c_vec.y), float(c_vec.z)])
        total_mass = stand_mass + PHONE_MASS
        combined_com_x = (stand_mass * stand_com[0] + PHONE_MASS * PHONE_COM[0]) / total_mass
        combined_com_y = (stand_mass * stand_com[1] + PHONE_MASS * PHONE_COM[1]) / total_mass
        bbox = shape.BoundingBox()
        margin = 5.0
        in_x = (bbox.xmin + margin) <= combined_com_x <= (bbox.xmax - margin)
        in_y = (bbox.ymin + margin) <= combined_com_y <= (bbox.ymax - margin)
        is_ok_r6 = in_x and in_y
        results["R6"] = {
            "status": "pass" if is_ok_r6 else "fail",
            "value": [clean(combined_com_x), clean(combined_com_y)],
            "method": f"Combined COM: x={combined_com_x}, y={combined_com_y}. Footprint: x[{bbox.xmin},{bbox.xmax}], y[{bbox.ymin},{bbox.ymax}]",
            "criteria": [{"condition": "COM projects inside contact area with 5mm margin", "measured": [clean(combined_com_x), clean(combined_com_y)], "ok": is_ok_r6}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7 Mass
    try:
        mass_g = shape.Volume() * DENSITY_PLA
        is_ok_r7 = mass_g <= 60.01
        results["R7"] = {
            "status": "pass" if is_ok_r7 else "fail",
            "value": clean(mass_g),
            "method": f"Volume={shape.Volume():.2f} mm3 * Density=1.24 g/cm3",
            "criteria": [{"condition": "Mass <= 60 g", "measured": clean(mass_g), "ok": is_ok_r7}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(clean(results)))

if __name__ == "__main__":
    solve()