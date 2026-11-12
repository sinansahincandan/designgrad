import cadquery as cq
import trimesh
import numpy as np
import json

def check_requirements():
    results = {}
    
    # Load the part
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return

    # Constants
    DENSITY_PLA = 1.24 / 1000  # g/mm3
    E_PLA = 3500                # MPa (N/mm2)
    FORCE_F = 50.0              # N
    LOAD_X = 40.0               # mm

    def clean(val):
        if isinstance(val, (np.bool_, bool)):
            return bool(val)
        if isinstance(val, (np.integer, int)):
            return int(val)
        if isinstance(val, (np.floating, float)):
            return float(val)
        if isinstance(val, (np.ndarray, list)):
            return [clean(x) for x in val]
        if isinstance(val, dict):
            return {k: clean(v) for k, v in val.items()}
        return val

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": float(n_solids),
            "method": "Counted number of solids in STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": n_solids == 1}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Back plate (0 <= x <= 2, |y| <= 8, -5 <= z <= 45)
    try:
        r_xmin, r_xmax = 0.0, 2.0
        r_ymin, r_ymax = -8.0, 8.0
        r_zmin, r_zmax = -5.0, 45.0
        region_vol = (r_xmax - r_xmin) * (r_ymax - r_ymin) * (r_zmax - r_zmin)
        tool = cq.Solid.makeBox(2, 16, 50, pnt=cq.Vector(0, -8, -5))
        intersected_vol = shape.intersect(tool).Volume()
        fill_fraction = intersected_vol / region_vol
        bbox = shape.BoundingBox()
        min_x_ok = bbox.xmin <= 0.001 
        status = "pass" if fill_fraction > 0.95 and min_x_ok else "fail"
        results["R2"] = {
            "status": status,
            "value": float(fill_fraction),
            "method": f"Intersected part with box [0,2]x[-8,8]x[-5,45], vol ratio={fill_fraction:.3f}",
            "criteria": [
                {"condition": "solid material at 0 <= x <= 2 over |y| <= 8, -5 <= z <= 45", "measured": float(fill_fraction), "ok": fill_fraction > 0.95},
                {"condition": "minimum x = 0", "measured": float(bbox.xmin), "ok": min_x_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Two screw holes (dia 4.5 at (0,0) and (0,40))
    try:
        holes_ok = True
        for (hy, hz) in [(0, 0), (0, 40)]:
            # Check for emptiness/absence of material at the hole locations through the plate thickness
            # A screw hole is a void. We probe if there is NO material inside a cylinder passing through x=0 to x=2.
            hole_radius = 2.25
            # Probe with a small cylinder centered on (y,z) and spanning the plate thickness [0, 2]
            probe_tool = cq.Solid.makeCylinder(hole_radius, 3.0, pnt=cq.Vector(0.5, hy, hz), dir=cq.Vector(1, 0, 0))
            # If the intersection volume is near zero, it means there's a hole (no material)
            if shape.intersect(probe_tool).Volume() > 0.1: # threshold for "not a hole"
                holes_ok = False
        status = "pass" if holes_ok else "fail"
        results["R3"] = {
            "status": status,
            "value": float(holes_ok),
            "method": f"Probed cylinders of diameter 4.5 at (y,z)={[(0,0), (0,40)]} through plate",
            "criteria": [{"condition": "Two screw holes, diameter 4.5 mm", "measured": float(holes_ok), "ok": holes_ok}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Strap seat (Bed top at z=-14; Pocket 35<=x<=45, |y|<=6, -13<=z<=-6 must be empty)
    try:
        # Check bed geometry: solid material under 34 <= x <= 46, |y| <= 4, with top at z = -14.
        # We check for presence of material in a thin slice just below the target Z level.
        res_h = 0.2
        bed_x_range = (34, 46)
        bed_y_range = (-4, 4)
        z_target = -14.0
        
        # Check if there is material at z=-14 by checking a slice from -14.5 to -14.0
        slice_tool = cq.Solid.makeBox(12, 8, 0.5, pnt=cq.Vector(34, -4, -14.5))
        slice_vol = shape.intersect(slice_tool).Volume()
        # Expected volume of a solid bed in this slice: 12 * 8 * 0.5 = 48 mm3
        bed_top_at_z = abs(slice_vol - 48.0) < 5.0 # Increased tolerance for mesh/step precision

        # Pocket check: space (35<=x<=45, |y|<=6, -13<=z<=-6) must be empty.
        pocket_tool = cq.Solid.makeBox(10, 12, 7, pnt=cq.Vector(35, -6, -13))
        pocket_vol = shape.intersect(pocket_tool).Volume()
        pocket_empty = pocket_vol < 0.5

        status = "pass" if bed_top_at_z and pocket_empty else "fail"
        results["R4"] = {
            "status": status,
            "value": [float(bed_top_at_z), float(pocket_vol)],
            "method": f"Bed top at z=-14: {bed_top_at_z}, Pocket vol: {pocket_vol:.2f} mm3",
            "criteria": [
                {"condition": "solid bed whose top is at z = -14 under 34 <= x <= 46, |y| <= 4", "measured": float(bed_top_at_z), "ok": bed_top_at_z},
                {"condition": "space (35<=x<=45, |y|<=6, -13<=z<=-6) must be empty", "measured": float(pocket_vol), "ok": pocket_empty}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Retaining lip
    try:
        lip_tool = cq.Solid.makeBox(5, 8, 5, pnt=cq.Vector(47, -4, -13))
        lip_fill = shape.intersect(lip_tool).Volume() / lip_tool.Volume()
        status = "pass" if lip_fill > 0.9 else "fail"
        results["R5"] = {
            "status": status,
            "value": float(lip_fill),
            "method": f"Lip fill ratio: {lip_fill:.2f}",
            "criteria": [{"condition": "solid material at 47 <= x <= 52, |y| <= 4, -13 <= z <= -8", "measured": float(lip_fill), "ok": lip_fill > 0.9}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Strength (F=50N at x=40, section x=8)
    try:
        x_cut = 8.0
        y_min, y_max = mesh.bounds[0][1], mesh.bounds[1][1]
        z_min, z_max = mesh.bounds[0][2], mesh.bounds[1][2]
        res = 0.15 # Higher resolution for better I calculation
        y_grid = np.arange(y_min, y_max + res, res)
        z_grid = np.arange(z_min, z_max + res, res)
        Y, Z = np.meshgrid(y_grid, z_grid)
        Y += res/2
        Z += res/2
        pts = np.column_stack([np.full(Y.size, x_cut), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        if not np.any(inside): raise ValueError("Section at x=8 is empty")
        z_in = pts[inside, 2]
        zc = np.mean(z_in)
        I = np.sum((z_in - zc)**2) * (res**2)
        c = np.max(np.abs(z_in - zc))
        M = FORCE_F * (LOAD_X - x_cut) # Nmm
        sigma = M * c / I
        L = LOAD_X - x_cut
        deflection = (FORCE_F * (L**3)) / (3 * E_PLA * I)

        status = "pass" if sigma <= 25.0 and deflection <= 1.5 else "fail"
        results["R6"] = {
            "status": status,
            "value": [float(sigma), float(deflection)],
            "method": f"M={M:.1f}Nmm, x=8 section: I={I:.1f}, c={c:.2f}, sigma={sigma:.2f}MPa, defl={deflection:.2f}mm",
            "criteria": [
                {"condition": "bending stress <= 25 MPa", "measured": float(sigma), "ok": sigma <= 25.0},
                {"condition": "tip deflection estimate ... <= 1.5 mm", "measured": float(deflection), "ok": deflection <= 1.5}
            ],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 25g; X extent <= 55mm
    try:
        vol_mm3 = mesh.volume
        calc_mass = vol_mm3 * DENSITY_PLA
        bbox = shape.BoundingBox()
        x_extent = bbox.xmax - bbox.xmin
        status = "pass" if calc_mass <= 25.0 and x_extent <= 55.0 else "fail"
        results["R7"] = {
            "status": status,
            "value": [float(calc_mass), float(x_extent)],
            "method": f"Mass={calc_mass:.2f}g (vol={vol_mm3:.1f}), X-ext={x_extent:.1f}mm",
            "criteria": [
                {"condition": "Mass <= 25 g", "measured": float(calc_mass), "ok": calc_mass <= 25.0},
                {"condition": "X extent <= 55 mm", "measured": float(x_extent), "ok": x_extent <= 55.0}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(clean(results)))

if __name__ == "__main__":
    check_requirements()