**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD and 2.2mm pilot holes.
- **Cutout**: Rectangular subtraction through the -X wall for cable access.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load from the top of the floor ($z=2$) up to the bottom of the board cavity ($z=8$).

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a boolean subtraction of a box spanning $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$ from the main body to ensure this volume is completely free of material.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, pilot hole 2.2mm diameter. Bosses extend from the floor ($z=2$) up to exactly $z=8$ to ensure no encroachment into the R3 cavity; pilot holes are at least 4mm deep (extending from $z=8$ down to $z=4$).
- R6: USB-C cutout is a rectangular subtraction through the entire thickness of the -X wall, spanning $x \in [-42.5, -40], y \in [-4.5, 4.5], z \in [12.5, 15.5]$ (centered at $y=0, z=14$ with dimensions 9mm Y x 3mm Z).
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.