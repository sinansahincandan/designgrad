import cadquery as cq
import trimesh
import numpy as np
import json
from shapely.geometry import Point, Polygon

def check_requirements():
    try:
        # Load the part
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return

    results = {}

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": int(n_solids),
            "method": "Counted number of solids in the STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": int(n_solids), "ok": bool(status == "pass")}],
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
        
        c1 = (0 <= xmin) and (xmax <= 170)
        c2 = (-20 <= ymin) and (ymax <= 20)
        c3 = (0 <= zmin) and (zmax <= 130)
        c4 = abs(xmin) < 1e-2 # Touches wall x=0
        
        ok = all([c1, c2, c3, c4])
        results["R2"] = {
            "status": "pass" if ok else "fail",
            "value": [float(xmin), float(xmax), float(ymin), float(ymax), float(zmin), float(zmax)],
            "method": f"Checked bounding box: x[{xmin:.1f},{xmax:.1f}], y[{ymin:.1f},{ymax:.1f}], z[{zmin:.1f},{zmax:.1f}]",
            "criteria": [
                {"condition": "0 <= x <= 170", "measured": [float(xmin), float(xmax)], "ok": bool(c1)},
                {"condition": "-20 <= y <= 20", "measured": [float(ymin), float(ymax)], "ok": bool(c2)},
                {"condition": "0 <= z <= 130", "measured": [float(zmin), float(zmax)], "ok": bool(c3)},
                {"condition": "touches wall (min x = 0)", "measured": float(xmin), "ok": bool(c4)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Screw holes and screwdriver access
    try:
        hole_centers = [(0, 20), (0, 60)] # y, z
        diameters = []
        access_ok = True
        
        for yc, zc in hole_centers:
            # Check diameter: A hole exists if the intersection of a probe cylinder and the part is nearly zero.
            probe_r_hole = 2.75 # 5.5/2
            tool_h = cq.Solid.makeCylinder(probe_r_hole, 10, pnt=cq.Vector(-1, yc, zc), dir=cq.Vector(1, 0, 0))
            intersect_vol_hole = shape.intersect(tool_h).Volume()
            if intersect_vol_hole > 1e-3:
                diameters.append(0.0) # Material found in hole volume
            else:
                diameters.append(5.5)

            # Check screwdriver access: no material within 4mm of axis for x >= 10
            probe_r_access = 4.0
            tool_access = cq.Solid.makeCylinder(probe_r_access, 160, pnt=cq.Vector(10, yc, zc), dir=cq.Vector(1, 0, 0))
            intersect_vol_access = shape.intersect(tool_access).Volume()
            if intersect_vol_access > 1e-3: 
                access_ok = False

        status = "pass" if (access_ok and all(d >= 5.4 for d in diameters)) else "fail"
        results["R3"] = {
            "status": status,
            "value": [float(d) for d in diameters],
            "method": f"Checked hole diameter at x~0 and screwdriver clearance (r=4) for x>=10",
            "criteria": [
                {"condition": "diameter 5.5 mm", "measured": [float(d) for d in diameters], "ok": bool(all(d >= 5.4 for d in diameters))},
                {"condition": "no material within 4mm of axis for x>=10", "measured": access_ok, "ok": bool(access_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Shelf support
    try:
        # 1. Verify shelf surface is at exactly z=110 and reaches x=150.
        # We check the cross-section of the part at z=110.
        sec = mesh.section(plane_origin=[0, 0, 110], plane_normal=[0, 0, 1])
        shelf_exists = False
        if sec is not None:
            path2d, T = sec.to_2D()
            polys = path2d.polygons_full
            # Requirement: solid material directly below z=110 between x=140 and x=150 around y=0.
            # We check if the intersection of the slice with a rectangle [140, 150] x [-5, 5] is non-empty.
            from shapely.geometry import box
            check_area = box(140, -5, 150, 5)
            shelf_exists = any(p.intersection(check_area).area > 1e-3 for p in polys)

        # 2. Nothing of the bracket may be above z = 110 for x >= 8.
        tool_above = cq.Solid.makeBox(162, 40, 50, pnt=cq.Vector(8, -20, 110))
        above_vol = shape.intersect(tool_above).Volume()
        above_ok = above_vol < 1e-3

        status = "pass" if (shelf_exists and above_ok) else "fail"
        results["R4"] = {
            "status": status,
            "value": [float(shelf_exists), float(above_vol)],
            "method": f"Shelf existence at z=110: {bool(shelf_exists)}; Volume above z=110 for x>=8: {above_vol:.2f}",
            "criteria": [
                {"condition": "horizontal top surface at z=110 reaching x=150", "measured": float(shelf_exists), "ok": bool(shelf_exists)},
                {"condition": "nothing above z=110 for x>=8", "measured": float(above_vol), "ok": bool(above_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5 & R6: Strength and Stiffness (Section at x=10)
    try:
        x0 = 10.0
        F = 150.0
        L = 140.0 
        E = 3500.0
        M = F * L
        
        # Robust section property calculation via sampling
        h_step = 0.2 # Smaller step for better accuracy
        bounds = mesh.bounds
        x_min, y_min, z_min = bounds[0]
        x_max, y_max, z_max = bounds[1]

        Y_range = np.arange(y_min, y_max, h_step) + h_step/2
        Z_range = np.arange(z_min, z_max, h_step) + h_step/2
        Y, Z = np.meshgrid(Y_range, Z_range)
        pts = np.column_stack([np.full(Y.size, x0), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not np.any(inside):
            raise ValueError("No material found at section x=10")
            
        z_vals = pts[inside, 2]
        y_vals = pts[inside, 1]
        A = inside.sum() * (h_step**2)
        zc = z_vals.mean()
        # I = sum((z - zc)^2 * dA)
        I = np.sum((z_vals - zc)**2) * (h_step**2)
        c = np.max(np.abs(z_vals - zc))

        stress = M * c / I
        deflection = (F * L**3) / (3 * E * I)

        r5_ok = stress <= 20.0
        r6_ok = deflection <= 2.0

        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": float(stress),
            "method": f"M={M}Nmm, c={c:.2f}mm, I={I:.1f}mm4, sigma=Mc/I",
            "criteria": [{"condition": "stress <= 20 MPa", "measured": float(stress), "ok": bool(r5_ok)}],
            "note": ""
        }
        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": float(deflection),
            "method": f"F={F}N, L={L}mm, E={E}MPa, I={I:.1f}mm4, delta=FL^3/3EI",
            "criteria": [{"condition": "deflection <= 2.0 mm", "measured": float(deflection), "ok": bool(r6_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass
    try:
        volume_mm3 = shape.Volume()
        density_gcm3 = 1.24
        mass_g = (volume_mm3 * density_gcm3) / 1000.0
        
        ok = mass_g <= 90.0
        results["R7"] = {
            "status": "pass" if ok else "fail",
            "value": float(mass_g),
            "method": f"mass = volume({volume_mm3:.1f}) * density(1.24) / 1000",
            "criteria": [{"condition": "Mass <= 90 g", "measured": float(mass_g), "ok": bool(ok)}],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    check_requirements()