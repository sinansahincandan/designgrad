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
        
        # To ensure through-hole and correct position: probe from y=-1 to y=10 (covers face plate thickness)
        probe_len = 15.0
        pnt_start = (0, -1, 30)

        # R3: Central Bore diameter check
        # We use a slightly smaller cylinder to ensure it's "empty" and a ring to ensure it's surrounded by solid
        core = cq.Solid.makeCylinder(bore_radius - 0.1, probe_len, pnt=cq.Vector(*pnt_start), dir=cq.Vector(*dir_vec))
        # Check if the core is actually empty (the hole exists)
        empty_vol_ratio = shape.intersect(core).Volume() / core.Volume()
        
        # R2: Face plate thickness and material around bore
        # Verify thickness at y=0 to 4 by checking intersection with a slice/box
        thickness_probe = cq.Solid.makeBox(100, 4, 100, pnt=cq.Vector(-50, 0, -20))
        inter_vol = shape.intersect(thickness_probe).Volume()
        # Check if the intersection volume is roughly equal to the probe volume (meaning plate exists there)
        # But more specifically, we check the y-extent of the solid within that region
        bbox_inter = shape.intersect(thickness_probe).BoundingBox()
        thick_measured = bbox_inter.ymax - bbox_inter.ymin if inter_vol > 1e-3 else 0.0

        # Verify material exists around the bore (R2) using a ring probe
        ring_inner = bore_radius + 0.5
        ring_outer = bore_radius + 4.0
        ring_core = cq.Solid.makeCylinder(ring_inner, probe_len, pnt=cq.Vector(*pnt_start), dir=cq.Vector(*dir_vec))
        ring_shell = cq.Solid.makeCylinder(ring_outer, probe_len, pnt=cq.Vector(*pnt_start), dir=cq.Vector(*dir_vec)).cut(ring_core)
        walled_vol_ratio = shape.intersect(ring_shell).Volume() / ring_shell.Volume()

        # R3: Through-hole check - the core must be empty AND the shell must be solid
        r2_ok = thick_measured >= 4.0 and walled_vol_ratio > 0.9
        r3_ok = empty_vol_ratio < 0.05 and walled_vol_ratio > 0.8 # Bore is a hole if core is empty
        
        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": [round(thick_measured, 2), round(walled_vol_ratio, 3)],
            "method": f"Thickness check (y=0 to 4) and ring-shell material presence around bore radius {bore_radius}",
            "criteria": [
                {"condition": "Face plate at least 4 mm thick", "measured": thick_measured, "ok": thick_measured >= 4.0},
                {"condition": "Solid material all around the central bore", "measured": walled_vol_ratio, "ok": walled_vol_ratio > 0.9}
            ],
            "note": ""
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": [round(empty_vol_ratio, 3), round(walled_vol_ratio, 3)],
            "method": f"Cylinder probe at (0, -1, 30) dir (0,1,0) to verify diameter and through-hole",
            "criteria": [
                {"condition": "Central bore diameter 22.5 mm", "measured": empty_vol_ratio, "ok": empty_vol_ratio < 0.05},
                {"condition": "Bore is a through-hole in material", "measured": walled_vol_ratio, "ok": walled_vol_ratio > 0.8}
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
            # Probe from y=-1 to y=10 to ensure it's through the face plate
            hpnt = (hx, -1, hz)
            hdir = (0, 1, 0)
            hlen = 15.0
            h_radius = 3.4 / 2
            
            hcore = cq.Solid.makeCylinder(h_radius - 0.1, hlen, pnt=cq.Vector(*hpnt), dir=cq.Vector(*hdir))
            hring_inner = h_radius + 0.5
            hring_outer = h_radius + 3.0
            hring_core = cq.Solid.makeCylinder(hring_inner, hlen, pnt=cq.Vector(*hpnt), dir=cq.Vector(*hdir))
            hring_shell = cq.Solid.makeCylinder(hring_outer, hlen, pnt=cq.Vector(*hpnt), dir=cq.Vector(*hdir)).cut(hring_core)
            
            ev = shape.intersect(hcore).Volume() / hcore.Volume()
            wv = shape.intersect(hring_shell).Volume() / hring_shell.Volume()
            measured_vals.append((round(ev, 3), round(wv, 3)))
            if ev > 0.1 or wv < 0.8: holes_ok = False
        
        results["R4"] = {
            "status": "pass" if holes_ok else "fail",
            "value": measured_vals,
            "method": f"Cylinder probes at {hole_coords} spanning y=-1 to 14",
            "criteria": [{"condition": "Four motor screw holes diameter 3.4 mm through face plate", "measured": measured_vals, "ok": holes_ok}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Motor clearance (-21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5)
    try:
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        inter_vol = shape.intersect(clearance_box).Volume()
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
            # Probe from z=0 to z=bbox.zmax+1 to ensure through-hole
            h_radius = 5.5 / 2
            hcore = cq.Solid.makeCylinder(h_radius - 0.1, bbox.zmax + 2, pnt=cq.Vector(hx, hy, 0), dir=cq.Vector(0, 0, 1))
            hring_inner = h_radius + 0.5
            hring_outer = h_radius + 3.0
            hring_core = cq.Solid.makeCylinder(hring_inner, bbox.zmax + 2, pnt=cq.Vector(hx, hy, 0), dir=cq.Vector(0, 0, 1))
            hring_shell = cq.Solid.makeCylinder(hring_outer, bbox.zmax + 2, pnt=cq.Vector(hx, hy, 0), dir=cq.Vector(0, 0, 1)).cut(hring_core)
            
            ev = shape.intersect(hcore).Volume() / hcore.Volume()
            wv = shape.intersect(hring_shell).Volume() / hring_shell.Volume()
            measured_r6.append((round(ev, 3), round(wv, 3)))
            if ev > 0.1 or wv < 0.8: holes_r6_ok = False
        
        results["R6"] = {
            "status": "pass" if (r6_z_ok and holes_r6_ok) else "fail",
            "value": [round(z_min, 3), measured_r6],
            "method": f"z_min check; Hole empty/wall fraction for vertical cylinders at {hole_coords_r6}",
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