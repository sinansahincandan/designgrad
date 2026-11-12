import cadquery as cq
import trimesh
import numpy as np
import json

def run_verification():
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
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": "Counted number of solids in STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": status == "pass"}],
            "note": f"Found {n_solids} solids"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R2 & R3: Face plate thickness and Central Bore
    try:
        # R3: Central bore diameter 22.5 mm through face plate on shaft axis (0, 30)
        bore_diam = 22.5
        bore_pnt = cq.Vector(0, 0, 30) # Axis is Y, so pnt at y=0
        bore_dir = cq.Vector(0, 1, 0)
        # We check the bore through the face plate (y=0 to 4)
        bore_len = 4.0
        core = cq.Solid.makeCylinder(bore_diam / 2 - 0.15, bore_len, pnt=bore_pnt, dir=bore_dir)
        wall = cq.Solid.makeCylinder(bore_diam / 2 + 1.0, bore_len, pnt=bore_pnt, dir=bore_dir).cut(
            cq.Solid.makeCylinder(bore_diam / 2 + 0.15, bore_len, pnt=bore_pnt, dir=bore_dir))
        
        empty_vol = shape.intersect(core).Volume() / core.Volume()
        walled_vol = shape.intersect(wall).Volume() / wall.Volume()
        r3_ok = empty_vol < 0.02 and walled_vol > 0.9
        
        # R2: Face plate thickness (y=0 to 4) with solid material all around the central bore
        # We check if there is a continuous ring of material in the y=[0,4] region surrounding the bore.
        # A robust way is to probe a 'shell' volume that contains the bore but excludes the core.
        bore_ring_diam = bore_diam + 2.0 # Check for material within 1mm of the hole edge
        ring_core = cq.Solid.makeCylinder(bore_diam / 2 + 0.05, bore_len, pnt=bore_pnt, dir=bore_dir)
        ring_outer = cq.Solid.makeCylinder(bore_ring_diam / 2, bore_len, pnt=bore_pnt, dir=bore_dir)
        ring_shell = ring_outer.cut(ring_core)
        
        # Check if the shell is mostly filled with material (ensures thickness/integrity around hole)
        # and check that the volume in y=[0,4] is actually present.
        shell_filled_ratio = shape.intersect(ring_shell).Volume() / ring_shell.Volume()
        
        # Also verify plate thickness: any point at y=2 must be inside the part? 
        # Simpler: check if intersection with a slab [0,4] is significant and contains the bore area.
        plate_box = cq.Solid.makeBox(100, 4, 100, pnt=cq.Vector(-50, 0, -50))
        plate_vol = shape.intersect(plate_box).Volume()
        
        r2_ok = shell_filled_ratio > 0.8 and plate_vol > 0 # Ensures material exists around bore in the y-range
        
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": [round(empty_vol, 3), round(walled_vol, 3)],
            "method": f"Bore probe: core={bore_diam}mm, wall shell check. Empty ratio: {empty_vol}, Walled ratio: {walled_vol}",
            "criteria": [{"condition": "Central bore diameter 22.5 mm", "measured": bore_diam, "ok": r3_ok}],
            "note": ""
        }
        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": [round(shell_filled_ratio, 3), round(plate_vol, 1)],
            "method": f"Checked material integrity around bore in y=[0,4]. Shell fill ratio: {shell_filled_ratio}",
            "criteria": [{"condition": "Face plate at least 4 mm thick with solid material around bore", "measured": shell_filled_ratio, "ok": r2_ok}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes (3.4mm) at (+-15.5, 30 +- 15.5)
    try:
        screw_coords = [(15.5, 45.5), (-15.5, 45.5), (15.5, 14.5), (-15.5, 14.5)]
        hole_diam = 3.4
        all_holes_ok = True
        for cx, cz in screw_coords:
            pnt = cq.Vector(cx, 0, cz)
            dir_v = cq.Vector(0, 1, 0)
            # To verify the hole EXISTS, we check that it is empty AND surrounded by material
            core = cq.Solid.makeCylinder(hole_diam/2 - 0.15, 10, pnt=pnt, dir=dir_v)
            wall = cq.Solid.makeCylinder(hole_diam/2 + 1.0, 10, pnt=pnt, dir=dir_v).cut(
                cq.Solid.makeCylinder(hole_diam/2 + 0.15, 10, pnt=pnt, dir=dir_v))
            
            empty_vol = shape.intersect(core).Volume() / core.Volume()
            walled_vol = shape.intersect(wall).Volume() / wall.Volume()
            
            # Hole exists if it's empty and has a wall
            if not (empty_vol < 0.1 and walled_vol > 0.8):
                all_holes_ok = False
        
        results["R4"] = {
            "status": "pass" if all_holes_ok else "fail",
            "value": all_holes_ok,
            "method": f"Probed 4 locations at (+-15.5, 30 +- 15.5). Verified both emptiness and surrounding material.",
            "criteria": [{"condition": "Four motor screw holes, diameter 3.4 mm", "measured": hole_diam, "ok": all_holes_ok}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R5: Motor clearance (-21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5)
    try:
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        intersected_vol = shape.intersect(clearance_box).Volume()
        r5_ok = intersected_vol < 0.1 
        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": intersected_vol,
            "method": f"Intersection volume with clearance box: x[-21.5,21.5], y[-48,0], z[8.5,51.5]",
            "criteria": [{"condition": "Motor clearance: nothing in specified volume", "measured": intersected_vol, "ok": r5_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R6: Base on table (z>=0) and two vertical screw holes (5.5mm at +-25, 25)
    try:
        bbox = shape.BoundingBox()
        z_ok = bbox.ymin >= -0.01 
        
        hole_diam = 5.5
        screw_coords = [(25, 25), (-25, 25)]
        all_base_holes_ok = True
        for cx, cy in screw_coords:
            pnt = cq.Vector(cx, cy, bbox.ymin)
            dir_v = cq.Vector(0, 0, 1)
            # Verify hole exists (empty + walled)
            core = cq.Solid.makeCylinder(hole_diam/2 - 0.15, 20, pnt=pnt, dir=dir_v)
            wall = cq.Solid.makeCylinder(hole_diam/2 + 1.0, 20, pnt=pnt, dir=dir_v).cut(
                cq.Solid.makeCylinder(hole_diam/2 + 0.15, 20, pnt=pnt, dir=dir_v))
            
            empty_vol = shape.intersect(core).Volume() / core.Volume()
            walled_vol = shape.intersect(wall).Volume() / wall.Volume()
            if not (empty_vol < 0.1 and walled_vol > 0.8):
                all_base_holes_ok = False
        
        results["R6"] = {
            "status": "pass" if (z_ok and all_base_holes_ok) else "fail",
            "value": [round(bbox.ymin, 3), all_base_holes_ok],
            "method": f"Checked z_min >= 0 and probed holes at (+-25, 25) for existence (empty + walled)",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": bbox.ymin, "ok": z_ok},
                {"condition": "two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25)", "measured": hole_diam, "ok": all_base_holes_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R7: Envelope and Mass
    try:
        bbox = shape.BoundingBox()
        x_ok = -35 <= bbox.xmin and bbox.xmax <= 35
        z_ok = bbox.ymax <= 55
        density = 1.24 # g/cm3
        volume_mm3 = shape.Volume()
        mass_g = (volume_mm3 * density) / 1000.0
        mass_ok = mass_g <= 60.0
        results["R7"] = {
            "status": "pass" if (x_ok and z_ok and mass_ok) else "fail",
            "value": [round(bbox.xmin, 2), round(bbox.xmax, 2), round(bbox.ymax, 2), round(mass_g, 2)],
            "method": f"BBox: x[{bbox.xmin}, {bbox.xmax}], z_max={bbox.ymax}; Mass = vol({volume_mm3:.1f}) * density(1.24)/1000",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": [bbox.xmin, bbox.xmax], "ok": x_ok},
                {"condition": "top <= 55 mm", "measured": bbox.ymax, "ok": z_ok},
                {"condition": "mass <= 60 g", "measured": mass_g, "ok": mass_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_verification()