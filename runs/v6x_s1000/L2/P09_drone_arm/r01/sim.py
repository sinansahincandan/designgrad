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

    # R3 & R4: Holes (Improved probe method)
    # To ensure holes are part of a continuous solid and not just empty space or thin shells,
    # we check: 1. The core is empty. 2. A slightly larger cylinder around the hole is mostly solid material.
    def check_hole_robust(center_x, center_y, diameter, height=30.0):
        # We probe a vertical column through the part's expected Z range
        p = (center_x, center_y, -15.0) 
        a = (0, 0, 1)
        
        # Core: The actual hole diameter. Should be empty.
        core = cq.Solid.makeCylinder(diameter / 2.0, height, pnt=cq.Vector(*p), dir=cq.Vector(*a))
        # Shell: A larger cylinder around the hole. Should contain significant material to prove it's a feature in a solid.
        shell_r = diameter / 2.0 + 2.0 
        shell = cq.Solid.makeCylinder(shell_r, height, pnt=cq.Vector(*p), dir=cq.Vector(*a))
        
        # Intersection volumes
        core_empty_ratio = shape.intersect(core).Volume() / core.Volume()
        shell_solid_ratio = shape.intersect(shell).Volume() / shell.Volume()
        
        # A hole is valid if the center is empty AND the surrounding area is mostly solid material.
        # This distinguishes a hole in a part from just an empty region or a floating thin ring.
        is_hole = (core_empty_ratio < 0.05) and (shell_solid_ratio > 0.7)
        return is_hole, core_empty_ratio, shell_solid_ratio

    # R3: Frame attachment holes (6, +-6)
    try:
        h1_ok, h1_e, h1_s = check_hole_robust(6, 6, 3.2)
        h2_ok, h2_e, h2_s = check_hole_robust(6, -6, 3.2)
        r3_ok = h1_ok and h2_ok
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": [float(h1_e), float(h1_s), float(h2_e), float(h2_s)],
            "method": f"Robustly probed two vertical holes at (6, +-6) with D=3.2mm",
            "criteria": [{"condition": "two vertical holes, diameter 3.2 mm, at (x, y) = (6, +-6)", "measured": float(r3_ok), "ok": bool(r3_ok)}]
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R4: Motor mount holes (120 +- 8, +-9.5) and shaft hole (120, 0)
    try:
        motor_holes = [(112, 9.5), (128, 9.5), (112, -9.5), (128, -9.5)]
        m_ok = True
        for mx, my in motor_holes:
            h_ok, _, _ = check_hole_robust(mx, my, 3.2)
            if not h_ok: m_ok = False
        
        s_ok, _, _ = check_hole_robust(120, 0, 6.0)
        r4_ok = m_ok and s_ok

        results["R4"] = {
            "status": "pass" if r4_ok else "fail",
            "value": {"motor_holes_ok": bool(m_ok), "shaft_hole_ok": bool(s_ok)},
            "method": "Robustly probed four 3.2mm holes and one 6mm shaft hole",
            "criteria": [
                {"condition": "four vertical holes, diameter 3.2 mm, at (x, y) = (120 +- 8, +-9.5)", "measured": float(m_ok), "ok": bool(m_ok)},
                {"condition": "6 mm vertical clearance hole for the shaft at (120, 0)", "measured": float(s_ok), "ok": bool(s_ok)}
            ]
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

    # R5 & R6: Strength and Stiffness (Section at x=20)
    try:
        x_cut = 20.0
        h_step = 0.4 
        y_lo, y_hi = mesh.bounds[0][1], mesh.bounds[1][1]
        z_lo, z_hi = mesh.bounds[0][2], mesh.bounds[1][2]
        Y, Z = np.meshgrid(np.arange(y_lo, y_hi, h_step) + h_step/2, np.arange(z_lo, z_hi, h_step) + h_step/2)
        pts = np.column_stack([np.full(Y.size, x_cut), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not np.any(inside):
            for dx in [0.1, -0.1, 0.5, -0.5, 1.0, -1.0]:
                pts = np.column_stack([np.full(Y.size, x_cut + dx), Y.ravel(), Z.ravel()])
                inside = mesh.contains(pts)
                if np.any(inside):
                    x_cut += dx
                    break

        if not np.any(inside):
            raise ValueError("No material found at or near section x=20")

        z_vals = pts[inside, 2]
        zc = z_vals.mean()
        I = ((z_vals - zc)**2).sum() * (h_step**2)
        c = np.max(np.abs(z_vals - zc))

        F = 12.0
        L_moment = 100.0 
        M = F * L_moment
        sigma = (M * c) / I if I > 0 else float('inf')

        E = 3500.0
        L_deflect = 100.0 
        deflection = (F * L_deflect**3) / (3 * E * I) if I > 0 else float('inf')

        r5_ok = sigma <= 30.0
        r6_ok = deflection <= 1.0

        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": float(sigma),
            "method": f"M={F}*L={L_moment}, c={c:.2f}, I={I:.2f}, sigma=Mc/I at x={x_cut}",
            "criteria": [{"condition": "bending stress must be <= 30 MPa", "measured": float(sigma), "ok": bool(r5_ok)}]
        }
        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": float(deflection),
            "method": f"Deflection estimate: {deflection:.2f} mm (I={I:.2f}) at x={x_cut}",
            "criteria": [{"condition": "tip deflection <= 1.0 mm", "measured": float(deflection), "ok": bool(r6_ok)}]
        }
    except Exception as e:
        results["R5"] = {"status": "fail", "value": None, "method": "N/A", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "fail", "value": None, "method": "N/A", "criteria": [], "note": str(e)}

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