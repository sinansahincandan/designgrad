import cadquery as cq
import trimesh
import numpy as np
import json

def check_requirements():
    results = {}
    
    # Load geometry
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    # Constants
    DENSITY_PLA = 1.24 / 1000  # g/mm3 (converted from 1.24 g/cm3)
    E_PLA = 3500  # MPa (N/mm2)
    F_LOAD = 50.0 # N
    X_LOAD = 40.0 # mm

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": float(n_solids),
            "method": "Counted number of solids in STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": bool(n_solids == 1)}],
            "note": f"Found {n_solids} solids"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "Counted solids", "criteria": [], "note": str(e)}

    # R2: Back plate (0 <= x <= 2, |y| <= 8, -5 <= z <= 45)
    try:
        r_xmin, r_xmax = 0.0, 2.0
        r_ymin, r_ymax = -8.0, 8.0
        r_zmin, r_zmax = -5.0, 45.0
        vol_region = (r_xmax - r_xmin) * (r_ymax - r_ymin) * (r_zmax - r_zmin)
        
        tool = cq.Solid.makeBox(2.0, 16.0, 50.0, pnt=cq.Vector(0, -8, -5))
        intersect_vol = shape.intersect(tool).Volume()
        fill_fraction = intersect_vol / vol_region
        
        bbox = shape.BoundingBox()
        x_min_ok = abs(bbox.xmin) < 0.1
        
        status = "pass" if fill_fraction > 0.95 and x_min_ok else "fail"
        results["R2"] = {
            "status": status,
            "value": float(fill_fraction),
            "method": f"Intersection volume / region volume ({vol_region} mm3) and bbox.xmin check",
            "criteria": [
                {"condition": "solid material at 0 <= x <= 2, |y| <= 8, -5 <= z <= 45", "measured": float(fill_fraction), "ok": bool(fill_fraction > 0.95)},
                {"condition": "minimum x = 0", "measured": float(bbox.xmin), "ok": bool(x_min_ok)}
            ],
            "note": f"Fill: {fill_fraction:.2%}"
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "Volume intersection", "criteria": [], "note": str(e)}

    # R3: Two screw holes (dia 4.5 at (0,0) and (0,40)) + plate thickness check
    try:
        hole_centers = [(0, 0), (0, 40)]
        req_dia = 4.5
        min_thickness_around = 4.0
        holes_pass = True
        
        for hy, hz in hole_centers:
            # 1. Verify holes exist along X through the plate region [0,2]
            # A hole is a void. We check if a cylinder probe contains NO material.
            cyl_tool = cq.Solid.makeCylinder(req_dia/2, 3.0, pnt=cq.Vector(-0.5, hy, hz), dir=cq.Vector(1, 0, 0))
            hole_vol = shape.intersect(cyl_tool).Volume()
            if hole_vol > 0.5: # If significant material is found inside the cylinder, it's not a through-hole
                holes_pass = False
            
            # 2. Verify plate thickness around them (X-dimension)
            # The requirement says "plate at least 4mm thick around them". 
            # Since R2 defines the plate as 0 <= x <= 2, and holes are through it, 
            # this implies the material in X must be >= 4mm.
            # However, R2 and R3 are contradictory if R2 is strictly 2mm thick.
            # Given the reviewer's note: "interprets 'thickness around them' as distance to plate boundaries... rather than checking X-dimension".
            # We check that for points in the YZ plane near the hole, the material extent in X is >= 4mm.
            # Since we can only measure what exists, we probe the thickness at the hole boundary.
            
            # Check if there's a solid region with x-thickness >= 4mm nearby? 
            # Actually, let's check the distance from the hole edge to the plate boundaries in Y/Z as requested by the reviewer's logic fix:
            # "interprets 'thickness around them' as distance to the plate boundaries... rather than checking X-dimension".
            # Wait, the reviewer says the CURRENT script is flawed because it checks Y/Z. 
            # The requirement R3 says "plate at least 4mm thick around them". 
            # If the holes are through the plate, 'thickness' usually refers to the dimension perpendicular to the hole (X).
            # But if X is only 2mm (R2), then R3 requires a thicker plate.
            # Let's check the thickness in X at several points around the hole circumference.
            
            for angle in np.linspace(0, 2*np.pi, 8):
                py = hy + (req_dia/2 + 0.5) * np.cos(angle)
                pz = hz + (req_dia/2 + 0.5) * np.sin(angle)
                # Probe X thickness at this (y,z)
                probe_x = cq.Solid.makeBox(10.0, 1.0, 1.0, pnt=cq.Vector(-1, py-0.5, pz-0.5))
                thick_vol = shape.intersect(probe_x).Volume()
                # thickness approx vol / area (1*1)
                if thick_vol < min_thickness_around - 0.1:
                    holes_pass = False
                    break
            if not holes_pass: break

        status = "pass" if holes_pass else "fail"
        results["R3"] = {
            "status": status,
            "value": 1.0 if holes_pass else 0.0,
            "method": f"Cylinder intersection for through-hole check and X-thickness probe around hole",
            "criteria": [{"condition": "Two screw holes dia 4.5mm and 4mm plate thickness around them", "measured": 1.0 if holes_pass else 0.0, "ok": bool(holes_pass)}],
            "note": ""
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "Hole probe", "criteria": [], "note": str(e)}

    # R4: Strap seat (top at z=-14 under 34<=x<=46, |y|<=4; space above empty)
    try:
        bed_probe = cq.Solid.makeBox(12, 8, 1, pnt=cq.Vector(34, -4, -15))
        bed_vol = shape.intersect(bed_probe).Volume()
        bed_ok = bed_vol > (12 * 8 * 0.5)

        pocket_tool = cq.Solid.makeBox(10, 12, 7, pnt=cq.Vector(35, -6, -13))
        pocket_vol = shape.intersect(pocket_tool).Volume()
        pocket_ok = pocket_vol < 0.5
        
        status = "pass" if bed_ok and pocket_ok else "fail"
        results["R4"] = {
            "status": status,
            "value": [float(bed_vol), float(pocket_vol)],
            "method": f"Bed volume probe: {bed_vol}, Pocket volume probe: {pocket_vol}",
            "criteria": [
                {"condition": "solid bed top at z=-14", "measured": float(bed_vol), "ok": bool(bed_ok)},
                {"condition": "space above empty", "measured": float(pocket_vol), "ok": bool(pocket_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "Strap seat probe", "criteria": [], "note": str(e)}

    # R5: Retaining lip (47 <= x <= 52, |y| <= 4, -13 <= z <= -8)
    try:
        lip_tool = cq.Solid.makeBox(5, 8, 5, pnt=cq.Vector(47, -4, -13))
        lip_vol = shape.intersect(lip_tool).Volume()
        lip_ok = lip_vol > (5 * 8 * 5 * 0.5)
        status = "pass" if lip_ok else "fail"
        results["R5"] = {
            "status": status,
            "value": float(lip_vol),
            "method": f"Intersection volume with lip region: {lip_vol}",
            "criteria": [{"condition": "solid material at 47<=x<=52, |y|<=4, -13<=z<=-8", "measured": float(lip_vol), "ok": bool(lip_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "Lip probe", "criteria": [], "note": str(e)}

    # R6: Strength (F=50N at x=40, plane x=8)
    try:
        x_cut = 8.0
        h = 1.0
        b_min = mesh.bounds[0]
        b_max = mesh.bounds[1]
        Y, Z = np.meshgrid(np.arange(b_min[1], b_max[1], h) + h/2, np.arange(b_min[2], b_max[2], h) + h/2)
        pts = np.column_stack([np.full(Y.size, x_cut), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        
        if not np.any(inside):
            raise ValueError("Plane x=8 does not intersect the part")

        z_vals = pts[inside, 2]
        A = inside.sum() * h * h
        zc = z_vals.mean()
        I = ((z_vals - zc)**2).sum() * h * h
        c = np.max(np.abs(z_vals - zc))

        M = F_LOAD * 32.0 
        sigma = M * c / I
        deflection = (F_LOAD * (32.0**3)) / (3 * E_PLA * I)

        stress_ok = sigma <= 25.0 + 1e-3
        defl_ok = deflection <= 1.5 + 1e-3
        
        status = "pass" if stress_ok and defl_ok else "fail"
        results["R6"] = {
            "status": status,
            "value": [float(sigma), float(deflection)],
            "method": f"Section x={x_cut}: A={A:.1f}, I={I:.1f}, c={c:.1f}. M=F*32={M}. sigma=Mc/I, defl=FL^3/3EI",
            "criteria": [
                {"condition": "bending stress <= 25 MPa", "measured": float(sigma), "ok": bool(stress_ok)},
                {"condition": "tip deflection estimate <= 1.5 mm", "measured": float(deflection), "ok": bool(defl_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "Beam theory calculation", "criteria": [], "note": str(e)}

    # R7: Mass <= 25g; X extent <= 55mm
    try:
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * DENSITY_PLA
        bbox = shape.BoundingBox()
        x_extent = bbox.xmax - bbox.xmin
        
        mass_ok = mass_g <= 25.0 + 0.1
        ext_ok = x_extent <= 55.0 + 0.01
        
        status = "pass" if mass_ok and ext_ok else "fail"
        results["R7"] = {
            "status": status,
            "value": [float(mass_g), float(x_extent)],
            "method": f"Mass = vol * density ({DENSITY_PLA}), X-extent = bbox.xmax - bbox.xmin",
            "criteria": [
                {"condition": "Mass <= 25 g", "measured": float(mass_g), "ok": bool(mass_ok)},
                {"condition": "X extent <= 55 mm", "measured": float(x_extent), "ok": bool(ext_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "Mass/Extent check", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    check_requirements()