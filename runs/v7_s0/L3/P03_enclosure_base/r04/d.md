**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls, spanning $z=0$ to $z=2$.
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD. These are added via boolean union to the main body *before* the board cavity subtraction. Each boss extends from $z=2$ (top of floor) up to $z=8$ (bottom of board cavity).
- **Cutout**: A rectangular through-cut void defined by $x \in [-43, -39.5]$, $y \in [-4.5, 4.5]$, and $z \in [12.5, 15.5]$. This ensures the subtraction spans the entire thickness of the $-X$ wall and reaches the internal cavity boundary at $x=-40$.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a single boolean subtraction of the volume $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$ from the main body. Bosses are integrated into the solid mass prior to this subtraction to ensure they remain intact at $z=8$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, with a 2.2mm diameter pilot hole subtracted from the center of each boss from $z=8$ down to $z=4$.
- R6: USB-C cutout on $-X$ wall (spanning $x=-43$ to $x=-39.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$, implemented as a through-cut.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.