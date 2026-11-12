**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD, spanning from the bottom of the floor ($z=0$) up to the board underside ($z=8$).
- **Cutout**: A rectangular through-hole subtraction on the $-X$ face for cable access.

**Load Path**: PCB weight is transferred through screws into the bosses, which are anchored to the floor and walls, distributing the load across the base.

**Requirement Compliance**:
- R1: Create a single solid by first performing a `union` of the floor ($z=0$ to $2$), the walls, and the bosses (extending from $z=0$ to $8$). Then, perform `subtractions` for the board cavity (R3), the pilot holes (R5), and the USB-C cutout (R6).
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, spanning $z=0$ to $z=8$. Pilot holes (2.2mm diameter) are subtracted from the bosses from $z=8$ down to $z=4$.
- R6: USB-C cutout via a through-hole subtraction on the $-X$ wall; volume defined by $x \in [-43, -39]$, $y \in [-4.5, 4.5]$ (9mm width), and $z \in [12.5, 15.5]$ (3mm height), centered at $y=0, z=14$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.