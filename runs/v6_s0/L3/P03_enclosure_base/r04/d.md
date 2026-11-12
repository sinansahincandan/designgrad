**Concept**: A compact, injection-molding/3D-printable enclosure base designed to house an 80x50mm PCB with integrated screw bosses and a USB-C port cutout.

**Main Features**:
- **Floor**: 2mm thick base covering the footprint of the board and walls ($z=0$ to $z=2$).
- **Walls**: 85x55mm outer perimeter, height ~31mm, wall thickness ~2.5mm.
- **Bosses**: Four solid cylinders with OD = 6mm, centered at $(\pm35, \pm20)$, extending from the floor ($z=2$) up to $z=8$. Each boss contains a 2.2mm diameter pilot hole subtracted from its center, extending from $z=8$ down to $z=4$ (providing a 4mm depth).
- **Cutout**: A through-wall rectangular subtraction on the $-X$ face for cable access. The volume spans $x \in [-42.5, -37.5]$ to ensure it clears both the outer wall ($x=-42.5$) and the inner cavity boundary ($x=-40$), with dimensions $y \in [-4.5, 4.5]$ (9mm width) and $z \in [12.5, 15.5]$ (3mm height).

**Load Path**: PCB weight is transferred through screws into the bosses, which distribute the load from $z=8$ down to the floor at $z=2$.

**Requirement Compliance**:
- R1: Single solid created via boolean union of floor, walls, and bosses (as positive volumes), then subtracting holes/cutouts.
- R2: Floor spans $z=0$ to $z=2$.
- R3: Board cavity defined by a large subtraction from $x \in [-40, 40], y \in [-25, 25], z \in [8, 32]$.
- R4: Outer dimensions 85x55mm; wall top at $z=31$.
- R5: Bosses are solid material added to the base, with a hole subtracted from them. Bosses at $(\pm35, \pm20)$, OD 6mm, extending from $z=2$ to $z=8$; pilot hole (2.2mm diameter) extends from $z=8$ down to $z=4$.
- R6: USB-C through-cutout on $-X$ wall; the cutout must be a through-hole that intersects both the outer perimeter ($x=-42.5$) and the inner board cavity boundary ($x=-40$). Volume defined by $x \in [-42.5, -37.5]$, $y \in [-4.5, 4.5]$, and $z \in [12.5, 15.5]$.
- R7: Estimated volume $\approx 4500 \text{ mm}^3 \rightarrow \text{Mass} \approx 5.6\text{g}$, well under 70g limit.