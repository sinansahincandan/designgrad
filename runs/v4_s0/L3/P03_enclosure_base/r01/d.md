**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick solid base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD, spanning from the top of the floor ($z=2$) to the bottom of the board cavity ($z=8$).
- **Cutout**: A subtractive rectangular aperture on the $-X$ face for cable access.

**Load Path**: PCB weight is transferred through screws into the bosses; the bosses are physically fused to the floor at $z=2$ and terminate exactly at the board interface at $z=8$, distributing the load into the base and side walls.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting the board cavity, pilot holes, and USB-C cutout.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, spanning $z \in [2, 8]$. Each includes a 2.2mm diameter pilot hole (subtractive cylinder) starting at $z=8$ and extending down to $z=4$.
- R6: USB-C cutout on $-X$ wall realized via subtraction of a rectangular volume: $x \in [-45, -40]$, $y \in [-4.5, 4.5]$, $z \in [12.5, 15.5]$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.