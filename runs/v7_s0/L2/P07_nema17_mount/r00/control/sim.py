import cadquery as cq
import trimesh
import numpy as np
import json

def check_requirements():
    results = {}
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        r1_status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": r1_status,
            "value": n_solids,
            "method": f"Counted number of solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": n_solids == 1}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2 & R3: Face plate thickness (y=0 to 4) and Central Bore (D=22.5)
    try:
        bore_diam = 22.5
        bore_r = bore_diam / 2
        bbox = shape.BoundingBox()
        # The face plate is at y=[0, 4]. We probe along Y through the shaft axis (x=0, z=30).
        # To ensure we hit the part, we use a probe that spans from slightly before y=0 to slightly after y=4.
        p_start = (0, -1, 30) 
        L_probe = 7.0 # Covers y=-1 to 6
        dir_vec = (0, 1, 0)
        
        # R3: Central bore diameter check
        core = cq.Solid.makeCylinder(bore_r - 0.1, L_probe, pnt=cq.Vector(*p_start), dir=cq.Vector(*dir_vec))
        intersection_vol = shape.intersect(core).Volume()
        # A hole is valid if the core volume is mostly empty AND it intersects the part's bounding box/volume
        empty_ratio = intersection_vol / core.Volume()
        r3_ok = empty_ratio < 0.05 and (bbox.ymin <= 30 <= bbox.ymax) # Check axis alignment roughly

        # R2: Face plate thickness (y=0 to 4) and material around bore
        shell_r_inner = bore_r + 1.0
        shell_r_outer = bore_r + 5.0
        shell_core = cq.Solid.makeCylinder(shell_r_outer, L_probe, pnt=cq.Vector(*p_start), dir=cq.Vector(*dir_vec))
        shell_inner = cq.Solid.makeCylinder(shell_r_inner, L_probe, pnt=cq.Vector(*p_start), dir=cq.Vector(*dir_vec))
        wall_shell = shell_core.cut(shell_inner)
        walled_ratio = shape.intersect(wall_shell).Volume() / wall_shell.Volume()

        # Thickness check: Probe the region y=[3.9, 4.1] at a point away from the bore (e.g., x=20)
        thick_probe = cq.Solid.makeBox(2, 0.5, 2, pnt=cq.Vector(20, 3.75, 30))
        has_thickness = shape.intersect(thick_probe).Volume() > 0
        
        r2_ok = walled_ratio > 0.8 and has_thickness

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": round(walled_ratio, 3),
            "method": f"Wall shell volume ratio: {walled_ratio}, Thickness probe (y=4): {has_thickness}",
            "criteria": [{"condition": "Face plate >= 4mm thick with solid material around bore", "measured": r2_ok, "ok": r2_ok}],
            "note": ""
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": round(empty_ratio, 3),
            "method": f"Bore emptiness ratio: {empty_ratio}",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": r3_ok, "ok": r3_ok}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes (3.4mm) at (+-15.5, 30 +- 15.5) through face plate along Y
    try:
        screw_coords = [(15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)]
        holes_exist = []
        for cx, cz in screw_coords:
            # Ensure the probe is within the Z-range of the part to avoid false negatives
            if not (bbox.zmin <= cz <= bbox.zmax):
                holes_exist.append(False)
                continue
            p_start = (cx, -2, cz)
            L_hole = 8.0
            core = cq.Solid.makeCylinder(3.4/2 - 0.1, L_hole, pnt=cq.Vector(*p_start), dir=cq.Vector(0, 1, 0))
            intersection_v = shape.intersect(core).Volume()
            empty_v = intersection_v / core.Volume()
            # Hole exists if cylinder is mostly empty and it actually intersects the part's volume
            holes_exist.append(empty_v < 0.1 and intersection_v > 0)
        
        all_r4_ok = all(holes_exist)
        results["R4"] = {
            "status": "pass" if all_r4_ok else "fail",
            "value": [int(h) for h in holes_exist],
            "method": "Checked 4 cylinders of D=3.4 at specified (x,z). Verified emptiness and intersection.",
            "criteria": [{"condition": "Four motor screw holes diameter 3.4 mm", "measured": all_r4_ok, "ok": all_r4_ok}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Motor clearance (-21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5)
    try:
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        intersected_vol = shape.intersect(clearance_box).Volume()
        r5_ok = intersected_vol < 0.1
        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": intersected_vol,
            "method": f"Volume of part intersecting clearance box: {intersected_vol} mm3",
            "criteria": [{"condition": "Motor clearance region is empty", "measured": intersected_vol, "ok": r5_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Base on table (min z=0) with two 5.5mm holes at (+-25, 25)
    try:
        bbox = shape.BoundingBox()
        z_min = bbox.zmin
        r6_z_ok = abs(z_min) < 0.1 
        
        hole_coords = [(25, 25), (-25, 25)]
        holes_exist = []
        # Use a probe that spans the full Z-height of the part to ensure we find the holes
        z_span = bbox.zmax - bbox.zmin
        for cx, cy in hole_coords:
            p_start = (cx, cy, bbox.zmin)
            core = cq.Solid.makeCylinder(5.5/2 - 0.1, z_span + 1.0, pnt=cq.Vector(*p_start), dir=cq.Vector(0, 0, 1))
            intersection_v = shape.intersect(core).Volume()
            empty_v = intersection_v / core.Volume()
            # A hole exists if the cylinder is mostly empty and it actually intersects the part's volume
            holes_exist.append(empty_v < 0.1 and intersection_v > 0)
        
        r6_ok = r6_z_ok and all(holes_exist)
        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": {"z_min": z_min, "holes": [int(h) for h in holes_exist]},
            "method": f"Min Z: {z_min}, Hole existence check at (+-25, 25)",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": z_min, "ok": r6_z_ok},
                {"condition": "two vertical screw holes diameter 5.5 mm", "measured": all(holes_exist), "ok": all(holes_exist)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Envelope and Mass
    try:
        bbox = shape.BoundingBox()
        x_min, x_max = bbox.xmin, bbox.xmax
        z_max = bbox.zmax
        mass_g = (shape.Volume() * 1.24) / 1000.0 
        
        r7_x_ok = -35 <= x_min and x_max <= 35
        r7_z_ok = z_max <= 55
        r7_m_ok = mass_g <= 60.0
        
        results["R7"] = {
            "status": "pass" if (r7_x_ok and r7_z_ok and r7_m_ok) else "fail",
            "value": [round(x_min,2), round(x_max,2), round(z_max,2), round(mass_g,2)],
            "method": f"BBox: x[{x_min},{x_max}], z_max:{z_max}, Mass:{mass_g}g",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": x_min, "ok": r7_x_ok},
                {"condition": "top <= 55 mm", "measured": z_max, "ok": r7_z_ok},
                {"condition": "mass <= 60 g", "measured": mass_g, "ok": r7_m_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    check_requirements()