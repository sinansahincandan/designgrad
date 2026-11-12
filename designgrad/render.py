"""Deterministic 4-view render of an STL (iso, front, top, right) into one PNG."""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import trimesh
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

VIEWS = [("Isometric", 25, -60), ("Front (looking +Y)", 0, -90), ("Top (looking -Z)", 90, -90), ("Right (looking -X)", 0, 0)]


def render(stl: Path, png: Path, size_px: int = 1000):
    m = trimesh.load(stl)
    tris = m.vertices[m.faces]
    lo, hi = m.bounds
    span = (hi - lo).max()
    ctr = (hi + lo) / 2
    fig = plt.figure(figsize=(size_px / 100, size_px / 100), dpi=100)
    for k, (name, elev, azim) in enumerate(VIEWS):
        ax = fig.add_subplot(2, 2, k + 1, projection="3d")
        e, a = np.radians(elev), np.radians(azim)
        view = np.array([np.cos(e) * np.cos(a), np.cos(e) * np.sin(a), np.sin(e)])
        light = view + np.array([0.3, -0.2, 0.5])
        light /= np.linalg.norm(light)
        shade = 0.35 + 0.65 * np.clip(np.abs(m.face_normals @ light), 0, 1)
        cols = np.stack([0.55 * shade, 0.65 * shade, 0.8 * shade, np.ones_like(shade)], 1)
        pc = Poly3DCollection(tris, facecolors=cols, edgecolors=(0, 0, 0, 0.08), linewidths=0.2)
        ax.add_collection3d(pc)
        for i, setlim in enumerate((ax.set_xlim, ax.set_ylim, ax.set_zlim)):
            setlim(ctr[i] - span / 2, ctr[i] + span / 2)
        ax.set_box_aspect((1, 1, 1))
        ax.view_init(elev=elev, azim=azim)
        if hasattr(ax, "set_proj_type"):
            ax.set_proj_type("ortho")
        ax.set_xlabel("X mm", fontsize=7); ax.set_ylabel("Y mm", fontsize=7); ax.set_zlabel("Z mm", fontsize=7)
        ax.tick_params(labelsize=6)
        ax.set_title(name, fontsize=9)
    fig.suptitle(f"bbox {hi[0]-lo[0]:.1f} x {hi[1]-lo[1]:.1f} x {hi[2]-lo[2]:.1f} mm", fontsize=9)
    fig.tight_layout()
    fig.savefig(png)
    plt.close(fig)
    return png


if __name__ == "__main__":
    render(Path(sys.argv[1]), Path(sys.argv[2]))
