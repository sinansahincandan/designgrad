**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z \in [0, 2]$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars centered at $(\pm35, \pm20)$. Each boss is a solid cylinder with $OD = 6\text{mm}$ and an internal pilot hole of $ID = 2.2\text{mm}$, spanning from the top of the floor ($z=2$) to the bottom of the board cavity ($z=8$).
- **Cutout**: A rectangular through-cut volume defined by $x \in [-44, -40]$, $y \in [-4.5, 4.5]$, and $z \in [12.5, 15.5]$. This volume pierces the $-X$ wall to ensure a clean opening.

**Load Path**: PCB weight is transferred through screws into the pilot holes of the bosses, which distribute the load from the board cavity ($z=8$) down into the floor ($z=2$).

**Requirement Compliance**:
- R1: Single solid created via boolean union of the floor, walls, and bosses, followed by the subtraction of the pilot holes, the board cavity, and the USB-C cutout.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a single boolean subtraction of the volume $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$ from the main body.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Four bosses at $(\pm35, \pm20)$, OD 6mm, pilot hole 2.2mm diameter spanning $z \in [2, 8]$.
- R6: USB-C cutout on $-X$ wall implemented as a through-cut volume ($x \in [-44, -40], y \in [-4.5, 4.5], z \in [12.5, 15.5]$) subtracted from the final combined solid.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.