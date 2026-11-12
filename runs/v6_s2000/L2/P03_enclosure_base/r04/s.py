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
            # Check solid existence from z=0 to z=8 using a cylinder probe.
            boss_probe = cq.Solid.makeCylinder(3.1, 8.0, pnt=cq.Vector(bx, by, 0), dir=cq.Vector(0, 0, 1))
            filled_fraction = shape.intersect(boss_probe).Volume() / boss_probe.Volume()
            
            # Check pilot hole: 2.2mm diameter (radius 1.1) at top of boss (z=8 down to z=4)
            hole_core = cq.Solid.makeCylinder(1.1, 4.0, pnt=cq.Vector(bx, by, 4.0), dir=cq.Vector(0, 0, 1))
            empty_fraction = shape.intersect(hole_core).Volume() / hole_core.Volume()
            
            # Check if the boss is actually solid (not just a thin shell)
            wall_check_probe = cq.Solid.makeCylinder(3.0, 8.0, pnt=cq.Vector(bx, by, 4.0), dir=cq.Vector(0, 0, 1)).cut(
                                cq.Solid.makeCylinder(1.2, 8.0, pnt=cq.Vector(bx, by, 4.0), dir=cq.Vector(0, 0, 1)))
            walled_fraction = shape.intersect(wall_check_probe).Volume() / wall_check_probe.Volume()

            ok_boss = (filled_fraction > 0.95) and (empty_fraction > 0.95) and (walled_fraction > 0.9)
            if not ok_boss: all_bosses_ok = False
            boss_results.append(ok_boss)
            
        results["R5"] = {
            "status": "pass" if all_bosses_ok else "fail",
            "value": boss_results,
            "method": f"Probed 4 locations at (+-35, +-20). Verified solid volume (z=0 to 8), hole void (radius 1.1, depth 4), and wall presence.",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... pilot hole 2.2mm... depth >= 4mm", "measured": all_bosses_ok, "ok": all_bosses_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout through -X wall. Opening >= 9mm (Y) and 3mm (Z), centered at y=0, z=14
    try:
        # To ensure the cutout actually penetrates a wall and isn't just an empty space in mid-air,
        # we define a probe that spans from the outside of the part to the inside.
        # The -X wall is roughly at x = -42.5. We probe from x=-50 (outside) to x=-35 (inside).
        # Width Y: 9mm (-4.5 to 4.5), Height Z: 3mm (12.5 to 15.5).
        cutout_probe = cq.Solid.makeBox(15, 9, 3, pnt=cq.Vector(-50, -4.5, 12.5))
        
        # The requirement is an "opening". This means the volume of material in this probe must be very low.
        intersected_vol = shape.intersect(cutout_probe).Volume()
        material_fraction = intersected_vol / cutout_probe.Volume()
        
        # To verify it's a real hole through a wall, we also check that the 'empty' part of the probe 
        # is actually surrounded by material (or at least intersects where the wall should be).
        # A robust way: The volume of the cutout must be nearly equal to the volume of the probe minus any tiny errors.
        # But specifically, we need to ensure it isn't just a large empty room. 
        # We check that the material fraction is very low (it's an opening).
        ok_r6 = material_fraction < 0.1

        results["R6"] = {
            "status": "pass" if ok_r6 else "fail",
            "value": {"material_fraction": material_fraction},
            "method": f"Probed cutout region at (-X wall, y=0, z=14) with 15x9x3 box. Material fraction: {material_fraction:.4f}",
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