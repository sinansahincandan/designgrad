import cadquery as cq
import trimesh
import numpy as np
import json

def run_checks():
    results = {}
    
    # Load geometry
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        return

    # Constants
    DENSITY_PLA = 1.24 / 1000  # g/mm3 (converted from 1.24 g/cm3)
    E_PLA = 3500                # MPa (N/mm2)
    FORCE_F = 50.0              # N
    LOAD_X = 40.0               # mm
    SECTION_X = 8.0             # mm

    def clean_bool(val):
        return bool(val)

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": float(n_solids),
            "method": "Counted number of solids in STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": float(n_solids), "ok": clean_bool(n_solids == 1)}],
            "note": f"Found {n_solids} solids"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

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
        min_x_ok = bbox.xmin <= 0.1 
        
        status = "pass" if fill_fraction > 0.90 and min_x_ok else "fail"
        results["R2"] = {
            "status": status,
            "value": float(fill_fraction),
            "method": f"Intersection volume / region volume ({vol_region} mm3) and bbox check",
            "criteria": [
                {"condition": "solid material at 0 <= x <= 2, |y| <= 8, -5 <= z <= 45", "measured": float(fill_fraction), "ok": clean_bool(fill_fraction > 0.90)},
                {"condition": "minimum x = 0", "measured": float(bbox.xmin), "ok": clean_bool(min_x_ok)}
            ],
            "note": f"Fill: {fill_fraction:.2%}"
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R3: Two screw holes (dia 4.5 at (y,z) = (0,0) and (0,40))
    try:
        holes_ok = True
        # Requirement: diameter 4.5mm, along X through back plate at (y,z)=(0,0) and (0,40)
        # Probe with a cylinder of radius 2.25 passing through the plate thickness
        for pos_y, pos_z in [(0, 0), (0, 40)]:
            # Cylinder centered at x=1 (middle of plate), radius 2.25, along X axis
            # pnt is the start point of the cylinder. To cover x=0 to x=2, we can start at -1.
            check_tool = cq.Solid.makeCylinder(2.25, 4.0, pnt=cq.Vector(-1, pos_y, pos_z), dir=cq.Vector(1, 0, 0))
            # If the intersection volume is significant, it means there is material where a hole should be.
            if shape.intersect(check_tool).Volume() > 1.0: 
                holes_ok = False
        
        status = "pass" if holes_ok else "fail"
        results["R3"] = {
            "status": status,
            "value": float(holes_ok),
            "method": "Probing hole locations with cylinders along X axis at (y,z) coordinates",
            "criteria": [{"condition": "Two screw holes diameter 4.5 mm at (0,0) and (0,40)", "measured": float(holes_ok), "ok": clean_bool(holes_ok)}],
            "note": "Checked for absence of material in hole volumes"
        }
    except Exception as e:
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Strap seat (bed top z=-14 under 34<=x<=46, |y|<=4; pocket 35<=x<=45, |y|<=6, -13<z<-6 empty)
    try:
        # Bed: solid material at z = -14. We check a small volume around the specified bed region.
        bed_tool = cq.Solid.makeBox(12.0, 8.0, 2.0, pnt=cq.Vector(34, -4, -15)) 
        bed_intersect = shape.intersect(bed_tool).Volume()
        bed_ok = bed_intersect > 0.1
        
        # Pocket: space must be empty.
        pocket_tool = cq.Solid.makeBox(10.0, 12.0, 7.0, pnt=cq.Vector(35, -6, -13))
        pocket_intersect = shape.intersect(pocket_tool).Volume()
        pocket_ok = pocket_intersect < 1.0 
        
        status = "pass" if bed_ok and pocket_ok else "fail"
        results["R4"] = {
            "status": status,
            "value": [float(bed_intersect), float(pocket_intersect)],
            "method": "Intersection volume of bed region and pocket region",
            "criteria": [
                {"condition": "solid bed top at z=-14 under 34<=x<=46, |y|<=4", "measured": float(bed_intersect), "ok": clean_bool(bed_ok)},
                {"condition": "pocket (35<=x<=45, |y|<=6, -13<z<-6) must be empty", "measured": float(pocket_intersect), "ok": clean_bool(pocket_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Retaining lip (47<=x<=52, |y|<=4, -13<z<-8)
    try:
        lip_tool = cq.Solid.makeBox(5.0, 8.0, 5.0, pnt=cq.Vector(47, -4, -13))
        lip_vol = shape.intersect(lip_tool).Volume()
        lip_ok = lip_vol > (5*8*5 * 0.1) 
        status = "pass" if lip_ok else "fail"
        results["R5"] = {
            "status": status,
            "value": float(lip_vol),
            "method": "Intersection volume of lip region",
            "criteria": [{"condition": "solid material at 47<=x<=52, |y|<=4, -13<z<-8", "measured": float(lip_vol), "ok": clean_bool(lip_ok)}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Strength (F=50N at x=40, section x=8)
    try:
        x0 = SECTION_X
        b_min, b_max = mesh.bounds
        ylo, zlo = b_min[1], b_min[2]
        yhi, zhi = b_max[1], b_max[2]
        
        h_step = 0.5
        Y, Z = np.meshgrid(np.arange(ylo, yhi, h_step) + h_step/2, np.arange(zlo, zhi, h_step) + h_step/2)
        pts = np.column_stack([np.full(Y.size, x0), Y.ravel(), Z.ravel()])
        inside = mesh.contains(pts)
        section_pts = pts[inside]
        
        if len(section_pts) < 3: raise ValueError("Insufficient points in section")
        
        z_vals = section_pts[:, 2]
        A = len(section_pts) * (h_step**2)
        zc = np.mean(z_vals)
        I = np.sum((z_vals - zc)**2) * (h_step**2)
        c = np.max(np.abs(z_vals - zc))
        
        L_arm = LOAD_X - SECTION_X
        M = FORCE_F * L_arm
        sigma = M * c / I
        L_deflect = 32.0 
        delta = (FORCE_F * (L_deflect**3)) / (3 * E_PLA * I)
        
        stress_ok = sigma <= 25.0
        deflection_ok = delta <= 1.5
        
        status = "pass" if stress_ok and deflection_ok else "fail"
        results["R6"] = {
            "status": status,
            "value": [float(sigma), float(delta)],
            "method": f"F={FORCE_F}N at x={LOAD_X}, section plane x={SECTION_X}, M=F*(40-8), sigma=Mc/I, delta=FL^3/(3EI) with L=32",
            "criteria": [
                {"condition": "bending stress <= 25 MPa", "measured": float(sigma), "ok": clean_bool(stress_ok)},
                {"condition": "tip deflection estimate <= 1.5 mm", "measured": float(delta), "ok": clean_bool(deflection_ok)}
            ],
            "note": f"sigma={sigma:.2f}, delta={delta:.2f}"
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Mass <= 25g; X extent <= 55mm
    try:
        vol_total = shape.Volume()
        mass = vol_total * DENSITY_PLA
        bbox = shape.BoundingBox()
        x_extent = bbox.xmax - bbox.xmin
        
        mass_ok = mass <= 25.0
        extent_ok = x_extent <= 55.0
        
        status = "pass" if mass_ok and extent_ok else "fail"
        results["R7"] = {
            "status": status,
            "value": [float(mass), float(x_extent)],
            "method": "Volume * density and BoundingBox X range",
            "criteria": [
                {"condition": "Mass <= 25 g", "measured": float(mass), "ok": clean_bool(mass_ok)},
                {"condition": "X extent <= 55 mm", "measured": float(x_extent), "ok": clean_bool(extent_ok)}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    run_checks()