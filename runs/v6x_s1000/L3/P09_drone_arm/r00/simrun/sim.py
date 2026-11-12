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
            "note": f"Found {n_solids} solid(s)"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R2: Envelope
    try:
        bbox = shape.BoundingBox()
        xmin, xmax = bbox.xmin, bbox.xmax
        ymin, ymax = bbox.ymin, bbox.ymax
        zmin, zmax = bbox.zmin, bbox.zmax
        height = zmax - zmin
        
        c1 = xmin >= -0.01
        c2 = xmax <= 136.01
        c3 = ymin >= -16.01 and ymax <= 16.01
        c4 = zmin >= -0.01
        c5 = height <= 20.01

        ok = all([c1, c2, c3, c4, c5])
        results["R2"] = {
            "status": "pass" if ok else "fail",
            "value": [float(xmin), float(xmax), float(ymin), float(ymax), float(zmin), float(height)],
            "method": f"Measured bounding box: x[{xmin:.2f},{xmax:.2f}], y[{ymin:.2f},{ymax:.2f}], z[{zmin:.2f},{zmax:.2f}]",
            "criteria": [
                {"condition": "minimum x = 0", "measured": float(xmin), "ok": bool(c1)},
                {"condition": "maximum x <= 136", "measured": float(xmax), "ok": bool(c2)},
                {"condition": "|y| <= 16", "measured": [float(ymin), float(ymax)], "ok": bool(c3)},
                {"condition": "minimum z = 0", "measured": float(zmin), "ok": bool(c4)},
                {"condition": "height <= 20 mm", "measured": float(height), "ok": bool(c5)}
            ]
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R3 & R4: Holes (using probe method)
    def check_hole(center_x, center_y, diameter, length=150):
        p = (center_x, center_y, -20.0) 
        a = (0, 0, 1)
        core = cq.Solid.makeCylinder(diameter / 2.0 - 0.15, length, pnt=cq.Vector(*p), dir=cq.Vector(*a))
        wall_inner = diameter / 2.0 + 0.15
        wall_outer = diameter / 2.0 + 1.0
        wall = cq.Solid.makeCylinder(wall_outer, length, pnt=cq.Vector(*p), dir=cq.Vector(*a)).cut(
               cq.Solid.makeCylinder(wall_inner, length, pnt=cq.Vector(*p), dir=cq.Vector(*a)))
        
        empty_vol = shape.intersect(core).Volume() / core.Volume()
        walled_vol = shape.intersect(wall).Volume() / wall.Volume()
        return empty_vol, walled_vol

    # R3: Frame attachment holes (6, +-6)
    try:
        h1_e, h1_w = check_hole(6, 6, 3.2)
        h2_e, h2_w = check_hole(6, -6, 3.2)
        r3_ok = (h1_e < 0.05 and h1_w > 0.9) and (h2_e < 0.05 and h2_w > 0.9)
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": [float(h1_e), float(h1_w), float(h2_e), float(h2_w)],
            "method": f"Probed two vertical holes at (6, +-6) with D=3.2mm",
            "criteria": [{"condition": "two vertical holes, diameter 3.2 mm, at (x, y) = (6, +-6)", "measured": float(r3_ok), "ok": bool(r3_ok)}]
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R4: Motor mount holes (120 +- 8, +-9.5) and shaft hole (120, 0)
    try:
        motor_holes = [(112, 9.5), (128, 9.5), (112, -9.5), (128, -9.5)]
        m_ok = True
        for mx, my in motor_holes:
            e, w = check_hole(mx, my, 3.2)
            if not (e < 0.05 and w > 0.9): m_ok = False
        
        s_e, s_w = check_hole(120, 0, 6.0)
        shaft_ok = (s_e < 0.05 and s_w > 0.9)
        r4_ok = m_ok and shaft_ok

        results["R4"] = {
            "status": "pass" if r4_ok else "fail",
            "value": {"motor_holes_ok": bool(m_ok), "shaft_hole_ok": bool(shaft_ok)},
            "method": "Probed four 3.2mm holes and one 6mm shaft hole",
            "criteria": [
                {"condition": "four vertical holes, diameter 3.2 mm, at (x, y) = (120 +- 8, +-9.5)", "measured": float(m_ok), "ok": bool(m_ok)},
                {"condition": "6 mm vertical clearance hole for the shaft at (120, 0)", "measured": float(shaft_ok), "ok": bool(shaft_ok)}
            ]
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R5 & R6: Strength and Stiffness (Section at x=20)
    try:
        x_cut = 20.0
        h_step = 0.2 # Finer step for better integration accuracy
        y_lo, y_hi = mesh.bounds[0][1], mesh.bounds[1][1]
        z_lo, z_hi = mesh.bounds[0][2], mesh.bounds[1][2]
        Y, Z = np.meshgrid(np.arange(y_lo, y_hi, h_step) + h_step/2, np.arange(z_lo, z_hi, h_step) + h_step/2)
        pts = np.column_stack([np.full(Y.size, x_cut), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not np.any(inside):
            raise ValueError("No material found at section x=20")

        # Correct Section Properties Calculation via discrete integration
        z_vals = pts[inside, 2]
        y_vals = pts[inside, 1]
        A = inside.sum() * (h_step**2)
        zc = z_vals.mean() # Neutral axis in Z
        # I = integral( (z - zc)^2 dA )
        I = ((z_vals - zc)**2).sum() * (h_step**2)
        # c is the distance to the extreme fiber from neutral axis
        c = np.max(np.abs(z_vals - zc))

        F = 12.0
        L_moment = 100.0 # Distance from load at x=120 to section at x=20 is 100mm
        M = F * L_moment
        sigma = (M * c) / I if I > 0 else float('inf')

        E = 3500.0
        L_deflect = 100.0 # Specified deflection length
        # R6 asks for tip deflection estimate: F*L^3/(3*E*I) <= 1.0 mm
        # Note: The requirement says "I of the x=20 section <= 1.0 mm" which is a typo in spec, 
        # but it likely means the resulting deflection must be <= 1.0mm. 
        # However, I will follow the literal text for R6's 'criteria' if possible, 
        # but usually "I ... <= 1.0" refers to the result of the formula.
        deflection = (F * L_deflect**3) / (3 * E * I) if I > 0 else float('inf')

        r5_ok = sigma <= 30.0
        # Re-reading R6: "I of the x=20 section <= 1.0 mm" is dimensionally wrong for I.
        # It must mean deflection <= 1.0mm.
        r6_ok = deflection <= 1.0

        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": float(sigma),
            "method": f"M={F}*L={L_moment}, c={c:.2f}, I={I:.2f}, sigma=Mc/I",
            "criteria": [{"condition": "bending stress must be <= 30 MPa", "measured": float(sigma), "ok": bool(r5_ok)}]
        }
        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": float(deflection),
            "method": f"Deflection estimate: {deflection:.2f} mm (I={I:.2f})",
            "criteria": [{"condition": "tip deflection <= 1.0 mm", "measured": float(deflection), "ok": bool(r6_ok)}]
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R7: Mass <= 20g
    try:
        vol_mm3 = mesh.volume
        density_gcm3 = 1.24
        mass_g = (vol_mm3 * density_gcm3) / 1000.0
        r7_ok = mass_g <= 20.001
        results["R7"] = {
            "status": "pass" if r7_ok else "fail",
            "value": float(mass_g),
            "method": f"mass = volume({vol_mm3:.1f}) * density(1.24) / 1000",
            "criteria": [{"condition": "Mass <= 20 g", "measured": float(mass_g), "ok": bool(r7_ok)}]
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()