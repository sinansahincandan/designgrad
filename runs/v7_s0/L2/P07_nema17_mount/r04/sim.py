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
        
        # R3: Central bore diameter check (shaft axis x=0, z=30)
        # To ensure we measure a "through-hole", the probe must span the entire thickness of the plate.
        # The face plate is at y=0 to 4. We probe from y=-1 to y=5.
        p_start_bore = (0, -1, 30) 
        L_probe_bore = 7.0 # Spans y=-1 to y=6
        dir_vec = (0, 1, 0)
        
        # Core: The volume that SHOULD be empty.
        core_bore = cq.Solid.makeCylinder(bore_r - 0.05, L_probe_bore, pnt=cq.Vector(*p_start_bore), dir=cq.Vector(*dir_vec))
        # Wall: A shell that SHOULD be solid to confirm the bore is surrounded by material.
        wall_shell = cq.Solid.makeCylinder(bore_r + 2.0, L_probe_bore, pnt=cq.Vector(*p_start_bore), dir=cq.Vector(*dir_vec)).cut(
                     cq.Solid.makeCylinder(bore_r - 0.1, L_probe_bore, pnt=cq.Vector(*p_start_bore), dir=cq.Vector(*dir_vec)))
        
        # empty_ratio: volume of part inside the core cylinder. Should be ~0 for a hole.
        empty_ratio = shape.intersect(core_bore).Volume() / core_bore.Volume()
        # walled_ratio: volume of part inside the shell. Should be ~1 for a solid plate.
        walled_ratio = shape.intersect(wall_shell).Volume() / wall_shell.Volume()
        
        # A clean through-hole has very low empty_ratio and high walled_ratio.
        r3_ok = (empty_ratio < 0.05) and (walled_ratio > 0.8)

        # R2: Face plate thickness (y=0 to 4)
        # Check material presence at y=4 in a ring around the bore.
        thickness_ok = True
        for angle in np.linspace(0, 2*np.pi, 8):
            test_r = bore_r + 5.0 
            tx = test_r * np.cos(angle)
            tz = 30 + test_r * np.sin(angle)
            # Probe at y=4 to ensure the plate hasn't ended prematurely.
            probe_size = 1.0
            thick_probe = cq.Solid.makeBox(probe_size, probe_size, probe_size, pnt=cq.Vector(tx - probe_size/2, 3.5, tz - probe_size/2))
            if shape.intersect(thick_probe).Volume() < (0.1 * thick_probe.Volume()):
                thickness_ok = False
                break

        r2_ok = thickness_ok
        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": float(r2_ok),
            "method": f"Checked material presence at y=4 in ring around bore: {thickness_ok}",
            "criteria": [{"condition": "Face plate >= 4mm thick with solid material around bore", "measured": r2_ok, "ok": r2_ok}],
            "note": ""
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": {"empty_ratio": round(float(empty_ratio), 3), "walled_ratio": round(float(walled_ratio), 3)},
            "method": f"Bore emptiness: {round(empty_ratio, 3)}, Bore wall existence: {round(walled_ratio, 3)}",
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
            # Probe from y=-2 to y=6 (covers plate thickness)
            p_start = (cx, -2, cz)
            L_hole = 8.0 
            core = cq.Solid.makeCylinder(3.4/2 - 0.1, L_hole, pnt=cq.Vector(*p_start), dir=cq.Vector(0, 1, 0))
            # A hole is valid if the core cylinder contains very little part volume (empty)
            intersection_v = shape.intersect(core).Volume()
            empty_ratio = intersection_v / core.Volume()
            
            wall_shell = cq.Solid.makeCylinder(3.4/2 + 1.0, L_hole, pnt=cq.Vector(*p_start), dir=cq.Vector(0, 1, 0)).cut(
                         cq.Solid.makeCylinder(3.4/2 - 0.1, L_hole, pnt=cq.Vector(*p_start), dir=cq.Vector(0, 1, 0)))
            walled_ratio = shape.intersect(wall_shell).Volume() / wall_shell.Volume()
            
            # Improved check: must be empty AND have material around it
            holes_exist.append(empty_ratio < 0.1 and walled_ratio > 0.5)
        
        all_r4_ok = all(holes_exist)
        results["R4"] = {
            "status": "pass" if all_r4_ok else "fail",
            "value": [int(h) for h in holes_exist],
            "method": "Checked 4 cylinders of D=3.4 at specified (x,z). Verified emptiness and surrounding wall.",
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
        r6_z_ok = -0.1 <= z_min <= 0.1
        
        hole_coords = [(25, 25), (-25, 25)]
        holes_exist = []
        # Use a large Z span to ensure we catch the hole through the base
        z_span = bbox.zmax - bbox.zmin
        for cx, cy in hole_coords:
            p_start = (cx, cy, bbox.zmin - 1.0)
            core = cq.Solid.makeCylinder(5.5/2 - 0.1, z_span + 2.0, pnt=cq.Vector(*p_start), dir=cq.Vector(0, 0, 1))
            intersection_v = shape.intersect(core).Volume()
            empty_ratio = intersection_v / core.Volume()
            # A hole is valid if the cylinder is mostly empty (the hole) and intersects the part (it's in the base)
            holes_exist.append(empty_ratio < 0.1 and intersection_v > 0)
        
        r6_ok = r6_z_ok and all(holes_exist)
        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": {"z_min": round(z_min, 3), "holes": [int(h) for h in holes_exist]},
            "method": f"Min Z: {round(z_min, 3)}, Hole existence check at (+-25, 25)",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": round(z_min, 3), "ok": r6_z_ok},
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
            "method": f"BBox: x[{round(x_min,1)},{round(x_max,1)}], z_max:{round(z_max,1)}, Mass:{round(mass_g,2)}g",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": round(x_min,2), "ok": r7_x_ok},
                {"condition": "top <= 55 mm", "measured": round(z_max,2), "ok": r7_z_ok},
                {"condition": "mass <= 60 g", "measured": round(mass_g,2), "ok": r7_m_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    check_requirements()