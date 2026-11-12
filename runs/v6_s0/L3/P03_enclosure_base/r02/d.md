**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four additive solid cylinders with $OD = 6\text{mm}$ placed at $(\pm35, \pm20)$ extending from $z=2$ to $z=8$. A $2.2\text{mm}$ diameter pilot hole is then subtracted from the center of each boss, extending from $z=8$ down to $z=2$ (6mm depth).
- **Cutout**: A through-wall rectangular subtraction on the $-X$ face for cable access, defined by $x \in [-45, -37.5]$ to ensure full penetration of the wall.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load from $z=8$ down to the floor at $z=2$.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and additive boss cylinders, then subtracting pilot holes and the cutout.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm. Boss bodies are additive cylinders from $z=2$ to $z=8$; pilot holes (2.2mm diameter) are subtractive operations extending from $z=8$ down to $z=2$, providing a 6mm depth.
- R6: USB-C through-cutout on $-X$ wall; volume defined by $x \in [-45, -37.5]$ (ensuring full penetration), $y \in [-4.5, 4.5]$ (9mm width, centered at $y=0$), and $z \in [12.5, 15.5]$ (3mm height, centered at $z=14$).
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.