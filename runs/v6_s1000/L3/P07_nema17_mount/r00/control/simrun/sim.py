import cadquery as cq
import trimesh
import numpy as np
import json

def solve():
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(f"Error loading files: {e}")
        return

    results = {}

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": n_solids,
            "method": f"Counted number of solids in CQ shape: {n_solids}",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": status == "pass"}],
            "note": ""
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2 & R3: Face plate thickness and Central Bore
    try:
        bore_diam = 22.5
        bore_radius = bore_diam / 2
        pnt = (0, 0, 30) # Shaft axis center at y=0 plane
        dir_vec = (0, 1, 0)
        # Probe length must span the plate thickness to ensure it's a through-hole
        probe_len = 10.0 
        
        # R3: Central Bore diameter 22.5 through face plate
        core = cq.Solid.makeCylinder(bore_radius - 0.1, probe_len, pnt=cq.Vector(*pnt), dir=cq.Vector(*dir_vec))
        empty_vol_ratio = shape.intersect(core).Volume() / core.Volume()
        
        ring_inner = bore_radius + 0.5
        ring_outer = bore_radius + 3.0
        ring_core = cq.Solid.makeCylinder(ring_inner, probe_len, pnt=cq.Vector(*pnt), dir=cq.Vector(*dir_vec))
        ring_shell = cq.Solid.makeCylinder(ring_outer, probe_len, pnt=cq.Vector(*pnt), dir=cq.Vector(*dir_vec)).cut(ring_core)
        walled_vol_ratio = shape.intersect(ring_shell).Volume() / ring_shell.Volume()

        # R2: Face plate at least 4 mm thick (y = 0 to 4)
        thickness_probe = cq.Solid.makeBox(100, 4, 100, pnt=cq.Vector(-50, 0, -20))
        inter_vol = shape.intersect(thickness_probe).Volume()
        inter_bbox = shape.intersect(thickness_probe).BoundingBox()
        thick_measured = inter_bbox.ymax - inter_bbox.ymin if inter_vol > 1e-3 else 0.0

        r2_ok = thick_measured >= 3.9 and walled_vol_ratio > 0.7
        r3_ok = empty_vol_ratio < 0.05 and walled_vol_ratio > 0.7
        
        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": [round(thick_measured, 2), round(walled_vol_ratio, 3)],
            "method": f"Thickness: y-range of intersection with box [y=0,4]. Material: filled fraction of ring r=[{bore_radius+0.5}, {bore_radius+3}]",
            "criteria": [
                {"condition": "Face plate at least 4 mm thick", "measured": thick_measured, "ok": thick_measured >= 3.9},
                {"condition": "Solid material all around the central bore", "measured": walled_vol_ratio, "ok": walled_vol_ratio > 0.7}
            ],
            "note": ""
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": [round(empty_vol_ratio, 3), round(walled_vol_ratio, 3)],
            "method": f"Empty volume fraction and wall presence for cylinder radius {bore_radius} at (0,0,30) dir (0,1,0)",
            "criteria": [
                {"condition": "Central bore diameter 22.5 mm", "measured": empty_vol_ratio, "ok": empty_vol_ratio < 0.05},
                {"condition": "Bore exists in material", "measured": walled_vol_ratio, "ok": walled_vol_ratio > 0.7}
            ],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes (3.4mm) at (+-15.5, 30 +- 15.5)
    try:
        holes_ok = True
        hole_coords = [(15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)]
        measured_vals = []
        for hx, hz in hole_coords:
            hpnt = (hx, 0, hz)
            hcore = cq.Solid.makeCylinder(3.4/2 - 0.1, 10.0, pnt=cq.Vector(*hpnt), dir=cq.Vector(0, 1, 0))
            hring_inner = 3.4/2 + 0.5
            hring_outer = 3.4/2 + 2.0
            hring_core = cq.Solid.makeCylinder(hring_inner, 10.0, pnt=cq.Vector(*hpnt), dir=cq.Vector(0, 1, 0))
            hring_shell = cq.Solid.makeCylinder(hring_outer, 10.0, pnt=cq.Vector(*hpnt), dir=cq.Vector(0, 1, 0)).cut(hring_core)
            
            ev = shape.intersect(hcore).Volume() / hcore.Volume()
            wv = shape.intersect(hring_shell).Volume() / hring_shell.Volume()
            measured_vals.append((round(ev, 3), round(wv, 3)))
            if ev > 0.1 or wv < 0.7: holes_ok = False
        
        results["R4"] = {
            "status": "pass" if holes_ok else "fail",
            "value": measured_vals,
            "method": f"Empty volume fraction and wall presence for 4 cylinders at {hole_coords}",
            "criteria": [{"condition": "Four motor screw holes diameter 3.4 mm", "measured": measured_vals, "ok": holes_ok}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Motor clearance (-21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5)
    try:
        # To avoid the 'control run' false positive (where a small cube in the zone passes),
        # we check that the intersection volume is effectively zero relative to the box size.
        # More importantly, we ensure the probe is actually placed correctly in world space.
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        inter_vol = shape.intersect(clearance_box).Volume()
        # A real clearance violation would be a significant portion of the box or at least > 0.1mm^3
        r5_ok = inter_vol < 0.01 
        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": round(inter_vol, 4),
            "method": f"Intersection volume with clearance box [-21.5, 21.5] x [-48, 0] x [8.5, 51.5]",
            "criteria": [{"condition": "Motor clearance: nothing in specified region", "measured": inter_vol, "ok": r5_ok}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Base on table (z>=0) and two 5.5mm holes at (+-25, 25)
    try:
        bbox = shape.BoundingBox()
        z_min = bbox.zmin
        r6_z_ok = abs(z_min) < 0.1 
        
        hole_coords_r6 = [(25, 25), (-25, 25)]
        holes_r6_ok = True
        measured_r6 = []
        for hx, hy in hole_coords_r6:
            hcore = cq.Solid.makeCylinder(5.5/2 - 0.1, bbox.zmax + 5, pnt=cq.Vector(hx, hy, 0), dir=cq.Vector(0, 0, 1))
            hring_inner = 5.5/2 + 0.5
            hring_outer = 5.5/2 + 2.0
            hring_core = cq.Solid.makeCylinder(hring_inner, bbox.zmax + 5, pnt=cq.Vector(hx, hy, 0), dir=cq.Vector(0, 0, 1))
            hring_shell = cq.Solid.makeCylinder(hring_outer, bbox.zmax + 5, pnt=cq.Vector(hx, hy, 0), dir=cq.Vector(0, 0, 1)).cut(hring_core)
            
            ev = shape.intersect(hcore).Volume() / hcore.Volume()
            wv = shape.intersect(hring_shell).Volume() / hring_shell.Volume()
            measured_r6.append((round(ev, 3), round(wv, 3)))
            if ev > 0.1 or wv < 0.7: holes_r6_ok = False
        
        results["R6"] = {
            "status": "pass" if (r6_z_ok and holes_r6_ok) else "fail",
            "value": [round(z_min, 3), measured_r6],
            "method": f"z_min check; Hole empty/wall fraction for cylinders at {hole_coords_r6}",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": z_min, "ok": r6_z_ok},
                {"condition": "Two vertical screw holes diameter 5.5 mm", "measured": measured_r6, "ok": holes_r6_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Envelope and Mass
    try:
        bbox = shape.BoundingBox()
        x_min, x_max = bbox.xmin, bbox.xmax
        y_min, y_max = bbox.ymin, bbox.ymax
        z_min, z_max = bbox.zmin, bbox.zmax

        r7_x_ok = (x_min >= -35.01) and (x_max <= 35.01)
        r7_z_ok = z_max <= 55.01
        
        vol_mm3 = shape.Volume()
        mass_g = vol_mm3 * 1.24 / 1000.0
        r7_m_ok = mass_g <= 60.01

        results["R7"] = {
            "status": "pass" if (r7_x_ok and r7_z_ok and r7_m_ok) else "fail",
            "value": [round(x_min, 2), round(x_max, 2), round(z_max, 2), round(mass_g, 2)],
            "method": f"BBox check; Mass = volume({vol_mm3:.1f}) * 1.24 / 1000",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": [x_min, x_max], "ok": r7_x_ok},
                {"condition": "top <= 55 mm", "measured": z_max, "ok": r7_z_ok},
                {"condition": "mass <= 60 g", "measured": mass_g, "ok": r7_m_ok}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    solve()