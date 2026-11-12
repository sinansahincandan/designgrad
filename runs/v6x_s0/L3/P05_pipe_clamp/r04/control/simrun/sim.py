import cadquery as cq
import trimesh
import numpy as np
import json

def check_requirements():
    results = {}
    
    # Load part
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
            "method": f"Counted number of solids in STEP file: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Sits on z=0; clamp width (Y) 18-22 mm; total X extent <= 80 mm
    try:
        bbox = shape.BoundingBox()
        xmin, xmax = bbox.xmin, bbox.xmax
        ymin, ymax = bbox.ymin, bbox.ymax
        zmin, zmax = bbox.zmin, bbox.zmax
        x_ext = xmax - xmin
        y_ext = ymax - ymin
        
        on_z0 = abs(zmin) < 0.01
        width_ok = 18.0 <= y_ext <= 22.0
        x_ok = x_ext <= 80.0
        
        status = "pass" if (on_z0 and width_ok and x_ok) else "fail"
        results["R2"] = {
            "status": status,
            "value": [x_ext, y_ext, zmin],
            "method": f"BBox: X={x_ext}, Y={y_ext}, Zmin={zmin}",
            "criteria": [
                {"condition": "Sits on z=0", "measured": zmin, "ok": on_z0},
                {"condition": "Width (Y) between 18 and 22 mm", "measured": y_ext, "ok": width_ok},
                {"condition": "Total X extent <= 80 mm", "measured": x_ext, "ok": x_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Pipe volume (radius 12.6 around x=0, z=12.5) must be free of material
    try:
        pipe_r = 12.6
        pnt = cq.Vector(0, 0, 12.5)
        direction = cq.Vector(0, 1, 0)
        length = (shape.BoundingBox().ymax - shape.BoundingBox().ymin) + 4.0
        
        core = cq.Solid.makeCylinder(pipe_r, length, pnt=pnt, dir=direction)
        intersection_vol = shape.intersect(core).Volume()
        
        # Requirement: "must be free of material". 
        # We check if the intersection volume is essentially zero.
        ratio_filled = intersection_vol / core.Volume()
        status = "pass" if ratio_filled < 0.01 else "fail"
        results["R3"] = {
            "status": status,
            "value": ratio_filled,
            "method": f"Intersection volume of cylinder (r=12.6) / Cylinder Volume",
            "criteria": [{"condition": "Pipe volume free of material", "measured": ratio_filled, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Clamp wraps over top (band 12.7 to 15.5 from pipe axis |x| <= 7)
    try:
        r_in = 12.7
        r_out = 15.5
        L = (shape.BoundingBox().ymax - shape.BoundingBox().ymin) + 4.0
        pnt_band = cq.Vector(0, shape.BoundingBox().ymin - 2, 12.5)
        dir_band = cq.Vector(0, 1, 0)
        
        shell = cq.Solid.makeCylinder(r_out, L, pnt=pnt_band, dir=dir_band).cut(
                cq.Solid.makeCylinder(r_in, L, pnt=pnt_band, dir=dir_band))
        box_constraint = cq.Solid.makeBox(14, L, 30, pnt=cq.Vector(-7, shape.BoundingBox().ymin - 2, 0))
        probe_region = shell.intersect(box_constraint)
        
        filled_vol = shape.intersect(probe_region).Volume()
        ratio = filled_vol / probe_region.Volume()
        status = "pass" if ratio > 0.8 else "fail"
        results["R4"] = {
            "status": status,
            "value": ratio,
            "method": f"Intersection volume of shell (r=12.7-15.5) intersected with |x|<=7 / Shell Volume",
            "criteria": [{"condition": "Solid material in the band 12.7 to 15.5 mm from pipe axis (|x| <= 7)", "measured": ratio, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Two screw holes, diameter 6.6 mm, vertical, centered at (+-27, 0)
    try:
        hole_d = 6.6
        r_h = hole_d / 2
        centers = [(27, 0), (-27, 0)]
        holes_ok = []
        for cx, cy in centers:
            pnt_h = cq.Vector(cx, cy, shape.BoundingBox().zmin - 1)
            dir_h = cq.Vector(0, 0, 1)
            length_h = (shape.BoundingBox().zmax - shape.BoundingBox().zmin) + 2.0
            
            core = cq.Solid.makeCylinder(r_h - 0.05, length_h, pnt=pnt_h, dir=dir_h)
            wall = cq.Solid.makeCylinder(r_h + 1.0, length_h, pnt=pnt_h, dir=dir_h).cut(
                   cq.Solid.makeCylinder(r_h + 0.05, length_h, pnt=pnt_h, dir=dir_h))
            
            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            walled_ratio = shape.intersect(wall).Volume() / wall.Volume()
            holes_ok.append(empty_ratio < 0.1 and walled_ratio > 0.8)
        
        status = "pass" if all(holes_ok) else "fail"
        results["R5"] = {
            "status": status,
            "value": holes_ok,
            "method": f"Checked two vertical cylinders (d=6.6) at (+-27, 0) for emptiness and surrounding material",
            "criteria": [{"condition": "Two screw holes, diameter 6.6 mm, vertical, centred at (x, y) = (+-27, 0)", "measured": holes_ok, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Flanges at least 3 mm thick: solid from z=0 to 3 for 18.5 <= |x| <= 23, |y| <= 4
    try:
        thick_ok = True
        for sx in [1, -1]:
            x_start = 18.5 * sx
            x_end = 23.0 * sx
            xmin_f = min(x_start, x_end)
            xmax_f = max(x_start, x_end)
            probe = cq.Solid.makeBox(xmax_f - xmin_f, 8.0, 3.0, pnt=cq.Vector(xmin_f, -4, 0))
            ratio = shape.intersect(probe).Volume() / probe.Volume()
            if ratio < 0.95:
                thick_ok = False
        
        status = "pass" if thick_ok else "fail"
        results["R6"] = {
            "status": status,
            "value": thick_ok,
            "method": f"Intersection volume of probe boxes (z=0-3, |y|<=4, 18.5<=|x|<=23) / Probe Volume",
            "criteria": [{"condition": "Flanges at least 3 mm thick: solid from z = 0 to 3 for 18.5 <= |x| <= 23, |y| <= 4", "measured": thick_ok, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 25 g. PLA density 1.24 g/cm3
    try:
        vol_mm3 = shape.Volume()
        density_g_mm3 = 1.24 / 1000.0
        mass = vol_mm3 * density_g_mm3
        status = "pass" if mass <= 25.001 else "fail"
        results["R7"] = {
            "status": status,
            "value": mass,
            "method": f"Volume={vol_mm3} mm3 * Density=0.00124 g/mm3",
            "criteria": [{"condition": "Mass <= 25 g", "measured": mass, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    check_requirements()