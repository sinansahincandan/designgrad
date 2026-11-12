import cadquery as cq
import trimesh
import numpy as np
import json

def solve():
    try:
        # Load the part
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    results = {}
    density = 1.24  # g/cm3 (PLA)
    E = 3500.0      # MPa
    F = 150.0       # N
    L_load = 140.0  # mm (distance from x=10 to load at x=150)

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": "Counted number of solids in the STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": status == "pass"}],
            "note": f"Found {n_solids} solid(s)"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Envelope
    try:
        bbox = shape.BoundingBox()
        xmin, xmax = bbox.xmin, bbox.xmax
        ymin, ymax = bbox.ymin, bbox.ymax
        zmin, zmax = bbox.zmin, bbox.zmax
        
        c1 = (0 <= xmin + 1e-3 and xmax <= 170 + 1e-3)
        c2 = (-20 - 1e-3 <= ymin and ymax <= 20 + 1e-3)
        c3 = (0 <= zmin + 1e-3 and zmax <= 130 + 1e-3)
        c4 = abs(xmin) < 0.1 # touches wall at x=0
        
        ok = all([c1, c2, c3, c4])
        results["R2"] = {
            "status": "pass" if ok else "fail",
            "value": [float(xmin), float(xmax), float(ymin), float(ymax), float(zmin), float(zmax)],
            "method": f"Checked bounding box: x[{xmin:.2f},{xmax:.2f}], y[{ymin:.2f},{ymax:.2f}], z[{zmin:.2f},{zmax:.2f}]",
            "criteria": [
                {"condition": "0 <= x <= 170", "measured": [float(xmin), float(xmax)], "ok": bool(c1)},
                {"condition": "-20 <= y <= 20", "measured": [float(ymin), float(ymax)], "ok": bool(c2)},
                {"condition": "0 <= z <= 130", "measured": [float(zmin), float(zmax)], "ok": bool(c3)},
                {"condition": "touches wall (min x = 0)", "measured": float(xmin), "ok": bool(c4)}
            ]
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Screw holes and screwdriver access
    try:
        hole_centers = [(0, 20), (0, 60)] # y, z
        target_diameter = 5.5
        radius = target_diameter / 2.0
        access_ok = True
        hole_measurements = []

        for yc, zc in hole_centers:
            # R3 Fix: To ensure the hole is actually there (and not just a solid block),
            # we check that the core cylinder is empty AND that material exists around it.
            probe_len = 200.0
            core = cq.Solid.makeCylinder(radius + 0.1, probe_len, pnt=cq.Vector(0, yc, zc), dir=cq.Vector(1, 0, 0))
            empty_vol = shape.intersect(core).Volume()
            diameter_ok = empty_vol < 0.5 # Hole is mostly empty

            # Verify material exists around the hole axis (walled check)
            wall_radius = radius + 2.0
            wall_shell = cq.Solid.makeCylinder(wall_radius, probe_len, pnt=cq.Vector(0, yc, zc), dir=cq.Vector(1, 0, 0)).cut(core)
            walled_vol = shape.intersect(wall_shell).Volume() / wall_shell.Volume()
            material_exists = walled_vol > 0.8 # Material surrounds the hole

            # Screwdriver access: no material within 4 mm of axis for x >= 10
            access_probe = cq.Solid.makeCylinder(4.0, 170.0, pnt=cq.Vector(10, yc, zc), dir=cq.Vector(1, 0, 0))
            intersection_vol = shape.intersect(access_probe).Volume()
            clearance_ok = intersection_vol < 1e-3

            hole_measurements.append({
                "center": [yc, zc],
                "diameter_check_ok": bool(diameter_ok and material_exists),
                "empty_vol": float(empty_vol),
                "clearance_vol": float(intersection_vol)
            })

            if not (diameter_ok and material_exists and clearance_ok):
                access_ok = False

        results["R3"] = {
            "status": "pass" if access_ok else "fail",
            "value": hole_measurements,
            "method": "Verified 5.5mm diameter holes are empty, surrounded by material, and have 4mm clearance for x >= 10.",
            "criteria": [
                {"condition": "Two screw holes diameter 5.5 mm", "measured": bool(all(h["diameter_check_ok"] for h in hole_measurements)), "ok": bool(all(h["diameter_check_ok"] for h in hole_measurements))},
                {"condition": "No material within 4mm of axis for x >= 10", "measured": bool(access_ok), "ok": bool(access_ok)}
            ]
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Shelf support
    try:
        # R4 Fix: Verify top surface is at exactly z=110. 
        # We check if material exists in a very thin slice just below z=110 and none above it.
        z_target = 110.0
        thickness = 0.2
        
        # Check solid material directly below z=110 between x=140 and 150 around y=0
        support_probe = cq.Solid.makeBox(10, 2, thickness, pnt=cq.Vector(140, -1, z_target - thickness)) 
        support_vol = shape.intersect(support_probe).Volume()
        # Expected volume: 10 * 2 * 0.2 = 4.0 mm3
        shelf_ok = support_vol > (10 * 2 * thickness * 0.9)

        # Check nothing is above z=110 for x >= 8
        probe_above = cq.Solid.makeBox(162, 40, 20, pnt=cq.Vector(8, -20, z_target))
        above_vol = shape.intersect(probe_above).Volume()
        nothing_above_ok = above_vol < 1e-3

        results["R4"] = {
            "status": "pass" if (shelf_ok and nothing_above_ok) else "fail",
            "value": {"support_vol": float(support_vol), "above_z110_vol": float(above_vol)},
            "method": f"Verified material exists in slice [x:140-150, y:-1-1, z:{z_target-thickness}-{z_target}] and no material above z={z_target} for x>=8",
            "criteria": [
                {"condition": "top surface at z=110 reaches x=150 (solid below)", "measured": float(support_vol), "ok": bool(shelf_ok)},
                {"condition": "nothing above z=110 for x >= 8", "measured": float(above_vol), "ok": bool(nothing_above_ok)}
            ]
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5 & R6: Strength and Stiffness (Section at x=10)
    try:
        x0 = 10.0
        h_step = 0.5 
        ylo, yhi = mesh.bounds[0][1], mesh.bounds[1][1]
        zlo, zhi = mesh.bounds[0][2], mesh.bounds[1][2]
        
        Y, Z = np.meshgrid(np.arange(ylo, yhi, h_step) + h_step/2, 
                           np.arange(zlo, zhi, h_step) + h_step/2)
        pts = np.column_stack([np.full(Y.size, x0), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not np.any(inside):
            raise ValueError("No material found at section x=10")

        z_vals = pts[inside, 2]
        A = inside.sum() * (h_step**2)
        zc = z_vals.mean()
        I = ((z_vals - zc)**2).sum() * (h_step**2)
        c = np.max(np.abs(z_vals - zc))

        M = F * L_load
        sigma = M * c / I
        stress_ok = sigma <= 20.0 + 1e-3

        delta = (F * (L_load**3)) / (3 * E * I)
        stiffness_ok = delta <= 2.0 + 1e-3

        results["R5"] = {
            "status": "pass" if stress_ok else "fail",
            "value": float(sigma),
            "method": f"M={M} Nmm, c={c:.2f} mm, I={I:.1f} mm4. sigma=Mc/I",
            "criteria": [{"condition": "bending stress <= 20 MPa", "measured": float(sigma), "ok": bool(stress_ok)}]
        }
        results["R6"] = {
            "status": "pass" if stiffness_ok else "fail",
            "value": float(delta),
            "method": f"F={F} N, L={L_load} mm, E={E} MPa, I={I:.1f} mm4. delta=FL^3/3EI",
            "criteria": [{"condition": "deflection <= 2.0 mm", "measured": float(delta), "ok": bool(stiffness_ok)}]
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass
    try:
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * density / 1000.0
        mass_ok = mass_g <= 90.0 + 1e-3
        results["R7"] = {
            "status": "pass" if mass_ok else "fail",
            "value": float(mass_g),
            "method": f"Volume={vol_mm3:.1f} mm3, density=1.24 g/cm3. mass = vol * dens / 1000",
            "criteria": [{"condition": "Mass <= 90 g", "measured": float(mass_g), "ok": bool(mass_ok)}]
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()