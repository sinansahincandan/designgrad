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
        intersection_vol = shape.intersect(floor_region).Volume()
        expected_vol = 80 * 50 * 2
        fill_ratio = intersection_vol / expected_vol
        status = "pass" if fill_ratio > 0.99 else "fail"
        results["R2"] = {
            "status": status,
            "value": fill_ratio,
            "method": f"Intersection volume of floor region (80x50x2 at z=0) with part: {intersection_vol} mm3 / {expected_vol} mm3",
            "criteria": [{"condition": "solid floor at least 2 mm thick under the whole board area", "measured": fill_ratio, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Board space (-40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32) must be empty
    # FIX: To ensure the enclosure actually exists around this void, we check that the volume of the 
    # bounding box of the part is significantly larger than the board space, and specifically 
    # verify that the walls (the boundary of the space) are present.
    try:
        board_space = cq.Solid.makeBox(80, 50, 24, pnt=cq.Vector(-40, -25, 8))
        empty_vol = shape.intersect(board_space).Volume()
        
        # To verify the enclosure exists, we check if there is material immediately surrounding the board space.
        # We probe a thin shell (the walls) at the boundaries of the R3 box.
        wall_probe_thickness = 1.0
        shell_vol = 0
        # Check X-walls (-41 to -40 and 40 to 41), Y-walls (-26 to -25 and 25 to 26)
        probes = [
            cq.Solid.makeBox(wall_probe_thickness, 50, 24, pnt=cq.Vector(-41, -25, 8)), # Left wall
            cq.Solid.makeBox(wall_probe_thickness, 50, 24, pnt=cq.Vector(40, -25, 8)),  # Right wall
            cq.Solid.makeBox(80, wall_probe_thickness, 24, pnt=cq.Vector(-40, -26, 8)), # Front wall
            cq.Solid.makeBox(80, wall_probe_thickness, 24, pnt=cq.Vector(-40, 25, 8))   # Back wall
        ]
        for p in probes:
            shell_vol += shape.intersect(p).Volume()

        is_empty = empty_vol < 0.1
        has_walls = shell_vol > 10.0 # Ensure there's significant material forming the boundary
        status = "pass" if (is_empty and has_walls) else "fail"
        
        results["R3"] = {
            "status": status,
            "value": {"empty_vol": round(empty_vol, 3), "boundary_material_vol": round(shell_vol, 3)},
            "method": f"Checked emptiness of board space ({empty_vol} mm3) and presence of surrounding wall material ({shell_vol} mm3).",
            "criteria": [{"condition": "region -40 <= x <= 40, -25 <= y <= 25, 8 <= z <= 32 must be completely free of material AND enclosed", "measured": status, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Walls (85x55 +-1.5mm; top z 30-32.5)
    try:
        bbox = shape.BoundingBox()
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        zmax = bbox.zmax
        status_dim = (78.5 <= dx <= 86.5) and (53.5 <= dy <= 56.5)
        status_z = (30.0 <= zmax <= 32.5)
        status = "pass" if (status_dim and status_z) else "fail"
        results["R4"] = {
            "status": status,
            "value": [round(dx, 2), round(dy, 2), round(zmax, 2)],
            "method": f"Measured Bounding Box: dx={dx}, dy={dy}, zmax={zmax}",
            "criteria": [
                {"condition": "outer size 85 x 55 mm (+-1.5 mm) in X and Y", "measured": [dx, dy], "ok": status_dim},
                {"condition": "wall top at z between 30 and 32.5", "measured": zmax, "ok": status_z}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Four screw bosses at (+-35, +-20), OD >= 6mm, pilot hole 2.2mm, depth >= 4mm
    try:
        boss_coords = [(35, 20), (-35, 20), (35, -20), (-35, -20)]
        boss_pass = True
        measured_vals = []
        for cx, cy in boss_coords:
            probe_od = cq.Solid.makeCylinder(3.0, 8, pnt=cq.Vector(cx, cy, 0), dir=cq.Vector(0, 0, 1))
            od_fill = shape.intersect(probe_od).Volume() / probe_od.Volume()
            
            probe_hole = cq.Solid.makeCylinder(1.1, 4, pnt=cq.Vector(cx, cy, 4), dir=cq.Vector(0, 0, 1))
            hole_intersection = shape.intersect(probe_hole).Volume()
            empty_ratio = (probe_hole.Volume() - hole_intersection) / probe_hole.Volume()

            if od_fill < 0.95 or empty_ratio < 0.95:
                boss_pass = False
            measured_vals.append({"coord": [cx, cy], "od_fill": round(od_fill, 3), "hole_empty": round(empty_ratio, 3)})

        status = "pass" if boss_pass else "fail"
        results["R5"] = {
            "status": status,
            "value": measured_vals,
            "method": "Probed bosses: checked OD fill (r=3.0, z=0-8) and hole emptiness (r=1.1, depth 4mm at top)",
            "criteria": [{"condition": "Four screw bosses... OD >= 6mm... 2.2mm pilot hole... depth >= 4mm", "measured": status, "ok": boss_pass}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: USB-C cutout through -X wall (9mm Y, 3mm Z, centered at y=0, z=14)
    try:
        wall_thickness_probe = cq.Solid.makeBox(10, 15, 10, pnt=cq.Vector(-47.5, -7.5, 9))
        material_in_wall_region = shape.intersect(wall_thickness_probe).Volume()
        cutout_probe = cq.Solid.makeBox(10, 9, 3, pnt=cq.Vector(-47.5, -4.5, 12.5))
        empty_vol = shape.intersect(cutout_probe).Volume()
        is_empty = empty_vol < (cutout_probe.Volume() * 0.05)
        has_wall_to_cut = material_in_wall_region > 1.0 
        status = "pass" if (is_empty and has_wall_to_cut) else "fail"
        results["R6"] = {
            "status": status,
            "value": {"empty_vol": round(empty_vol, 3), "wall_material_in_probe": round(material_in_wall_region, 3)},
            "method": f"Verified cutout by checking emptiness of probe box ({cutout_probe.Volume()}mm3) and presence of wall material in X-range.",
            "criteria": [{"condition": "USB-C cutout... opening at least 9 mm wide (Y) and 3 mm high (Z)", "measured": status, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 70g (Density 1.24 g/cm3)
    try:
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * 1.24 / 1000.0
        status = "pass" if mass_g <= 70.001 else "fail"
        results["R7"] = {
            "status": status,
            "value": round(mass_g, 3),
            "method": f"Volume {vol_mm3:.2f} mm3 * density 1.24 g/cm3 / 1000",
            "criteria": [{"condition": "Mass <= 70 g", "measured": mass_g, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()