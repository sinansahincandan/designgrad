**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: A thin plate $2\text{ mm}$ thick covering the footprint of the board and walls, spanning $z \in [0, 2]$. No structural ribs are included to ensure mass optimization and R3 compliance.
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness $2.0\text{ mm}$ (optimized for mass).
- **Bosses**: Four cylindrical pillars located at $(\pm35, \pm20)$ with 6mm OD and 2.2mm pilot holes. Bosses extend strictly from the top of the floor ($z=2$) to the bottom of the board cavity ($z=8$).
- **Cutout**: Rectangular aperture on the $-X$ face for cable access.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a single continuous boolean subtraction of a box with dimensions $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$. No part of the floor or bosses protrudes into this volume.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, pilot hole 2.2mm diameter from $z=8$ down to $z=4$ (ensuring the hole is $\ge 4\text{ mm}$ deep and does not enter the R3 zone).
- R6: USB-C cutout on $-X$ wall (at $x=-42.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit due to optimized wall thickness and floor design.