"""physkit: put the built CAD part into a MuJoCo scene and observe it in realistic scenarios.

Problem-independent helper for the scenario agent (L6). Units at this API: millimetres, grams, newtons, seconds, degrees.
(Internally MuJoCo runs in SI units.)

    import physkit as pk
    sc = pk.Scene()                                   # desk plane at z = 0, gravity -Z, friction 0.5 (PLA on wood)
    part = sc.add_part()                              # the built part (part.stl), free to move, mass from its volume
    phone = sc.add_box("phone", size=(9, 75, 160), mass=200, pos=(-30, 0, 80), euler=(0, -25, 0))
    sc.push("phone", force=(0, 2, 0), at=(-60, 0, 150), start=1.0, duration=0.1)   # a 2 N side tap at a world point
    res = sc.run(3.0)                                 # simulate 3 s
    res.body("part").tilt_deg, res.body("part").slide_mm, res.body("phone").drop_mm, res.touching("phone", "part")

The part's collision shape is its volume voxelised into boxes (part_hulls.npz, computed once before the script runs), so concave
features such as slots, lips and hooks are kept. Mass and inertia come from the full part mesh and the material density.
"""
import json
import math
from dataclasses import dataclass, field
from pathlib import Path

import mujoco
import numpy as np

MM = 1e-3
G = 1e-3


def _quat_from_euler_deg(euler):
    """XYZ intrinsic rotations in degrees -> MuJoCo quaternion (w, x, y, z)."""
    q = np.zeros(4)
    mujoco.mju_euler2Quat(q, np.radians(euler), "XYZ")
    return q


def _merge_boxes(occ):
    """Greedy merge of a boolean voxel grid into axis-aligned boxes: list of (i0, j0, k0, i1, j1, k1), inclusive."""
    X, Y, Z = occ.shape
    used = np.zeros_like(occ, bool)
    boxes = []
    for k in range(Z):
        for j in range(Y):
            i = 0
            while i < X:
                if not occ[i, j, k] or used[i, j, k]:
                    i += 1
                    continue
                i1 = i
                while i1 + 1 < X and occ[i1 + 1, j, k] and not used[i1 + 1, j, k]:
                    i1 += 1
                j1 = j
                while j1 + 1 < Y and occ[i:i1 + 1, j1 + 1, k].all() and not used[i:i1 + 1, j1 + 1, k].any():
                    j1 += 1
                k1 = k
                while k1 + 1 < Z and occ[i:i1 + 1, j:j1 + 1, k1 + 1].all() and not used[i:i1 + 1, j:j1 + 1, k1 + 1].any():
                    k1 += 1
                used[i:i1 + 1, j:j1 + 1, k:k1 + 1] = True
                boxes.append((i, j, k, i1, j1, k1))
                i = i1 + 1
    return boxes


def _occupancy(m, axes):
    """Cell centres inside the mesh, layer by layer: the z-section's closed loops, even-odd rule (holes count)."""
    import shapely
    from shapely.geometry import Polygon
    xs, ys, zs = axes
    X, Y = np.meshgrid(xs, ys, indexing="ij")
    occ = np.zeros((len(xs), len(ys), len(zs)), bool)
    for k, z in enumerate(zs):
        sec = m.section(plane_origin=[0, 0, z], plane_normal=[0, 0, 1])
        if sec is None:
            continue
        inside = np.zeros(X.shape, bool)
        for loop in sec.discrete:
            if len(loop) < 3:
                continue
            poly = Polygon(loop[:, :2])
            if not poly.is_valid:
                poly = poly.buffer(0)
            inside ^= shapely.contains_xy(poly, X, Y)
        occ[:, :, k] = inside
    return occ


