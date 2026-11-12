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
    density_gcm3 = 1.24
    E_mpa = 3500.0
    F_n = 150.0
    L_cantilever = 140.0  # distance from x=10 to load at x=150

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        is_valid = n_solids == 1
        results["R1"] = {
            "status": "pass" if is_valid else "fail",
            "value": n_solids,
            "method": "Counted number of solids in the STEP file.",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": bool(is_valid)}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Envelope
    try:
        bbox = shape.BoundingBox()
        xmin, xmax = bbox.xmin, bbox.xmax
        ymin, ymax = bbox.ymin, bbox.ymax
        zmin, zmax = bbox.zmin, bbox.zmax
        
        c1 = (0 <= xmin <= 0.1) and (xmax <= 170.1)
        c2 = (-20.1 <= ymin) and (ymax <= 20.1)
        c3 = (0 <= zmin <= 0.1) and (zmax <= 130.1)
        c4 = abs(xmin - 0) < 0.5 # touches wall
        
        ok = all([c1, c2, c3, c4])
        results["R2"] = {
            "status": "pass" if ok else "fail",
            "value": [float(xmin), float(xmax), float(ymin), float(ymax), float(zmin), float(zmax)],
            "method": f"Checked bounding box: x[{xmin:.2f},{xmax:.2f}], y[{ymin:.2f},{ymax:.2f}], z[{zmin:.2f},{zmax:.2f}]",
            "criteria": [
                {"condition": "0 <= x <= 170 and touches wall (x=0)", "measured": float(xmin), "ok": bool(c1 and c4)},
                {"condition": "-20 <= y <= 20", "measured": [float(ymin), float(ymax)], "ok": bool(c2)},
                {"condition": "0 <= z <= 130", "measured": [float(zmin), float(zmax)], "ok": bool(c3)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Screw holes and screwdriver access
    try:
        diameter_req = 5.5
        radius_req = diameter_req / 2.0
        access_ok = True
        hole_results = []

        for cy, cz in [(0, 20), (0, 60)]:
            # To verify the hole exists and has correct diameter:
            # We probe with a cylinder of exactly the required diameter.
            # If it's a real hole, the intersection volume should be near zero.
            # To ensure it's not just "empty space" elsewhere, we check if material 
            # surrounds it (walled_vol).
            probe_len = 180.0 # Long enough to pass through part
            hole_probe = cq.Solid.makeCylinder(radius_req, probe_len, pnt=cq.Vector(-5, cy, cz), dir=cq.Vector(1, 0, 0))
            
            # The volume of the hole in the part should be near zero
            empty_vol_ratio = shape.intersect(hole_probe).Volume() / hole_probe.Volume()
            
            # Check if there is material around it (to distinguish from a void/missing part)
            wall_thickness = 1.0
            wall_shell = cq.Solid.makeCylinder(radius_req + wall_thickness, probe_len, pnt=cq.Vector(-5, cy, cz), dir=cq.Vector(1, 0, 0)).cut(
                         cq.Solid.makeCylinder(radius_req - 0.1, probe_len, pnt=cq.Vector(-5, cy, cz), dir=cq.Vector(1, 0, 0)))
            walled_vol_ratio = shape.intersect(wall_shell).Volume() / wall_shell.Volume()

            # Screwdriver clearance: no material within 4mm of axis for x >= 10
            clearance_probe = cq.Solid.makeCylinder(4.0, 170.0, pnt=cq.Vector(10, cy, cz), dir=cq.Vector(1, 0, 0))
            inter_vol = shape.intersect(clearance_probe).Volume()
            
            # A hole is valid if it's empty (ratio ~0) AND surrounded by material (ratio ~1)
            # and screwdriver clearance has no intersection volume.
            h_ok = (empty_vol_ratio < 0.05) and (walled_vol_ratio > 0.8) and (inter_vol < 0.1)
            hole_results.append({"cy": cy, "cz": cz, "empty_ratio": float(empty_vol_ratio), "walled_ratio": float(walled_vol_ratio), "clearance_vol": float(inter_vol), "ok": bool(h_ok)})
            if not h_ok: access_ok = False

        results["R3"] = {
            "status": "pass" if access_ok else "fail",
            "value": hole_results,
            "method": "Verified holes via intersection with diameter-matched cylinders and checked screwdriver clearance (R=4) for x>=10.",
            "criteria": [
                {"condition": "Two 5.5mm holes exist and are surrounded by material", "measured": access_ok, "ok": bool(access_ok)},
                {"condition": "Screwdriver clearance (R=4, x>=10) is empty", "measured": access_ok, "ok": bool(access_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Shelf support
    try:
        # Check solid material directly below z=110 between x=140 and 150 around y=0
        probe_box = cq.Solid.makeBox(10, 10, 5, pnt=cq.Vector(140, -5, 105))
        fill_fraction = shape.intersect(probe_box).Volume() / probe_box.Volume()
        shelf_ok = fill_fraction > 0.9

        # Nothing of the bracket may be above z = 110 for x >= 8
        forbidden_zone = cq.Solid.makeBox(200, 50, 50, pnt=cq.Vector(8, -25, 110))
        forbidden_vol = shape.intersect(forbidden_zone).Volume()
        no_overhang = forbidden_vol < 0.01

        results["R4"] = {
            "status": "pass" if (shelf_ok and no_overhang) else "fail",
            "value": [float(fill_fraction), float(forbidden_vol)],
            "method": f"Checked fill fraction in x[140,150],y[-5,5],z[105,110] ({fill_fraction:.2f}) and volume above z=110 for x>=8 ({forbidden_vol:.2f})",
            "criteria": [
                {"condition": "Solid material below z=110 between x=140-150", "measured": float(fill_fraction), "ok": bool(shelf_ok)},
                {"condition": "Nothing above z=110 for x >= 8", "measured": float(forbidden_vol), "ok": bool(no_overhang)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5 & R6: Strength and Stiffness (Section at x=10)
    try:
        x_plane = 10.0
        h_step = 0.4
        b = mesh.bounds
        y_range = np.arange(b[0][1], b[1][1], h_step) + h_step/2
        z_range = np.arange(b[0][2], b[1][2], h_step) + h_step/2
        Y, Z = np.meshgrid(y_range, z_range)
        pts_slice = np.column_stack([np.full(Y.size, x_plane), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts_slice)
        
        if not np.any(inside):
            raise ValueError("No material found at section x=10")

        A = inside.sum() * (h_step**2)
        z_vals = Z.ravel()[inside]
        zc = np.mean(z_vals)
        I = np.sum((z_vals - zc)**2) * (h_step**2)
        c = np.max(np.abs(z_vals - zc))

        M = F_n * L_cantilever
        sigma = (M * c) / I
        r5_ok = sigma <= 20.01

        deflection = (F_n * (L_cantilever**3)) / (3 * E_mpa * I)
        r6_ok = deflection <= 2.01

        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": float(sigma),
            "method": f"M={M} Nmm, c={c:.2f} mm, I={I:.2f} mm4, sigma=M*c/I",
            "criteria": [{"condition": "bending stress <= 20 MPa", "measured": float(sigma), "ok": bool(r5_ok)}],
            "note": ""
        }
        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": float(deflection),
            "method": f"F={F_n} N, L={L_cantilever} mm, E={E_mpa} MPa, I={I:.2f} mm4, delta=FL^3/3EI",
            "criteria": [{"condition": "deflection <= 2.0 mm", "measured": float(deflection), "ok": bool(r6_ok)}],
            "note": ""
        }

    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 90 g
    try:
        vol_mm3 = mesh.volume
        mass_g = vol_mm3 * density_gcm3 / 1000.0
        r7_ok = mass_g <= 90.01
        results["R7"] = {
            "status": "pass" if r7_ok else "fail",
            "value": float(mass_g),
            "method": f"Volume={vol_mm3:.2f} mm3, density=1.24 g/cm3, mass=V*rho/1000",
            "criteria": [{"condition": "Mass <= 90 g", "measured": float(mass_g), "ok": bool(r7_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()