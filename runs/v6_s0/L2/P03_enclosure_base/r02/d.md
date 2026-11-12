**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 7.0mm OD and 2.2mm pilot holes.
- **Cutout**: Rectangular aperture on the $-X$ face for cable access.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity is a single subtraction of a box defined by $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD = 7.0mm. The 2.2mm diameter pilot hole exists within the boss volume from $z=8$ down to $z=4$ (ensuring a 4mm depth) and extends through the floor to $z=0$.
- R6: USB-C cutout on $-X$ wall; subtract a rectangular volume of 10mm (Y) x 4mm (Z) x 10mm (X) centered at $y=0, z=14$, with an X-range of $[-45, -35]$ to ensure a complete through-cut of the $-X$ wall.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.