**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four solid cylindrical pillars at $(\pm35, \pm20)$ with 6.0mm OD, extending from the top of the floor ($z=2$) to the bottom of the board cavity ($z=8$).
- **Pilot Holes**: Four cylindrical voids at $(\pm35, \pm20)$ with 2.2mm diameter, extending from $z=2$ up to $z=8$, ensuring the hole is open at the top (at $z=8$).
- **Cutout**: Rectangular aperture on the $-X$ face for cable access, spanning the wall thickness.

**Load Path**: PCB weight is transferred through screws into the bosses; the pilot holes are subtracted from the solid boss volumes, ensuring the load is distributed through the 6mm OD boss structure and into the floor.

**Requirement Compliance**:
- R1: Create a single solid by first performing a union of the Floor, Walls, and Bosses; then perform boolean subtractions for the Board Cavity (R3), the four Boss Pilot Holes (R5), and the USB-C rectangular volume (R6).
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6.0mm, existing as solid volumes from $z=2$ to $z=8$; Pilot holes are 2.2mm diameter cylinders subtracted from $z=2$ up to $z=8$ (6mm depth), ensuring the hole is open at the top ($z=8$).
- R6: USB-C cutout on $-X$ wall defined by a rectangular volume: $x \in [-42.5, -39]$, $y \in [-4.5, 4.5]$ (9mm width), and $z \in [12.5, 15.5]$ (3mm height centered at $z=14$).
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.