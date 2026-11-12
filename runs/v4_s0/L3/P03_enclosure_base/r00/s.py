import cadquery as cq
import trimesh
import numpy as np
import json

def solve():
    try:
        # Load the part
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    results = {}

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        valid = True # Assuming metrics.json or shape check
        # Check validity via trimesh if possible, but we use n_solids from cq
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": f"Counted number of solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Floor thickness (z from 0 to 2 under board area)
    try:
        # Board area: -40 <= x <= 40, -25 <= y <= 25
        # Check if material exists at z=1 (middle of floor) within the footprint
        # Or more robustly: check volume of intersection with a box [min_x, max_x, min_y, max_y, 0, 2]
        floor_box = cq.Solid.makeBox(80, 50, 2, pnt=cq.Vector(-40, -25, 0))
        intersection_vol = shape.intersect(floor_box).Volume()
        target_vol = 80 * 50 * 2
        fill_ratio = intersection_vol / target_vol
        
        # Requirement: "solid floor at least 2mm thick under the whole board area"
        # We check if the volume is nearly 100% of the specified box.
        status = "pass" if fill_ratio > 0.95 else "fail"
        results["R2"] = {
            "status": status,
            "value": fill_ratio,
            "method": f"Intersection volume of part with floor region [-40,40]x[-25,25]x[0,2] divided by region volume ({target_vol})",
            "criteria": [{"condition": "solid floor at least 2 mm thick under the whole board area", "measured": fill_ratio, "ok": status == "pass"}],
            "note": f"Fill ratio: {fill_ratio:.3f}"
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Board space (completely free of material)
    try:
        # Region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32
        board_space = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        intersect_vol = shape.intersect(board_space).Volume()
        # "Completely free" means intersection volume should be ~0
        status = "pass" if intersect_vol < 1e-3 else "fail"
        results["R3"] = {
            "status": status,
            "value": intersect_vol,
            "method": f"Intersection volume with board space box [-40,40]x[-25,25]x[8,32]",
            "criteria": [{"condition": "region ... must be completely free of material", "measured": intersect_vol, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Walls (Outer size 85x55 +-1.5; top z between 30 and 32.5)
    try:
        bbox = shape.BoundingBox()
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        z_max = bbox.zmax
        
        # Check dimensions
        dim_x_ok = 83.5 <= dx <= 86.5
        dim_y_ok = 53.5 <= dy <= 56.5
        # Check top height (assuming floor is at z=0)
        z_ok = 30.0 <= z_max <= 32.5
        
        status = "pass" if (dim_x_ok and dim_y_ok and z_ok) else "fail"
        results["R4"] = {
            "status": status,
            "value": [round(dx, 2), round(dy, 2), round(z_max, 2)],
            "method": f"Bounding box dimensions: dx={dx}, dy={dy}, zmax={z_max}",
            "criteria": [
                {"condition": "outer size 85 x 55 mm (+-1.5 mm) in X and Y", "measured": [dx, dy], "ok": dim_x_ok and dim_y_ok},
                {"condition": "wall top at z between 30 and 32.5", "measured": z_max, "ok": z_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Four screw bosses at (+-35, +-20), OD >= 6mm, pilot hole 2.2mm, depth >= 4mm
    try:
        boss_coords = [(35, 20), (35, -20), (-35, 20), (-35, -20)]
        boss_failures = []
        for cx, cy in boss_coords:
            # Check OD: Intersection with cylinder of radius 3 at (cx, cy) from z=0 to 8
            # Actually the requirement says "from floor up to z=8". Floor is at z=0.
            check_cyl = cq.Solid.makeCylinder(3.0, 8.0, pnt=cq.Vector(cx, cy, 0))
            vol_boss = shape.intersect(check_cyl).Volume()
            # Ideal volume of a 6mm dia, 8mm high cylinder is pi * 3^2 * 8 = 226.19
            # We check if the intersection volume is close to this (accounting for pilot hole)
            # Pilot hole: radius 1.1, depth 4. Vol_hole = pi * 1.1^2 * 4 = 15.2
            expected_vol = (np.pi * 3**2 * 8) - (np.pi * 1.1**2 * 4)
            if abs(vol_boss - expected_vol) > 10: # tolerance for small geometry variations
                boss_failures.append(f"Boss at {cx},{cy} failed volume check")

            # Check pilot hole depth: probe the center (cx, cy) from z=8 downwards
            # The hole must be open at its top (z=8) and go down to at least z=4.
            # We'll use a small cylinder of radius 1.1 and check if it is 'empty' in the part.
            # Wait, "pilot hole open at its top" means material should NOT be there.
            probe_hole = cq.Solid.makeCylinder(1.1, 4.0, pnt=cq.Vector(cx, cy, 4))
            hole_vol_in_part = shape.intersect(probe_hole).Volume()
            if hole_vol_in_part > 0.5: # If there's material in the probe cylinder, hole is not deep enough or blocked
                boss_failures.append(f"Boss at {cx},{cy} pilot hole depth/clearance fail")

        status = "pass" if not boss_failures else "fail"
        results["R5"] = {
            "status": status,
            "value": len(boss_failures),
            "method": f"Checked 4 bosses at (+-35, +-20) for volume and pilot hole clearance (r=1.1, depth=4)",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... pilot hole 2.2mm... hole at least 4mm deep", "measured": len(boss_failures), "ok": status == "pass"}],
            "note": "; ".join(boss_failures) if boss_failures else ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout through -X wall (9mm Y, 3mm Z, centered at y=0, z=14)
    try:
        # Cutout region: x < 0, y in [-4.5, 4.5], z in [12.5, 15.5]
        cutout_box = cq.Solid.makeBox(100, 9, 3, pnt=cq.Vector(-50, -4.5, 12.5))
        # The requirement says "cutout through the -X wall". This implies a hole exists.
        # We check if the volume of intersection is near zero (meaning it's empty).
        intersect_vol = shape.intersect(cutout_box).Volume()
        status = "pass" if intersect_vol < 5.0 else "fail" # Allow small tolerance for mesh/precision
        results["R6"] = {
            "status": status,
            "value": intersect_vol,
            "method": f"Intersection volume with cutout box [-50, -4.5, 12.5] to [50, 4.5, 15.5]",
            "criteria": [{"condition": "opening at least 9 mm wide (Y) and 3 mm high (Z), centred at y = 0, z = 14", "measured": intersect_vol, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 70 g (PLA density 1.24 g/cm3)
    try:
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * 1.24 / 1000.0
        status = "pass" if mass_g <= 70.0 else "fail"
        results["R7"] = {
            "status": status,
            "value": round(mass_g, 3),
            "method": f"Volume ({vol_mm3:.2f} mm3) * density (1.24 g/cm3) / 1000",
            "criteria": [{"condition": "Mass <= 70 g", "measured": mass_g, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()