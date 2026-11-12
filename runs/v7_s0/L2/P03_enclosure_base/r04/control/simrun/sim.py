import cadquery as cq
import trimesh
import numpy as np
import json

def check_requirements():
    results = {}
    # Load the part
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(f"Critical Error loading files: {e}")
        return

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": f"Counted solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Floor thickness (z from 0 to 2) under board area (-40..40, -25..25)
    try:
        floor_box = cq.Solid.makeBox(80, 50, 2, pnt=cq.Vector(-40, -25, 0))
        intersected_vol = shape.intersect(floor_box).Volume()
        target_vol = floor_box.Volume()
        fill_fraction = intersected_vol / target_vol
        status = "pass" if fill_fraction > 0.99 else "fail"
        results["R2"] = {
            "status": status,
            "value": fill_fraction,
            "method": f"Intersected floor box (80x50x2 at z=0) with part; ratio={fill_fraction:.4f}",
            "criteria": [{"condition": "solid floor at least 2 mm thick under board area", "measured": fill_fraction, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Board space (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32) must be empty
    try:
        board_space = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        intersected_vol = shape.intersect(board_space).Volume()
        fill_fraction = intersected_vol / board_space.Volume()
        status = "pass" if fill_fraction < 0.01 else "fail"
        results["R3"] = {
            "status": status,
            "value": fill_fraction,
            "method": f"Intersected board cavity (80x50x24 at z=8) with part; ratio={fill_fraction:.4f}",
            "criteria": [{"condition": "region -40<=x<=40, -25<=y<=25, 8<=z<=32 must be completely free of material", "measured": fill_fraction, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Walls (85x55 +/- 1.5mm; top z between 30 and 32.5)
    try:
        bbox = shape.BoundingBox()
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        z_top = bbox.zmax
        x_ok = 83.5 <= dx <= 86.5
        y_ok = 53.5 <= dy <= 56.5
        z_ok = 30.0 <= z_top <= 32.5
        status = "pass" if (x_ok and y_ok and z_ok) else "fail"
        results["R4"] = {
            "status": status,
            "value": [dx, dy, z_top],
            "method": f"Measured BoundingBox: dx={dx}, dy={dy}, zmax={z_top}",
            "criteria": [
                {"condition": "outer size 85 x 55 mm (+-1.5 mm) in X and Y", "measured": dx, "ok": x_ok},
                {"condition": "outer size 85 x 55 mm (+-1.5 mm) in X and Y", "measured": dy, "ok": y_ok},
                {"condition": "wall top at z between 30 and 32.5", "measured": z_top, "ok": z_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Four screw bosses at (+-35, +-20), OD >= 6mm, pilot hole 2.2mm, depth >= 4mm
    try:
        boss_coords = [(35, 20), (-35, 20), (35, -20), (-35, -20)]
        all_bosses_ok = True
        for bx, by in boss_coords:
            # Check OD >= 6mm. Probe with a cylinder of r=3.0 at z=0 to 8.
            boss_probe = cq.Solid.makeCylinder(3.0, 8.0, pnt=cq.Vector(bx, by, 0), dir=cq.Vector(0,0,1))
            fill_boss = shape.intersect(boss_probe).Volume() / boss_probe.Volume()
            
            # Check pilot hole (r=1.1) is empty at the top of the boss (z from 4 to 8)
            # The requirement says "at least 4mm deep" and bosses go up to z=8.
            hole_core = cq.Solid.makeCylinder(1.1, 4.0, pnt=cq.Vector(bx, by, 4.0), dir=cq.Vector(0,0,1))
            empty_ratio = shape.intersect(hole_core).Volume() / hole_core.Volume()
            
            # Check that the boss is solid around the hole (r=3.0)
            # We check a ring from r=1.2 to r=3.0 in the z=4..8 region
            wall_ring = cq.Solid.makeCylinder(3.0, 4.0, pnt=cq.Vector(bx, by, 4.0), dir=cq.Vector(0,0,1)).cut(
                        cq.Solid.makeCylinder(1.2, 4.0, pnt=cq.Vector(bx, by, 4.0), dir=cq.Vector(0,0,1)))
            wall_fill = shape.intersect(wall_ring).Volume() / wall_ring.Volume()

            if not (fill_boss > 0.95 and empty_ratio < 0.05 and wall_fill > 0.8):
                all_bosses_ok = False

        status = "pass" if all_bosses_ok else "fail"
        results["R5"] = {
            "status": status,
            "value": "All bosses checked",
            "method": f"Probed 4 bosses at (+-35, +-20). Checked cylinder fill, hole emptiness (r=1.1), and wall presence.",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... pilot hole 2.2mm... depth >= 4mm", "measured": status, "ok": all_bosses_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout through -X wall. Opening >= 9mm (Y) and 3mm (Z), centered at y=0, z=14
    try:
        y_req, z_req = 9.0, 3.0
        bbox = shape.BoundingBox()
        # The cutout is in the -X wall. We probe a volume that spans from x_min to inside the part.
        # To ensure it's an "opening", we check if the material is missing in this box.
        probe_x_start = bbox.xmin - 1.0
        probe_x_end = bbox.xmin + 15.0 # Sufficiently deep to cross the wall
        thickness = probe_x_end - probe_x_start
        
        # Center: y=0, z=14. Box dimensions: thickness (X), 9 (Y), 3 (Z)
        cutout_box = cq.Solid.makeBox(thickness, y_req, z_req, pnt=cq.Vector(probe_x_start, -y_req/2, 14 - z_req/2))
        
        # Check if the cutout volume is empty (material in it should be ~0)
        intersected_vol = shape.intersect(cutout_box).Volume()
        empty_ratio = intersected_vol / cutout_box.Volume()
        
        # To ensure it's an "opening", we check that the surrounding area is solid.
        # We use a slightly larger box and subtract the cutout to define the 'wall' region.
        surround_box = cq.Solid.makeBox(thickness, y_req + 10.0, z_req + 10.0, pnt=cq.Vector(probe_x_start, -(y_req+10.0)/2, 14 - (z_req+10.0)/2)).cut(cutout_box)
        walled_ratio = shape.intersect(surround_box).Volume() / surround_box.Volume()

        # Requirement: empty_ratio < 0.05 (it's a hole) and walled_ratio > 0.3 (it's in a wall)
        status = "pass" if (empty_ratio < 0.1 and walled_ratio > 0.3) else "fail"
        results["R6"] = {
            "status": status,
            "value": {"empty_ratio": empty_ratio, "walled_ratio": walled_ratio},
            "method": f"Checked cutout void (empty={empty_ratio:.4f}) and wall presence (walled={walled_ratio:.4f}) in -X wall.",
            "criteria": [{"condition": "opening at least 9 mm wide (Y) and 3 mm high (Z)", "measured": status, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 70 g. PLA density 1.24 g/cm3
    try:
        vol_mm3 = shape.Volume()
        mass_g = (vol_mm3 * 1.24) / 1000.0
        status = "pass" if mass_g <= 70.0 else "fail"
        results["R7"] = {
            "status": status,
            "value": mass_g,
            "method": f"Mass = (Volume {vol_mm3:.2f} mm3 * 1.24 g/cm3) / 1000",
            "criteria": [{"condition": "Mass <= 70 g", "measured": mass_g, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    check_requirements()