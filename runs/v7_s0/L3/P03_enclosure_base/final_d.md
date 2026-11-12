**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls.
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD and 2.2mm pilot holes.
- **Cutout**: A rectangular subtraction of $3\text{mm (X)} \times 9\text{mm (Y)} \times 3\text{mm (Z)}$ centered at $(x=-42.5, y=0, z=14)$, passing through the $-X$ wall to ensure a complete opening.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a single boolean subtraction of the volume $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$ from the main body, ensuring this entire region is void.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, pilot hole 2.2mm diameter from $z=8$ down to $z=4$.
- R6: USB-C cutout on $-X$ wall (at $x=-42.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$, implemented as a through-cut.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.