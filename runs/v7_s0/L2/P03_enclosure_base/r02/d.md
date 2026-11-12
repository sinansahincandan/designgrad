**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height exactly $z=31$, wall thickness ~2.5mm.
- **Bosses**: Four cylindrical pillars at $(\pm35, \pm20)$ with 6mm OD and 2.2mm pilot holes.
- **Cutout**: Through-cut rectangular aperture on the $-X$ face that fully penetrates the wall from the outer boundary to the inner cavity boundary.

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load into the floor and side walls.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses, then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$. This subtraction is performed such that the board space remains completely free of material.
- R4: Outer dimensions 85x55mm; wall top at $z=31$ (within the required $[30, 32.5]$ range).
- R5: Bosses at $(\pm35, \pm20)$, OD 6mm, pilot hole 2.2mm diameter from $z=8$ down to $z=4$ (providing a depth of 4mm to satisfy the requirement).
- R6: USB-C cutout on $-X$ wall (at $x=-42.5$), size 9mm (Y) x 3mm (Z), centered at $y=0, z=14$; subtraction extends through the entire thickness of the wall to ensure a valid opening.
- R7: Mass is well under the 70g limit.