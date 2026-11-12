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
            "method": "count number of solids in CQ shape",
            "criteria": [{"condition": "One single, valid solid", "measured": n_solids, "ok": status == "pass"}],
            "note": f"{n_solids} solid(s) found"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "count solids", "criteria": [], "note": str(e)}

    # R2 & R3: Face plate thickness and Central Bore
    try:
        bbox = shape.BoundingBox()
        y_min, y_max = bbox.ymin, bbox.ymax
        
        # R2: Face plate at least 4 mm thick (y = 0 to 4) with solid material all around the central bore.
        # To verify thickness is actually >= 4mm throughout the region of interest, we probe a slab [0, 4]
        # and check if it's fully occupied by material relative to the expected geometry.
        # A more robust way: Check that for any point in the central bore area at y=2, there is material.
        # Or simply: The intersection of the part with a slab [0, 4] must have a volume close to its theoretical max.
        # However, R2 specifically asks for "solid material all around the central bore".
        # We'll check that the thickness at the bore boundary is >= 4mm.
        
        bore_diam = 22.5
        bore_pnt = cq.Vector(0, -1, 30) 
        bore_dir = cq.Vector(0, 1, 0)
        
        # Probe the thickness at the bore edge (radius R)
        # We check if there is material at y=0 and y=4 at a radius slightly larger than the bore.
        check_r = (bore_diam / 2) + 2.0
        thickness_points = [
            cq.Vector(check_r, 0, 30),
            cq.Vector(-check_r, 0, 30),
            cq.Vector(check_r, 4, 30),
            cq.Vector(-check_r, 4, 30)
        ]
        
        thickness_ok = True
        for pt in thickness_points:
            # Check if material exists at y=0 and y=4 near the bore
            # We use a small probe to see if the point is inside the solid
            probe_size = 0.5
            p_box = cq.Solid.makeBox(probe_size, probe_size, probe_size, pnt=cq.Vector(pt.x-probe_size/2, pt.y-probe_size/2, pt.z-probe_size/2))
            if shape.intersect(p_box).Volume() < (probe_size**3 * 0.1):
                thickness_ok = False
                break

        # R3: Central bore diameter 22.5 mm through the face plate on shaft axis (x=0, z=30).
        core = cq.Solid.makeCylinder(bore_diam/2 - 0.1, 10.0, pnt=bore_pnt, dir=bore_dir)
        wall = cq.Solid.makeCylinder(bore_diam/2 + 2.0, 10.0, pnt=bore_pnt, dir=bore_dir).cut(
            cq.Solid.makeCylinder(bore_diam/2 + 0.1, 10.0, pnt=bore_pnt, dir=bore_dir))
        
        empty_vol = shape.intersect(core).Volume() / core.Volume()
        walled_vol = shape.intersect(wall).Volume() / wall.Volume()
        
        r3_ok = (empty_vol < 0.1) and (walled_vol > 0.8)
        # R2 requires thickness >= 4mm AND material around bore. 
        # Since we checked points at y=0 and y=4, we satisfy the "at least 4mm thick" requirement.
        r2_ok = thickness_ok

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": thickness_ok,
            "method": "check material presence at y=0 and y=4 near bore radius",
            "criteria": [{"condition": "Face plate at least 4 mm thick (y = 0 to 4) with solid material around bore", "measured": thickness_ok, "ok": r2_ok}],
            "note": f"Thickness check: {thickness_ok}"
        }

        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": [empty_vol, walled_vol],
            "method": f"bore probe at (0, y, 30) with D={bore_diam}",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": empty_vol, "ok": r3_ok}],
            "note": f"Empty: {empty_vol:.3f}, Walled: {walled_vol:.3f}"
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "thickness check", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "bore probe", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes (3.4mm) at (+-15.5, 30 +- 15.5)
    try:
        holes_ok = 0
        coords = [(15.5, 30+15.5), (15.5, 30-15.5), (-15.5, 30+15.5), (-15.5, 30-15.5)]
        for cx, cz in coords:
            core = cq.Solid.makeCylinder(3.4/2 - 0.1, 15.0, pnt=cq.Vector(cx, -1, cz), dir=cq.Vector(0, 1, 0))
            wall = cq.Solid.makeCylinder(3.4/2 + 2.0, 15.0, pnt=cq.Vector(cx, -1, cz), dir=cq.Vector(0, 1, 0)).cut(
                cq.Solid.makeCylinder(3.4/2 + 0.1, 15.0, pnt=cq.Vector(cx, -1, cz), dir=cq.Vector(0, 1, 0)))
            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            walled_ratio = shape.intersect(wall).Volume() / wall.Volume()
            if empty_ratio < 0.2 and walled_ratio > 0.7:
                holes_ok += 1
        r4_status = holes_ok == 4
        results["R4"] = {
            "status": "pass" if r4_status else "fail",
            "value": holes_ok,
            "method": f"probed 4 cylinders of D=3.4 at coords {coords}",
            "criteria": [{"condition": "Four motor screw holes, diameter 3.4 mm", "measured": holes_ok, "ok": r4_status}],
            "note": f"Found {holes_ok}/4 valid holes"
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "hole probe", "criteria": [], "note": str(e)}

    # R5: Motor clearance (-21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5)
    try:
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        intersected_vol = shape.intersect(clearance_box).Volume()
        r5_ok = intersected_vol < 0.5 
        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": intersected_vol,
            "method": f"intersected shape with box [-21.5, 21.5]x[-48, 0]x[8.5, 51.5]",
            "criteria": [{"condition": "Motor clearance: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5", "measured": intersected_vol, "ok": r5_ok}],
            "note": f"Interference vol: {intersected_vol}"
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "box intersection", "criteria": [], "note": str(e)}

    # R6: Base on the table (minimum z = 0) and two 5.5mm holes at (+-25, 25)
    try:
        bbox = shape.BoundingBox()
        z_min = bbox.zmin
        z_ok = z_min <= 0.1 
        holes_ok = 0
        coords = [(25, 25), (-25, 25)]
        for cx, cy in coords:
            core = cq.Solid.makeCylinder(5.5/2 - 0.1, 40.0, pnt=cq.Vector(cx, cy, z_min-5), dir=cq.Vector(0, 0, 1))
            wall = cq.Solid.makeCylinder(5.5/2 + 2.0, 40.0, pnt=cq.Vector(cx, cy, z_min-5), dir=cq.Vector(0, 0, 1)).cut(
                cq.Solid.makeCylinder(5.5/2 + 0.1, 40.0, pnt=cq.Vector(cx, cy, z_min-5), dir=cq.Vector(0, 0, 1)))
            empty_ratio = shape.intersect(core).Volume() / core.Volume()
            walled_ratio = shape.intersect(wall).Volume() / wall.Volume()
            if empty_ratio < 0.2 and walled_ratio > 0.7:
                holes_ok += 1
        r6_status = z_ok and (holes_ok == 2)
        results["R6"] = {
            "status": "pass" if r6_status else "fail",
            "value": [z_min, holes_ok],
            "method": f"checked z_min and probed 2 cylinders of D=5.5 at (+-25, 25)",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": z_min, "ok": z_ok},
                {"condition": "Two vertical screw holes, diameter 5.5 mm", "measured": holes_ok, "ok": holes_ok == 2}
            ],
            "note": f"z_min={z_min:.3f}, holes={holes_ok}"
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "base check", "criteria": [], "note": str(e)}

    # R7: Envelope and Mass
    try:
        bbox = shape.BoundingBox()
        x_min, x_max = bbox.xmin, bbox.xmax
        z_max = bbox.zmax
        vol_mm3 = shape.Volume()
        density = 1.24 # g/cm3
        mass_g = (vol_mm3 * density) / 1000.0
        env_x_ok = (-35 <= x_min + 0.01) and (x_max - 0.01 <= 35)
        env_z_ok = z_max <= 55.01
        mass_ok = mass_g <= 60.01
        r7_status = env_x_ok and env_z_ok and mass_ok
        results["R7"] = {
            "status": "pass" if r7_status else "fail",
            "value": [round(x_min, 2), round(x_max, 2), round(z_max, 2), round(mass_g, 2)],
            "method": f"bbox check and mass = vol * {density}/1000",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": [x_min, x_max], "ok": env_x_ok},
                {"condition": "top <= 55 mm", "measured": z_max, "ok": env_z_ok},
                {"condition": "mass <= 60 g", "measured": mass_g, "ok": mass_ok}
            ],
            "note": f"x:[{x_min:.1f},{x_max:.1f}], z:{z_max:.1f}, m:{mass_g:.1f}"
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "envelope/mass check", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()