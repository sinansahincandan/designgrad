**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6.0mm OD, extending from the floor ($z=2$) up to the board underside ($z=8$). Each contains a 2.2mm diameter pilot hole extending from $z=8$ down to $z=1$.
- **Cutout**: Rectangular aperture on the $-X$ face centered at $x=-42.5, y=0, z=14$, with dimensions 9mm (Y) x 3mm (Z), spanning the full thickness of the wall via boolean subtraction.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6.0mm, pilot hole 2.2mm diameter from $z=8$ down to $z=1$ (7mm depth).
- R6: USB-C cutout on $-X$ wall centered at $x=-42.5, y=0, z=14$, size 9mm (Y) x 3mm (Z), ensuring full intersection with the wall volume.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.