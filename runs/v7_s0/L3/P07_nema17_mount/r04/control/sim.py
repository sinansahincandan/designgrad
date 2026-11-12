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
        shaft_pnt = cq.Vector(0, 0, 30) 
        shaft_dir = cq.Vector(0, 1, 0)
        L_plate = 4.0 

        # R3: Central bore diameter check (must be empty in the plate region y=0 to 4)
        # To fix the "empty cube" issue, we must ensure that a solid exists around the hole.
        core = cq.Solid.makeCylinder(bore_r, L_plate, pnt=shaft_pnt, dir=shaft_dir)
        intersection_vol = shape.intersect(core).Volume()
        empty_ratio = intersection_vol / core.Volume() if core.Volume() > 0 else 1.0
        
        # Verification that the hole is actually inside a solid:
        # We check a "shell" around the bore. If the shell is mostly empty, there's no plate.
        ring_inner_r = bore_r + 0.5
        ring_outer_r = bore_r + 3.0
        ring_core = cq.Solid.makeCylinder(ring_outer_r, L_plate, pnt=shaft_pnt, dir=shaft_dir)
        ring_inner = cq.Solid.makeCylinder(ring_inner_r, L_plate, pnt=shaft_pnt, dir=shaft_dir)
        ring_shell = ring_core.cut(ring_inner)
        walled_vol = shape.intersect(ring_shell).Volume()
        walled_ratio = walled_vol / ring_shell.Volume() if ring_shell.Volume() > 0 else 0
        
        # R3 is only valid if the bore is empty AND it's surrounded by material (the plate)
        r3_ok = (empty_ratio < 0.05) and (walled_ratio > 0.5)

        # R2: Face plate thickness (y=0 to 4) and material around bore
        # Check a probe in a solid region (e.g., x=10, z=30) to ensure the plate exists at y=0-4
        thick_probe = cq.Solid.makeBox(5, L_plate, 5, pnt=cq.Vector(10, 0, 27.5))
        has_thickness = shape.intersect(thick_probe).Volume() > (5 * L_plate * 5 * 0.8)

        r2_ok = walled_ratio > 0.8 and has_thickness

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": round(walled_ratio, 3),
            "method": f"Ring ratio (y=0-4): {round(walled_ratio,3)}, Thickness probe: {has_thickness}",
            "criteria": [{"condition": "Face plate >= 4mm thick with solid material around bore", "measured": r2_ok, "ok": r2_ok}],
            "note": ""
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": round(empty_ratio, 3),
            "method": f"Bore emptiness ratio: {round(empty_ratio,3)}, Surrounding material ratio: {round(walled_ratio,3)}",
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
            p_start = cq.Vector(cx, 0, cz)
            L_hole = 4.0 
            core = cq.Solid.makeCylinder(3.4/2, L_hole, pnt=p_start, dir=cq.Vector(0, 1, 0))
            intersection_v = shape.intersect(core).Volume()
            empty_ratio = intersection_v / core.Volume() if core.Volume() > 0 else 1.0
            # Ensure there is material around the hole to avoid false positives on empty space
            material_check = cq.Solid.makeCylinder(3.4/2 + 5, L_hole, pnt=p_start, dir=cq.Vector(0, 1, 0))
            hits_material = shape.intersect(material_check).Volume() > (material_check.Volume() * 0.2)
            holes_exist.append(empty_ratio < 0.2 and hits_material)
        
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
        z_span = bbox.zmax - bbox.zmin
        for cx, cy in hole_coords:
            p_start = cq.Vector(cx, cy, bbox.zmin)
            core = cq.Solid.makeCylinder(5.5/2, z_span + 2.0, pnt=p_start, dir=cq.Vector(0, 0, 1))
            intersection_v = shape.intersect(core).Volume()
            material_check = cq.Solid.makeCylinder(5.5/2 + 5, z_span + 2.0, pnt=p_start, dir=cq.Vector(0, 0, 1))
            hits_material = shape.intersect(material_check).Volume() > (material_check.Volume() * 0.2)
            empty_ratio = intersection_v / core.Volume() if core.Volume() > 0 else 1.0
            holes_exist.append(empty_ratio < 0.2 and hits_material)
        
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