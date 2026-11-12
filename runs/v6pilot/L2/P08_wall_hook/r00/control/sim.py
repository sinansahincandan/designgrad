import cadquery as cq
import trimesh
import numpy as np
import json

def solve():
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {e}"}))
        return

    results = {}

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        is_ok = (n_solids == 1)
        results["R1"] = {
            "status": "pass" if is_ok else "fail",
            "value": n_solids,
            "method": "Counted number of solids in the STEP file.",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": bool(is_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2: Back plate (0 <= x <= 2, |y| <= 8, -5 <= z <= 45)
    try:
        dx, dy, dz = 2.0, 16.0, 50.0
        pnt = cq.Vector(0, -8, -5)
        plate_tool = cq.Solid.makeBox(dx, dy, dz, pnt=pnt)
        vol_region = plate_tool.Volume()
        intersected_vol = shape.intersect(plate_tool).Volume()
        fill_fraction = intersected_vol / vol_region
        
        bbox = shape.BoundingBox()
        min_x_ok = abs(bbox.xmin) < 0.01
        
        is_ok = fill_fraction > 0.95 and min_x_ok
        results["R2"] = {
            "status": "pass" if is_ok else "fail",
            "value": [round(float(fill_fraction), 3), round(float(bbox.xmin), 3)],
            "method": f"Intersected part with box [0,2]x[-8,8]x[-5,45]. Vol ratio: {fill_fraction:.3f}",
            "criteria": [
                {"condition": "solid material at 0 <= x <= 2 over |y| <= 8, -5 <= z <= 45", "measured": float(fill_fraction), "ok": bool(fill_fraction > 0.95)},
                {"condition": "minimum x = 0", "measured": float(bbox.xmin), "ok": bool(min_x_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Two screw holes (D=4.5, at (0,0) and (0,40)) + thickness check
    try:
        hole_params = [(0, 0), (0, 40)]
        diam = 4.5
        radius = diam / 2
        all_holes_ok = True
        thickness_vals = []
        measured_vals = []

        for y_h, z_h in hole_params:
            # Check if the hole exists (empty core)
            core = cq.Solid.makeCylinder(radius - 0.15, 10.0, pnt=cq.Vector(0, y_h, z_h), dir=cq.Vector(1, 0, 0))
            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            
            # Check thickness: The requirement is "plate at least 4mm thick around them".
            # Since the holes go through the plate (x=0 to x=2), we check if there's material 
            # in a shell of radius R + 4mm. However, the spec says 'plate at least 4mm thick'.
            # In context of a hole in a plate, this usually means the distance from the hole edge 
            # to any other void or the thickness of the slab itself must be >= 4mm.
            # Given R2 defines the plate as 0 <= x <= 2 (thickness 2), but R3 asks for 4mm thick...
            # This implies the material surrounding the hole in the X-direction (or locally) must be 4mm.
            # We will probe a cylinder of radius (radius + 4.0) to ensure it is solid.
            thick_probe_r = radius + 4.0
            thick_tool = cq.Solid.makeCylinder(thick_probe_r, 10.0, pnt=cq.Vector(0, y_h, z_h), dir=cq.Vector(1, 0, 0))
            # The 'hole' itself is empty. We want the material around it to be solid.
            # A robust way: check if (Volume of thick_tool - Volume of hole) is contained in shape.
            core_large = cq.Solid.makeCylinder(radius + 0.15, 10.0, pnt=cq.Vector(0, y_h, z_h), dir=cq.Vector(1, 0, 0))
            material_in_probe = shape.intersect(thick_tool).Volume()
            expected_material = thick_tool.Volume() - core_large.Volume()
            thickness_ratio = material_in_probe / expected_material if expected_material > 0 else 0
            
            thickness_vals.append(float(thickness_ratio))
            hole_ok = empty_ratio < 0.05 and thickness_ratio > 0.98
            if not hole_ok: all_holes_ok = False
            measured_vals.append({"empty": float(empty_ratio), "thickness_ratio": float(thickness_ratio)})

        results["R3"] = {
            "status": "pass" if all_holes_ok else "fail",
            "value": measured_vals,
            "method": f"Probed holes at (0,0) and (0,40). Checked hole emptiness and material thickness ratio around radius+4mm.",
            "criteria": [{"condition": "Two screw holes diameter 4.5mm... plate at least 4mm thick", "measured": float(all_holes_ok), "ok": bool(all_holes_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Strap seat (bed at z=-14, pocket 35<=x<=45, |y|<=6, -13<z<-6)
    try:
        pocket_tool = cq.Solid.makeBox(10, 12, 7, pnt=cq.Vector(35, -6, -13))
        empty_vol = shape.intersect(pocket_tool).Volume() / pocket_tool.Volume()
        bed_tool = cq.Solid.makeBox(12, 8, 2, pnt=cq.Vector(34, -4, -15))
        bed_vol = shape.intersect(bed_tool).Volume() / bed_tool.Volume()
        
        is_ok = empty_vol < 0.05 and bed_vol > 0.95
        results["R4"] = {
            "status": "pass" if is_ok else "fail",
            "value": [round(float(empty_vol), 3), round(float(bed_vol), 3)],
            "method": f"Checked pocket (35-45x,-6-6y,-13--6z) emptiness and bed (34-46x,-4-4y,-15--13z) solidity.",
            "criteria": [
                {"condition": "space just above it must be empty", "measured": float(empty_vol), "ok": bool(empty_vol < 0.05)},
                {"condition": "strap rests on a solid bed at z=-14", "measured": float(bed_vol), "ok": bool(bed_vol > 0.95)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Retaining lip (47<=x<=52, |y|<=4, -13<z<-8)
    try:
        lip_tool = cq.Solid.makeBox(5, 8, 5, pnt=cq.Vector(47, -4, -13))
        fill_fraction = shape.intersect(lip_tool).Volume() / lip_tool.Volume()
        is_ok = fill_fraction > 0.9
        results["R5"] = {
            "status": "pass" if is_ok else "fail",
            "value": float(fill_fraction),
            "method": f"Intersected part with lip box [47,52]x[-4,4]x[-13,-8].",
            "criteria": [{"condition": "solid material at 47 <= x <= 52, |y| <= 4, -13 <= z <= -8", "measured": float(fill_fraction), "ok": bool(is_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Strength (F=50N at x=40, plane x=8)
    try:
        x_cut = 8.0
        F = 50.0
        E = 3500.0
        L = 32.0 
        h_step = 0.5
        b = mesh.bounds
        y_range = np.arange(b[0][1], b[1][1], h_step) + h_step/2
        z_range = np.arange(b[0][2], b[1][2], h_step) + h_step/2
        Y, Z = np.meshgrid(y_range, z_range)
        pts = np.column_stack([np.full(Y.size, x_cut), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not np.any(inside):
            raise ValueError("Plane x=8 misses the part")

        z_vals = pts[inside, 2]
        A = inside.sum() * (h_step**2)
        zc = z_vals.mean()
        I = ((z_vals - zc)**2).sum() * (h_step**2)
        c = np.max(np.abs(z_vals - zc))
        
        sigma = (F * (40 - x_cut) * c) / I
        deflection = (F * L**3) / (3 * E * I)
        
        stress_ok = sigma <= 25.0
        defl_ok = deflection <= 1.5
        is_ok = stress_ok and defl_ok
        
        results["R6"] = {
            "status": "pass" if is_ok else "fail",
            "value": [round(float(sigma), 2), round(float(deflection), 3)],
            "method": f"F=50N at x=40, section plane x={x_cut}, I={I:.1f}, c={c:.1f}. sigma = M*c/I, defl = FL^3/3EI",
            "criteria": [
                {"condition": "bending stress <= 25 MPa", "measured": float(sigma), "ok": bool(stress_ok)},
                {"condition": "tip deflection <= 1.5 mm", "measured": float(deflection), "ok": bool(defl_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 25g; X extent <= 55mm
    try:
        density = 1.24 
        vol_mm3 = mesh.volume
        mass_g = vol_mm3 * (density / 1000.0)
        bbox = shape.BoundingBox()
        x_extent = bbox.xmax - bbox.xmin
        
        mass_ok = mass_g <= 25.0
        ext_ok = x_extent <= 55.0
        is_ok = mass_ok and ext_ok
        
        results["R7"] = {
            "status": "pass" if is_ok else "fail",
            "value": [round(float(mass_g), 2), round(float(x_extent), 2)],
            "method": f"Mass = vol * density ({density} g/cm3). X-extent = bbox.xmax - bbox.xmin.",
            "criteria": [
                {"condition": "Mass <= 25 g", "measured": float(mass_g), "ok": bool(mass_ok)},
                {"condition": "X extent <= 55 mm", "measured": float(x_extent), "ok": bool(ext_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()