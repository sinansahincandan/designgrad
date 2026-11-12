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
        print(f"Critical error loading files: {e}")
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

    # R2: Floor thickness (z from 0 to 2 under board area)
    try:
        floor_box = cq.Solid.makeBox(80, 50, 2, pnt=cq.Vector(-40, -25, 0))
        intersected_vol = shape.intersect(floor_box).Volume()
        target_vol = floor_box.Volume()
        fill_fraction = intersected_vol / target_vol
        status = "pass" if fill_fraction > 0.99 else "fail"
        results["R2"] = {
            "status": status,
            "value": fill_fraction,
            "method": f"Intersected floor box (80x50x2) with part; ratio={fill_fraction:.4f}",
            "criteria": [{"condition": "solid floor at least 2 mm thick under board area", "measured": fill_fraction, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Board space (completely free of material)
    # FIX: To ensure the region is actually a cavity within an enclosure and not just empty air, 
    # we check that the volume is zero AND that the boundary of this box is enclosed by the part.
    try:
        board_space = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        intersected_vol = shape.intersect(board_space).Volume()
        
        # To verify it's a "space" inside an enclosure, we probe the boundary of the box.
        # If the space is truly enclosed, material should exist at the boundaries (walls/floor/ceiling) 
        # just outside this volume. We check if the part exists in a thin shell surrounding the board space.
        shell_thickness = 1.0
        outer_shell = cq.Solid.makeBox(80 + 2*shell_thickness, 50 + 2*shell_thickness, 24 + 2*shell_thickness, 
                                      pnt=cq.Vector(-40-shell_thickness, -25-shell_thickness, 8-shell_thickness))
        inner_space = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        boundary_shell = outer_shell.cut(inner_space)
        shell_intersect_vol = shape.intersect(boundary_shell).Volume()
        shell_fill_ratio = shell_intersect_vol / boundary_shell.Volume()

        # Requirement: Volume in box is ~0 AND the part exists around it (shell_fill_ratio > 0)
        space_is_empty = intersected_vol < 0.1
        space_is_enclosed = shell_fill_ratio > 0.1 # Significant material must exist to form walls/floor
        
        status = "pass" if (space_is_empty and space_is_enclosed) else "fail"
        results["R3"] = {
            "status": status,
            "value": {"intersected_vol": intersected_vol, "shell_fill_ratio": shell_fill_ratio},
            "method": f"Verified board space volume is ~0 and boundary shell has material (ratio={shell_fill_ratio:.4f})",
            "criteria": [{"condition": "-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be completely free of material", "measured": status, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Walls (85x55 +-1.5, top z 30-32.5)
    try:
        bbox = shape.BoundingBox()
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        z_top = bbox.zmax
        dim_x_ok = 83.5 <= dx <= 86.5
        dim_y_ok = 53.5 <= dy <= 56.5
        z_ok = 30.0 <= z_top <= 32.5
        status = "pass" if (dim_x_ok and dim_y_ok and z_ok) else "fail"
        results["R4"] = {
            "status": status,
            "value": [round(dx, 2), round(dy, 2), round(z_top, 2)],
            "method": f"Measured BoundingBox: dx={dx}, dy={dy}, zmax={z_top}",
            "criteria": [
                {"condition": "outer size 85 x 55 mm (+-1.5)", "measured": [dx, dy], "ok": dim_x_ok and dim_y_ok},
                {"condition": "wall top at z between 30 and 32.5", "measured": z_top, "ok": z_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Four screw bosses (at +-35, +-20; OD >= 6; pilot hole 2.2mm; depth >= 4)
    try:
        boss_coords = [(35, 20), (-35, 20), (35, -20), (-35, -20)]
        boss_results = []
        all_bosses_ok = True
        for cx, cy in boss_coords:
            # OD check: probe a cylinder from floor to top of board space
            probe_od = cq.Solid.makeCylinder(3.0, 12.0, pnt=cq.Vector(cx, cy, 2), dir=cq.Vector(0, 0, 1))
            intersected_vol = shape.intersect(probe_od).Volume()
            fill_fraction_od = intersected_vol / probe_od.Volume()
            
            # Pilot hole check: 2.2mm diameter (r=1.1), depth >= 4mm at top of boss (z=8)
            hole_probe = cq.Solid.makeCylinder(1.1, 5.0, pnt=cq.Vector(cx, cy, 8), dir=cq.Vector(0, 0, -1))
            hole_empty_vol = shape.intersect(hole_probe).Volume()
            
            # Verify the hole is actually surrounded by material (the ring)
            ring_outer = cq.Solid.makeCylinder(3.1, 5.0, pnt=cq.Vector(cx, cy, 8), dir=cq.Vector(0, 0, -1))
            ring_inner = cq.Solid.makeCylinder(1.2, 5.0, pnt=cq.Vector(cx, cy, 8), dir=cq.Vector(0, 0, -1))
            ring_shell = ring_outer.cut(ring_inner)
            ring_fill = shape.intersect(ring_shell).Volume() / ring_shell.Volume()
            
            od_ok = fill_fraction_od > 0.9
            hole_ok = hole_empty_vol < 0.1 and ring_fill > 0.9
            boss_results.append({"od_ok": od_ok, "hole_ok": hole_ok})
            if not (od_ok and hole_ok): all_bosses_ok = False
        status = "pass" if all_bosses_ok else "fail"
        results["R5"] = {
            "status": status,
            "value": boss_results,
            "method": f"Probed 4 cylinders at (+-35, +-20) for OD and pilot hole (2.2mm dia, depth >= 4mm)",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... 2.2mm pilot hole... 4mm deep", "measured": status, "ok": all_bosses_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout (-X wall, 9mm Y, 3mm Z, centered at y=0, z=14)
    try:
        cutout_box = cq.Solid.makeBox(5, 9, 3, pnt=cq.Vector(-45, -4.5, 12.5))
        intersected_vol_void = shape.intersect(cutout_box).Volume()
        opening_is_empty = intersected_vol_void < 0.5

        wall_block = cq.Solid.makeBox(10, 12, 6, pnt=cq.Vector(-47, -6, 11))
        material_in_block = shape.intersect(wall_block).Volume()
        void_in_block = wall_block.Volume() - material_in_block
        
        cutout_vol = cutout_box.Volume()
        removal_ok = (void_in_block > 0.5 * cutout_vol) and (void_in_block < 1.5 * cutout_vol)

        status = "pass" if (opening_is_empty and removal_ok) else "fail"
        results["R6"] = {
            "status": status,
            "value": {"void_volume": void_in_block, "opening_intersected": intersected_vol_void},
            "method": f"Checked if cutout box is empty and if material was removed from the wall block (void={void_in_block:.2f})",
            "criteria": [{"condition": "USB-C cutout... 9mm wide (Y) and 3mm high (Z)", "measured": status, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 70g (PLA density 1.24 g/cm3)
    try:
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * 1.24 / 1000.0
        status = "pass" if mass_g <= 70.0 else "fail"
        results["R7"] = {
            "status": status,
            "value": round(mass_g, 2),
            "method": f"Mass = Volume({vol_mm3:.1f} mm3) * density(1.24 g/cm3) / 1000",
            "criteria": [{"condition": "Mass <= 70 g", "measured": mass_g, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    run_checks()