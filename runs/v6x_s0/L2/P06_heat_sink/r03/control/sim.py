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
        is_single = (n_solids == 1)
        results["R1"] = {
            "status": "pass" if is_single else "fail",
            "value": n_solids,
            "method": f"Counted number of solids in STEP file: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": bool(is_single)}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Footprint 40x40 (+-0.5), centered on origin; height <= 25
    try:
        bbox = shape.BoundingBox()
        dx = bbox.xmax - bbox.xmin
        dy = bbox.ymax - bbox.ymin
        dz = bbox.zmax - bbox.zmin
        cx, cy = (bbox.xmin + bbox.xmax)/2, (bbox.ymin + bbox.ymax)/2
        
        dim_ok = abs(dx - 40) <= 0.5 and abs(dy - 40) <= 0.5
        center_ok = abs(cx) <= 0.5 and abs(cy) <= 0.5
        height_ok = dz <= 25.0
        
        status = "pass" if (dim_ok and center_ok and height_ok) else "fail"
        results["R2"] = {
            "status": status,
            "value": [round(dx, 3), round(dy, 3), round(dz, 3), round(cx, 3), round(cy, 3)],
            "method": f"BBox: dx={dx}, dy={dy}, dz={dz}, cx={cx}, cy={cy}",
            "criteria": [
                {"condition": "Footprint exactly 40 x 40 mm (+-0.5)", "measured": [round(dx,3), round(dy,3)], "ok": bool(dim_ok)},
                {"condition": "Centred on the origin", "measured": [round(cx,3), round(cy,3)], "ok": bool(center_ok)},
                {"condition": "Total height <= 25 mm", "measured": round(dz, 3), "ok": bool(height_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Solid base at least 3 mm thick (z=0 to 3) over whole footprint
    try:
        base_box = cq.Solid.makeBox(40, 40, 3, pnt=cq.Vector(-20, -20, 0))
        intersected_vol = shape.intersect(base_box).Volume()
        hole_area = np.pi * (3.2/2)**2
        expected_vol = (40 * 40 * 3) - (2 * hole_area * 3)
        thickness_ok = intersected_vol >= (expected_vol * 0.95)
        results["R3"] = {
            "status": "pass" if thickness_ok else "fail",
            "value": round(intersected_vol, 2),
            "method": f"Intersection volume in z=[0,3]: {intersected_vol} mm3. Expected (minus holes): {expected_vol:.2f} mm3.",
            "criteria": [{"condition": "Solid base at least 3 mm thick (z = 0 to 3) over the whole footprint", "measured": round(intersected_vol, 2), "ok": bool(thickness_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Thermal Resistance R <= 9 K/W
    try:
        area_mm2 = mesh.area
        area_m2 = area_mm2 / 1_000_000.0
        h = 10.0 
        eta = 0.85
        R = 1.0 / (h * area_m2 * eta)
        r_ok = R <= 9.0 + 0.01 
        results["R4"] = {
            "status": "pass" if r_ok else "fail",
            "value": round(R, 3),
            "method": f"R = 1 / (h * A * eta) with h=10, eta=0.85, A={area_m2:.6f} m2",
            "criteria": [{"condition": "Thermal resistance R <= 9 K/W", "measured": round(R, 3), "ok": bool(r_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Two mounting holes (D=3.2) at (+-15, 0). Clearance z>=3: no material within 3mm of axis.
    try:
        holes_ok = True
        hole_details = []
        for x_pos in [-15, 15]:
            # 1. Verify hole diameter/existence via core emptiness
            # Probe from z=-0.5 to z=4.0 (covers base and part of clearance zone)
            core = cq.Solid.makeCylinder(3.2/2, 4.5, pnt=cq.Vector(x_pos, 0, -0.5), dir=cq.Vector(0, 0, 1))
            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            
            # 2. Verify hole is actually in the base (material exists around it at z=[0,3])
            # We check a ring just outside the diameter within the base thickness
            ring_inner = 3.2/2
            ring_outer = 4.0
            base_ring = cq.Solid.makeCylinder(ring_outer, 3.0, pnt=cq.Vector(x_pos, 0, 0), dir=cq.Vector(0, 0, 1)).cut(
                         cq.Solid.makeCylinder(ring_inner, 3.0, pnt=cq.Vector(x_pos, 0, 0), dir=cq.Vector(0, 0, 1)))
            walled_ratio = shape.intersect(base_ring).Volume() / base_ring.Volume()

            # 3. Clearance check: no material within 3mm of axis for z >= 3
            # We probe the volume from z=3 to z=25 (max height)
            clearance_cyl = cq.Solid.makeCylinder(3.0, 22.0, pnt=cq.Vector(x_pos, 0, 3.0), dir=cq.Vector(0, 0, 1))
            clearance_vol = shape.intersect(clearance_cyl).Volume()

            # Criteria: empty_ratio ~ 0 (hole is there), walled_ratio ~ 1 (it's in the base), clearance_vol ~ 0 (screwdriver access)
            h_ok = empty_ratio < 0.05 and walled_ratio > 0.9 and clearance_vol < 0.5
            if not h_ok: holes_ok = False
            hole_details.append({
                "x": float(x_pos), 
                "empty_ratio": round(empty_ratio, 3), 
                "walled_ratio": round(walled_ratio, 3), 
                "clearance_vol": round(clearance_vol, 3)
            })

        results["R5"] = {
            "status": "pass" if holes_ok else "fail",
            "value": hole_details,
            "method": "Verified hole emptiness (core), base material presence (ring at z=0-3), and screwdriver clearance (z>=3 cylinder).",
            "criteria": [
                {"condition": "Two mounting holes, diameter 3.2 mm", "measured": [hole_details[0]['empty_ratio'], hole_details[1]['empty_ratio']], "ok": bool(holes_ok)},
                {"condition": "Screwdriver clearance: no material within 3mm of axis above z=3", "measured": [hole_details[0]['clearance_vol'], hole_details[1]['clearance_vol']], "ok": bool(holes_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Mass <= 45 g (Al 6063: 2.70 g/cm3)
    try:
        vol_mm3 = shape.Volume()
        density_g_mm3 = 2.70 / 1000.0
        mass_g = vol_mm3 * density_g_mm3
        mass_ok = mass_g <= 45.0 + 0.1
        results["R6"] = {
            "status": "pass" if mass_ok else "fail",
            "value": round(mass_g, 2),
            "method": f"Mass = Volume ({round(vol_mm3, 1)} mm3) * Density (0.0027 g/mm3)",
            "criteria": [{"condition": "Mass <= 45 g", "measured": round(mass_g, 2), "ok": bool(mass_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    run_verification()