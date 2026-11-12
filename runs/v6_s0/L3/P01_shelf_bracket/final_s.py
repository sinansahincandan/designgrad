import cadquery as cq
import trimesh
import numpy as np
import json

def run_checks():
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    results = {}
    density_gcm3 = 1.24
    E_mpa = 3500.0
    F_n = 150.0
    L_load = 140.0  # distance from x=10 to x=150

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": f"Counted solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R2: Envelope
    try:
        bbox = shape.BoundingBox()
        xmin, xmax = bbox.xmin, bbox.xmax
        ymin, ymax = bbox.ymin, bbox.ymax
        zmin, zmax = bbox.zmin, bbox.zmax
        
        c1 = (0 <= xmin <= 0.1) and (xmax <= 170.1)
        c2 = (-20.1 <= ymin) and (ymax <= 20.1)
        c3 = (0 <= zmin <= 0.1) and (zmax <= 130.1)
        
        status = "pass" if (c1 and c2 and c3) else "fail"
        results["R2"] = {
            "status": status,
            "value": [float(xmin), float(xmax), float(ymin), float(ymax), float(zmin), float(zmax)],
            "method": f"Checked BoundingBox: x[{xmin},{xmax}], y[{ymin},{ymax}], z[{zmin},{zmax}]",
            "criteria": [
                {"condition": "0 <= x <= 170 and touches wall (x=0)", "measured": [float(xmin), float(xmax)], "ok": bool(c1)},
                {"condition": "-20 <= y <= 20", "measured": [float(ymin), float(ymax)], "ok": bool(c2)},
                {"condition": "0 <= z <= 130", "measured": [float(zmin), float(zmax)], "ok": bool(c3)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R3: Screw holes and screwdriver access (FIXED)
    try:
        target_dia = 5.5
        access_radius = 4.0
        hole_results = []
        all_holes_ok = True

        for cy, cz in [(0, 20), (0, 60)]:
            # To verify a hole exists at the right place:
            # 1. A probe cylinder of diameter D must be empty (intersecting volume ~ 0)
            # 2. A slightly larger shell around that cylinder must contain material (walled check)
            
            # Probe for emptiness (the actual hole)
            core = cq.Solid.makeCylinder(target_dia / 2, 5.0, pnt=cq.Vector(-1, cy, cz), dir=cq.Vector(1, 0, 0))
            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            
            # Probe for material presence (the wall)
            shell_outer = cq.Solid.makeCylinder(target_dia / 2 + 1.0, 5.0, pnt=cq.Vector(-1, cy, cz), dir=cq.Vector(1, 0, 0))
            shell_inner = cq.Solid.makeCylinder(target_dia / 2 + 0.1, 5.0, pnt=cq.Vector(-1, cy, cz), dir=cq.Vector(1, 0, 0))
            wall_probe = shell_outer.cut(shell_inner)
            walled_ratio = shape.intersect(wall_probe).Volume() / wall_probe.Volume()

            # Verify screwdriver access: no material within 4mm of axis for x >= 10
            access_probe = cq.Solid.makeCylinder(access_radius, 160, pnt=cq.Vector(10, cy, cz), dir=cq.Vector(1, 0, 0))
            material_in_access = shape.intersect(access_probe).Volume()
            access_ok = material_in_access < 0.5 # Allow tiny tolerance for mesh/precision

            # A hole is valid if it's empty AND has a surrounding wall
            hole_exists_ok = (empty_ratio < 0.02) and (walled_ratio > 0.8)
            
            if not (hole_exists_ok and access_ok):
                all_holes_ok = False
            
            hole_results.append({
                "diameter_check_passed": bool(hole_exists_ok),
                "access_material_vol": float(material_in_access),
                "empty_ratio": float(empty_ratio),
                "walled_ratio": float(walled_ratio)
            })

        status = "pass" if all_holes_ok else "fail"
        results["R3"] = {
            "status": status,
            "value": hole_results,
            "method": f"Verified holes via emptiness/wall probes and screwdriver clearance (R=4 for x>=10)",
            "criteria": [
                {"condition": "Two screw holes diameter 5.5mm at correct locations", "measured": [h['diameter_check_passed'] for h in hole_results], "ok": all_holes_ok},
                {"condition": "No material within 4mm of axis for x >= 10", "measured": [h['access_material_vol'] for h in hole_results], "ok": all_holes_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R4: Shelf support
    try:
        support_probe = cq.Solid.makeBox(10, 2, 110, pnt=cq.Vector(140, -1, 0))
        support_fill = shape.intersect(support_probe).Volume() / support_probe.Volume()
        c1 = support_fill > 0.95

        excess_probe = cq.Solid.makeBox(162, 40, 20, pnt=cq.Vector(8, -20, 110))
        excess_vol = shape.intersect(excess_probe).Volume()
        c2 = excess_vol < 0.01

        status = "pass" if (c1 and c2) else "fail"
        results["R4"] = {
            "status": status,
            "value": [float(support_fill), float(excess_vol)],
            "method": f"Checked support column fill at x[140,150] and excess volume above z=110 for x>=8",
            "criteria": [
                {"condition": "Solid material below z=110 between x=140-150 around y=0", "measured": float(support_fill), "ok": bool(c1)},
                {"condition": "Nothing above z=110 for x >= 8", "measured": float(excess_vol), "ok": bool(c2)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R5 & R6: Strength and Stiffness (Section at x=10)
    try:
        x0 = 10.0
        h_grid = 0.5
        y_min, z_min = mesh.bounds[0][1], mesh.bounds[0][2]
        y_max, z_max = mesh.bounds[1][1], mesh.bounds[1][2]
        Y, Z = np.meshgrid(np.arange(y_min, y_max, h_grid) + h_grid/2, 
                           np.arange(z_min, z_max, h_grid) + h_grid/2)
        pts = np.column_stack([np.full(Y.size, x0), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not np.any(inside):
            raise ValueError("No material found at section x=10")

        z_vals = pts[inside, 2]
        A = inside.sum() * (h_grid**2)
        zc = z_vals.mean()
        I = ((z_vals - zc)**2).sum() * (h_grid**2)
        c = abs(z_vals - zc).max() 

        M = F_n * L_load
        sigma = M * c / I
        delta = (F_n * (L_load**3)) / (3 * E_mpa * I)

        c5 = sigma <= 20.01
        c6 = delta <= 2.01
        
        results["R5"] = {
            "status": "pass" if c5 else "fail",
            "value": float(sigma),
            "method": f"M={M} Nmm, c={c:.2f} mm, I={I:.2f} mm4, sigma=Mc/I",
            "criteria": [{"condition": "bending stress <= 20 MPa", "measured": float(sigma), "ok": bool(c5)}],
            "note": ""
        }
        results["R6"] = {
            "status": "pass" if c6 else "fail",
            "value": float(delta),
            "method": f"F={F_n} N, L={L_load} mm, E={E_mpa} MPa, I={I:.2f} mm4, delta=FL^3/3EI",
            "criteria": [{"condition": "deflection <= 2.0 mm", "measured": float(delta), "ok": bool(c6)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass
    try:
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * density_gcm3 / 1000.0
        c7 = mass_g <= 90.01
        results["R7"] = {
            "status": "pass" if c7 else "fail",
            "value": float(mass_g),
            "method": f"Volume={vol_mm3:.2f} mm3, density={density_gcm3} g/cm3, mass=V*rho/1000",
            "criteria": [{"condition": "Mass <= 90 g", "measured": float(mass_g), "ok": bool(c7)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    run_checks()