def decompose(stl="part.stl", out="part_hulls.npz", pitch=None, max_boxes=4000):
    """Collision shape of the part: its volume voxelised (cell centres inside the mesh) and merged into boxes. Keeps holes, slots,
    lips and hooks down to about one cell (default 1 mm). Called by the harness before the agent's script runs."""
    import trimesh
    m = trimesh.load(stl, force="mesh")
    lo, hi = m.bounds
    pitch = pitch or max(0.5, (np.prod(hi - lo) / 4e6) ** (1 / 3))
    while True:
        axes = [np.arange(lo[d] + pitch / 2, hi[d], pitch) for d in range(3)]
        G3 = np.stack(np.meshgrid(*axes, indexing="ij"), -1)
        occ = _occupancy(m, axes)
        boxes = _merge_boxes(occ)
        if len(boxes) <= max_boxes or pitch > 4:
            break
        pitch *= 1.25
    b = np.array(boxes, float).reshape(-1, 6)
    blo = lo + b[:, :3] * pitch
    bhi = lo + (b[:, 3:] + 1) * pitch
    np.savez_compressed(out, lo=blo, hi=bhi, pitch=pitch, fill_ratio=occ.sum() * pitch ** 3 / m.volume)
    return len(boxes)


@dataclass
class BodyResult:
    name: str
    start_mm: list
    end_mm: list
    tilt_deg: float          # rotation between start and end orientation
    max_tilt_deg: float      # largest rotation reached during the run
    slide_mm: float          # horizontal (XY) displacement start -> end
    max_slide_mm: float
    drop_mm: float           # how far the body's centre went DOWN (start z - end z); negative = went up
    min_z_mm: float          # lowest z reached by the body's centre
    toppled: bool            # tilt > 30 deg at the end
    settled: bool            # speed at the end < 5 mm/s and < 5 deg/s

    def as_dict(self):
        return {k: (round(v, 2) if isinstance(v, float) else v) for k, v in self.__dict__.items()}


@dataclass
class Result:
    bodies: dict
    contacts: dict = field(default_factory=dict)    # (a, b) -> True if in contact at the end
    initial_penetration_mm: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)

    def body(self, name) -> BodyResult:
        return self.bodies[name]

    def touching(self, a, b) -> bool:
        return bool(self.contacts.get(tuple(sorted((a, b))), False))

    def summary(self):
        return {"bodies": {k: v.as_dict() for k, v in self.bodies.items()},
                "contacts_at_end": [f"{a}-{b}" for (a, b), v in self.contacts.items() if v],
                "initial_penetration_mm": self.initial_penetration_mm, "warnings": self.warnings}


