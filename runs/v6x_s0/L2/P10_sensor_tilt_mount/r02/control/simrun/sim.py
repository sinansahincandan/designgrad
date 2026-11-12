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
    density_pla_g_mm3 = 1.24 / 1000  # g/cm3 -> g/mm3 is density/1000
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
            # To ensure we check material presence, we use a probe cylinder that is slightly larger than the hole
            # and verify it's mostly empty (the hole) AND that there is surrounding material (the wall).
            core = cq.Solid.makeCylinder(d/2 - 0.1, 100, pnt=cq.Vector(*pos), dir=cq.Vector(*direction))
            wall_outer = cq.Solid.makeCylinder(d/2 + 1.5, 100, pnt=cq.Vector(*pos), dir=cq.Vector(*direction))
            wall_inner = cq.Solid.makeCylinder(d/2 + 0.15, 100, pnt=cq.Vector(*pos), dir=cq.Vector(*direction))
            wall = wall_outer.cut(wall_inner)
            
            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            walled_ratio = shape.intersect(wall).Volume() / wall.Volume()
            # empty_ratio ~ 0 means the hole is actually there (material is NOT in the core)
            # walled_ratio ~ 1 means material surrounds the hole
            hole_results_bool.append(empty_ratio < 0.05 and walled_ratio > 0.8)

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

    # R3, R4, R5 Logic
    face_center_3d = None
    n_vec = np.array([0, np.cos(np.radians(30)), np.sin(np.radians(30))])
    r3_val, r4_val, r5_val = 0.0, 0.0, False
    
    try:
        verts = mesh.vertices
        proj = verts @ n_vec
        d_min, d_max = proj.min(), proj.max()
        best_area = 0
        best_center = None
        
        for d in np.linspace(d_min, d_max, 100):
            b = mesh.bounds
            origin = np.array([(b[0][0]+b[1][0])/2, (b[0][1]+b[1][1])/2, (b[0][2]+b[1][2])/2])
            origin = origin + (d - np.dot(origin, n_vec)) * n_vec
            sec = mesh.section(plane_origin=origin, plane_normal=n_vec)
            if sec is not None:
                path2d, T = sec.to_2D()
                area = sum(p.area for p in path2d.polygons_full)
                if area > best_area:
                    best_area = area
                    pts_2d = []
                    for poly in path2d.polygons_full:
                        pts_2d.extend(list(poly.exterior.coords))
                    if pts_2d:
                        c2d = np.array(pts_2d).mean(axis=0)
                        basis_x = T[:3, 0]
                        basis_y = T[:3, 1]
                        translation = T[:3, 3]
                        c3d = c2d[0] * basis_x + c2d[1] * basis_y + translation
                        best_center = c3d

        if best_center is not None:
            face_center_3d = best_center
            r3_val = best_area
            r4_val = face_center_3d[2]
            hole_ok_count = 0
            for offset in [-10, 10]:
                h_pos = face_center_3d + np.array([offset, 0, 0])
                # R5: Perpendicular to mounting face (axis is -n_vec)
                core = cq.Solid.makeCylinder(3.2/2 - 0.1, 15, pnt=cq.Vector(*h_pos), dir=cq.Vector(*( -n_vec )))
                wall_outer = cq.Solid.makeCylinder(3.2/2 + 1.5, 15, pnt=cq.Vector(*h_pos), dir=cq.Vector(*( -n_vec )))
                wall_inner = cq.Solid.makeCylinder(3.2/2 + 0.15, 15, pnt=cq.Vector(*h_pos), dir=cq.Vector(*( -n_vec )))
                wall = wall_outer.cut(wall_inner)
                
                empty_ratio = shape.intersect(core).Volume() / core.Volume()
                walled_ratio = shape.intersect(wall).Volume() / wall.Volume()
                if empty_ratio < 0.05 and walled_ratio > 0.8:
                    hole_ok_count += 1
            r5_val = (hole_ok_count == 2)

            r3_ok = r3_val >= 900 - 0.1
            r4_ok = 35 <= r4_val <= 50
            r5_ok = r5_val
            
            results["R3"] = {
                "status": "pass" if r3_ok else "fail",
                "value": round(float(r3_val), 2),
                "method": f"Sectioned plane normal={n_vec}, area={r3_val:.1f}",
                "criteria": [{"condition": "one flat face of at least 900 mm2", "measured": round(float(r3_val), 2), "ok": bool(r3_ok)}],
                "note": ""
            }
            results["R4"] = {
                "status": "pass" if r4_ok else "fail",
                "value": round(float(r4_val), 2),
                "method": f"Face center height z={r4_val:.2f}",
                "criteria": [{"condition": "centre of that face is at a height between 35 and 50 mm", "measured": round(float(r4_val), 2), "ok": bool(r4_ok)}],
                "note": ""
            }
            results["R5"] = {
                "status": "pass" if r5_ok else "fail",
                "value": bool(r5_val),
                "method": f"Probed 3.2mm holes at face center +-10mm along X, axis=-n (checked empty core and walled shell)",
                "criteria": [{"condition": "Two sensor screw holes, diameter 3.2 mm... at face centre +- 10 mm along X", "measured": bool(r5_val), "ok": bool(r5_ok)}],
                "note": ""
            }
        else:
            raise Exception("Could not find mounting face")
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}
        results["R4"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}
        results["R5"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R6: Stability
    try:
        part_mass = shape.Volume() * density_pla_g_mm3
        part_com_raw = shape.Center()
        part_com = np.array([float(part_com_raw.x), float(part_com_raw.y), float(part_com_raw.z)])
        if face_center_3d is not None:
            sensor_com = face_center_3d + 15 * n_vec
        else:
            b = shape.BoundingBox()
            sensor_com = np.array([0, (b.ymin+b.ymax)/2 + 15, (b.zmin+b.ymax)/2])
        combined_com = (part_com * part_mass + sensor_com * sensor_mass) / (part_mass + sensor_mass)
        bbox = shape.BoundingBox()
        margin = 5.0
        # Contact area is the footprint on z=0. Since it's a desk mount, we check x and y bounds of contact.
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