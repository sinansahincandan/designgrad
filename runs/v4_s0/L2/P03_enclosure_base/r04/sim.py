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

    # R2: Floor thickness (z from 0 to 2) under board area (-40<=x<=40, -25<=y<=25)
    try:
        floor_region = cq.Solid.makeBox(80, 50, 2, pnt=cq.Vector(-40, -25, 0))
        intersected_vol = shape.intersect(floor_region).Volume()
        target_vol = floor_region.Volume()
        fill_ratio = intersected_vol / target_vol
        bbox = shape.BoundingBox()
        z_min = bbox.zmin
        status = "pass" if fill_ratio > 0.98 and z_min <= 0.1 else "fail"
        results["R2"] = {
            "status": status,
            "value": {"fill_ratio": fill_ratio, "z_min": z_min},
            "method": f"Intersection volume of floor region (80x50x2 at z=0) with part: {intersected_vol} mm3",
            "criteria": [
                {"condition": "solid floor at least 2 mm thick under the whole board area", "measured": fill_ratio, "ok": fill_ratio > 0.98},
                {"condition": "floor z from 0 to 2", "measured": z_min, "ok": z_min <= 0.1}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Board space (-40<=x<=40, -25<=y<=25, 8<=z<=32) must be free
    try:
        board_space = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        intersected_vol = shape.intersect(board_space).Volume()
        status = "pass" if intersected_vol < 1.0 else "fail"
        results["R3"] = {
            "status": status,
            "value": intersected_vol,
            "method": f"Intersection volume of board cavity region (80x50x24 at z=8) with part: {intersected_vol} mm3",
            "criteria": [{"condition": "region -40<=x<=40, -25<=y<=25, 8<=z<=32 must be completely free of material", "measured": intersected_vol, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Walls (85x55 +/- 1.5, top z 30-32.5)
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
            "method": f"Measured Bounding Box: dx={dx}, dy={dy}, zmax={z_max}",
            "criteria": [
                {"condition": "outer size 85 x 55 mm (+-1.5 mm) in X and Y", "measured": [dx, dy], "ok": x_ok and y_ok},
                {"condition": "wall top at z between 30 and 32.5", "measured": z_max, "ok": z_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Four screw bosses (+-35, +-20), OD >= 6, pilot hole 2.2, depth >= 4
    try:
        boss_coords = [(35, 20), (35, -20), (-35, 20), (-35, -20)]
        bosses_ok = 0
        for cx, cy in boss_coords:
            probe_od = cq.Solid.makeCylinder(3.0, 8.0, pnt=cq.Vector(cx, cy, 0))
            vol_od_region = shape.intersect(probe_od).Volume()
            expected_min_vol = np.pi * (3.0**2 - 1.1**2) * 8.0 * 0.9
            od_ok = vol_od_region >= expected_min_vol

            probe_hole = cq.Solid.makeCylinder(1.1, 8.0, pnt=cq.Vector(cx, cy, 0))
            vol_hole_region = shape.intersect(probe_hole).Volume()
            hole_diam_ok = vol_hole_region < 1.0

            probe_depth = cq.Solid.makeCylinder(1.1, 4.0, pnt=cq.Vector(cx, cy, 4))
            vol_depth_region = shape.intersect(probe_depth).Volume()
            depth_ok = vol_depth_region < 1.0

            if od_ok and hole_diam_ok and depth_ok:
                bosses_ok += 1
        
        status = "pass" if bosses_ok == 4 else "fail"
        results["R5"] = {
            "status": status,
            "value": bosses_ok,
            "method": f"Verified 4 bosses: OD (vol check), Hole Diameter (empty cylinder r=1.1), and Depth (empty cylinder z=4-8)",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... pilot hole 2.2mm... depth >= 4mm", "measured": bosses_ok, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout (-X wall), 9mm (Y) x 3mm (Z), centered at y=0, z=14
    try:
        # The wall is located around x = -42.5. We probe a box that spans the thickness of the wall.
        # A typical wall thickness for an 85x55 outer / 80x50 inner enclosure is ~2.5mm.
        # Let's probe from x=-45 to x=-40 to ensure we capture the full cutout through the wall.
        cutout_probe = cq.Solid.makeBox(5, 9, 3, pnt=cq.Vector(-45, -4.5, 12.5))
        intersected_vol = shape.intersect(cutout_probe).Volume()
        # Requirement: The cutout must exist. If the intersection volume is near zero, it means material was removed.
        # We check if the intersection of the part with this "cutout zone" is very small (the remaining wall edges).
        status = "pass" if intersected_vol < 2.0 else "fail"
        results["R6"] = {
            "status": status,
            "value": intersected_vol,
            "method": f"Intersection volume of cutout probe box (5x9x3 at x=-42.5, y=0, z=14) with part: {intersected_vol} mm3",
            "criteria": [{"condition": "opening at least 9 mm wide (Y) and 3 mm high (Z), centred at y = 0, z = 14", "measured": intersected_vol, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 70g (Density 1.24 g/cm3)
    try:
        vol_mm3 = mesh.volume
        mass_g = vol_mm3 * 1.24 / 1000.0
        status = "pass" if mass_g <= 70.0 else "fail"
        results["R7"] = {
            "status": status,
            "value": mass_g,
            "method": f"Mass calculation: volume({vol_mm3:.2f} mm3) * density(1.24 g/cm3) / 1000",
            "criteria": [{"condition": "Mass <= 70 g", "measured": mass_g, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()