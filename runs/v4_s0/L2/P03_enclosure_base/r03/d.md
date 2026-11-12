**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four solid cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD, spanning from the top of the floor ($z=2$) to the underside of the board ($z=8$). Each boss contains a 2.2mm diameter pilot hole subtracted from $z=4$ to $z=8$.
- **Cutout**: A rectangular through-cut subtraction on the $-X$ face for USB-C access, spanning the wall thickness from the outer boundary ($x=-42.5$) to the inner cavity boundary ($x=-40$).

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, spanning $z \in [2, 8]$, with a 2.2mm diameter pilot hole from $z=4$ to $z=8$ (ensuring 4mm depth and open top).
- R6: USB-C cutout on $-X$ wall; subtraction volume defined by $x \in [-42.5, -40]$, $y \in [-4.5, 4.5]$ (9mm width), and $z \in [12.5, 15.5]$ (3mm height), centered at $y=0, z=14$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.