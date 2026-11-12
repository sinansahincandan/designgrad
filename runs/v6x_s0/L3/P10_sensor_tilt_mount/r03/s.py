import cadquery as cq
import trimesh
import numpy as np
import json
from shapely.geometry import Point, Polygon

def solve():
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    results = {}
    density_pla_g_mm3 = 1.24 / 1000  # g/mm3
    sensor_mass = 50.0 # g
    
    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": "Counted number of solids in the STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": n_solids == 1}],
            "note": f"Found {n_solids} solids"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R2: Base on desk (min z=0) and two vertical screw holes (D=4.5 at +-20, -10)
    try:
        bbox = shape.BoundingBox()
        z_min = bbox.zmin
        hole_params = [((20, -10), (0, 0, 1)), ((-20, -10), (0, 0, 1))]
        hole_results_bool = []
        for pos, direction in hole_params:
            d = 4.5
            core = cq.Solid.makeCylinder(d/2 - 0.1, 100, pnt=cq.Vector(*pos), dir=cq.Vector(*direction))
            wall_outer = cq.Solid.makeCylinder(d/2 + 1.0, 100, pnt=cq.Vector(*pos), dir=cq.Vector(*direction))
            wall_inner = cq.Solid.makeCylinder(d/2 + 0.15, 100, pnt=cq.Vector(*pos), dir=cq.Vector(*direction))
            wall = wall_outer.cut(wall_inner)
            empty_vol = shape.intersect(core).Volume() / core.Volume()
            walled_vol = shape.intersect(wall).Volume() / wall.Volume()
            hole_results_bool.append(empty_vol < 0.05 and walled_vol > 0.8)

        z_ok = abs(z_min) < 0.1
        holes_ok = all(hole_results_bool)
        status = "pass" if (z_ok and holes_ok) else "fail"
        results["R2"] = {
            "status": status,
            "value": [round(float(z_min), 3), [int(x) for x in hole_results_bool]],
            "method": f"Checked z_min={z_min} and probe cylinders at (+-20, -10) with D=4.5",
            "criteria": [
                {"condition": "minimum z = 0", "measured": round(float(z_min), 3), "ok": bool(z_ok)},
                {"condition": "two vertical screw holes diameter 4.5 mm at (+-20, -10)", "measured": [int(x) for x in hole_results_bool], "ok": bool(holes_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R3, R4, R5: Mounting Face and Sensor Holes
    face_center_3d = None
    n_vec = np.array([0, np.cos(np.radians(30)), np.sin(np.radians(30))])
    try:
        proj = mesh.points @ n_vec
        d_min, d_max = proj.min(), proj.max()
        best_d = 0
        max_a = 0
        for d in np.linspace(d_min, d_max, 50):
            origin = np.array([0, 0, d / n_vec[2]]) if abs(n_vec[2]) > 1e-3 else np.array([0, d/n_vec[1], 0])
            sec = mesh.section(plane_origin=origin, plane_normal=n_vec)
            if sec is not None:
                path2d, T = sec.to_2D()
                area = sum(p.area for p in path2d.polygons_full)
                if area > max_a:
                    max_a = area
                    best_d = d
        
        origin_face = np.array([0, 0, best_d / n_vec[2]]) if abs(n_vec[2]) > 1e-3 else np.array([0, best_d/n_vec[1], 0])
        sec = mesh.section(plane_origin=origin_face, plane_normal=n_vec)
        if sec is not None:
            path2d, T = sec.to_2D()
            pts_2d = np.array([p for poly in path2d.polygons_full for p in poly.exterior.coords])
            pts_3d = (T[:3, :3] @ pts_2d.T).T + T[:3, 3]
            face_center_3d = pts_3d.mean(axis=0)
            face_height = face_center_3d[2]
            
            area_ok = max_a >= 900 - 1.0
            height_ok = 35 <= face_height <= 50
            
            hole_ok = True
            for offset in [-10, 10]:
                h_pos = face_center_3d + np.array([offset, 0, 0])
                core = cq.Solid.makeCylinder(3.2/2 - 0.1, 20, pnt=cq.Vector(*h_pos), dir=cq.Vector(*n_vec))
                empty_vol = shape.intersect(core).Volume() / core.Volume()
                if empty_vol > 0.05: hole_ok = False

            status = "pass" if (area_ok and height_ok and hole_ok) else "fail"
            results["R3_5"] = {
                "status": status,
                "value": [round(float(max_a), 1), round(float(face_height), 2), int(hole_ok)],
                "method": f"Sectioned plane normal={n_vec}, area={max_a:.1f}, center_z={face_height:.2f}",
                "criteria": [
                    {"condition": "one flat face of at least 900 mm2", "measured": round(float(max_a), 1), "ok": bool(area_ok)},
                    {"condition": "centre of that face is at a height between 35 and 50 mm", "measured": round(float(face_height), 2), "ok": bool(height_ok)},
                    {"condition": "Two sensor screw holes, diameter 3.2 mm... at face centre +- 10 mm along X", "measured": int(hole_ok), "ok": bool(hole_ok)}
                ],
                "note": ""
            }
        else:
            raise Exception("Could not find mounting face section")
    except Exception as e:
        results["R3_5"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R6: Stability
    try:
        part_mass = shape.Volume() * density_pla_g_mm3
        part_com_raw = shape.Center()
        part_com = np.array([float(part_com_raw.x), float(part_com_raw.y), float(part_com_raw.z)])
        if face_center_3d is not None:
            sensor_com = face_center_3d + 15 * n_vec
            combined_com = (part_com * part_mass + sensor_com * sensor_mass) / (part_mass + sensor_mass)
        else:
            bbox = shape.BoundingBox()
            est_y = (bbox.ymin + bbox.ymax) / 2
            est_z = (bbox.zmin + bbox.ymax) / 2
            sensor_com = np.array([0, est_y + 15, est_z])
            combined_com = (part_com * part_mass + sensor_com * sensor_mass) / (part_mass + sensor_mass)

        bbox = shape.BoundingBox()
        margin = 5.0
        stability_ok = (bbox.xmin + margin <= combined_com[0] <= bbox.xmax - margin) and \
                       (bbox.ymin + margin <= combined_com[1] <= bbox.ymax - margin)
        results["R6"] = {
            "status": "pass" if stability_ok else "fail",
            "value": [round(float(combined_com[0]), 2), round(float(combined_com[1]), 2)],
            "method": f"Combined CoM with sensor at {sensor_com}, part mass {part_mass:.2f}g, margin 5mm",
            "criteria": [{"condition": "combined centre of mass must lie inside the contact area with >= 5 mm margin", "measured": [round(float(combined_com[0]),2), round(float(combined_com[1]),2)], "ok": bool(stability_ok)}],
            "note": f"Footprint: x[{bbox.xmin},{bbox.xmax}] y[{bbox.ymin},{bbox.ymax}]"
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R7: Mass <= 35 g
    try:
        part_mass = shape.Volume() * density_pla_g_mm3
        mass_ok = part_mass <= 35.0 + 0.1
        results["R7"] = {
            "status": "pass" if mass_ok else "fail",
            "value": round(float(part_mass), 3),
            "method": f"Volume={shape.Volume():.2f} mm3 * density=0.00124 g/mm3",
            "criteria": [{"condition": "Mass <= 35 g", "measured": round(float(part_mass), 3), "ok": bool(mass_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()