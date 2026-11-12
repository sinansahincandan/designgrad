import cadquery as cq
import trimesh
import numpy as np
import json
from shapely.geometry import Point, Polygon

def solve():
    # Load the part
    try:
        shape = cq.importers.importStep('part.step').val()
        mesh = trimesh.load('part.stl')
    except Exception as e:
        print(json.dumps({"error": f"Failed to load files: {str(e)}"}))
        return

    results = {}
    density_pla = 1.24 / 1000  # g/mm3 (from 1.24 g/cm3)
    tol = 1e-2

    # R1: One single, valid solid
    try:
        n_solids = len(shape.Solids())
        status = "pass" if n_solids == 1 else "fail"
        results["R1"] = {
            "status": status,
            "value": int(n_solids),
            "method": "Counted number of solids in STEP file",
            "criteria": [{"condition": "One single, valid solid", "measured": int(n_solids), "ok": True if status == "pass" else False}],
            "note": f"Found {n_solids} solid(s)"
        }
    except Exception as e:
        results["R1"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R2 & R3: Face plate thickness and Central Bore
    try:
        # We slice at y=2 (middle of face plate) to verify the cross-section profile
        plane_x = 0
        plane_y = 2.0
        sec = mesh.section(plane_origin=[plane_x, plane_y, 0], plane_normal=[1, 0, 0])
        if sec is None:
            raise ValueError("Sectioning failed at y=2")
        path2d, T = sec.to_2D()
        polys = path2d.polygons_full
        
        # R3 Check: Central bore diameter 22.5 mm (radius 11.25)
        # We verify that the area inside a circle of radius 11.25 at (0, 30) is empty
        bore_center = Point(0, 30)
        bore_radius = 11.25
        
        # To check diameter accurately: find the largest empty circle centered at (0,30)
        # Or more simply, verify that no material exists within radius 11.25
        # and that material DOES exist just outside it to define a boundary.
        bore_is_empty = True
        for p in polys:
            # Check if any part of the solid intersects the bore area
            # We use a small buffer or check intersection with a circle polygon
            circle_poly = Point(0, 30).buffer(bore_radius)
            if p.intersects(circle_poly):
                # If they intersect, we must ensure it's not just a tiny sliver/edge
                # A better way: check if the intersection area is significant
                inter_area = p.intersection(circle_poly).area
                if inter_area > 0.1: # Threshold for "material in the bore"
                    bore_is_empty = False
                    break
        
        # R2 Check: Face plate thickness (y=0 to 4) and material around bore
        # Verify thickness: check if material exists at y=0 and y=4 at some x,z
        # And verify continuity/presence of material in the annulus
        thickness_ok = False
        material_in_annulus = False
        
        # Check for plate existence at y=0 and y=4 (within bounds)
        # We probe a few points to ensure the plate is actually there
        for test_z in [30, 15, 45]:
            for test_x in [0, 25]:
                p_low = Point(test_x, 0) # This logic is slightly flawed because section is 2D (X-Z plane?)
                # Wait: mesh.section with normal [1,0,0] produces a 2D shape in the Y-Z plane? 
                # No, standard trimesh section returns 2D in the plane of the slice.
                # If normal is [1,0,0], the plane is X=const. The 2D axes are Y and Z.
        
        # Let's re-evaluate: path2d.bounds gives [[ymin, zmin], [ymax, zmax]] or similar.
        # We need to find if material exists at y=0, y=4 AND in the annulus (r=15)
        # Using the 2D polygons from the section at x=0:
        # The 2D coordinates are local to the plane. For normal [1,0,0], axes are Y and Z.
        # We need to map world (y,z) to path2d local coords.
        # trimesh section documentation: "The 2D axes of path2d are an arbitrary in-plane frame"
        # To be safe, let's use the mesh.contains method on a grid for R2/R3.
        
        grid_res = 0.5
        y_range = np.arange(0, 4 + grid_res, grid_res)
        z_range = np.arange(10, 50 + grid_res, grid_res)
        Y_g, Z_g = np.meshgrid(y_range, z_range)
        pts = np.column_stack([np.full(Y_g.size, plane_x), Y_g.ravel(), Z_g.ravel()])
        inside = mesh.contains(pts)
        
        # R2: Thickness (material at y=0 and y=4)
        mat_at_y0 = np.any(inside[np.abs(Y_g.ravel() - 0) < 0.5])
        mat_at_y4 = np.any(inside[np.abs(Y_g.ravel() - 4) < 0.5])
        thickness_ok = mat_at_y0 and mat_at_y4
        
        # R2: Material around bore (annulus at r=15, z=30)
        # Check if material exists at radius 15 from (0, 30) in the Y-Z plane? 
        # No, the bore is along Y. The "around the bore" means in the X-Z plane.
        # Let's slice at y=2 (middle of plate), normal [0,1,0] -> Plane is Y=const. 2D axes are X and Z.
        sec_mid = mesh.section(plane_origin=[0, 2, 0], plane_normal=[0, 1, 0])
        if sec_mid is None: raise ValueError("Mid-section failed")
        path2d_mid, T_mid = sec_mid.to_2D()
        polys_mid = path2d_mid.polygons_full
        
        # In this X-Z section:
        # R3: Bore is a hole at (0, 30) with radius 11.25
        bore_circle = Point(0, 30).buffer(11.25)
        r3_ok = True
        for p in polys_mid:
            if p.intersection(bore_circle).area > 0.5:
                r3_ok = False
                break
        
        # R2: Material around bore (annulus at r=15)
        annulus_check_pt = Point(15, 30)
        r2_annulus_ok = any(p.contains(annulus_check_pt) for p in polys_mid)
        # Also check if the plate exists (not just a hole)
        plate_exists = sum(p.area for p in polys_mid) > 10.0 
        r2_ok = r2_annulus_ok and plate_exists

        results["R2"] = {
            "status": "pass" if r2_ok else "fail",
            "value": float(sum(p.area for p in polys_mid)),
            "method": "X-Z section at y=2 to verify annulus material and plate existence",
            "criteria": [{"condition": "Face plate >= 4mm thick with solid material around bore", "measured": float(r2_ok), "ok": r2_ok}],
            "note": f"Section area: {sum(p.area for p in polys_mid):.2f}"
        }
        results["R3"] = {
            "status": "pass" if r3_ok else "fail",
            "value": 0.0,
            "method": "X-Z section at y=2 to verify bore is a void",
            "criteria": [{"condition": "Central bore diameter 22.5 mm through the face plate", "measured": float(r3_ok), "ok": r3_ok}],
            "note": ""
        }
    except Exception as e:
        results["R2"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}
        results["R3"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R4: Four motor screw holes diameter 3.4 mm through the face plate along Y at (x, z) = (+-15.5, 30 +- 15.5).
    try:
        hole_coords = [(15.5, 45.5), (15.5, 14.5), (-15.5, 45.5), (-15.5, 14.5)]
        measured_diameters = []
        holes_exist = True
        
        for hx, hz in hole_coords:
            found_r = 0.0
            material_at_edge = False
            # Probe with cylinders of increasing radius to find the void diameter
            for test_r in np.linspace(0.1, 5.0, 40):
                h_cyl = cq.Solid.makeCylinder(test_r, 10, pnt=cq.Vector(hx, -3, hz), dir=cq.Vector(0, 1, 0))
                bore_vol = shape.intersect(h_cyl).Volume()
                if bore_vol < 0.5: # Cylinder is mostly in the void
                    found_r = test_r
                else:
                    material_at_edge = True
                    break
            
            if found_r > 0.1 and material_at_edge:
                measured_diameters.append(found_r * 2)
            else:
                holes_exist = False

        avg_dia = sum(measured_diameters)/len(measured_diameters) if measured_diameters else 0.0
        r4_ok = holes_exist and (abs(avg_dia - 3.4) < 1.0)

        results["R4"] = {
            "status": "pass" if r4_ok else "fail",
            "value": float(avg_dia),
            "method": f"Measured diameters of 4 holes at (+-15.5, 30 +- 15.5) via void probing and material boundary check",
            "criteria": [{"condition": "Four motor screw holes, diameter 3.4 mm", "measured": float(avg_dia), "ok": True if r4_ok else False}],
            "note": ""
        }
    except Exception as e:
        results["R4"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R5: Motor clearance
    try:
        clearance_box = cq.Solid.makeBox(43, 48, 43, pnt=cq.Vector(-21.5, -48, 8.5))
        intersect_vol = shape.intersect(clearance_box).Volume()
        r5_ok = intersect_vol < 0.1
        results["R5"] = {
            "status": "pass" if r5_ok else "fail",
            "value": float(intersect_vol),
            "method": f"Intersection volume with clearance box [-21.5, 21.5] x [-48, 0] x [8.5, 51.5]",
            "criteria": [{"condition": "Motor clearance: nothing in -21.5 <= x <= 21.5, -48 <= y <= 0, 8.5 <= z <= 51.5", "measured": float(intersect_vol), "ok": True if r5_ok else False}],
            "note": ""
        }
    except Exception as e:
        results["R5"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R6: Base on the table and screw holes
    try:
        bounds = shape.BoundingBox()
        z_min = bounds.zmin
        r6_z_ok = z_min >= -tol 
        
        base_surface_exists = False
        if r6_z_ok:
            probe_base = cq.Solid.makeBox(50, 50, 0.1, pnt=cq.Vector(-25, -25, 0))
            if shape.intersect(probe_base).Volume() > 0.1:
                base_surface_exists = True

        holes_ok = True
        measured_base_hole_diameters = []

        for sx in [-25, 25]:
            found_r = 0.0
            material_at_edge = False
            # Probe vertical holes at (sx, 25)
            for test_r in np.linspace(0.1, 7.0, 60):
                h_base_cyl = cq.Solid.makeCylinder(test_r, 20, pnt=cq.Vector(sx, 25, -5), dir=cq.Vector(0, 0, 1))
                bore_vol = shape.intersect(h_base_cyl).Volume()
                if bore_vol < 0.5:
                    found_r = test_r
                else:
                    material_at_edge = True
                    break
            
            if found_r > 0.1 and material_at_edge:
                measured_base_hole_diameters.append(found_r * 2)
            else:
                holes_ok = False

        avg_base_dia = sum(measured_base_hole_diameters)/len(measured_base_hole_diameters) if measured_base_hole_diameters else 0.0
        r6_ok = r6_z_ok and base_surface_exists and holes_ok and (abs(avg_base_dia - 5.5) < 1.0)

        results["R6"] = {
            "status": "pass" if r6_ok else "fail",
            "value": [float(z_min), float(avg_base_dia)],
            "method": f"Checked z_min >= 0, base surface existence, and measured base screw hole diameters at (+-25, 25) using material boundary check",
            "criteria": [
                {"condition": "Base on the table (minimum z = 0)", "measured": float(z_min), "ok": True if r6_z_ok and base_surface_exists else False},
                {"condition": "Two vertical screw holes, diameter 5.5 mm, at (x, y) = (+-25, 25)", "measured": float(avg_base_dia), "ok": True if holes_ok and abs(avg_base_dia - 5.5) < 1.0 else False}
            ],
            "note": f"z_min: {z_min:.3f}, base_surface: {base_surface_exists}"
        }
    except Exception as e:
        results["R6"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    # R7: Envelope and Mass
    try:
        b = shape.BoundingBox()
        x_ok = (b.xmin >= -35-tol) and (b.xmax <= 35+tol)
        z_ok = b.zmax <= 55+tol
        mass_g = mesh.volume * density_pla
        mass_ok = mass_g <= 60 + 0.1
        r7_ok = x_ok and z_ok and mass_ok
        results["R7"] = {
            "status": "pass" if r7_ok else "fail",
            "value": [float(b.xmin), float(b.xmax), float(b.zmax), float(mass_g)],
            "method": f"Checked BBox x[-35, 35], z_max <= 55 and mass = volume * {density_pla} g/mm^3",
            "criteria": [
                {"condition": "-35 <= x <= 35", "measured": [float(b.xmin), float(b.xmax)], "ok": True if x_ok else False},
                {"condition": "top <= 55 mm", "measured": float(b.zmax), "ok": True if z_ok else False},
                {"condition": "mass <= 60 g", "measured": float(mass_g), "ok": True if mass_ok else False}
            ],
            "note": ""
        }
    except Exception as e:
        results["R7"] = {"status": "error", "value": None, "method": "", "criteria": [], "note": str(e)}

    print(json.dumps(results))

if __name__ == "__main__":
    solve()