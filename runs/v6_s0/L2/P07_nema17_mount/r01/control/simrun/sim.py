import cadquery as cq
import trimesh
import numpy as np
import json

def run_verification():
    results = {}
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": "Counted number of solids in STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": status == "pass"}],
            "note": f"Found {n_solids} solids"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R2 & R3: Face plate thickness and Central Bore
    try:
        bore_diam = 22.5
        bore_pnt = cq.Vector(0, -1, 30) 
        bore_dir = cq.Vector(0, 1, 0)
        
        # R3 Probe
        core = cq.Solid.makeCylinder(bore_diam / 2 - 0.15, 10, pnt=bore_pnt, dir=bore_dir)
        empty_vol = shape.intersect(core).Volume() / core.Volume()
        wall_outer = cq.Solid.makeCylinder(bore_diam / 2 + 1.0, 10, pnt=bore_pnt, dir=bore_dir)
        wall_inner = cq.Solid.makeCylinder(bore_diam / 2 + 0.15, 10, pnt=bore_pnt, dir=bore_dir)
        wall_shell = wall_outer.cut(wall_inner)
        walled_vol = shape.intersect(wall_shell).Volume() / wall_shell.Volume()

        # R2: Face plate thickness (y=0 to 4)
        plate_box = cq.Solid.makeBox(100, 4, 100, pnt=cq.Vector(-50, 0, -50))
        plate_material_ratio = shape.intersect(plate_box).Volume() / plate_box.Volume()

        r3_ok = empty_vol < 0.02 and walled_vol > 0.9
        # R2 check: ensure material exists in the specified thickness region AND around the bore
        r2_ok = plate_material_ratio > 0.8 and walled_vol > 0.5

        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": [round(empty_vol, 3), round(walled_vol, 3)],
            "method": f"Cylinder probe at (0, y, 30) dir (0,1,0) diam {bore_diam}",
            "criteria": [{"condition": "Central bore diameter 22.5 mm", "measured": empty_vol, "ok": r3_ok}],
            "note": f"Empty: {empty_vol}, Walled: {walled_vol}"
        }
        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": round(plate_material_ratio, 3),
            "method": f"Intersection volume ratio in box y=[0,4]",
            "criteria": [{"condition": "Face plate at least 4 mm thick with solid material around bore", "measured": plate_material_ratio, "ok": r2_ok}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes (3.4mm) at (+-15.5, 30 +- 15.5)
    try:
        holes_ok = True
        hole_coords = [(15.5, 30+15.5), (15.5, 30-15.5), (-15.5, 30+15.5), (-15.5, 30-15.5)]
        hole_diam = 3.4
        for hx, hz in hole_coords:
            pnt = cq.Vector(hx, -1, hz)
            dir_vec = cq.Vector(0, 1, 0)
            core = cq.Solid.makeCylinder(hole_diam/2 - 0.15, 10, pnt=pnt, dir=dir_vec)
            wall_outer = cq.Solid.makeCylinder(hole_diam/2 + 1.0, 10, pnt=pnt, dir=dir_vec)
            wall_inner = cq.Solid.makeCylinder(hole_diam/2 + 0.15, 10, pnt=pnt, dir=dir_vec)
            wall_shell = wall_outer.cut(wall_inner)
            
            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            walled_ratio = shape.intersect(wall_shell).Volume() / wall_shell.Volume()
            
            # A hole exists if it is empty AND surrounded by material
            if not (empty_ratio < 0.05 and walled_ratio > 0.8):
                holes_ok = False
                break
        results["R4"] = {
            "status": "pass" if holes_ok else "fail",
            "value": holes_ok,
            "method": f"Probed 4 cylinders diam {hole_diam} at specified (x,z) coords for both emptiness and walls",
            "criteria": [{"condition": "Four motor screw holes diameter 3.4 mm", "measured": holes_ok, "ok": holes_ok}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R5: Motor clearance (-21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5)
    try:
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        intersected_vol = shape.intersect(clearance_box).Volume()
        r5_ok = intersected_vol < 0.1 
        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": round(intersected_vol, 3),
            "method": f"Intersection volume with clearance box x[-21.5,21.5], y[-48,0], z[8.5,51.5]",
            "criteria": [{"condition": "Motor clearance: nothing in specified region", "measured": intersected_vol, "ok": r5_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R6: Base on table (z>=0) with two 5.5mm holes at (+-25, 25)
    try:
        holes_ok = True
        hole_coords = [(25, 25), (-25, 25)]
        hole_diam = 5.5
        for hx, hy in hole_coords:
            pnt = cq.Vector(hx, hy, -1)
            dir_vec = cq.Vector(0, 0, 1)
            core = cq.Solid.makeCylinder(hole_diam/2 - 0.15, 10, pnt=pnt, dir=dir_vec)
            wall_outer = cq.Solid.makeCylinder(hole_diam/2 + 1.0, 10, pnt=pnt, dir=dir_vec)
            wall_inner = cq.Solid.makeCylinder(hole_diam/2 + 0.15, 10, pnt=pnt, dir=dir_vec)
            wall_shell = wall_outer.cut(wall_inner)

            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            walled_ratio = shape.intersect(wall_shell).Volume() / wall_shell.Volume()

            if not (empty_ratio < 0.05 and walled_ratio > 0.8):
                holes_ok = False
                break
        results["R6"] = {
            "status": "pass" if holes_ok else "fail",
            "value": holes_ok,
            "method": f"Probed 2 cylinders diam {hole_diam} at (x,y) coords for both emptiness and walls",
            "criteria": [{"condition": "Two vertical screw holes diameter 5.5 mm", "measured": holes_ok, "ok": holes_ok}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R7: Envelope and Mass
    try:
        bbox = shape.BoundingBox()
        xmin, xmax = bbox.xmin, bbox.xmax
        ymin, ymax = bbox.ymin, bbox.ymax
        zmin, zmax = bbox.zmin, bbox.zmax
        
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * 1.24 / 1000.0
        
        x_ok = (-35 <= xmin) and (xmax <= 35)
        z_ok = (zmax <= 55)
        m_ok = (mass_g <= 60.0)
        
        results["R7"] = {
            "status": "pass" if (x_ok and z_ok and m_ok) else "fail",
            "value": [round(xmax-xmin, 2), round(zmax, 2), round(mass_g, 2)],
            "method": f"BBox: x[{xmin:.1f},{xmax:.1f}], z_max={zmax:.1f}; Mass = vol * density",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": xmax-xmin, "ok": x_ok},
                {"condition": "top <= 55 mm", "measured": zmax, "ok": z_ok},
                {"condition": "mass <= 60 g", "measured": mass_g, "ok": m_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    run_verification()