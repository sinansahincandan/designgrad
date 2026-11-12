import cadquery as cq
import trimesh
import numpy as np
import json

def run_checks():
    results = {}
    
    # Load geometry
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(f"Critical Error loading files: {e}")
        return

    # Constants
    DENSITY_PLA = 1.24 / 1000  # g/mm3
    
    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": f"Counted number of solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": n_solids == 1}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Floor thickness (z from 0 to 2 under board area)
    try:
        floor_box = cq.Solid.makeBox(80, 50, 2, pnt=cq.Vector(-40, -25, 0))
        intersected_vol = shape.intersect(floor_box).Volume()
        expected_vol = 80 * 50 * 2
        fill_ratio = intersected_vol / expected_vol
        status = "pass" if fill_ratio > 0.99 else "fail"
        results["R2"] = {
            "status": status,
            "value": fill_ratio,
            "method": f"Intersected floor region (80x50x2 at z=0) with part; ratio={fill_ratio:.4f}",
            "criteria": [{"condition": "solid floor at least 2 mm thick under whole board area", "measured": fill_ratio, "ok": fill_ratio > 0.99}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Board space (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32) must be free
    try:
        # To ensure the region is actually empty AND that there's material surrounding it (the floor/walls),
        # we check that the volume of intersection is near zero.
        # To address the reviewer's concern about a "1mm cube" passing, 
        # we verify that the board space is indeed empty by sampling or checking the volume.
        # The previous logic was correct for emptiness, but to ensure it isn't just "missing", 
        # we rely on R2 and R4 to prove existence of surrounding structure.
        board_space = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        intersected_vol = shape.intersect(board_space).Volume()
        # A tiny epsilon for floating point errors
        status = "pass" if intersected_vol < 0.1 else "fail"
        results["R3"] = {
            "status": status,
            "value": intersected_vol,
            "method": f"Intersected board space box (80x50x24 at z=8) with part; volume={intersected_vol:.4f}",
            "criteria": [{"condition": "region -40<=x<=40, -25<=y<=25, 8<=z<=32 must be completely free", "measured": intersected_vol, "ok": intersected_vol < 0.1}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Walls (85x55 +-1.5, top z 30-32.5)
    try:
        bbox = shape.BoundingBox()
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        z_max = bbox.zmax
        x_ok = 83.5 <= dx <= 86.5
        y_ok = 53.5 <= dy <= 56.5
        z_ok = 30.0 <= z_max <= 32.5
        status = "pass" if (x_ok and y_ok and z_ok) else "fail"
        results["R4"] = {
            "status": status,
            "value": [dx, dy, z_max],
            "method": f"Measured bounding box: dx={dx:.2f}, dy={dy:.2f}, zmax={z_max:.2f}",
            "criteria": [
                {"condition": "outer size 85x55 (+-1.5) in X and Y", "measured": [dx, dy], "ok": x_ok and y_ok},
                {"condition": "wall top at z between 30 and 32.5", "measured": z_max, "ok": z_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Four screw bosses at (+-35, +-20), OD >= 6mm, pilot hole 2.2mm (depth >= 4mm)
    try:
        boss_coords = [(35, 20), (-35, 20), (35, -20), (-35, -20)]
        boss_failures = []
        for cx, cy in boss_coords:
            # Check OD: probe a cylinder of radius 3.0 at z=4 (middle of boss)
            probe_od = cq.Solid.makeCylinder(3.0, 8, pnt=cq.Vector(cx, cy, 0))
            od_fill = shape.intersect(probe_od).Volume() / probe_od.Volume()
            
            # Check hole: pilot hole 2.2mm diameter (r=1.1) at the top of boss (z=8 down to z=4)
            probe_hole = cq.Solid.makeCylinder(1.1, 5, pnt=cq.Vector(cx, cy, 4)) 
            hole_empty_ratio = shape.intersect(probe_hole).Volume() / probe_hole.Volume()
            
            if od_fill < 0.9: boss_failures.append("OD")
            if hole_empty_ratio > 0.1: boss_failures.append("Hole Not Open")

        status = "pass" if not boss_failures else "fail"
        results["R5"] = {
            "status": status,
            "value": len(boss_failures),
            "method": f"Probed 4 bosses at (+-35, +-20) for OD (r=3) and hole emptiness (r=1.1)",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm, pilot hole 2.2mm open at top", "measured": boss_failures, "ok": not boss_failures}],
            "note": f"Failures: {boss_failures}" if boss_failures else ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout through -X wall (9mm Y, 3mm Z, centered at y=0, z=14)
    try:
        # To fix the reviewer's concern that a missing cutout passes because the cube is not there:
        # We must verify two things: 
        # 1. The specified volume IS empty (the hole exists).
        # 2. The surrounding wall material DOES exist (it's not just an empty space where the part is missing).
        
        # Probe 1: The cutout volume itself (must be empty)
        cutout_probe = cq.Solid.makeBox(10, 9, 3, pnt=cq.Vector(-47.5, -4.5, 12.5))
        intersected_vol = shape.intersect(cutout_probe).Volume()
        is_empty = intersected_vol < 0.5

        # Probe 2: The wall material around the cutout (must be solid)
        # We probe a small volume just outside the cutout in the X direction to ensure the -X wall exists.
        wall_probe = cq.Solid.makeBox(5, 15, 10, pnt=cq.Vector(-53, -7.5, 9))
        wall_intersected_vol = shape.intersect(wall_probe).Volume()
        is_walled = wall_intersected_vol > (wall_probe.Volume() * 0.8)

        status = "pass" if (is_empty and is_walled) else "fail"
        results["R6"] = {
            "status": status,
            "value": {"cutout_intersection": intersected_vol, "wall_presence": wall_intersected_vol},
            "method": f"Verified cutout emptiness (vol={intersected_vol:.2f}) and surrounding wall presence (vol={wall_intersected_vol:.2f})",
            "criteria": [{"condition": "USB-C cutout through the -X wall: opening >= 9mm (Y) and 3mm (Z)", "measured": status, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 70 g
    try:
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * DENSITY_PLA
        status = "pass" if mass_g <= 70.01 else "fail"
        results["R7"] = {
            "status": status,
            "value": mass_g,
            "method": f"Mass = Volume ({vol_mm3:.2f} mm3) * Density ({DENSITY_PLA*1000} g/cm3 / 1000)",
            "criteria": [{"condition": "Mass <= 70 g", "measured": mass_g, "ok": mass_g <= 70.01}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    run_checks()