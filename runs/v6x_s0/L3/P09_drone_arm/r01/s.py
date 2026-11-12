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
            "value": float(n_solids),
            "method": "Counted number of solids in the STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": status == "pass"}],
            "note": f"{n_solids} solid(s) found"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "Count solids", "criteria": [], "note": str(e)}

    # R2: Envelope
    try:
        bbox = shape.BoundingBox()
        xmin, xmax = bbox.xmin, bbox.xmax
        ymin, ymax = bbox.ymin, bbox.ymax
        zmin, zmax = bbox.zmin, bbox.zmax
        height = zmax - zmin
        
        c1 = xmin >= -0.01
        c2 = xmax <= 136.01
        c3 = (ymin >= -16.01) and (ymax <= 16.01)
        c4 = zmin >= -0.01
        c5 = height <= 20.01
        
        ok = all([c1, c2, c3, c4, c5])
        results["R2"] = {
            "status": "pass" if ok else "fail",
            "value": [float(xmin), float(xmax), float(ymin), float(ymax), float(zmin), float(height)],
            "method": f"Measured BBox: x[{xmin:.2f}, {xmax:.2f}], y[{ymin:.2f}, {ymax:.2f}], z[{zmin:.2f}, {zmax:.2f}], h={height:.2f}",
            "criteria": [
                {"condition": "minimum x = 0", "measured": float(xmin), "ok": bool(c1)},
                {"condition": "maximum x <= 136", "measured": float(xmax), "ok": bool(c2)},
                {"condition": "|y| <= 16", "measured": [float(ymin), float(ymax)], "ok": bool(c3)},
                {"condition": "minimum z = 0", "measured": float(zmin), "ok": bool(c4)},
                {"condition": "height <= 20 mm", "measured": float(height), "ok": bool(c5)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "BBox check", "criteria": [], "note": str(e)}

    # R3 & R4: Holes (Helper function)
    def check_hole(p, a, D):
        L = 200.0 
        core = cq.Solid.makeCylinder(D/2 - 0.1, L, pnt=cq.Vector(*p), dir=cq.Vector(*a))
        wall = cq.Solid.makeCylinder(D/2 + 1.0, L, pnt=cq.Vector(*p), dir=cq.Vector(*a)).cut(
               cq.Solid.makeCylinder(D/2 + 0.1, L, pnt=cq.Vector(*p), dir=cq.Vector(*a)))
        
        empty_frac = shape.intersect(core).Volume() / core.Volume()
        walled_frac = shape.intersect(wall).Volume() / wall.Volume()
        return empty_frac, walled_frac

    # R3: Frame attachment holes
    try:
        h1_e, h1_w = check_hole((6, 6, -10), (0, 0, 1), 3.2)
        h2_e, h2_w = check_hole((6, -6, -10), (0, 0, 1), 3.2)
        r3_ok = (h1_e < 0.05 and h1_w > 0.9) and (h2_e < 0.05 and h2_w > 0.9)
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": [float(h1_e), float(h1_w), float(h2_e), float(h2_w)],
            "method": f"Probed two vertical holes at (6, +-6) with D=3.2mm. Empty/Walled ratios: {h1_e:.2f}/{h1_w:.2f}, {h2_e:.2f}/{h2_w:.2f}",
            "criteria": [{"condition": "two vertical holes, diameter 3.2 mm, at (x, y) = (6, +-6)", "measured": [float(h1_e), float(h1_w), float(h2_e), float(h2_w)], "ok": bool(r3_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "Hole check R3", "criteria": [], "note": str(e)}

    # R4: Motor mount holes
    try:
        m_holes = [(120+8, 9.5), (120-8, 9.5), (120+8, -9.5), (120-8, -9.5)]
        motor_ok = True
        for mx, my in m_holes:
            e, w = check_hole((mx, my, -10), (0, 0, 1), 3.2)
            if not (e < 0.05 and w > 0.9): motor_ok = False
        
        s_e, s_w = check_hole((120, 0, -10), (0, 0, 1), 6.0)
        if not (s_e < 0.05 and s_w > 0.9): motor_ok = False

        results["R4"] = {
            "status": "pass" if motor_ok else "fail",
            "value": None,
            "method": "Probed four 3.2mm holes at (120 +-8, +-9.5) and one 6mm shaft hole at (120, 0)",
            "criteria": [{"condition": "four vertical holes... and a 6 mm vertical clearance hole", "measured": 0.0, "ok": bool(motor_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "Hole check R4", "criteria": [], "note": str(e)}

    # R5 & R6: Section Properties at x=20 (Fixed Beam Theory)
    try:
        x0 = 20.0
        h_step = 0.1 # Finer step for better integration accuracy
        ylo, yhi = mesh.bounds[0][1], mesh.bounds[1][1]
        zlo, zhi = mesh.bounds[0][2], mesh.bounds[1][2]
        
        # Create a grid on the plane x=x0 within the bounding box of Y and Z
        Y_grid, Z_grid = np.meshgrid(np.arange(ylo, yhi, h_step) + h_step/2, 
                                     np.arange(zlo, zhi, h_step) + h_step/2)
        pts = np.column_stack([np.full(Y_grid.size, x0), Y_grid.ravel(), Z_grid.ravel()])
        
        # Check which points are inside the mesh at this specific slice
        inside = mesh.contains(pts)
        if not np.any(inside): 
            raise ValueError(f"No material found at section x={x0}")
        
        z_vals = pts[inside, 2]
        y_vals = pts[inside, 1]
        
        # Area and Moment of Inertia (I_zz) for the cross-section at x=20
        A = inside.sum() * (h_step**2)
        zc = z_vals.mean() # Neutral axis height (assuming symmetric/uniform density)
        # I = integral(z^2 dA) -> sum((z - zc)^2 * delta_A)
        I = ((z_vals - zc)**2).sum() * (h_step**2)
        # c is the distance to the extreme fiber from neutral axis
        c = np.max(np.abs(z_vals - zc))
        
        # R5: Bending Stress at x=20 due to 12N load at x=120
        F = 12.0
        L_moment = 120.0 - x0 # Distance from load to section
        M = F * L_moment
        sigma = M * c / I
        r5_ok = sigma <= 30.0
        
        # R6: Stiffness (Tip deflection)
        E = 3500.0
        L_deflect = 100.0 # Length for deflection calculation as per spec
        delta = (F * (L_deflect**3)) / (3 * E * I)
        r6_ok = delta <= 1.0

        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": float(sigma),
            "method": f"M={F}N*(120-{x0})mm={M:.1f}Nmm, c={c:.3f}, I={I:.3f}, sigma=Mc/I",
            "criteria": [{"condition": "bending stress must be <= 30 MPa", "measured": float(sigma), "ok": bool(r5_ok)}],
            "note": ""
        }
        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": float(delta),
            "method": f"F={F}N, L={L_deflect}mm, E={E}MPa, I={I:.3f}, delta=FL^3/3EI",
            "criteria": [{"condition": "tip deflection estimate ... <= 1.0 mm", "measured": float(delta), "ok": bool(r6_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "Beam theory R5", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "error", "value": None, "method": "Beam theory R6", "criteria": [], "note": str(e)}

    # R7: Mass
    try:
        vol_mm3 = mesh.volume
        density_gcm3 = 1.24
        mass_g = vol_mm3 * density_gcm3 / 1000.0
        r7_ok = mass_g <= 20.0
        results["R7"] = {
            "status": "pass" if r7_ok else "fail",
            "value": float(mass_g),
            "method": f"Volume={vol_mm3:.2f}mm3, Density=1.24g/cm3, Mass=V*rho/1000",
            "criteria": [{"condition": "Mass <= 20 g", "measured": float(mass_g), "ok": bool(r7_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "Mass check", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()