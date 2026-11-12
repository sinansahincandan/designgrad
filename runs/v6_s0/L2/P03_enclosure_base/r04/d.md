**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6.0mm OD and 2.2mm pilot holes.
- **Cutout**: Rectangular aperture on the $-X$ face for cable access.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load from $z=8$ down to the floor.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity is a single subtraction of a box defined by $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD = 6.0mm. The boss solid extends from $z=2$ to $z=8$. A 2.2mm diameter pilot hole is subtracted starting at $z=8$ and extending down to $z=4$ (providing a 4mm depth).
- R6: USB-C cutout on $-X$ wall; subtract a rectangular volume of 9mm (Y) x 3mm (Z) x 7mm (X) centered at $y=0, z=14$. The subtraction volume is defined by $x \in [-45, -38], y \in [-4.5, 4.5], z \in [12.5, 15.5]$ to ensure full penetration through the wall into the cavity.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.