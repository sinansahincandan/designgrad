import cadquery as cq
import trimesh
import numpy as np
import json

def run_verification():
    results = {}
    # Load the part
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(f"Critical Error: Could not load files: {e}")
        return

    # Constants
    DENSITY_GCM3 = 1.24
    DENSITY_GMM3 = DENSITY_GCM3 / 1000  # g/mm3
    E_MODULUS = 3500       # MPa (N/mm2)
    LOAD_F = 150           # N
    LOAD_X = 150           # mm
    SECTION_X = 10         # mm
    L_CANTILEVER = 140     # mm (distance from x=10 to load at x=150)

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": float(n_solids),
            "method": f"Counted solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": status == "pass"}],
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
        
        c_x = (xmin >= -0.1) and (xmax <= 170.1)
        c_y = (ymin >= -20.1) and (ymax <= 20.1)
        c_z = (zmin >= -0.1) and (zmax <= 130.1)
        c_wall = abs(xmin) < 0.5

        status = "pass" if all([c_x, c_y, c_z, c_wall]) else "fail"
        results["R2"] = {
            "status": status,
            "value": [float(xmin), float(xmax), float(ymin), float(ymax), float(zmin), float(zmax)],
            "method": f"Checked BBox: x[{xmin:.2f},{xmax:.2f}], y[{ymin:.2f},{ymax:.2f}], z[{zmin:.2f},{zmax:.2f}]",
            "criteria": [
                {"condition": "0 <= x <= 170", "measured": [float(xmin), float(xmax)], "ok": bool(c_x)},
                {"condition": "-20 <= y <= 20", "measured": [float(ymin), float(ymax)], "ok": bool(c_y)},
                {"condition": "0 <= z <= 130", "measured": [float(zmin), float(zmax)], "ok": bool(c_z)},
                {"condition": "touches wall (min x = 0)", "measured": float(xmin), "ok": bool(c_wall)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Screw holes and clearance (FIXED)
    try:
        holes_ok = True
        hole_centers = [(0, 20), (0, 60)] # y, z
        target_dia = 5.5
        target_rad = target_dia / 2
        bbox_xmax = shape.BoundingBox().xmax
        
        for hy, hz in hole_centers:
            # 1. Verify the hole exists (absence of material) and has correct diameter
            # We check if a cylinder of the target diameter is empty.
            hole_probe = cq.Solid.makeCylinder(target_rad, bbox_xmax + 2, pnt=cq.Vector(-0.1, hy, hz), dir=cq.Vector(1, 0, 0))
            # If volume of intersection is > small epsilon, the hole is not empty/correctly sized
            if shape.intersect(hole_probe).Volume() > 0.5:
                holes_ok = False

            # 2. Verify presence of surrounding material (the part isn't just a void)
            # We check if there is solid material at the hole location but slightly offset in Y/Z
            # This ensures we aren't just looking at an empty space.
            material_probe = cq.Solid.makeBox(2, 10, 10, pnt=cq.Vector(-1, hy-5, hz-5))
            if shape.intersect(material_probe).Volume() < 1.0:
                holes_ok = False

            # 3. Verify clearance for x >= 10 (no material within 4mm of axis)
            clearance_tool = cq.Solid.makeCylinder(4.0, bbox_xmax + 5, pnt=cq.Vector(10, hy, hz), dir=cq.Vector(1, 0, 0))
            clearance_vol = shape.intersect(clearance_tool).Volume()
            if clearance_vol > 0.1: 
                holes_ok = False

        status = "pass" if holes_ok else "fail"
        results["R3"] = {
            "status": status,
            "value": float(holes_ok),
            "method": f"Verified 5.5mm through-holes at (0,20),(0,60) with surrounding material and 4mm clearance for x>=10",
            "criteria": [{"condition": "Holes diameter 5.5mm, correct location, and 4mm clearance for x>=10", "measured": float(holes_ok), "ok": bool(holes_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Shelf support
    try:
        z_target = 110.0
        shelf_probe = cq.Solid.makeBox(10, 5, 10, pnt=cq.Vector(140, -2.5, 100))
        intersect_vol = shape.intersect(shelf_probe).Volume()
        shelf_exists = intersect_vol > 10.0 

        forbidden_mask = (mesh.vertices[:, 0] >= 8.0) & (mesh.vertices[:, 2] > z_target + 0.1)
        too_high = np.any(forbidden_mask)

        shelf_region_mask = (mesh.vertices[:, 0] >= 139) & (mesh.vertices[:, 0] <= 151) & \
                            (mesh.vertices[:, 1] >= -2.5) & (mesh.vertices[:, 1] <= 2.5)
        if np.any(shelf_region_mask):
            max_z_at_shelf = np.max(mesh.vertices[shelf_region_mask, 2])
            surface_ok = abs(max_z_at_shelf - z_target) < 0.5
        else:
            surface_ok = False

        status = "pass" if (shelf_exists and not too_high and surface_ok) else "fail"
        results["R4"] = {
            "status": status,
            "value": [float(shelf_exists), float(too_high), float(surface_ok)],
            "method": f"Shelf existence: {shelf_exists}; High material check (z>110, x>=8): {too_high}; Surface at z=110: {surface_ok}",
            "criteria": [
                {"condition": "solid material directly below z=110 between x=140 and 150 around y=0", "measured": float(shelf_exists), "ok": bool(shelf_exists)},
                {"condition": "Nothing of the bracket may be above z=110 for x >= 8", "measured": float(too_high), "ok": not bool(too_high)},
                {"condition": "Shelf surface at exactly z=110", "measured": float(surface_ok), "ok": bool(surface_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5 & R6: Strength and Stiffness
    try:
        x0 = SECTION_X
        h = 0.5 
        ylo, yhi = mesh.bounds[0][1], mesh.bounds[1][1]
        zlo, zhi = mesh.bounds[0][2], mesh.bounds[1][2]
        Y, Z = np.meshgrid(np.arange(ylo, yhi, h) + h/2, np.arange(zlo, zhi, h) + h/2)
        pts = np.column_stack([np.full(Y.size, x0), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not inside.any():
            x0_alt = SECTION_X + 0.5
            pts = np.column_stack([np.full(Y.size, x0_alt), Y.ravel(), Z.ravel()])
            inside = mesh.contains(pts)
            if not inside.any():
                raise ValueError("No material found at section x=10")

        z_vals = pts[inside, 2]
        y_vals = pts[inside, 1]
        A = inside.sum() * (h**2)
        zc = np.mean(z_vals)
        I = np.sum((z_vals - zc)**2) * (h**2)
        c = np.max(np.abs(z_vals - zc))

        if I <= 0: raise ValueError("Moment of inertia is zero or negative")

        M = LOAD_F * (LOAD_X - SECTION_X)
        stress = M * c / I
        r5_ok = stress <= 20.0 + 1e-3

        deflection = (LOAD_F * L_CANTILEVER**3) / (3 * E_MODULUS * I)
        r6_ok = deflection <= 2.0 + 1e-3

        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": float(stress),
            "method": f"M={M} Nmm, c={c:.2f} mm, I={I:.2f} mm4, sigma=M*c/I={stress:.2f} MPa",
            "criteria": [{"condition": "bending stress <= 20 MPa", "measured": float(stress), "ok": bool(r5_ok)}],
            "note": ""
        }
        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": float(deflection),
            "method": f"F={LOAD_F} N, L={L_CANTILEVER} mm, E={E_MODULUS} MPa, I={I:.2f} mm4, delta=FL^3/3EI={deflection:.2f} mm",
            "criteria": [{"condition": "tip deflection <= 2.0 mm", "measured": float(deflection), "ok": bool(r6_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass
    try:
        vol_mm3 = mesh.volume
        mass_g = vol_mm3 * DENSITY_GMM3
        r7_ok = mass_g <= 90.0 + 1e-3
        results["R7"] = {
            "status": "pass" if r7_ok else "fail",
            "value": float(mass_g),
            "method": f"Volume={vol_mm3:.2f} mm3, density={DENSITY_GCM3} g/cm3, mass={mass_g:.2f} g",
            "criteria": [{"condition": "Mass <= 90 g", "measured": float(mass_g), "ok": bool(r7_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    run_verification()