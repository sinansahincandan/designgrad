import cadquery as cq
import trimesh
import numpy as np
import json

def check_requirements():
    results = {}
    
    # Load geometry
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
        n_solids = len(shape.Solids())
        volume = shape.Volume()
        bbox = shape.BoundingBox()
    except Exception as e:
        print(f"Critical error loading files: {e}")
        return

    # R1: One single, valid solid
    try:
        valid_r1 = (n_solids == 1)
        results["R1"] = {
            "status": "pass" if valid_r1 else "fail",
            "value": n_solids,
            "method": "Counted number of solids in the STEP file.",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": valid_r1}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Floor thickness (z from 0 to 2 under board area)
    try:
        floor_probe = cq.Solid.makeBox(80, 50, 2, pnt=cq.Vector(-40, -25, 0))
        intersected_vol = shape.intersect(floor_probe).Volume()
        target_vol = floor_probe.Volume()
        filled_fraction = intersected_vol / target_vol
        ok_r2 = filled_fraction > 0.99
        results["R2"] = {
            "status": "pass" if ok_r2 else "fail",
            "value": filled_fraction,
            "method": f"Intersection volume of part with floor probe box (80x50x2 at z=0) / probe volume. Filled fraction: {filled_fraction:.4f}",
            "criteria": [{"condition": "solid floor at least 2 mm thick under the whole board area", "measured": filled_fraction, "ok": ok_r2}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Board space (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32) must be free
    try:
        void_probe = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        intersected_vol = shape.intersect(void_probe).Volume()
        empty_fraction = intersected_vol / void_probe.Volume()
        ok_r3 = empty_fraction < 0.01 
        results["R3"] = {
            "status": "pass" if ok_r3 else "fail",
            "value": empty_fraction,
            "method": f"Intersection volume of part with void probe box (80x50x24 at z=8) / probe volume. Empty fraction: {empty_fraction:.4f}",
            "criteria": [{"condition": "-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be completely free of material", "measured": empty_fraction, "ok": ok_r3}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Walls (85x55 +-1.5mm; top z 30-32.5)
    try:
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        dz_top = bbox.zmax
        ok_dx = 83.5 <= dx <= 86.5
        ok_dy = 53.5 <= dy <= 56.5
        ok_dz = 30.0 <= dz_top <= 32.5
        results["R4"] = {
            "status": "pass" if (ok_dx and ok_dy and ok_dz) else "fail",
            "value": [round(dx, 2), round(dy, 2), round(dz_top, 2)],
            "method": f"Measured bounding box dimensions: dx={dx}, dy={dy}, zmax={dz_top}",
            "criteria": [
                {"condition": "outer size 85 x 55 mm (+-1.5 mm) in X and Y", "measured": [dx, dy], "ok": ok_dx and ok_dy},
                {"condition": "wall top at z between 30 and 32.5", "measured": dz_top, "ok": ok_dz}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Four screw bosses at (+-35, +-20), OD >= 6mm, pilot hole 2.2mm (depth >= 4mm)
    try:
        boss_coords = [(35, 20), (-35, 20), (35, -20), (-35, -20)]
        boss_results = []
        all_bosses_ok = True
        for bx, by in boss_coords:
            # Check OD: Probe from z=0 to z=8. Cylinder radius 3.1 (OD 6.2)
            od_probe = cq.Solid.makeCylinder(3.1, 8.0, pnt=cq.Vector(bx, by, 0), dir=cq.Vector(0, 0, 1))
            filled_fraction = shape.intersect(od_probe).Volume() / od_probe.Volume()
            
            # Check Pilot Hole: A hole at the top (z=4 to z=8) must be empty. Diameter 2.2 -> radius 1.1
            hole_probe = cq.Solid.makeCylinder(1.1, 4.0, pnt=cq.Vector(bx, by, 4), dir=cq.Vector(0, 0, 1))
            empty_fraction = shape.intersect(hole_probe).Volume() / hole_probe.Volume()
            
            # Check Wall integrity: A ring around the hole must be solid
            wall_ring = cq.Solid.makeCylinder(3.1, 4.0, pnt=cq.Vector(bx, by, 4), dir=cq.Vector(0, 0, 1)).cut(
                        cq.Solid.makeCylinder(1.2, 4.0, pnt=cq.Vector(bx, by, 4), dir=cq.Vector(0, 0, 1)))
            walled_fraction = shape.intersect(wall_ring).Volume() / wall_ring.Volume()

            # Criteria: OD >= 6 (filled fraction high), Hole exists (empty fraction ~0), Wall is solid (walled fraction high)
            ok_boss = (filled_fraction > 0.95) and (empty_fraction < 0.05) and (walled_fraction > 0.95)
            if not ok_boss: all_bosses_ok = False
            boss_results.append(ok_boss)

        results["R5"] = {
            "status": "pass" if all_bosses_ok else "fail",
            "value": boss_results,
            "method": f"Probed 4 locations at (+-35, +-20). Checked OD (z:0-8), hole (z:4-8, empty), and wall thickness.",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... pilot hole 2.2mm... depth >= 4mm", "measured": all_bosses_ok, "ok": all_bosses_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout through -X wall. Opening >= 9mm (Y) and 3mm (Z), centered at y=0, z=14
    try:
        # The opening is in the -X wall. We probe a box that spans the wall thickness.
        # Wall is roughly at x = -42.5. Box from x=-45 to x=-40.
        # Opening requirement: Y width 9, Z height 3. Centered y=0, z=14 -> y range [-4.5, 4.5], z range [12.5, 15.5]
        cutout_probe = cq.Solid.makeBox(5, 9, 3, pnt=cq.Vector(-45, -4.5, 12.5))
        
        # To verify it's a hole THROUGH the wall:
        # 1. The probe volume must be empty (empty_fraction ~0)
        # 2. There must be material in the vicinity of the cutout to form a wall
        empty_fraction = shape.intersect(cutout_probe).Volume() / cutout_probe.Volume()
        
        # Check if there is actually material around it by checking a larger volume that includes the wall
        wall_check_volume = cq.Solid.makeBox(10, 20, 10, pnt=cq.Vector(-50, -10, 9))
        material_in_vicinity = shape.intersect(wall_check_volume).Volume()
        
        # A real cutout means the probe is empty AND there's significant material around it (the wall)
        ok_r6 = (empty_fraction < 0.05) and (material_in_vicinity > 100)

        results["R6"] = {
            "status": "pass" if ok_r6 else "fail",
            "value": {"empty_fraction": empty_fraction, "vicinity_material": material_in_vicinity},
            "method": f"Probed cutout void (empty fraction: {empty_fraction:.4f}) and surrounding wall volume.",
            "criteria": [{"condition": "USB-C cutout... opening at least 9 mm wide (Y) and 3 mm high (Z)", "measured": ok_r6, "ok": ok_r6}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 70 g. PLA density 1.24 g/cm3
    try:
        density_g_mm3 = 1.24 / 1000.0
        mass = volume * density_g_mm3
        ok_r7 = mass <= 70.001
        results["R7"] = {
            "status": "pass" if ok_r7 else "fail",
            "value": round(mass, 2),
            "method": f"Mass = Volume ({volume:.2f} mm3) * Density (0.00124 g/mm3)",
            "criteria": [{"condition": "Mass <= 70 g", "measured": mass, "ok": ok_r7}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    check_requirements()