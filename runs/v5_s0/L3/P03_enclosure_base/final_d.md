**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6.0mm OD, extending from the top of the floor ($z=2$) to the bottom of the board cavity ($z=8$).
- **Cutout**: Rectangular aperture on the $-X$ face for cable access, spanning the wall thickness.

**Load Path**: PCB weight is transferred through screws into the bosses; the pilot holes extend from $z=8$ down to $z=2$, ensuring load distribution through the boss and into the floor structure.

**Requirement Compliance**:
- R1: Create a single solid by unioning the floor, walls, and bosses; then perform boolean subtractions for the board cavity (R3), the four boss pilot holes (R5), and the USB-C rectangular volume (R6).
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6.0mm, with a 2.2mm diameter pilot hole extending from $z=8$ down to $z=2$ (6mm depth).
- R6: USB-C cutout on $-X$ wall defined by a rectangular volume: $x \in [-42.5, -39]$, $y \in [-4.5, 4.5]$ (9mm width), and $z \in [12.5, 15.5]$ (3mm height centered at $z=14$).
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.