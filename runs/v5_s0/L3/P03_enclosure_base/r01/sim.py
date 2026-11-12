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

    results = {}

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        is_single = (n_solids == 1)
        results["R1"] = {
            "status": "pass" if is_single else "fail",
            "value": n_solids,
            "method": f"Counted number of solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": is_single}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Floor thickness (z from 0 to 2 under board area)
    try:
        board_footprint = cq.Solid.makeBox(80, 50, 2, pnt=cq.Vector(-40, -25, 0))
        intersection_vol = shape.intersect(board_footprint).Volume()
        target_vol = board_footprint.Volume()
        fill_ratio = intersection_vol / target_vol
        bbox = shape.BoundingBox()
        floor_z_ok = abs(bbox.zmin) < 0.01
        results["R2"] = {
            "status": "pass" if (fill_ratio > 0.99 and floor_z_ok) else "fail",
            "value": fill_ratio,
            "method": f"Intersection volume of part with box [-40,40]x[-25,25]x[0,2]. Ratio: {fill_ratio:.3f}",
            "criteria": [
                {"condition": "solid floor at least 2 mm thick (z from 0 to 2) under the whole board area", "measured": fill_ratio, "ok": fill_ratio > 0.99},
                {"condition": "floor starts at z=0", "measured": bbox.zmin, "ok": floor_z_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Board space (completely free of material)
    try:
        board_space = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        intersection_vol = shape.intersect(board_space).Volume()
        is_free = intersection_vol < 1e-3 
        results["R3"] = {
            "status": "pass" if is_free else "fail",
            "value": intersection_vol,
            "method": f"Intersection volume of part with board space box [-40,40]x[-25,25]x[8,32]. Vol: {intersection_vol:.4f}",
            "criteria": [{"condition": "region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be completely free", "measured": intersection_vol, "ok": is_free}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Walls (85x55 +/- 1.5, top z between 30-32.5)
    try:
        bbox = shape.BoundingBox()
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        top_z = bbox.zmax
        x_ok = 83.5 <= dx <= 86.5
        y_ok = 53.5 <= dy <= 56.5
        z_ok = 30.0 <= top_z <= 32.5
        results["R4"] = {
            "status": "pass" if (x_ok and y_ok and z_ok) else "fail",
            "value": [dx, dy, top_z],
            "method": f"Measured bounding box: dx={dx:.2f}, dy={dy:.2f}, zmax={top_z:.2f}",
            "criteria": [
                {"condition": "outer size 85 x 55 mm (+-1.5 mm) in X and Y", "measured": [dx, dy], "ok": x_ok and y_ok},
                {"condition": "wall top at z between 30 and 32.5", "measured": top_z, "ok": z_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Four screw bosses at (+-35, +-20), OD >= 6mm, pilot hole 2.2mm (depth >= 4mm)
    try:
        boss_coords = [(35, 20), (35, -20), (-35, 20), (-35, -20)]
        boss_results = []
        for cx, cy in boss_coords:
            # To verify the boss exists, we check if a cylinder of diameter 6mm is mostly solid.
            probe_od = cq.Solid.makeCylinder(3.0, 8, pnt=cq.Vector(cx, cy, 0), dir=cq.Vector(0,0,1))
            vol_od = shape.intersect(probe_od).Volume() / probe_od.Volume()
            
            # To verify the hole exists, we check if a cylinder of diameter 2.2mm is mostly empty at the top (z:4-8)
            # AND that there is actually material around it (the boss itself).
            probe_hole = cq.Solid.makeCylinder(1.1, 4, pnt=cq.Vector(cx, cy, 4), dir=cq.Vector(0,0,1))
            vol_hole_ratio = shape.intersect(probe_hole).Volume() / probe_hole.Volume()
            
            # Check that the hole is actually inside a boss (the material at z:0-4 should be solid)
            probe_base = cq.Solid.makeCylinder(3.0, 4, pnt=cq.Vector(cx, cy, 0), dir=cq.Vector(0,0,1))
            vol_base_ratio = shape.intersect(probe_base).Volume() / probe_base.Volume()

            boss_results.append({
                "od_ok": vol_od > 0.95, 
                "hole_ok": vol_hole_ratio < 0.05,
                "base_ok": vol_base_ratio > 0.95
            })
            
        all_bosses_ok = all(b["od_ok"] and b["hole_ok"] and b["base_ok"] for b in boss_results)
        results["R5"] = {
            "status": "pass" if all_bosses_ok else "fail",
            "value": boss_results,
            "method": f"Checked 4 bosses at (+-35, +-20). Verified OD (r=3.0) fill, hole (r=1.1, z:4-8) emptiness, and base (r=3.0, z:0-4) presence.",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... pilot hole 2.2mm... depth at least 4mm", "measured": all_bosses_ok, "ok": all_bosses_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout on -X wall (9mm Y, 3mm Z, centered at y=0, z=14)
    try:
        # Cutout dimensions: Width 9 (Y), Height 3 (Z). Center y=0, z=14.
        # Probe box spans the thickness of the wall on the -X side.
        cutout_probe = cq.Solid.makeBox(10, 9, 3, pnt=cq.Vector(-45, -4.5, 12.5))
        vol_in_cutout = shape.intersect(cutout_probe).Volume()
        is_empty = vol_in_cutout < 1e-2

        # To ensure the cutout is actually IN a wall (and not just empty space), 
        # we check that there is material immediately to the left and right of the cutout in X.
        probe_left = cq.Solid.makeBox(5, 10, 10, pnt=cq.Vector(-50, -5, 9))
        probe_right = cq.Solid.makeBox(5, 10, 10, pnt=cq.Vector(-40, -5, 9))
        has_wall_material = (shape.intersect(probe_left).Volume() > 1.0 and shape.intersect(probe_right).Volume() > 1.0)

        results["R6"] = {
            "status": "pass" if (is_empty and has_wall_material) else "fail",
            "value": vol_in_cutout,
            "method": f"Cutout probe [-45,-4.5]x[-4.5,4.5]x[12.5,15.5]. Vol: {vol_in_cutout:.4f}. Wall presence check (material flanking cutout): {has_wall_material}",
            "criteria": [{"condition": "USB-C cutout... opening at least 9 mm wide (Y) and 3 mm high (Z), centred at y = 0, z = 14", "measured": is_empty, "ok": is_empty}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 70g (Density 1.24 g/cm3)
    try:
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * 1.24 / 1000.0
        results["R7"] = {
            "status": "pass" if mass_g <= 70.0 else "fail",
            "value": mass_g,
            "method": f"Mass = Volume ({vol_mm3:.2f} mm3) * Density (1.24 g/cm3) / 1000",
            "criteria": [{"condition": "Mass <= 70 g", "measured": mass_g, "ok": mass_g <= 70.0}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()