class Scene:
    def __init__(self, table=True, friction=0.5, gravity=(0, 0, -9.81), timestep=0.0005, folder="."):
        self.folder = Path(folder)
        self.meta = json.loads((self.folder / "metrics.json").read_text()) if (self.folder / "metrics.json").exists() else {}
        self.density = self._density()
        self.friction = friction
        self.gravity = gravity
        self.timestep = timestep
        self.table = table
        self.items = []          # xml snippets for bodies
        self.assets = []
        self.pushes = []
        self.welds = []
        self.names = []
        self.notes = []
        self.carries = []
        self._part_added = False

    def _density(self):
        p = self.folder / "density.txt"
        return float(p.read_text()) if p.exists() else 1.24

    # ------------------------------------------------------------------ bodies
    def add_part(self, name="part", pos=(0, 0, 0), euler=(0, 0, 0), fixed=False, friction=None, lift=0.5, on_desk=True):
        """The built part, at its CAD position moved by pos (mm) and rotated by euler (deg, about its centre of mass).
        on_desk=True (default for a free part) first shifts it vertically so its lowest point is `lift` mm above the desk, then it
        drops onto the desk. fixed=True welds it to the world where it is (e.g. a part screwed to a wall)."""
        import trimesh
        m = trimesh.load(self.folder / "part.stl", force="mesh")
        boxes = np.load(self.folder / "part_hulls.npz")
        mass = m.volume * self.density / 1000.0  # g
        com = m.center_mass
        inertia = m.moment_inertia * (self.density / 1000.0)  # g*mm^2 about com (trimesh: unit density)
        fr = friction or self.friction
        geoms = []
        for lo_, hi_ in zip(boxes["lo"], boxes["hi"]):   # collision: voxel boxes (hidden group 3)
            c = ((lo_ + hi_) / 2 - com) * MM; h = (hi_ - lo_) / 2 * MM
            geoms.append(f'<geom type="box" pos="{c[0]:.6f} {c[1]:.6f} {c[2]:.6f}" size="{h[0]:.6f} {h[1]:.6f} {h[2]:.6f}" group="3" '
                         f'rgba="0.55 0.68 0.86 0.3" friction="{fr} 0.005 0.0001" condim="4" mass="0"/>')
        vis = f"{name}_visual"   # visual: the real mesh, no collisions
        self.assets.append(f'<mesh name="{vis}" vertex="{" ".join(f"{x:.5f}" for x in ((m.vertices - com) * MM).ravel())}" '
                           f'face="{" ".join(str(x) for x in m.faces.ravel())}"/>')
        geoms.append(f'<geom type="mesh" mesh="{vis}" contype="0" conaffinity="0" group="1" rgba="0.55 0.68 0.86 1" mass="0"/>')
        I = inertia * G * MM * MM
        full = f"{I[0,0]:.6e} {I[1,1]:.6e} {I[2,2]:.6e} {I[0,1]:.6e} {I[0,2]:.6e} {I[1,2]:.6e}"
        q = _quat_from_euler_deg(euler)
        dz = 0.0
        if on_desk and not fixed:
            R = np.zeros(9); mujoco.mju_quat2Mat(R, q); R = R.reshape(3, 3)
            zmin = ((m.vertices - com) @ R.T)[:, 2].min() + com[2] + pos[2]
            dz = lift - zmin
            if abs(dz) > 1.0:
                self.notes.append(f"part shifted {dz:+.1f} mm in z so it rests on the desk (its lowest point was at z = {zmin:.1f})")
        p = (np.asarray(com) + np.asarray(pos) + np.array([0, 0, dz])) * MM
        joint = "" if fixed else "<freejoint/>"
        self.items.append(f'<body name="{name}" pos="{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}" quat="{q[0]} {q[1]} {q[2]} {q[3]}">{joint}'
                          f'<inertial pos="0 0 0" mass="{mass * G:.6e}" fullinertia="{full}"/>{"".join(geoms)}</body>')
        self.names.append(name)
        self._part_added = True
        return name

    def _prim(self, kind, name, size_xml, mass, pos, euler, friction, rgba, fixed):
        p = np.asarray(pos, float) * MM
        q = _quat_from_euler_deg(euler)
        joint = "" if fixed else "<freejoint/>"
        self.items.append(f'<body name="{name}" pos="{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}" quat="{q[0]} {q[1]} {q[2]} {q[3]}">{joint}'
                          f'<geom type="{kind}" size="{size_xml}" mass="{mass * G:.6e}" rgba="{rgba}" '
                          f'friction="{friction or self.friction} 0.005 0.0001" condim="4"/></body>')
        self.names.append(name)
        return name

    def add_box(self, name, size, mass, pos, euler=(0, 0, 0), friction=None, fixed=False, rgba="0.2 0.2 0.25 1"):
        """Box with full edge lengths size=(sx, sy, sz) mm, mass in g, centre at pos (mm), rotated by euler (deg, XYZ)."""
        s = np.asarray(size, float) / 2 * MM
        return self._prim("box", name, f"{s[0]:.6f} {s[1]:.6f} {s[2]:.6f}", mass, pos, euler, friction, rgba, fixed)

    def add_cylinder(self, name, radius, length, mass, pos, euler=(0, 0, 0), friction=None, fixed=False, rgba="0.8 0.8 0.85 1"):
        """Cylinder along its local z axis, radius and full length in mm."""
        return self._prim("cylinder", name, f"{radius * MM:.6f} {length / 2 * MM:.6f}", mass, pos, euler, friction, rgba, fixed)

    def add_sphere(self, name, radius, mass, pos, friction=None, fixed=False, rgba="0.8 0.3 0.3 1"):
        return self._prim("sphere", name, f"{radius * MM:.6f}", mass, pos, (0, 0, 0), friction, rgba, fixed)

    def add_wall(self, x=0.0, name="wall"):
        """A fixed vertical wall: the plane x = x0 (material on the -X side)."""
        self.items.append(f'<body name="{name}" pos="{(x - 50) * MM:.6f} 0 0.25"><geom type="box" size="0.05 1 0.5" '
                          f'rgba="0.9 0.9 0.88 1" friction="{self.friction} 0.005 0.0001"/></body>')
        self.names.append(name)
        return name

    # ------------------------------------------------------------------ disturbances
    def push(self, body, force, at=None, start=0.5, duration=0.1):
        """Apply a force (N, world frame) to `body` at world point `at` (mm; default its centre), `start` s after the beginning of the
        NEXT run() call, for `duration` s. (Several run() calls continue the same scene; each push applies in the run that follows it.)"""
        self.pushes.append((body, np.asarray(force, float), None if at is None else np.asarray(at, float) * MM, start, duration))

    def place_by_hand(self, body, approach=(0, 0, 40), seconds=1.0):
        """Place `body` the way a hand does: in the NEXT run() it starts `approach` mm away from the position you gave it, is carried
        smoothly to that position over `seconds`, and is released there (outcomes are measured from the release)."""
        self.carries.append((body, np.asarray(approach, float) * MM, seconds))

    def tilt_desk(self, deg, axis="x"):
        """Simulate a tilted desk by rotating gravity by `deg` degrees about the world x or y axis."""
        a = math.radians(deg)
        g = 9.81
        self.gravity = (0, g * math.sin(a), -g * math.cos(a)) if axis == "x" else (-g * math.sin(a), 0, -g * math.cos(a))
        if hasattr(self, "model"):            # scene already running: tilt from now on
            self.model.opt.gravity[:] = self.gravity

    # ------------------------------------------------------------------ build + run
    def xml(self):
        table = ('<geom name="desk" type="plane" size="1 1 0.01" rgba="0.82 0.74 0.62 1" '
                 f'friction="{self.friction} 0.005 0.0001" condim="4"/>') if self.table else ""
        return (f'<mujoco model="scenario"><option timestep="{self.timestep}" gravity="{self.gravity[0]} {self.gravity[1]} {self.gravity[2]}" '
                f'cone="elliptic" impratio="10"/><default><geom solref="0.004 1" solimp="0.95 0.99 0.001"/></default>'
                f'<visual><global offwidth="960" offheight="720"/></visual>'
                f'<asset><texture type="skybox" builtin="gradient" rgb1="0.97 0.97 0.98" rgb2="0.78 0.82 0.88" width="64" height="64"/>{"".join(self.assets)}</asset><worldbody><light pos="0.2 -0.3 0.6" dir="-0.3 0.5 -1"/>'
                f'<light pos="-0.3 0.2 0.5" dir="0.5 -0.3 -1" diffuse="0.4 0.4 0.4"/>{table}{"".join(self.items)}'
                f'<body name="_finger" mocap="true" pos="0 0 -1"><geom type="capsule" fromto="0 0 -0.07 0 0 -0.009" size="0.009" '
                f'contype="0" conaffinity="0" rgba="0.93 0.74 0.62 1"/></body></worldbody></mujoco>')

    def build(self):
        self.model = mujoco.MjModel.from_xml_string(self.xml())
        self.data = mujoco.MjData(self.model)
        mujoco.mj_forward(self.model, self.data)
        return self.model, self.data

    def _body_names_of_geom(self, gid):
        return mujoco.mj_id2name(self.model, mujoco.mjtObj.mjOBJ_BODY, self.model.geom_bodyid[gid]) or "desk"

    def _contacts(self):
        out, pen = {}, {}
        for i in range(self.data.ncon):
            c = self.data.contact[i]
            a, b = self._body_names_of_geom(c.geom1), self._body_names_of_geom(c.geom2)
            if a == b:
                continue
            k = tuple(sorted((a if a != "world" else "desk", b if b != "world" else "desk")))
            out[k] = True
            pen[k] = max(pen.get(k, 0.0), -c.dist / MM)
        return out, pen

    def overlaps(self):
        """Penetration depth (mm) between bodies in their start positions, e.g. {"part-phone": 23.0}. An object placed where the
        specification says it goes that overlaps the part means the part intrudes into the object's space: a DESIGN failure."""
        if not hasattr(self, "model"):
            self.build()
        _, pen = self._contacts()
        return {f"{a}-{b}": round(p, 1) for (a, b), p in pen.items() if p > 1.0}

    def run(self, seconds=3.0, record=None):
        """Simulate (continuing the scene if run() was called before). Returns a Result with, per body: tilt, slide, drop, toppled,
        settled (measured from the start of THIS run); and the contacts at the end.
        record=dict(fps=30, size=(480, 640), azim=..., elev=..., distance=mm, lookat=(x,y,z) mm) appends RGB frames to self.frames."""
        if not hasattr(self, "model"):
            self.build()
        m, d = self.model, self.data
        bid = {n: mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, n) for n in self.names}
        carries, self.carries = self.carries, []
        carry = []
        for body, off, dur in carries:
            i = bid[body]; qa = m.jnt_qposadr[m.body_jntadr[i]]; va = m.jnt_dofadr[m.body_jntadr[i]]
            carry.append((qa, va, d.qpos[qa:qa + 3].copy(), off, dur))
            d.qpos[qa:qa + 3] = d.qpos[qa:qa + 3] + off
        mujoco.mj_forward(m, d)
        t_release = max([c[4] for c in carry], default=0.0)
        start = {n: (d.xpos[i].copy(), d.xquat[i].copy()) for n, i in bid.items()}
        _, pen0 = self._contacts()
        fid = m.body_mocapid[mujoco.mj_name2id(m, mujoco.mjtObj.mjOBJ_BODY, "_finger")]
        bad = {f"{a}-{b}": round(p, 1) for (a, b), p in pen0.items() if p > 1.0}
        if bad:
            raise ValueError(f"invalid scene: bodies overlap at the start by {bad} mm. If the object is where the specification puts it, "
                             "the PART intrudes into its space: report the scenario as a design FAIL (use sc.overlaps() before run). "
                             "Otherwise place the object 0.5-1 mm away from the surfaces it rests on.")
        maxtilt = {n: 0.0 for n in bid}; maxslide = {n: 0.0 for n in bid}; minz = {n: d.xpos[i][2] for n, i in bid.items()}
        steps = int(seconds / m.opt.timestep)
        warnings = []
        pushes, self.pushes = self.pushes, []
        rec = None
        if record:
            if not hasattr(self, "frames"):
                self.frames = []
            h, w = record.get("size", (480, 640))
            rec = (mujoco.Renderer(m, h, w), mujoco.MjvCamera(), max(1, int(1 / (record.get("fps", 30) * m.opt.timestep))))
            cam = rec[1]; cam.azimuth = record.get("azim", -135); cam.elevation = record.get("elev", -20)
            cam.distance = record.get("distance", 350) * MM
            cam.lookat[:] = np.asarray(record.get("lookat", (0, 0, 40))) * MM
        for s in range(steps):
            t = s * m.opt.timestep
            for qa, va, target, off, dur in carry:
                if t <= dur:
                    a = min(1.0, t / dur); a = a * a * (3 - 2 * a)
                    d.qpos[qa:qa + 3] = target + off * (1 - a)
                    d.qvel[va:va + 6] = 0
            if carry and abs(t - t_release) < m.opt.timestep / 2:
                start = {n: (d.xpos[i].copy(), d.xquat[i].copy()) for n, i in bid.items()}
                maxtilt = {n: 0.0 for n in bid}; maxslide = {n: 0.0 for n in bid}; minz = {n: d.xpos[i][2] for n, i in bid.items()}
            d.mocap_pos[fid] = (0, 0, -1)
            for body, F, at, t0, dur in pushes:          # the finger that pushes (visual only)
                if at is not None and t0 - 0.15 <= t < t0 + dur + 0.15:
                    u = F / (np.linalg.norm(F) + 1e-12)
                    back = 0.0 if t0 <= t < t0 + dur else 0.03 * (min(abs(t - t0), abs(t - t0 - dur)) / 0.15)
                    d.mocap_pos[fid] = at - u * back
                    q = np.zeros(4); mujoco.mju_quatZ2Vec(q, u); d.mocap_quat[fid] = q
            d.xfrc_applied[:] = 0
            for body, F, at, t0, dur in pushes:
                if t0 <= t < t0 + dur and body in bid:
                    i = bid[body]
                    d.xfrc_applied[i, :3] = F
                    if at is not None:
                        r = at - d.xipos[i]
                        d.xfrc_applied[i, 3:] = np.cross(r, F)
            mujoco.mj_step(m, d)
            if rec and s % rec[2] == 0:
                rec[0].update_scene(d, rec[1]); self.frames.append(rec[0].render().copy())
            if s % 20 == 0:
                for n, i in bid.items():
                    dq = np.zeros(3); mujoco.mju_subQuat(dq, d.xquat[i], start[n][1])
                    maxtilt[n] = max(maxtilt[n], math.degrees(np.linalg.norm(dq)))
                    maxslide[n] = max(maxslide[n], np.linalg.norm(d.xpos[i][:2] - start[n][0][:2]) / MM)
                    minz[n] = min(minz[n], d.xpos[i][2])
            if not np.all(np.isfinite(d.qpos)) or (s % 200 == 0 and np.abs(d.qvel).max() > 50):
                raise ValueError(f"the simulation blew up at t={t:.3f} s (velocities > 50 m/s); check object placement, masses and "
                                 "forces (a light tap is 0.5-1 N for 0.1 s)")
        res = {}
        for n, i in bid.items():
            dq = np.zeros(3); mujoco.mju_subQuat(dq, d.xquat[i], start[n][1])
            tilt = math.degrees(np.linalg.norm(dq))
            v = np.zeros(6); mujoco.mj_objectVelocity(m, d, mujoco.mjtObj.mjOBJ_BODY, i, v, 0)
            res[n] = BodyResult(n, list(np.round(start[n][0] / MM, 2)), list(np.round(d.xpos[i] / MM, 2)), tilt, maxtilt[n],
                                float(np.linalg.norm(d.xpos[i][:2] - start[n][0][:2]) / MM), maxslide[n],
                                float((start[n][0][2] - d.xpos[i][2]) / MM), float(minz[n] / MM), tilt > 30,
                                bool(np.linalg.norm(v[3:]) / MM < 5 and math.degrees(np.linalg.norm(v[:3])) < 5))
        con, _ = self._contacts()
        return Result(res, con, {f"{a}-{b}": round(p, 2) for (a, b), p in pen0.items()}, self.notes + warnings)

    def snapshot(self, path, azim=-135, elev=-20, distance=None, lookat=None):
        """Save an RGB image of the current state (after run())."""
        if not hasattr(self, "model"):
            self.build()
        r = mujoco.Renderer(self.model, 720, 960)
        cam = mujoco.MjvCamera()
        cam.azimuth, cam.elevation = azim, elev
        cam.distance = distance * MM if distance else 0.35
        cam.lookat[:] = (np.asarray(lookat) * MM) if lookat is not None else self.data.xpos[1:].mean(0)
        r.update_scene(self.data, cam)
        img = r.render()
        from PIL import Image
        Image.fromarray(img).save(path)
        return path
