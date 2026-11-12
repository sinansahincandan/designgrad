"""Harness side of L6: turn the built part into MuJoCo model fragments the scenario agent includes in ITS OWN MuJoCo scene.

Writes, next to part.stl:
  part_body.xml    one <body name="part"> element in METRES at the part's CAD position: a free joint, the real mass and inertia
                   (from the mesh volume and the material density), collision boxes (the part's volume voxelised at 0.5-0.8 mm, so
                   holes, slots and lips are kept) and the real mesh as a visual-only geom
  part_assets.xml  the <mesh> asset that the visual geom uses (put it inside <asset>)
  part_info.json   mass_g, center_of_mass_mm, bbox_min_mm, bbox_max_mm, volume_mm3
The agent writes everything else (scene, objects, loads, simulation loop, measurements). This file is not shown to the agent.
"""
import json
from pathlib import Path

import numpy as np

from .physkit import decompose

MM = 1e-3


def build(folder, density):
    import trimesh
    folder = Path(folder)
    if not (folder / "part_hulls.npz").exists() or (folder / "part_hulls.npz").stat().st_mtime < (folder / "part.stl").stat().st_mtime:
        decompose(str(folder / "part.stl"), str(folder / "part_hulls.npz"))
    m = trimesh.load(folder / "part.stl", force="mesh")
    boxes = np.load(folder / "part_hulls.npz")
    com = m.center_mass
    mass_g = m.volume * density / 1000.0
    I = m.moment_inertia * (density / 1000.0) * 1e-3 * 1e-6          # g*mm^2 -> kg*m^2
    geoms = []
    for lo, hi in zip(boxes["lo"], boxes["hi"]):
        c = ((lo + hi) / 2 - com) * MM; h = (hi - lo) / 2 * MM
        geoms.append(f'  <geom type="box" pos="{c[0]:.6f} {c[1]:.6f} {c[2]:.6f}" size="{h[0]:.6f} {h[1]:.6f} {h[2]:.6f}" group="3" '
                     f'friction="0.5 0.005 0.0001" condim="4" rgba="0.55 0.68 0.86 0.3"/>')
    geoms.append('  <geom type="mesh" mesh="part_visual" contype="0" conaffinity="0" group="1" rgba="0.55 0.68 0.86 1"/>')
    p = com * MM
    body = (f'<body name="part" pos="{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}">\n  <freejoint name="part_free"/>\n'
            f'  <inertial pos="0 0 0" mass="{mass_g * 1e-3:.6e}" fullinertia="{I[0,0]:.6e} {I[1,1]:.6e} {I[2,2]:.6e} '
            f'{I[0,1]:.6e} {I[0,2]:.6e} {I[1,2]:.6e}"/>\n' + "\n".join(geoms) + "\n</body>\n")
    (folder / "part_body.xml").write_text(body)
    v = (m.vertices - com) * MM
    (folder / "part_assets.xml").write_text(
        f'<mesh name="part_visual" vertex="{" ".join(f"{x:.5f}" for x in v.ravel())}" face="{" ".join(str(x) for x in m.faces.ravel())}"/>\n')
    lo, hi = m.bounds
    (folder / "part_info.json").write_text(json.dumps({
        "mass_g": round(mass_g, 2), "center_of_mass_mm": [round(x, 2) for x in com], "bbox_min_mm": [round(x, 2) for x in lo],
        "bbox_max_mm": [round(x, 2) for x in hi], "volume_mm3": round(m.volume, 1), "n_collision_boxes": int(len(boxes["lo"]))}, indent=1))
    return folder / "part_body.xml"
