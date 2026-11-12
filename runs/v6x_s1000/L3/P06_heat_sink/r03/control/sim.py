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

    # R2: Footprint 40x40 (+-0.5) centered on origin; height <= 25
    try:
        bbox = shape.BoundingBox()
        xmin, xmax = bbox.xmin, bbox.xmax
        ymin, ymax = bbox.ymin, bbox.ymax
        zmin, zmax = bbox.zmin, bbox.zmax
        
        width_x = xmax - xmin
        width_y = ymax - ymin
        height = zmax - zmin
        center_x = (xmin + xmax) / 2
        center_y = (ymin + ymax) / 2
        
        tol = 0.5
        c1 = abs(width_x - 40) <= tol
        c2 = abs(width_y - 40) <= tol
        c3 = abs(center_x) <= tol
        c4 = abs(center_y) <= tol
        c5 = height <= 25.01
        
        status = "pass" if (c1 and c2 and c3 and c4 and c5) else "fail"
        results["R2"] = {
            "status": status,
            "value": [width_x, width_y, height],
            "method": f"BBox: x[{xmin:.2f},{xmax:.2f}], y[{ymin:.2f},{ymax:.2f}], z[{zmin:.2f},{zmax:.2f}]",
            "criteria": [
                {"condition": "Footprint 40x40 (+-0.5)", "measured": [width_x, width_y], "ok": c1 and c2},
                {"condition": "Centred on origin", "measured": [center_x, center_y], "ok": c3 and c4},
                {"condition": "Total height <= 25 mm", "measured": height, "ok": c5}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Solid base at least 3 mm thick (z=0 to 3) over whole footprint
    try:
        grid_res = 5 
        x_coords = np.linspace(-20, 20, grid_res)
        y_coords = np.linspace(-20, 20, grid_res)
        thickness_ok = True
        
        for x in x_coords:
            for y in y_coords:
                probe_r = 0.5 
                probe_len = 3.0
                # Probe from z=0 to z=3. If the part is present, intersection volume should match probe volume.
                probe = cq.Solid.makeCylinder(probe_r, probe_len, pnt=cq.Vector(x, y, 0), dir=cq.Vector(0, 0, 1))
                intersection_vol = shape.intersect(probe).Volume()
                if intersection_vol / probe.Volume() < 0.95:
                    thickness_ok = False
                    break
            if not thickness_ok: break

        status = "pass" if thickness_ok else "fail"
        results["R3"] = {
            "status": status,
            "value": thickness_ok,
            "method": f"Grid-based probe check (5x5) of 0.5mm radius cylinders from z=0 to 3",
            "criteria": [{"condition": "Solid base >= 3mm thick over whole footprint", "measured": thickness_ok, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Thermal resistance R <= 9 K/W. h=10, eta=0.85, A=surface area
    try:
        A_mm2 = mesh.area
        A_m2 = A_mm2 / 1_000_000.0
        h = 10.0
        eta = 0.85
        R = 1.0 / (h * A_m2 * eta)
        status = "pass" if R <= 9.001 else "fail"
        results["R4"] = {
            "status": status,
            "value": R,
            "method": f"R = 1 / (h * A_m2 * eta) with h=10, eta=0.85, A={A_m2:.6f} m2",
            "criteria": [{"condition": "Thermal resistance <= 9 K/W", "measured": R, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Two mounting holes (D=3.2) at (+-15, 0). Screwdriver access (no material within 3mm of axis for z >= 3)
    try:
        hole_centers = [(15, 0), (-15, 0)]
        hole_radius = 3.2 / 2.0
        access_radius = 3.0
        
        all_holes_exist = True
        all_access_clear = True
        
        for cx, cy in hole_centers:
            # 1. Verify Hole Existence: A real hole must be empty (core) AND surrounded by material (wall).
            # We check a cylinder from z=0 to z=3 (the base thickness).
            hole_height = 3.0
            pnt = cq.Vector(cx, cy, 0)
            direction = cq.Vector(0, 0, 1)
            
            core = cq.Solid.makeCylinder(hole_radius, hole_height, pnt=pnt, dir=direction)
            # Check if core is empty (volume of intersection should be ~0)
            if shape.intersect(core).Volume() > (core.Volume() * 0.05):
                all_holes_exist = False

            # Check if the hole is actually surrounded by material: 
            # A ring just outside the hole radius must contain significant part volume.
            ring_outer_r = hole_radius + 1.0
            ring_inner_r = hole_radius - 0.1
            ring_shell = cq.Solid.makeCylinder(ring_outer_r, hole_height, pnt=pnt, dir=direction).cut(
                         cq.Solid.makeCylinder(ring_inner_r, hole_height, pnt=pnt, dir=direction))
            
            if shape.intersect(ring_shell).Volume() / ring_shell.Volume() < 0.8:
                all_holes_exist = False

            # 2. Screwdriver access: No material within 3mm of axis for z >= 3
            # We probe from z=3 upwards to the top of the part (max height is 25)
            access_probe = cq.Solid.makeCylinder(access_radius, 25.0, pnt=cq.Vector(cx, cy, 3), dir=direction)
            if shape.intersect(access_probe).Volume() > 1.0: # Allow tiny epsilon for mesh artifacts
                all_access_clear = False

        status = "pass" if (all_holes_exist and all_access_clear) else "fail"
        results["R5"] = {
            "status": status,
            "value": [all_holes_exist, all_access_clear],
            "method": f"Verified hole existence via core-emptiness and wall-presence; access via cylinder clearance (r=3.0, z>=3)",
            "criteria": [
                {"condition": "Diameter 3.2 mm vertical through base", "measured": all_holes_exist, "ok": all_holes_exist},
                {"condition": "No material within 3mm of axis above z=3", "measured": all_access_clear, "ok": all_access_clear}
            ],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Mass <= 45 g. Density 2.70 g/cm3
    try:
        vol_mm3 = shape.Volume()
        density_g_cm3 = 2.70
        mass_g = (vol_mm3 / 1000.0) * density_g_cm3
        status = "pass" if mass_g <= 45.001 else "fail"
        results["R6"] = {
            "status": status,
            "value": mass_g,
            "method": f"Mass = (Volume[{vol_mm3:.2f} mm3] / 1000) * 2.70",
            "criteria": [{"condition": "Mass <= 45 g", "measured": mass_g, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()