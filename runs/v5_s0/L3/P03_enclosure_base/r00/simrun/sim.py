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
        boss_pass = []
        for cx, cy in boss_coords:
            # Check OD: Probe a cylinder of radius 3.0mm from z=0 to z=8 (the boss height)
            probe_od = cq.Solid.makeCylinder(3.0, 8, pnt=cq.Vector(cx, cy, 0), dir=cq.Vector(0,0,1))
            vol_od = shape.intersect(probe_od).Volume() / probe_od.Volume()
            
            # Check Pilot Hole: The hole must be at least 4mm deep relative to the boss top (z=8)
            # So the hole must exist from z=4 up to z=8.
            # We check if a cylinder of radius 1.1mm is empty in that specific range.
            probe_hole = cq.Solid.makeCylinder(1.1, 4, pnt=cq.Vector(cx, cy, 4), dir=cq.Vector(0,0,1))
            vol_hole = shape.intersect(probe_hole).Volume() / probe_hole.Volume()
            
            # Requirement: OD >= 6mm (r>=3) and hole is empty in the top 4mm of boss height.
            boss_pass.append(vol_od > 0.98 and vol_hole < 0.02)
            
        all_bosses_ok = all(boss_pass)
        results["R5"] = {
            "status": "pass" if all_bosses_ok else "fail",
            "value": boss_pass,
            "method": f"Checked 4 bosses at (+-35, +-20). OD probe (r=3.0) fill ratio and hole depth probe (r=1.1, z:4-8) empty ratio.",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... pilot hole 2.2mm... depth at least 4mm", "measured": all_bosses_ok, "ok": all_bosses_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout on -X wall (9mm Y, 3mm Z, centered at y=0, z=14)
    try:
        # Probe the specific volume where the cutout should be.
        # Center is y=0, z=14. Width 9 -> y from -4.5 to 4.5. Height 3 -> z from 12.5 to 15.5.
        # We place it in the wall (x approx -42.5).
        cutout_box = cq.Solid.makeBox(10, 9, 3, pnt=cq.Vector(-48, -4.5, 12.5))
        vol_in_cutout = shape.intersect(cutout_box).Volume()
        is_empty = vol_in_cutout < 0.1

        # Verify wall existence nearby to ensure we aren't just measuring empty space in the air
        wall_check_box = cq.Solid.makeBox(5, 30, 30, pnt=cq.Vector(-48, -15, 0))
        has_material_in_region = shape.intersect(wall_check_box).Volume() > 50.0

        results["R6"] = {
            "status": "pass" if (is_empty and has_material_in_region) else "fail",
            "value": vol_in_cutout,
            "method": f"Cutout probe [-48,-38]x[-4.5,4.5]x[12.5,15.5]. Vol: {vol_in_cutout:.4f}. Wall presence check: {has_material_in_region}",
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