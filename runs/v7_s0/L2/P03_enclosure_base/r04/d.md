**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls.
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD and 2.2mm pilot holes, extending from the floor ($z=0$) up to the board underside ($z=8$).
- **Cutout**: Rectangular aperture on the $-X$ face, centered at $y=0, z=14$, with dimensions 9mm (Y) x 3mm (Z), designed as a boolean subtraction that fully penetrates the wall from $x=-42.5$ to the inner cavity boundary ($x=-40$).

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load from the board underside ($z=8$) down through the floor to the mounting surface.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a boolean subtraction of the volume $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$ from the main body to ensure the region is completely free of material.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, pilot hole 2.2mm diameter extending from $z=0$ up to $z=8$.
- R6: USB-C cutout on $-X$ wall (at $x=-42.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$, penetrating the full thickness of the wall.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.