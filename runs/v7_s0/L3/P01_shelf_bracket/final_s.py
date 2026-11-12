import cadquery as cq
import numpy as np
import trimesh
import json

def run_checks():
    results = {}
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    # Constants
    DENSITY_G_MM3 = 1.24 / 1000  # g/mm3
    E_PLA = 3500          # MPa (N/mm2)
    LOAD_F = 150          # N
    SECTION_X = 10        # mm
    L_CANTILEVER = 140    # mm (distance from x=10 to x=150)

    # R1: Single valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": float(n_solids),
            "method": f"Counted number of solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": (status == "pass")}],
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
        
        c_fit_x = (xmin >= -0.1) and (xmax <= 170.1)
        c_fit_y = (ymin >= -20.1) and (ymax <= 20.1)
        c_fit_z = (zmin >= -0.1) and (zmax <= 130.1)
        c_touches_wall = abs(xmin) < 0.5

        ok = c_fit_x and c_fit_y and c_fit_z and c_touches_wall
        results["R2"] = {
            "status": "pass" if ok else "fail",
            "value": [float(xmin), float(xmax), float(ymin), float(ymax), float(zmin), float(zmax)],
            "method": f"Checked bounding box: x[{xmin:.2f},{xmax:.2f}], y[{ymin:.2f},{ymax:.2f}], z[{zmin:.2f},{zmax:.2f}]",
            "criteria": [
                {"condition": "0 <= x <= 170", "measured": float(xmin), "ok": bool(c_fit_x)},
                {"condition": "-20 <= y <= 20", "measured": float(ymin), "ok": bool(c_fit_y)},
                {"condition": "0 <= z <= 130", "measured": float(zmin), "ok": bool(c_fit_z)},
                {"condition": "touches the wall (min x = 0)", "measured": float(xmin), "ok": bool(c_touches_wall)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R3: Screw holes and screwdriver access (FIXED)
    try:
        diameter = 5.5
        radius = diameter / 2
        access_ok = True
        hole_metrics = []

        for cy, cz in [(0, 20), (0, 60)]:
            # Hole existence check: Must be empty AND must have material surrounding it at the wall (x=0)
            # We probe a cylinder from x=-1 to x=5. If it's mostly empty, there is a hole.
            # To ensure it "sits on the wall", we verify that a shell around the diameter exists near x=0.
            hole_probe = cq.Solid.makeCylinder(radius, 10, pnt=cq.Vector(-2, cy, cz), dir=cq.Vector(1, 0, 0))
            empty_vol_ratio = shape.intersect(hole_probe).Volume() / hole_probe.Volume()
            # A real hole should have near-zero intersection with the solid in its core
            hole_exists = empty_vol_ratio < 0.05

            # Check if material surrounds the hole at the wall (x=0)
            # We use a slightly larger cylinder to see if it's "walled"
            wall_probe = cq.Solid.makeCylinder(radius + 2.0, 4.0, pnt=cq.Vector(-1, cy, cz), dir=cq.Vector(1, 0, 0))
            # The material in the wall probe should be (Wall Volume - Hole Volume)
            material_in_wall = wall_probe.Volume() - shape.intersect(hole_probe).Volume()
            walled_ratio = shape.intersect(wall_probe).Volume() / wall_probe.Volume()
            # If walled_ratio is high, it means the probe volume (which includes the hole) contains mostly solid.
            # Actually, let's check if the material exists in a ring around the hole at x=0.
            ring_shell = cq.Solid.makeCylinder(radius + 1.5, 2.0, pnt=cq.Vector(-0.5, cy, cz), dir=cq.Vector(1, 0, 0)).cut(
                         cq.Solid.makeCylinder(radius - 0.1, 2.0, pnt=cq.Vector(-0.5, cy, cz), dir=cq.Vector(1, 0, 0)))
            shell_intersection = shape.intersect(ring_shell).Volume() / ring_shell.Volume()
            is_walled = shell_intersection > 0.8

            # Screwdriver access check: No material within 4mm of axis for x >= 10.
            access_probe = cq.Solid.makeCylinder(4.0, 165, pnt=cq.Vector(10, cy, cz), dir=cq.Vector(1, 0, 0))
            access_vol = shape.intersect(access_probe).Volume()
            screwdriver_ok = access_vol < 1e-3

            hole_metrics.append({"exists": bool(hole_exists and is_walled), "access_vol": float(access_vol)})
            if not (hole_exists and is_walled and screwdriver_ok):
                access_ok = False

        results["R3"] = {
            "status": "pass" if access_ok else "fail",
            "value": hole_metrics,
            "method": f"Checked holes at (y=0,z=20) and (y=0,z=60). Verified existence/walling and screwdriver clearance (r=4, x>=10)",
            "criteria": [
                {"condition": "Two 5.5mm diameter screw holes exist through the wall", "measured": float(hole_metrics[0]["exists"]), "ok": bool(hole_metrics[0]["exists"])},
                {"condition": "Screwdriver access (no material within 4mm for x>=10)", "measured": hole_metrics[0]["access_vol"], "ok": bool(screwdriver_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R4: Shelf support (RE-VERIFIED)
    try:
        support_probe = cq.Solid.makeBox(10, 2, 5, pnt=cq.Vector(140, -1, 105)) 
        fill_fraction = shape.intersect(support_probe).Volume() / support_probe.Volume()
        above_probe = cq.Solid.makeBox(162, 40, 20, pnt=cq.Vector(8, -20, 110))
        forbidden_vol = shape.intersect(above_probe).Volume()

        ok = (fill_fraction > 0.9) and (forbidden_vol < 1e-3)
        results["R4"] = {
            "status": "pass" if ok else "fail",
            "value": [float(fill_fraction), float(forbidden_vol)],
            "method": f"Shelf support: fill fraction at x[140,150], y[-1,1], z[105,110] is {fill_fraction:.2f}. Forbidden volume above z=110 (x>=8) is {forbidden_vol:.4f}",
            "criteria": [
                {"condition": "solid material directly below z=110 between x=140 and 150", "measured": float(fill_fraction), "ok": bool(fill_fraction > 0.9)},
                {"condition": "nothing above z=110 for x >= 8", "measured": float(forbidden_vol), "ok": bool(forbidden_vol < 1e-3)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R5 & R6: Strength and Stiffness
    try:
        x0 = 10
        h_step = 0.5 
        ylo, yhi = mesh.bounds[0][1], mesh.bounds[1][1]
        zlo, zhi = mesh.bounds[0][2], mesh.bounds[1][2]
        
        Y, Z = np.meshgrid(np.arange(ylo, yhi, h_step) + h_step/2, np.arange(zlo, zhi, h_step) + h_step/2)
        pts = np.column_stack([np.full(Y.size, x0), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not np.any(inside):
            raise ValueError("No material found at section x=10")

        z_vals = pts[inside, 2]
        A = inside.sum() * (h_step**2)
        zc = z_vals.mean()
        I = ((z_vals - zc)**2).sum() * (h_step**2)
        c = abs(z_vals - zc).max()

        M = LOAD_F * L_CANTILEVER
        stress = M * c / I
        deflection = (LOAD_F * (L_CANTILEVER**3)) / (3 * E_PLA * I)

        results["R5"] = {
            "status": "pass" if stress <= 20.01 else "fail",
            "value": float(stress),
            "method": f"Cantilever at x=10: M={M} Nmm, c={c:.2f}, I={I:.2f}, sigma = {stress:.2f} MPa",
            "criteria": [{"condition": "bending stress <= 20 MPa", "measured": float(stress), "ok": bool(stress <= 20.01)}],
            "note": ""
        }
        results["R6"] = {
            "status": "pass" if deflection <= 2.01 else "fail",
            "value": float(deflection),
            "method": f"Deflection: F=150N, L=140mm, E=3500MPa, I={I:.2f}, delta = {deflection:.2f} mm",
            "criteria": [{"condition": "tip deflection <= 2.0 mm", "measured": float(deflection), "ok": bool(deflection <= 2.01)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass
    try:
        vol_mm3 = mesh.volume
        mass_g = vol_mm3 * DENSITY_G_MM3
        results["R7"] = {
            "status": "pass" if mass_g <= 90.1 else "fail",
            "value": float(mass_g),
            "method": f"Mass = Volume({vol_mm3:.2f} mm3) * Density({DENSITY_G_MM3*1000:.2f} g/cm3) / 1000",
            "criteria": [{"condition": "Mass <= 90 g", "measured": float(mass_g), "ok": bool(mass_g <= 90.1)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": 0.0, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    run_checks()